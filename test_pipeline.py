"""
Main script for testing the YouTube Shorts AI Pipeline.
This script tests each component individually and then the complete pipeline.
"""

import os
import logging
from dotenv import load_dotenv

# Import all component modules
from src.text_generation import TextGenerator
from src.audio_generation import AudioGenerator
from src.video_generation import VideoGenerator
from src.music_generation import MusicGenerator
from src.pipeline_integration import YouTubeShortsCreator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("test_pipeline")

def test_text_generation():
    """Test the text generation module."""
    logger.info("Testing text generation module...")
    
    try:
        # Initialize the text generator
        text_generator = TextGenerator()
        
        # Generate a script
        result = text_generator.generate_short_script(
            topic="The future of AI in content creation",
            target_duration=30,
            output_file="test_output/text/test_script.txt"
        )
        
        logger.info(f"Text generation successful. Output: {result['output_path']}")
        logger.info(f"Generated text: {result['text'][:100]}...")
        return True
    except Exception as e:
        logger.error(f"Text generation test failed: {e}")
        return False

def test_audio_generation():
    """Test the audio generation module."""
    logger.info("Testing audio generation module...")
    
    try:
        # Initialize the audio generator
        audio_generator = AudioGenerator()
        
        # Generate speech
        result = audio_generator.generate_speech(
            text="This is a test of the audio generation module for YouTube Shorts. The goal is to create engaging voiceovers for short videos.",
            output_path="test_output/audio/test_speech.mp3"
        )
        
        logger.info(f"Audio generation successful. Output: {result['output_path']}")
        logger.info(f"Audio duration: {result['metadata']['duration']} seconds")
        return True
    except Exception as e:
        logger.error(f"Audio generation test failed: {e}")
        return False

def test_video_generation():
    """Test the video generation module."""
    logger.info("Testing video generation module...")
    
    try:
        # Initialize the video generator
        video_generator = VideoGenerator()
        
        # Generate a video
        result = video_generator.generate_video_from_text(
            prompt="A person explaining AI tools for content creation, with animated graphics showing different tools",
            output_path="test_output/video/test_video.mp4",
            duration=10
        )
        
        logger.info(f"Video generation successful. Output: {result['output_path']}")
        return True
    except Exception as e:
        logger.error(f"Video generation test failed: {e}")
        return False

def test_music_generation():
    """Test the music generation module."""
    logger.info("Testing music generation module...")
    
    try:
        # Initialize the music generator
        music_generator = MusicGenerator()
        
        # Generate background music
        result = music_generator.generate_background_music(
            prompt="Upbeat and energetic background music for a YouTube Short about AI tools",
            output_path="test_output/music/test_music.mp3",
            duration=30,
            genre="Electronic",
            mood="Energetic"
        )
        
        logger.info(f"Music generation successful. Output: {result['output_path']}")
        logger.info(f"Music duration: {result['metadata']['actual_duration']} seconds")
        return True
    except Exception as e:
        logger.error(f"Music generation test failed: {e}")
        return False

def test_complete_pipeline():
    """Test the complete pipeline."""
    logger.info("Testing complete YouTube Shorts pipeline...")
    
    try:
        # Initialize the pipeline
        creator = YouTubeShortsCreator({
            "output_dir": "test_output"
        })
        
        # Create a complete short
        result = creator.create_short(
            topic="How AI is revolutionizing content creation",
            output_name="test_complete_pipeline",
            duration=30,
            add_captions=True
        )
        
        logger.info(f"Pipeline test successful. Output: {result['output_path']}")
        logger.info(f"Metadata: {result['metadata_path']}")
        return True
    except Exception as e:
        logger.error(f"Complete pipeline test failed: {e}")
        return False

def main():
    """Run all tests."""
    # Load environment variables
    load_dotenv()
    
    # Create test output directory
    os.makedirs("test_output", exist_ok=True)
    os.makedirs("test_output/text", exist_ok=True)
    os.makedirs("test_output/audio", exist_ok=True)
    os.makedirs("test_output/video", exist_ok=True)
    os.makedirs("test_output/music", exist_ok=True)
    
    # Run individual component tests
    text_result = test_text_generation()
    audio_result = test_audio_generation()
    video_result = test_video_generation()
    music_result = test_music_generation()
    
    # Run complete pipeline test if all component tests pass
    if text_result and audio_result and video_result and music_result:
        pipeline_result = test_complete_pipeline()
    else:
        logger.warning("Skipping complete pipeline test due to component test failures")
        pipeline_result = False
    
    # Print summary
    logger.info("\n--- Test Summary ---")
    logger.info(f"Text Generation: {'PASS' if text_result else 'FAIL'}")
    logger.info(f"Audio Generation: {'PASS' if audio_result else 'FAIL'}")
    logger.info(f"Video Generation: {'PASS' if video_result else 'FAIL'}")
    logger.info(f"Music Generation: {'PASS' if music_result else 'FAIL'}")
    logger.info(f"Complete Pipeline: {'PASS' if pipeline_result else 'FAIL'}")
    
    if text_result and audio_result and video_result and music_result and pipeline_result:
        logger.info("All tests passed successfully!")
    else:
        logger.warning("Some tests failed. Check the log for details.")

if __name__ == "__main__":
    main()
