"""
Main module for text generation in the YouTube Shorts AI Pipeline.
This module provides a simplified interface for generating YouTube Shorts scripts.
"""

from .rytr_client import RytrClient

class TextGenerator:
    """Text generation component for YouTube Shorts pipeline."""
    
    def __init__(self, api_key=None):
        """
        Initialize the text generator.
        
        Args:
            api_key (str, optional): Rytr API key. If not provided, will look for RYTR_API_KEY in environment variables.
        """
        self.client = RytrClient(api_key)
    
    def generate_script(self, topic, tone="engaging", language="English", duration_seconds=60, keywords=None):
        """
        Generate a script for a YouTube Short.
        
        Args:
            topic (str): The main topic or theme for the YouTube Short
            tone (str, optional): The tone of the content. Defaults to "engaging".
            language (str, optional): The language to generate content in. Defaults to "English".
            duration_seconds (int, optional): Target duration in seconds. Defaults to 60.
            keywords (list, optional): List of keywords to include in the script. Defaults to None.
        
        Returns:
            dict: A dictionary containing the generated script and metadata
        """
        # Enhance the topic with keywords if provided
        enhanced_topic = topic
        if keywords and isinstance(keywords, list) and len(keywords) > 0:
            keyword_str = ", ".join(keywords)
            enhanced_topic = f"{topic} (including keywords: {keyword_str})"
        
        # Generate the script
        script_text = self.client.generate_youtube_shorts_script(
            topic=enhanced_topic,
            tone=tone,
            language=language,
            duration_seconds=duration_seconds
        )
        
        # Calculate estimated duration (rough approximation)
        word_count = len(script_text.split())
        estimated_duration = (word_count / 150) * 60  # Based on average speaking rate of 150 words per minute
        
        return {
            "script": script_text,
            "metadata": {
                "topic": topic,
                "tone": tone,
                "language": language,
                "word_count": word_count,
                "target_duration": duration_seconds,
                "estimated_duration": estimated_duration,
                "keywords": keywords
            }
        }
    
    def generate_hooks(self, topic, count=3, language="English"):
        """
        Generate multiple hook options for a YouTube Short.
        
        Args:
            topic (str): The main topic or theme for the YouTube Short
            count (int, optional): Number of hook options to generate. Defaults to 3.
            language (str, optional): The language to generate content in. Defaults to "English".
        
        Returns:
            list: A list of hook options
        """
        prompt = f"""
        Create {count} attention-grabbing hooks for a YouTube Short about {topic}.
        Each hook should be 1-2 sentences maximum and immediately capture viewer attention.
        Make them curiosity-driven, surprising, or challenge common assumptions.
        Format as a numbered list.
        """
        
        response = self.client.generate_content(
            prompt=prompt,
            use_case="social_media_post",
            tone="engaging",
            language=language,
            num_variants=1,
            creativity_level=5  # Maximum creativity for hooks
        )
        
        # Extract and parse the hooks
        if response and "data" in response:
            hooks_text = response["data"][0]["text"]
            # Split by newlines and filter out empty lines
            hooks = [line.strip() for line in hooks_text.split('\n') if line.strip()]
            # Remove numbering if present
            hooks = [h[h.find('.')+1:].strip() if '.' in h[:3] else h for h in hooks]
            return hooks[:count]  # Ensure we return only the requested number
        else:
            raise Exception("Failed to generate hooks")


if __name__ == "__main__":
    # Example usage
    try:
        generator = TextGenerator()
        
        # Generate a script
        result = generator.generate_script(
            topic="How AI is changing content creation",
            tone="informative",
            duration_seconds=30,
            keywords=["AI tools", "productivity", "creativity"]
        )
        
        print("Generated YouTube Shorts Script:")
        print(result["script"])
        print("\nMetadata:")
        for key, value in result["metadata"].items():
            print(f"{key}: {value}")
        
        # Generate hooks
        hooks = generator.generate_hooks(
            topic="How AI is changing content creation",
            count=3
        )
        
        print("\nHook Options:")
        for i, hook in enumerate(hooks, 1):
            print(f"{i}. {hook}")
            
    except Exception as e:
        print(f"Error: {e}")
