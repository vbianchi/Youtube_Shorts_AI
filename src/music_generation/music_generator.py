"""
Main module for music generation in the YouTube Shorts AI Pipeline.
This module provides a simplified interface for generating background music for YouTube Shorts.
"""

import os
from .suno_client import SunoClient
from pydub import AudioSegment

class MusicGenerator:
    """Music generation component for YouTube Shorts pipeline."""
    
    def __init__(self, api_key=None):
        """
        Initialize the music generator.
        
        Args:
            api_key (str, optional): Suno API key. If not provided, will look for SUNO_API_KEY in environment variables.
        """
        self.client = SunoClient(api_key)
    
    def generate_background_music(self, prompt, output_path, duration=30, genre=None, mood=None, tempo=None):
        """
        Generate background music for a YouTube Short.
        
        Args:
            prompt (str): The text prompt describing the music
            output_path (str): The path to save the audio file to
            duration (int, optional): Approximate duration in seconds. Defaults to 30.
            genre (str, optional): Music genre. Defaults to None.
            mood (str, optional): Mood of the music. Defaults to None.
            tempo (str, optional): Tempo of the music. Defaults to None.
            
        Returns:
            dict: A dictionary containing the output path and metadata
        """
        # Generate the music
        music_path = self.client.generate_music(
            prompt=prompt,
            output_path=output_path,
            duration=duration,
            genre=genre,
            mood=mood,
            tempo=tempo
        )
        
        # Get the actual duration of the generated music
        audio = AudioSegment.from_file(music_path)
        actual_duration = len(audio) / 1000  # Convert milliseconds to seconds
        
        return {
            "output_path": music_path,
            "metadata": {
                "prompt": prompt,
                "requested_duration": duration,
                "actual_duration": actual_duration,
                "genre": genre,
                "mood": mood,
                "tempo": tempo
            }
        }
    
    def adjust_music_duration(self, music_path, target_duration, output_path=None):
        """
        Adjust the duration of a music file to match a target duration.
        
        Args:
            music_path (str): Path to the input music file
            target_duration (float): Target duration in seconds
            output_path (str, optional): Path to save the adjusted music. Defaults to None (overwrites input).
            
        Returns:
            str: Path to the adjusted music file
        """
        if not output_path:
            output_path = music_path
        
        # Load the audio
        audio = AudioSegment.from_file(music_path)
        current_duration = len(audio) / 1000  # Convert milliseconds to seconds
        
        # If current duration is already close to target, just return
        if abs(current_duration - target_duration) < 1:
            return music_path
        
        # If current duration is shorter than target, loop the audio
        if current_duration < target_duration:
            # Calculate how many times to loop
            repeat_count = int(target_duration / current_duration) + 1
            # Create a new audio by concatenating the original multiple times
            extended_audio = audio * repeat_count
            # Trim to match target duration
            adjusted_audio = extended_audio[:int(target_duration * 1000)]
        else:
            # If current duration is longer than target, trim the audio
            adjusted_audio = audio[:int(target_duration * 1000)]
        
        # Add fade out at the end
        fade_duration = min(3000, int(target_duration * 1000 * 0.1))  # 10% of duration or 3 seconds, whichever is shorter
        adjusted_audio = adjusted_audio.fade_out(fade_duration)
        
        # Save the adjusted audio
        adjusted_audio.export(output_path, format=output_path.split(".")[-1])
        
        return output_path
    
    def adjust_music_volume(self, music_path, volume_adjustment_db, output_path=None):
        """
        Adjust the volume of a music file.
        
        Args:
            music_path (str): Path to the input music file
            volume_adjustment_db (float): Volume adjustment in decibels (negative values reduce volume)
            output_path (str, optional): Path to save the adjusted music. Defaults to None (overwrites input).
            
        Returns:
            str: Path to the adjusted music file
        """
        if not output_path:
            output_path = music_path
        
        # Load the audio
        audio = AudioSegment.from_file(music_path)
        
        # Adjust volume
        adjusted_audio = audio + volume_adjustment_db
        
        # Save the adjusted audio
        adjusted_audio.export(output_path, format=output_path.split(".")[-1])
        
        return output_path
    
    def create_music_for_voiceover(self, prompt, voiceover_path, output_path, volume_reduction_db=-10):
        """
        Create background music that complements a voiceover.
        
        Args:
            prompt (str): The text prompt describing the music
            voiceover_path (str): Path to the voiceover audio file
            output_path (str): Path to save the music file
            volume_reduction_db (float, optional): Volume reduction in decibels. Defaults to -10.
            
        Returns:
            dict: A dictionary containing the output path and metadata
        """
        # Get the duration of the voiceover
        voiceover = AudioSegment.from_file(voiceover_path)
        voiceover_duration = len(voiceover) / 1000  # Convert milliseconds to seconds
        
        # Generate music with matching duration
        result = self.generate_background_music(
            prompt=prompt,
            output_path=output_path,
            duration=voiceover_duration,
            mood="Background"  # Specify background mood for better results with voiceover
        )
        
        # Adjust the music duration to match the voiceover exactly
        adjusted_path = self.adjust_music_duration(
            music_path=result["output_path"],
            target_duration=voiceover_duration
        )
        
        # Reduce the volume to avoid overpowering the voiceover
        final_path = self.adjust_music_volume(
            music_path=adjusted_path,
            volume_adjustment_db=volume_reduction_db
        )
        
        # Update the metadata
        result["output_path"] = final_path
        result["metadata"].update({
            "voiceover_duration": voiceover_duration,
            "volume_adjustment": volume_reduction_db
        })
        
        return result


if __name__ == "__main__":
    # Example usage
    try:
        generator = MusicGenerator()
        
        # Generate background music
        result = generator.generate_background_music(
            prompt="Upbeat and energetic background music for a YouTube Short about AI tools",
            output_path="test_music.mp3",
            duration=30,
            genre="Electronic",
            mood="Energetic"
        )
        
        print(f"Music generated and saved to {result['output_path']}")
        print("\nMetadata:")
        for key, value in result["metadata"].items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Error: {e}")
