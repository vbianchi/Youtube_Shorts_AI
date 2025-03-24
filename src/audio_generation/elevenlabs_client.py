"""
ElevenLabs API Client for audio generation in the YouTube Shorts AI Pipeline.
This module handles the interaction with ElevenLabs' API to generate voiceovers for YouTube Shorts.
"""

import os
import requests
import json
from dotenv import load_dotenv
import time

class ElevenLabsClient:
    """Client for interacting with ElevenLabs' API to generate voice content."""
    
    def __init__(self, api_key=None):
        """
        Initialize the ElevenLabs client.
        
        Args:
            api_key (str, optional): ElevenLabs API key. If not provided, will look for ELEVENLABS_API_KEY in environment variables.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ElevenLabs API key is required. Set it as ELEVENLABS_API_KEY environment variable or pass it to the constructor.")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_voices(self):
        """
        Get available voices from ElevenLabs.
        
        Returns:
            list: Available voices
        """
        response = requests.get(f"{self.base_url}/voices", headers=self.headers)
        response.raise_for_status()
        return response.json().get("voices", [])
    
    def get_voice_by_name(self, name):
        """
        Find a voice by name.
        
        Args:
            name (str): The name of the voice to find
            
        Returns:
            dict: Voice information or None if not found
        """
        voices = self.get_voices()
        for voice in voices:
            if voice.get("name", "").lower() == name.lower():
                return voice
        return None
    
    def generate_speech(self, text, voice_id, model_id="eleven_turbo_v2", stability=0.5, similarity_boost=0.75, output_format="mp3"):
        """
        Generate speech from text using ElevenLabs API.
        
        Args:
            text (str): The text to convert to speech
            voice_id (str): The ID of the voice to use
            model_id (str, optional): The ID of the model to use. Defaults to "eleven_turbo_v2".
            stability (float, optional): Voice stability (0-1). Defaults to 0.5.
            similarity_boost (float, optional): Voice similarity boost (0-1). Defaults to 0.75.
            output_format (str, optional): Output audio format. Defaults to "mp3".
            
        Returns:
            bytes: Audio data
        """
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }
        
        headers = self.headers.copy()
        headers["Accept"] = f"audio/{output_format}"
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.content
    
    def save_audio(self, audio_data, output_path):
        """
        Save audio data to a file.
        
        Args:
            audio_data (bytes): The audio data to save
            output_path (str): The path to save the audio file to
            
        Returns:
            str: The path to the saved audio file
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(audio_data)
        
        return output_path
    
    def generate_and_save_speech(self, text, output_path, voice_id=None, voice_name=None, model_id="eleven_turbo_v2", 
                                stability=0.5, similarity_boost=0.75):
        """
        Generate speech from text and save it to a file.
        
        Args:
            text (str): The text to convert to speech
            output_path (str): The path to save the audio file to
            voice_id (str, optional): The ID of the voice to use. Defaults to None.
            voice_name (str, optional): The name of the voice to use. Defaults to None.
            model_id (str, optional): The ID of the model to use. Defaults to "eleven_turbo_v2".
            stability (float, optional): Voice stability (0-1). Defaults to 0.5.
            similarity_boost (float, optional): Voice similarity boost (0-1). Defaults to 0.75.
            
        Returns:
            str: The path to the saved audio file
        """
        # If voice_name is provided but not voice_id, look up the voice_id
        if not voice_id and voice_name:
            voice = self.get_voice_by_name(voice_name)
            if voice:
                voice_id = voice.get("voice_id")
            else:
                raise ValueError(f"Voice with name '{voice_name}' not found")
        
        # If neither voice_id nor voice_name is provided, use a default voice
        if not voice_id:
            voices = self.get_voices()
            if voices:
                voice_id = voices[0].get("voice_id")
            else:
                raise ValueError("No voices available")
        
        # Generate the speech
        audio_data = self.generate_speech(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            stability=stability,
            similarity_boost=similarity_boost,
            output_format=output_path.split(".")[-1]
        )
        
        # Save the audio
        return self.save_audio(audio_data, output_path)


if __name__ == "__main__":
    # Example usage
    try:
        client = ElevenLabsClient()
        
        # List available voices
        voices = client.get_voices()
        print(f"Available voices: {len(voices)}")
        for i, voice in enumerate(voices[:5]):  # Show first 5 voices
            print(f"{i+1}. {voice.get('name')} (ID: {voice.get('voice_id')})")
        
        # Generate and save speech
        output_file = "test_speech.mp3"
        client.generate_and_save_speech(
            text="This is a test of the ElevenLabs text-to-speech API. It can generate natural-sounding voiceovers for YouTube Shorts.",
            output_path=output_file,
            voice_name="Rachel"  # Use a common voice name, will fall back to first available if not found
        )
        
        print(f"Speech generated and saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
