# Examples

This document provides practical examples of using the YouTube Shorts AI Pipeline for different scenarios.

## Example 1: Creating a Tech Tutorial Short

This example demonstrates how to create a short tutorial about a tech topic.

```python
from src.pipeline_integration import YouTubeShortsCreator

# Initialize the pipeline
creator = YouTubeShortsCreator()

# Create a tech tutorial short
result = creator.create_short(
    topic="How to use ChatGPT effectively for productivity",
    output_name="chatgpt_tutorial",
    duration=45,  # Slightly longer for tutorial content
    add_captions=True  # Important for tutorials
)

print(f"Tutorial video created: {result['output_path']}")
```

## Example 2: Creating an Entertainment Short

This example shows how to create an entertainment-focused short.

```python
from src.pipeline_integration import YouTubeShortsCreator

# Initialize the pipeline
creator = YouTubeShortsCreator()

# Create an entertainment short
result = creator.create_short(
    topic="Amazing facts about space that will blow your mind",
    output_name="space_facts",
    duration=30,
    add_captions=True
)

print(f"Entertainment video created: {result['output_path']}")
```

## Example 3: Custom Voice Selection

This example demonstrates how to select a specific voice for your short.

```python
from src.audio_generation import AudioGenerator
from src.pipeline_integration import YouTubeShortsCreator

# First, list available voices to find the one you want
audio_generator = AudioGenerator()
voices = audio_generator.list_voices()

# Print voice options
for voice in voices:
    print(f"ID: {voice['voice_id']}, Name: {voice['name']}")

# Choose a voice ID from the list
selected_voice_id = "21m00Tcm4TlvDq8ikWAM"  # Example ID, use an actual ID from your results

# Initialize the pipeline
creator = YouTubeShortsCreator()

# Create a short with the selected voice
result = creator.create_short(
    topic="The history of artificial intelligence",
    output_name="ai_history",
    voice_id=selected_voice_id,
    duration=30,
    add_captions=True
)

print(f"Video with custom voice created: {result['output_path']}")
```

## Example 4: Batch Processing Multiple Topics

This example shows how to create multiple shorts in a batch process.

```python
from src.pipeline_integration import YouTubeShortsCreator
import csv
import os

# Initialize the pipeline
creator = YouTubeShortsCreator()

# Define a list of topics
topics = [
    "The future of renewable energy",
    "How blockchain is changing finance",
    "The impact of AI on healthcare",
    "Sustainable living tips for beginners",
    "The psychology of social media"
]

# Create a CSV file with the topics
with open('topics.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for topic in topics:
        writer.writerow([topic])

# Process all topics in the CSV
with open('topics.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        topic = row[0]
        print(f"Creating short for topic: {topic}")
        
        # Create a sanitized output name from the topic
        output_name = topic.replace(" ", "_").lower()
        
        result = creator.create_short(
            topic=topic,
            output_name=output_name,
            duration=30,
            add_captions=True
        )
        
        print(f"Created: {result['output_path']}")
```

## Example 5: Creating a Short with Custom Music Parameters

This example demonstrates how to create a short with custom music parameters.

