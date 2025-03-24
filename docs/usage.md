# Usage Guide

This guide provides detailed instructions on how to use the YouTube Shorts AI Pipeline to create engaging short-form videos for YouTube.

## Basic Usage

The simplest way to use the pipeline is through the command-line interface:

```bash
python -m src.pipeline_integration.pipeline --topic "Your topic here"
```

This will generate a complete YouTube Short based on the provided topic, including:
- A script tailored to the topic
- A voiceover of the script
- Background music that complements the content
- A video with visuals related to the topic
- Captions for accessibility

The final video will be saved in the `output/final` directory with a timestamp-based filename.

## Command-Line Options

The pipeline supports several command-line options for customization:

```bash
python -m src.pipeline_integration.pipeline \
  --topic "Your topic here" \
  --output "custom_name" \
  --voice "voice_id" \
  --duration 45 \
  --no-captions \
  --output-dir "custom_output_directory"
```

### Available Options

- `--topic`: (Required) The topic or idea for your YouTube Short
- `--output`: (Optional) Base name for output files (default: timestamp-based name)
- `--voice`: (Optional) Voice ID for text-to-speech (default: auto-selected)
- `--duration`: (Optional) Target duration in seconds (default: 30)
- `--no-captions`: (Optional) Disable captions (default: captions enabled)
- `--output-dir`: (Optional) Output directory (default: "output")

## Step-by-Step Workflow

### 1. Generate a Script

If you want to generate just a script without creating the full video:

```python
from src.text_generation import TextGenerator

generator = TextGenerator()
result = generator.generate_short_script(
    topic="The future of AI in content creation",
    target_duration=30,
    output_file="scripts/my_script.txt"
)

print(f"Generated script: {result['text']}")
```

### 2. Create a Voiceover

To convert a script to speech:

```python
from src.audio_generation import AudioGenerator

generator = AudioGenerator()
result = generator.generate_speech(
    text="Your script text here",
    output_path="audio/my_voiceover.mp3",
    voice_id=None  # Optional, will auto-select if None
)

print(f"Voiceover created: {result['output_path']}")
print(f"Duration: {result['metadata']['duration']} seconds")
```

### 3. Generate Background Music

To create background music:

```python
from src.music_generation import MusicGenerator

generator = MusicGenerator()
result = generator.generate_background_music(
    prompt="Upbeat and energetic background music for a tech tutorial",
    output_path="music/my_music.mp3",
    duration=30,
    genre="Electronic",
    mood="Energetic"
)

print(f"Music created: {result['output_path']}")
```

### 4. Generate a Video

To create a video:

```python
from src.video_generation import VideoGenerator

generator = VideoGenerator()
result = generator.generate_video_from_text(
    prompt="A person explaining AI tools for content creation, with animated graphics showing different tools",
    output_path="videos/my_video.mp4",
    duration=30
)

print(f"Video created: {result['output_path']}")
```

### 5. Combine Everything

To manually combine all components:

```python
from src.video_generation import VideoGenerator

video_generator = VideoGenerator()

# Add audio to video
video_with_audio = video_generator.add_audio_to_video(
    video_path="videos/my_video.mp4",
    audio_path="audio/my_voiceover.mp3",
    output_path="videos/video_with_audio.mp4"
)

# Add captions
final_video = video_generator.add_text_overlay(
    video_path=video_with_audio,
    text="Your caption text here",
    output_path="videos/final_video.mp4"
)

print(f"Final video created: {final_video}")
```

## Advanced Usage

### Creating a Custom Pipeline

You can create a custom pipeline by extending the `YouTubeShortsCreator` class:

```python
from src.pipeline_integration import YouTubeShortsCreator

class CustomYouTubeShortsCreator(YouTubeShortsCreator):
    def create_short(self, topic, output_name=None, voice_id=None, duration=30, add_captions=True):
        # Custom implementation
        # You can override specific parts of the pipeline
        
        # For example, use a custom prompt for video generation
        video_prompt = f"A cinematic YouTube Short about {topic} with professional lighting and camera movement"
        
        # Then call the parent method or implement your own logic
        return super().create_short(topic, output_name, voice_id, duration, add_captions)
```

### Batch Processing

To create multiple shorts in batch:

```python
from src.pipeline_integration import YouTubeShortsCreator
import csv

creator = YouTubeShortsCreator()

# Read topics from a CSV file
with open('topics.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        topic = row[0]
        print(f"Creating short for topic: {topic}")
        
        result = creator.create_short(
            topic=topic,
            output_name=topic.replace(" ", "_").lower(),
            duration=30,
            add_captions=True
        )
        
        print(f"Created: {result['output_path']}")
```

## Tips for Best Results

### Script Generation

- Use clear, specific topics
- For longer videos, specify a higher target duration
- Review and edit generated scripts for quality

### Voice Selection

- Test different voices to find the best match for your content
- Consider the tone and style of your content when selecting a voice
- Use consistent voices across related videos for brand recognition

### Video Generation

- Use descriptive prompts with visual details
- Specify the style, mood, and key visual elements
- For better results, include terms like "high quality", "professional", or specific visual styles

### Music Selection

- Match music mood to content tone
- For tutorials, use calm background music
- For energetic content, specify "upbeat" or "dynamic" in the prompt

## Uploading to YouTube

After creating your video:

1. Log in to your YouTube account
2. Click on the camera icon in the top right corner
3. Select "Upload video"
4. Choose your generated video file
5. Add a title, description, and tags
6. Set the video as "Not made for kids" or "Made for kids" as appropriate
7. Click "NEXT" through the remaining screens
8. Click "PUBLISH" to upload your Short

For best results on YouTube Shorts:
- Ensure your video is in vertical format (9:16 aspect ratio)
- Keep the duration under 60 seconds
- Use relevant hashtags including #Shorts in the description
