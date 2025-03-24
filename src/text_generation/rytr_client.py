"""
Rytr API Client for text generation in the YouTube Shorts AI Pipeline.
This module handles the interaction with Rytr's API to generate script content for YouTube Shorts.
"""

import os
import requests
import json
from dotenv import load_dotenv

class RytrClient:
    """Client for interacting with Rytr's API to generate text content."""
    
    def __init__(self, api_key=None):
        """
        Initialize the Rytr client.
        
        Args:
            api_key (str, optional): Rytr API key. If not provided, will look for RYTR_API_KEY in environment variables.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("RYTR_API_KEY")
        if not self.api_key:
            raise ValueError("Rytr API key is required. Set it as RYTR_API_KEY environment variable or pass it to the constructor.")
        
        self.base_url = "https://api.rytr.me/v1"
        self.headers = {
            "Authentication": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_languages(self):
        """
        Get available languages from Rytr.
        
        Returns:
            list: Available languages
        """
        response = requests.get(f"{self.base_url}/languages", headers=self.headers)
        response.raise_for_status()
        return response.json().get("data", [])
    
    def get_tones(self):
        """
        Get available tones from Rytr.
        
        Returns:
            list: Available tones
        """
        response = requests.get(f"{self.base_url}/tones", headers=self.headers)
        response.raise_for_status()
        return response.json().get("data", [])
    
    def get_use_cases(self):
        """
        Get available use cases (templates) from Rytr.
        
        Returns:
            list: Available use cases
        """
        response = requests.get(f"{self.base_url}/use-cases", headers=self.headers)
        response.raise_for_status()
        return response.json().get("data", [])
    
    def generate_content(self, prompt, use_case="social_media_post", tone="convincing", language="English", num_variants=1, creativity_level=3):
        """
        Generate content using Rytr API.
        
        Args:
            prompt (str): The prompt or context for content generation
            use_case (str, optional): The use case template to use. Defaults to "social_media_post".
            tone (str, optional): The tone of the content. Defaults to "convincing".
            language (str, optional): The language to generate content in. Defaults to "English".
            num_variants (int, optional): Number of content variants to generate. Defaults to 1.
            creativity_level (int, optional): Creativity level (1-5). Defaults to 3.
        
        Returns:
            dict: Generated content and metadata
        """
        payload = {
            "languageId": language,
            "toneId": tone,
            "useCaseId": use_case,
            "inputContexts": {
                "CONTEXT": prompt
            },
            "variations": num_variants,
            "creativityLevel": creativity_level,
            "format": "text"
        }
        
        response = requests.post(f"{self.base_url}/ryte", headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def generate_youtube_shorts_script(self, topic, tone="engaging", language="English", duration_seconds=60):
        """
        Generate a script specifically formatted for YouTube Shorts.
        
        Args:
            topic (str): The topic or theme for the YouTube Short
            tone (str, optional): The tone of the content. Defaults to "engaging".
            language (str, optional): The language to generate content in. Defaults to "English".
            duration_seconds (int, optional): Target duration in seconds. Defaults to 60.
        
        Returns:
            str: Generated script for YouTube Shorts
        """
        # Calculate approximate word count based on speaking rate (150 words per minute is average)
        word_count = int((duration_seconds / 60) * 150)
        
        prompt = f"""
        Create a script for a YouTube Short about {topic}.
        The video should be engaging, concise, and approximately {duration_seconds} seconds long.
        Focus on delivering value quickly with a hook in the first 3 seconds.
        Include a clear call-to-action at the end.
        Keep the total word count around {word_count} words.
        """
        
        # Use social media post or video script template based on what's available
        try:
            response = self.generate_content(
                prompt=prompt,
                use_case="video_script",  # Try video script template first
                tone=tone,
                language=language,
                creativity_level=4  # Higher creativity for more engaging content
            )
        except Exception:
            # Fallback to social media post if video script template isn't available
            response = self.generate_content(
                prompt=prompt,
                use_case="social_media_post",
                tone=tone,
                language=language,
                creativity_level=4
            )
        
        # Extract the generated content
        if response and "data" in response:
            return response["data"][0]["text"]
        else:
            raise Exception("Failed to generate YouTube Shorts script")


if __name__ == "__main__":
    # Example usage
    try:
        client = RytrClient()
        script = client.generate_youtube_shorts_script(
            topic="AI tools for content creation",
            tone="engaging",
            duration_seconds=30
        )
        print("Generated YouTube Shorts Script:")
        print(script)
    except Exception as e:
        print(f"Error: {e}")
