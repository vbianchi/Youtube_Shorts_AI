"""
Main module for video generation in the YouTube Shorts AI Pipeline.
This module provides a simplified interface for generating videos for YouTube Shorts.
"""

import os
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from .runway_client import RunwayClient

class VideoGenerator:
    """Video generation component for YouTube Shorts pipeline."""
    
    def __init__(self, api_key=None):
        """
        Initialize the video generator.
        
        Args:
            api_key (str, optional): Runway API key. If not provided, will look for RUNWAY_API_KEY in environment variables.
        """
        self.client = RunwayClient(api_key)
    
    def generate_video_from_text(self, prompt, output_path, duration=10, width=768, height=1344):
        """
        Generate a video from a text prompt.
        
        Args:
            prompt (str): The text prompt describing the video
            output_path (str): The path to save the video file to
            duration (int, optional): Duration in seconds. Defaults to 10.
            width (int, optional): Video width. Defaults to 768.
            height (int, optional): Video height. Defaults to 1344 (9:16 aspect ratio for Shorts).
            
        Returns:
            dict: A dictionary containing the output path and metadata
        """
        # Calculate frames based on duration (assuming 24fps)
        num_frames = duration * 24
        
        # Generate the video
        video_path = self.client.generate_video_from_text(
            prompt=prompt,
            output_path=output_path,
            duration=duration,
            num_frames=num_frames,
            width=width,
            height=height
        )
        
        return {
            "output_path": video_path,
            "metadata": {
                "prompt": prompt,
                "duration": duration,
                "width": width,
                "height": height,
                "num_frames": num_frames,
                "generation_type": "text-to-video"
            }
        }
    
    def generate_video_from_image(self, image_path, prompt, output_path, duration=10):
        """
        Generate a video from an image.
        
        Args:
            image_path (str): Path to the input image
            prompt (str): The text prompt describing the video
            output_path (str): The path to save the video file to
            duration (int, optional): Duration in seconds. Defaults to 10.
            
        Returns:
            dict: A dictionary containing the output path and metadata
        """
        # Calculate frames based on duration (assuming 24fps)
        num_frames = duration * 24
        
        # Generate the video
        video_path = self.client.generate_video_from_image(
            image_path=image_path,
            prompt=prompt,
            output_path=output_path,
            duration=duration,
            num_frames=num_frames
        )
        
        return {
            "output_path": video_path,
            "metadata": {
                "image_path": image_path,
                "prompt": prompt,
                "duration": duration,
                "num_frames": num_frames,
                "generation_type": "image-to-video"
            }
        }
    
    def add_audio_to_video(self, video_path, audio_path, output_path):
        """
        Add audio to a video.
        
        Args:
            video_path (str): Path to the input video
            audio_path (str): Path to the audio file
            output_path (str): The path to save the combined video file to
            
        Returns:
            str: The path to the saved video file
        """
        # Load the video and audio
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        # If audio is longer than video, trim it
        if audio_clip.duration > video_clip.duration:
            audio_clip = audio_clip.subclip(0, video_clip.duration)
        
        # If video is longer than audio, loop the audio
        elif video_clip.duration > audio_clip.duration:
            # Calculate how many times to loop
            repeat_count = int(video_clip.duration / audio_clip.duration) + 1
            # Create a new audio clip by concatenating the original multiple times
            from moviepy.editor import concatenate_audioclips
            audio_clip = concatenate_audioclips([audio_clip] * repeat_count)
            # Trim to match video duration
            audio_clip = audio_clip.subclip(0, video_clip.duration)
        
        # Set the audio
        video_clip = video_clip.set_audio(audio_clip)
        
        # Write the result
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        # Close the clips to release resources
        video_clip.close()
        audio_clip.close()
        
        return output_path
    
    def add_text_overlay(self, video_path, text, output_path, font_size=40, color='white', position='bottom'):
        """
        Add text overlay to a video.
        
        Args:
            video_path (str): Path to the input video
            text (str): Text to overlay
            output_path (str): The path to save the video file to
            font_size (int, optional): Font size. Defaults to 40.
            color (str, optional): Text color. Defaults to 'white'.
            position (str, optional): Text position ('top', 'center', 'bottom'). Defaults to 'bottom'.
            
        Returns:
            str: The path to the saved video file
        """
        # Load the video
        video_clip = VideoFileClip(video_path)
        
        # Create the text clip
        text_clip = TextClip(text, fontsize=font_size, color=color, bg_color='black', 
                            font='Arial-Bold', kerning=5, interline=-1)
        
        # Set the position
        if position == 'top':
            text_clip = text_clip.set_position(('center', 50))
        elif position == 'center':
            text_clip = text_clip.set_position('center')
        else:  # bottom
            text_clip = text_clip.set_position(('center', video_clip.h - text_clip.h - 50))
        
        # Set the duration to match the video
        text_clip = text_clip.set_duration(video_clip.duration)
        
        # Composite the clips
        final_clip = CompositeVideoClip([video_clip, text_clip])
        
        # Write the result
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        # Close the clips to release resources
        video_clip.close()
        text_clip.close()
        final_clip.close()
        
        return output_path
    
    def create_youtube_short(self, prompt, audio_path=None, output_path=None, add_captions=False, caption_text=None):
        """
        Create a complete YouTube Short with optional audio and captions.
        
        Args:
            prompt (str): The text prompt describing the video
            audio_path (str, optional): Path to the audio file. Defaults to None.
            output_path (str, optional): The path to save the final video. Defaults to None.
            add_captions (bool, optional): Whether to add captions. Defaults to False.
            caption_text (str, optional): Text for captions. Defaults to None.
            
        Returns:
            dict: A dictionary containing the output path and metadata
        """
        # Create temporary directory for intermediate files
        temp_dir = tempfile.mkdtemp()
        
        # Generate base video
        base_video_path = os.path.join(temp_dir, "base_video.mp4")
        video_result = self.generate_video_from_text(
            prompt=prompt,
            output_path=base_video_path,
            duration=10  # Default duration for Shorts
        )
        
        current_video_path = base_video_path
        
        # Add audio if provided
        if audio_path:
            audio_video_path = os.path.join(temp_dir, "audio_video.mp4")
            current_video_path = self.add_audio_to_video(
                video_path=current_video_path,
                audio_path=audio_path,
                output_path=audio_video_path
            )
        
        # Add captions if requested
        if add_captions and caption_text:
            caption_video_path = os.path.join(temp_dir, "caption_video.mp4")
            current_video_path = self.add_text_overlay(
                video_path=current_video_path,
                text=caption_text,
                output_path=caption_video_path
            )
        
        # Move to final output path if provided
        if output_path:
            import shutil
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            shutil.copy(current_video_path, output_path)
            final_path = output_path
        else:
            final_path = current_video_path
        
        return {
            "output_path": final_path,
            "metadata": {
                "prompt": prompt,
                "has_audio": audio_path is not None,
                "has_captions": add_captions and caption_text is not None,
                "temp_dir": temp_dir
            }
        }


if __name__ == "__main__":
    # Example usage
    try:
        generator = VideoGenerator()
        
        # Generate a simple video
        result = generator.generate_video_from_text(
            prompt="A person explaining AI tools for content creation, with animated graphics showing different tools",
            output_path="test_video.mp4",
            duration=10
        )
        
        print(f"Video generated and saved to {result['output_path']}")
        print("\nMetadata:")
        for key, value in result["metadata"].items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Error: {e}")
