"""
Suno API Client for music generation in the YouTube Shorts AI Pipeline.
This module handles the interaction with Suno's API to generate background music for YouTube Shorts.
"""

import os
import requests
import json
import time
from dotenv import load_dotenv

class SunoClient:
    """Client for interacting with Suno's API to generate music content."""
    
    def __init__(self, api_key=None):
        """
        Initialize the Suno client.
        
        Args:
            api_key (str, optional): Suno API key. If not provided, will look for SUNO_API_KEY in environment variables.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("SUNO_API_KEY")
        if not self.api_key:
            raise ValueError("Suno API key is required. Set it as SUNO_API_KEY environment variable or pass it to the constructor.")
        
        self.base_url = "https://api.suno.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_music(self, prompt, output_path, duration=30, genre=None, mood=None, tempo=None):
        """
        Generate music from a text prompt using Suno's API.
        
        Args:
            prompt (str): The text prompt describing the music
            output_path (str): The path to save the audio file to
            duration (int, optional): Approximate duration in seconds. Defaults to 30.
            genre (str, optional): Music genre. Defaults to None.
            mood (str, optional): Mood of the music. Defaults to None.
            tempo (str, optional): Tempo of the music. Defaults to None.
            
        Returns:
            str: The path to the saved audio file
        """
        url = f"{self.base_url}/generate"
        
        # Enhance the prompt with additional parameters if provided
        enhanced_prompt = prompt
        if genre:
            enhanced_prompt += f". Genre: {genre}"
        if mood:
            enhanced_prompt += f". Mood: {mood}"
        if tempo:
            enhanced_prompt += f". Tempo: {tempo}"
        if duration:
            enhanced_prompt += f". Duration: approximately {duration} seconds"
        
        payload = {
            "prompt": enhanced_prompt,
            "duration": duration
        }
        
        # Start the generation
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        
        # Get the generation ID
        generation_id = response.json().get("id")
        if not generation_id:
            raise ValueError("Failed to get generation ID from Suno API")
        
        # Poll for completion
        status_url = f"{self.base_url}/generations/{generation_id}"
        max_attempts = 60  # 5 minutes with 5-second intervals
        
        for attempt in range(max_attempts):
            status_response = requests.get(status_url, headers=self.headers)
            status_response.raise_for_status()
            
            status_data = status_response.json()
            status = status_data.get("status")
            
            if status == "completed":
                # Download the audio
                audio_url = status_data.get("audio_url")
                if not audio_url:
                    raise ValueError("No audio URL in completed generation")
                
                audio_response = requests.get(audio_url)
                audio_response.raise_for_status()
                
                # Save the audio
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(audio_response.content)
                
                return output_path
            
            elif status == "failed":
                error = status_data.get("error", "Unknown error")
                raise ValueError(f"Suno generation failed: {error}")
            
            # Wait before polling again
            time.sleep(5)
        
        raise TimeoutError("Suno generation timed out")
    
    def get_stems(self, generation_id, output_dir):
        """
        Get individual stems from a completed generation.
        
        Args:
            generation_id (str): The ID of the completed generation
            output_dir (str): Directory to save the stem files to
            
        Returns:
            dict: Dictionary mapping stem names to file paths
        """
        url = f"{self.base_url}/generations/{generation_id}/stems"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        stems_data = response.json().get("stems", {})
        stem_files = {}
        
        os.makedirs(output_dir, exist_ok=True)
        
        for stem_name, stem_url in stems_data.items():
            stem_response = requests.get(stem_url)
            stem_response.raise_for_status()
            
            stem_path = os.path.join(output_dir, f"{stem_name}.mp3")
            with open(stem_path, "wb") as f:
                f.write(stem_response.content)
            
            stem_files[stem_name] = stem_path
        
        return stem_files


if __name__ == "__main__":
    # Example usage
    try:
        client = SunoClient()
        
        # Generate music
        output_file = "test_music.mp3"
        client.generate_music(
            prompt="Upbeat and energetic background music for a YouTube Short about AI tools",
            output_path=output_file,
            duration=30,
            genre="Electronic",
            mood="Energetic"
        )
        
        print(f"Music generated and saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
