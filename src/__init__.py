"""
Main __init__.py file for the YouTube Shorts AI Pipeline package.
This file makes the directory a Python package and exposes key modules.
"""

from src.text_generation import TextGenerator
from src.audio_generation import AudioGenerator
from src.video_generation import VideoGenerator
from src.music_generation import MusicGenerator
from src.pipeline_integration import YouTubeShortsCreator

__version__ = "1.0.0"
__author__ = "YouTube Shorts AI Pipeline Team"

__all__ = [
    'TextGenerator',
    'AudioGenerator',
    'VideoGenerator',
    'MusicGenerator',
    'YouTubeShortsCreator'
]