```python
from src.text_generation import TextGenerator
from src.audio_generation import AudioGenerator
from src.video_generation import VideoGenerator
from src.music_generation import MusicGenerator
import os

# Create output directories
os.makedirs("custom_output/text", exist_ok=True)
os.makedirs("custom_output/audio", exist_ok=True)
os.makedirs("custom_output/music", exist_ok=True)
os.makedirs("custom_output/video", exist_ok=True)
os.makedirs("custom_output/final", exist_ok=True)

# Step 1: Generate script
text_generator = TextGenerator()
script_result = text_generator.generate_short_script(
    topic="Meditation techniques for beginners",
    target_duration=30,
    output_file="custom_output/text/meditation_script.txt"
)
script = script_result["text"]

# Step 2: Generate voiceover
audio_generator = AudioGenerator()
voiceover_result = audio_generator.generate_speech(
    text=script,
    output_path="custom_output/audio/meditation_voiceover.mp3"
)
voiceover_path = voiceover_result["output_path"]

# Step 3: Generate custom calm music
music_generator = MusicGenerator()
music_result = music_generator.generate_background_music(
    prompt="Calm, peaceful meditation music with gentle piano and ambient sounds",
    output_path="custom_output/music/meditation_music.mp3",
    duration=30,
    genre="Ambient",
    mood="Peaceful",
    tempo="Slow"
)
music_path = music_result["output_path"]

# Adjust music volume to be quieter for meditation content
adjusted_music_path = music_generator.adjust_music_volume(
    music_path=music_path,
    volume_adjustment_db=-15,  # Extra quiet for meditation
    output_path="custom_output/music/meditation_music_adjusted.mp3"
)

# Step 4: Generate video
video_generator = VideoGenerator()
video_result = video_generator.generate_video_from_text(
    prompt="Peaceful meditation scene with nature elements, soft lighting, and calming visuals",
    output_path="custom_output/video/meditation_video.mp4",
    duration=30
)
video_path = video_result["output_path"]

# Step 5: Add voiceover to video
video_with_voice = video_generator.add_audio_to_video(
    video_path=video_path,
    audio_path=voiceover_path,
    output_path="custom_output/video/meditation_with_voice.mp4"
)

# Step 6: Add music to video with voice
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

# Load video with voice
video = VideoFileClip("custom_output/video/meditation_with_voice.mp4")
# Get the existing audio (voice)
voice_audio = video.audio
# Load the music audio
music_audio = AudioFileClip(adjusted_music_path)
# If music is longer than video, trim it
if music_audio.duration > video.duration:
    music_audio = music_audio.subclip(0, video.duration)
# If music is shorter than video, loop it
elif music_audio.duration < video.duration:
    repeat_count = int(video.duration / music_audio.duration) + 1
    from moviepy.editor import concatenate_audioclips
    music_audio = concatenate_audioclips([music_audio] * repeat_count)
    music_audio = music_audio.subclip(0, video.duration)
# Combine voice and music
final_audio = CompositeAudioClip([voice_audio, music_audio])
# Set the combined audio to the video
final_video = video.set_audio(final_audio)
# Write the final video
final_video.write_videofile("custom_output/final/meditation_final.mp4", codec="libx264", audio_codec="aac")

print("Custom meditation short created: custom_output/final/meditation_final.mp4")
```

## Example 6: Creating a Short with Custom Video Style

This example shows how to create a short with a specific visual style.

