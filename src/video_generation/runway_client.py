"""
Runway API Client for video generation in the YouTube Shorts AI Pipeline.
This module handles the interaction with Runway's API to generate videos for YouTube Shorts.
"""

import os
import requests
import json
import time
from dotenv import load_dotenv

class RunwayClient:
    """Client for interacting with Runway's API to generate video content."""
    
    def __init__(self, api_key=None):
        """
        Initialize the Runway client.
        
        Args:
            api_key (str, optional): Runway API key. If not provided, will look for RUNWAY_API_KEY in environment variables.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("RUNWAY_API_KEY")
        if not self.api_key:
            raise ValueError("Runway API key is required. Set it as RUNWAY_API_KEY environment variable or pass it to the constructor.")
        
        self.base_url = "https://api.runwayml.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_video_from_text(self, prompt, output_path, duration=5, num_frames=24, width=768, height=1344):
        """
        Generate a video from a text prompt using Runway's text-to-video API.
        
        Args:
            prompt (str): The text prompt describing the video
            output_path (str): The path to save the video file to
            duration (int, optional): Duration in seconds. Defaults to 5.
            num_frames (int, optional): Number of frames to generate. Defaults to 24.
            width (int, optional): Video width. Defaults to 768.
            height (int, optional): Video height. Defaults to 1344 (9:16 aspect ratio for Shorts).
            
        Returns:
            str: The path to the saved video file
        """
        url = f"{self.base_url}/text-to-video"
        
        payload = {
            "prompt": prompt,
            "num_frames": num_frames,
            "width": width,
            "height": height
        }
        
        # Start the generation
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        
        # Get the generation ID
        generation_id = response.json().get("id")
        if not generation_id:
            raise ValueError("Failed to get generation ID from Runway API")
        
        # Poll for completion
        status_url = f"{self.base_url}/generations/{generation_id}"
        max_attempts = 60  # 5 minutes with 5-second intervals
        
        for attempt in range(max_attempts):
            status_response = requests.get(status_url, headers=self.headers)
            status_response.raise_for_status()
            
            status_data = status_response.json()
            status = status_data.get("status")
            
            if status == "completed":
                # Download the video
                video_url = status_data.get("output", {}).get("video")
                if not video_url:
                    raise ValueError("No video URL in completed generation")
                
                video_response = requests.get(video_url)
                video_response.raise_for_status()
                
                # Save the video
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(video_response.content)
                
                return output_path
            
            elif status == "failed":
                error = status_data.get("error", "Unknown error")
                raise ValueError(f"Runway generation failed: {error}")
            
            # Wait before polling again
            time.sleep(5)
        
        raise TimeoutError("Runway generation timed out")
    
    def generate_video_from_image(self, image_path, prompt, output_path, duration=5, num_frames=24):
        """
        Generate a video from an image using Runway's image-to-video API.
        
        Args:
            image_path (str): Path to the input image
            prompt (str): The text prompt describing the video
            output_path (str): The path to save the video file to
            duration (int, optional): Duration in seconds. Defaults to 5.
            num_frames (int, optional): Number of frames to generate. Defaults to 24.
            
        Returns:
            str: The path to the saved video file
        """
        url = f"{self.base_url}/image-to-video"
        
        # Read the image file
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Create multipart form data
        files = {
            "image": (os.path.basename(image_path), image_data)
        }
        
        data = {
            "prompt": prompt,
            "num_frames": str(num_frames)
        }
        
        # Remove Content-Type from headers for multipart request
        headers = self.headers.copy()
        headers.pop("Content-Type", None)
        
        # Start the generation
        response = requests.post(url, files=files, data=data, headers=headers)
        response.raise_for_status()
        
        # Get the generation ID
        generation_id = response.json().get("id")
        if not generation_id:
            raise ValueError("Failed to get generation ID from Runway API")
        
        # Poll for completion
        status_url = f"{self.base_url}/generations/{generation_id}"
        max_attempts = 60  # 5 minutes with 5-second intervals
        
        for attempt in range(max_attempts):
            status_response = requests.get(status_url, headers=self.headers)
            status_response.raise_for_status()
            
            status_data = status_response.json()
            status = status_data.get("status")
            
            if status == "completed":
                # Download the video
                video_url = status_data.get("output", {}).get("video")
                if not video_url:
                    raise ValueError("No video URL in completed generation")
                
                video_response = requests.get(video_url)
                video_response.raise_for_status()
                
                # Save the video
                os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(video_response.content)
                
                return output_path
            
            elif status == "failed":
                error = status_data.get("error", "Unknown error")
                raise ValueError(f"Runway generation failed: {error}")
            
            # Wait before polling again
            time.sleep(5)
        
        raise TimeoutError("Runway generation timed out")


if __name__ == "__main__":
    # Example usage
    try:
        client = RunwayClient()
        
        # Generate a video from text
        output_file = "test_video.mp4"
        client.generate_video_from_text(
            prompt="A person explaining AI tools for content creation, speaking to camera with animated graphics appearing around them",
            output_path=output_file,
            duration=5
        )
        
        print(f"Video generated and saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")
