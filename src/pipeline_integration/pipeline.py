"""
Pipeline integration script for the YouTube Shorts AI Pipeline.
This module combines all components to create complete YouTube Shorts videos.
"""

import os
import argparse
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Import all component modules
from src.text_generation import TextGenerator
from src.audio_generation import AudioGenerator
from src.video_generation import VideoGenerator
from src.music_generation import MusicGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("youtube_shorts_pipeline")

class YouTubeShortsCreator:
    """Main pipeline class for creating YouTube Shorts videos."""
    
    def __init__(self, config=None):
        """
        Initialize the YouTube Shorts creator pipeline.
        
        Args:
            config (dict, optional): Configuration dictionary. Defaults to None.
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize configuration
        self.config = config or {}
        
        # Set up output directories
        self.output_dir = self.config.get("output_dir", "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create subdirectories for each stage
        self.text_dir = os.path.join(self.output_dir, "text")
        self.audio_dir = os.path.join(self.output_dir, "audio")
        self.music_dir = os.path.join(self.output_dir, "music")
        self.video_dir = os.path.join(self.output_dir, "video")
        self.final_dir = os.path.join(self.output_dir, "final")
        
        for directory in [self.text_dir, self.audio_dir, self.music_dir, self.video_dir, self.final_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize component modules
        self.text_generator = TextGenerator(
            api_key=os.getenv("RYTR_API_KEY")
        )
        
        self.audio_generator = AudioGenerator(
            api_key=os.getenv("ELEVENLABS_API_KEY")
        )
        
        self.video_generator = VideoGenerator(
            api_key=os.getenv("RUNWAY_API_KEY")
        )
        
        self.music_generator = MusicGenerator(
            api_key=os.getenv("SUNO_API_KEY")
        )
        
        logger.info("YouTube Shorts Creator pipeline initialized")
    
    def create_short(self, topic, output_name=None, voice_id=None, duration=30, add_captions=True):
        """
        Create a complete YouTube Short from a topic.
        
        Args:
            topic (str): The topic or idea for the YouTube Short
            output_name (str, optional): Base name for output files. Defaults to timestamp.
            voice_id (str, optional): Voice ID for TTS. Defaults to None (auto-select).
            duration (int, optional): Target duration in seconds. Defaults to 30.
            add_captions (bool, optional): Whether to add captions. Defaults to True.
            
        Returns:
            dict: A dictionary containing paths to all generated files and metadata
        """
        # Generate a timestamp-based output name if not provided
        if not output_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"short_{timestamp}"
        
        logger.info(f"Creating YouTube Short on topic: {topic}")
        logger.info(f"Output name: {output_name}")
        
        # Step 1: Generate script
        logger.info("Step 1: Generating script")
        script_result = self.text_generator.generate_short_script(
            topic=topic,
            target_duration=duration,
            output_file=os.path.join(self.text_dir, f"{output_name}_script.txt")
        )
        script = script_result["text"]
        script_path = script_result["output_path"]
        
        # Step 2: Generate voiceover
        logger.info("Step 2: Generating voiceover")
        voiceover_result = self.audio_generator.generate_speech(
            text=script,
            output_path=os.path.join(self.audio_dir, f"{output_name}_voiceover.mp3"),
            voice_id=voice_id
        )
        voiceover_path = voiceover_result["output_path"]
        actual_duration = voiceover_result["metadata"]["duration"]
        
        # Step 3: Generate background music
        logger.info("Step 3: Generating background music")
        music_prompt = f"Background music for a YouTube Short about {topic}. Upbeat, energetic, and engaging."
        music_result = self.music_generator.create_music_for_voiceover(
            prompt=music_prompt,
            voiceover_path=voiceover_path,
            output_path=os.path.join(self.music_dir, f"{output_name}_music.mp3")
        )
        music_path = music_result["output_path"]
        
        # Step 4: Generate video
        logger.info("Step 4: Generating video")
        video_prompt = f"A visually engaging YouTube Short about {topic}. Dynamic visuals with motion and energy."
        video_result = self.video_generator.generate_video_from_text(
            prompt=video_prompt,
            output_path=os.path.join(self.video_dir, f"{output_name}_video.mp4"),
            duration=actual_duration
        )
        video_path = video_result["output_path"]
        
        # Step 5: Add audio to video
        logger.info("Step 5: Adding audio to video")
        video_with_audio_path = os.path.join(self.video_dir, f"{output_name}_with_audio.mp4")
        self.video_generator.add_audio_to_video(
            video_path=video_path,
            audio_path=voiceover_path,
            output_path=video_with_audio_path
        )
        
        # Step 6: Add captions if requested
        final_video_path = os.path.join(self.final_dir, f"{output_name}.mp4")
        if add_captions:
            logger.info("Step 6: Adding captions")
            self.video_generator.add_text_overlay(
                video_path=video_with_audio_path,
                text=script,
                output_path=final_video_path
            )
        else:
            # Just copy the video with audio to the final path
            import shutil
            shutil.copy(video_with_audio_path, final_video_path)
        
        # Step 7: Create metadata file
        metadata = {
            "topic": topic,
            "creation_date": datetime.now().isoformat(),
            "duration": actual_duration,
            "files": {
                "script": script_path,
                "voiceover": voiceover_path,
                "music": music_path,
                "video": video_path,
                "video_with_audio": video_with_audio_path,
                "final_video": final_video_path
            },
            "components": {
                "text_generation": script_result["metadata"],
                "audio_generation": voiceover_result["metadata"],
                "music_generation": music_result["metadata"],
                "video_generation": video_result["metadata"]
            }
        }
        
        metadata_path = os.path.join(self.final_dir, f"{output_name}_metadata.json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"YouTube Short created successfully: {final_video_path}")
        
        return {
            "output_path": final_video_path,
            "metadata_path": metadata_path,
            "metadata": metadata
        }


def main():
    """Command-line interface for the YouTube Shorts Creator pipeline."""
    parser = argparse.ArgumentParser(description="Create YouTube Shorts videos using AI")
    parser.add_argument("--topic", required=True, help="Topic or idea for the YouTube Short")
    parser.add_argument("--output", help="Base name for output files")
    parser.add_argument("--voice", help="Voice ID for text-to-speech")
    parser.add_argument("--duration", type=int, default=30, help="Target duration in seconds (default: 30)")
    parser.add_argument("--no-captions", action="store_true", help="Disable captions")
    parser.add_argument("--output-dir", default="output", help="Output directory (default: output)")
    
    args = parser.parse_args()
    
    config = {
        "output_dir": args.output_dir
    }
    
    creator = YouTubeShortsCreator(config)
    result = creator.create_short(
        topic=args.topic,
        output_name=args.output,
        voice_id=args.voice,
        duration=args.duration,
        add_captions=not args.no_captions
    )
    
    print(f"\nYouTube Short created successfully!")
    print(f"Final video: {result['output_path']}")
    print(f"Metadata: {result['metadata_path']}")


if __name__ == "__main__":
    main()