```python
from src.pipeline_integration import YouTubeShortsCreator
import os

# Create a custom configuration
config = {
    "output_dir": "styled_output"
}

# Initialize the pipeline with custom config
creator = YouTubeShortsCreator(config)

# Create a short with custom video styling through the prompt
result = creator.create_short(
    topic="The art of cinematography",
    output_name="cinematography_art",
    duration=30,
    add_captions=True
)

# Now let's customize the video generation by extending the class
from src.pipeline_integration import YouTubeShortsCreator

class StyledYouTubeShortsCreator(YouTubeShortsCreator):
    def create_short(self, topic, output_name=None, voice_id=None, duration=30, add_captions=True, style=None):
        # Generate a timestamp-based output name if not provided
        if not output_name:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"short_{timestamp}"
        
        # Set up directories
        self.text_dir = os.path.join(self.output_dir, "text")
        self.audio_dir = os.path.join(self.output_dir, "audio")
        self.music_dir = os.path.join(self.output_dir, "music")
        self.video_dir = os.path.join(self.output_dir, "video")
        self.final_dir = os.path.join(self.output_dir, "final")
        
        for directory in [self.text_dir, self.audio_dir, self.music_dir, self.video_dir, self.final_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Step 1: Generate script
        script_result = self.text_generator.generate_short_script(
            topic=topic,
            target_duration=duration,
            output_file=os.path.join(self.text_dir, f"{output_name}_script.txt")
        )
        script = script_result["text"]
        
        # Step 2: Generate voiceover
        voiceover_result = self.audio_generator.generate_speech(
            text=script,
            output_path=os.path.join(self.audio_dir, f"{output_name}_voiceover.mp3"),
            voice_id=voice_id
        )
        voiceover_path = voiceover_result["output_path"]
        actual_duration = voiceover_result["metadata"]["duration"]
        
        # Step 3: Generate background music
        music_prompt = f"Background music for a YouTube Short about {topic}. Upbeat, energetic, and engaging."
        music_result = self.music_generator.create_music_for_voiceover(
            prompt=music_prompt,
            voiceover_path=voiceover_path,
            output_path=os.path.join(self.music_dir, f"{output_name}_music.mp3")
        )
        music_path = music_result["output_path"]
        
        # Step 4: Generate video with custom style
        if style == "cinematic":
            video_prompt = f"A cinematic YouTube Short about {topic} with professional lighting, camera movement, and film-like quality. Dramatic visuals with depth of field."
        elif style == "minimalist":
            video_prompt = f"A minimalist YouTube Short about {topic} with clean, simple visuals, neutral colors, and elegant typography. Modern and sleek aesthetic."
        elif style == "retro":
            video_prompt = f"A retro-styled YouTube Short about {topic} with vintage filters, old film grain effect, and 80s/90s aesthetic. Nostalgic visuals."
        else:
            video_prompt = f"A visually engaging YouTube Short about {topic}. Dynamic visuals with motion and energy."
        
        video_result = self.video_generator.generate_video_from_text(
            prompt=video_prompt,
            output_path=os.path.join(self.video_dir, f"{output_name}_video.mp4"),
            duration=actual_duration
        )
        video_path = video_result["output_path"]
        
        # Step 5: Add audio to video
        video_with_audio_path = os.path.join(self.video_dir, f"{output_name}_with_audio.mp4")
        self.video_generator.add_audio_to_video(
            video_path=video_path,
            audio_path=voiceover_path,
            output_path=video_with_audio_path
        )
        
        # Step 6: Add captions if requested
        final_video_path = os.path.join(self.final_dir, f"{output_name}.mp4")
        if add_captions:
            self.video_generator.add_text_overlay(
                video_path=video_with_audio_path,
                text=script,
                output_path=final_video_path
            )
        else:
            # Just copy the video with audio to the final path
            import shutil
            shutil.copy(video_with_audio_path, final_video_path)
        
        # Create metadata
        from datetime import datetime
        metadata = {
            "topic": topic,
            "style": style,
            "creation_date": datetime.now().isoformat(),
            "duration": actual_duration,
            "files": {
                "script": os.path.join(self.text_dir, f"{output_name}_script.txt"),
                "voiceover": voiceover_path,
                "music": music_path,
                "video": video_path,
                "video_with_audio": video_with_audio_path,
                "final_video": final_video_path
            }
        }
        
        metadata_path = os.path.join(self.final_dir, f"{output_name}_metadata.json")
        import json
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        return {
            "output_path": final_video_path,
            "metadata_path": metadata_path,
            "metadata": metadata
        }

# Use the styled creator
styled_creator = StyledYouTubeShortsCreator({"output_dir": "styled_output"})

# Create shorts with different styles
cinematic_result = styled_creator.create_short(
    topic="The art of cinematography",
    output_name="cinematic_style",
    duration=30,
    style="cinematic"
)

minimalist_result = styled_creator.create_short(
    topic="Minimalism in modern design",
    output_name="minimalist_style",
    duration=30,
    style="minimalist"
)

retro_result = styled_creator.create_short(
    topic="The evolution of video games",
    output_name="retro_style",
    duration=30,
    style="retro"
)

print(f"Cinematic style video: {cinematic_result['output_path']}")
print(f"Minimalist style video: {minimalist_result['output_path']}")
print(f"Retro style video: {retro_result['output_path']}")
```

These examples demonstrate the flexibility and power of the YouTube Shorts AI Pipeline for creating various types of content with different styles and customizations.
