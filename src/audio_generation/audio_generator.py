"""
Main module for audio generation in the YouTube Shorts AI Pipeline.
This module provides a simplified interface for generating voiceovers for YouTube Shorts.
"""

import os
from .elevenlabs_client import ElevenLabsClient

class AudioGenerator:
    """Audio generation component for YouTube Shorts pipeline."""
    
    def __init__(self, api_key=None):
        """
        Initialize the audio generator.
        
        Args:
            api_key (str, optional): ElevenLabs API key. If not provided, will look for ELEVENLABS_API_KEY in environment variables.
        """
        self.client = ElevenLabsClient(api_key)
        self.available_voices = None
    
    def list_voices(self, refresh=False):
        """
        Get a list of available voices.
        
        Args:
            refresh (bool, optional): Whether to refresh the cache. Defaults to False.
            
        Returns:
            list: Available voices
        """
        if self.available_voices is None or refresh:
            self.available_voices = self.client.get_voices()
        return self.available_voices
    
    def find_voice(self, criteria):
        """
        Find a voice based on criteria.
        
        Args:
            criteria (dict): Criteria to match (e.g., {"name": "Rachel"} or {"gender": "female"})
            
        Returns:
            dict: Voice information or None if not found
        """
        voices = self.list_voices()
        
        for voice in voices:
            match = True
            for key, value in criteria.items():
                if key == "gender" and "labels" in voice:
                    # Handle gender in labels
                    if value.lower() not in voice.get("labels", {}).get("gender", "").lower():
                        match = False
                        break
                elif key == "accent" and "labels" in voice:
                    # Handle accent in labels
                    if value.lower() not in voice.get("labels", {}).get("accent", "").lower():
                        match = False
                        break
                elif key == "age" and "labels" in voice:
                    # Handle age in labels
                    if value.lower() not in voice.get("labels", {}).get("age", "").lower():
                        match = False
                        break
                elif voice.get(key, "").lower() != value.lower():
                    match = False
                    break
            
            if match:
                return voice
        
        return None
    
    def generate_voiceover(self, script, output_path, voice_criteria=None, voice_id=None, 
                          model_id="eleven_turbo_v2", stability=0.5, similarity_boost=0.75):
        """
        Generate a voiceover for a YouTube Short.
        
        Args:
            script (str): The script text to convert to speech
            output_path (str): The path to save the audio file to
            voice_criteria (dict, optional): Criteria to match for voice selection. Defaults to None.
            voice_id (str, optional): Specific voice ID to use. Defaults to None.
            model_id (str, optional): The ID of the model to use. Defaults to "eleven_turbo_v2".
            stability (float, optional): Voice stability (0-1). Defaults to 0.5.
            similarity_boost (float, optional): Voice similarity boost (0-1). Defaults to 0.75.
            
        Returns:
            dict: A dictionary containing the output path and metadata
        """
        # If voice_criteria is provided but not voice_id, find a matching voice
        if not voice_id and voice_criteria:
            voice = self.find_voice(voice_criteria)
            if voice:
                voice_id = voice.get("voice_id")
                voice_name = voice.get("name")
            else:
                # If no matching voice is found, use a default voice
                voices = self.list_voices()
                if voices:
                    voice_id = voices[0].get("voice_id")
                    voice_name = voices[0].get("name")
                else:
                    raise ValueError("No voices available")
        elif voice_id:
            # If voice_id is provided, get the voice name
            voices = self.list_voices()
            voice_name = next((v.get("name") for v in voices if v.get("voice_id") == voice_id), "Unknown")
        else:
            # If neither voice_id nor voice_criteria is provided, use a default voice
            voices = self.list_voices()
            if voices:
                voice_id = voices[0].get("voice_id")
                voice_name = voices[0].get("name")
            else:
                raise ValueError("No voices available")
        
        # Generate the voiceover
        output_file = self.client.generate_and_save_speech(
            text=script,
            output_path=output_path,
            voice_id=voice_id,
            model_id=model_id,
            stability=stability,
            similarity_boost=similarity_boost
        )
        
        return {
            "output_path": output_file,
            "metadata": {
                "voice_id": voice_id,
                "voice_name": voice_name,
                "model_id": model_id,
                "stability": stability,
                "similarity_boost": similarity_boost,
                "script_length": len(script),
                "word_count": len(script.split())
            }
        }
    
    def optimize_script_for_tts(self, script):
        """
        Optimize a script for text-to-speech by adding SSML tags or formatting.
        
        Args:
            script (str): The script to optimize
            
        Returns:
            str: The optimized script
        """
        # This is a simple implementation that could be expanded with more sophisticated SSML
        
        # Add pauses after sentences
        script = script.replace(". ", ". <break time='0.3s'/> ")
        script = script.replace("! ", "! <break time='0.3s'/> ")
        script = script.replace("? ", "? <break time='0.3s'/> ")
        
        # Emphasize questions
        lines = script.split("\n")
        for i, line in enumerate(lines):
            if "?" in line:
                lines[i] = f"<emphasis level='moderate'>{line}</emphasis>"
        
        # Wrap in SSML tags
        optimized_script = "<speak>\n" + "\n".join(lines) + "\n</speak>"
        
        return optimized_script


if __name__ == "__main__":
    # Example usage
    try:
        generator = AudioGenerator()
        
        # List available voices
        voices = generator.list_voices()
        print(f"Available voices: {len(voices)}")
        
        # Generate a voiceover
        script = "Welcome to our YouTube Short about AI tools for content creation. These tools are revolutionizing how creators work, making it faster and easier to produce high-quality content."
        
        result = generator.generate_voiceover(
            script=script,
            output_path="test_voiceover.mp3",
            voice_criteria={"gender": "female", "accent": "american"}
        )
        
        print(f"Voiceover generated and saved to {result['output_path']}")
        print("\nMetadata:")
        for key, value in result["metadata"].items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Error: {e}")
