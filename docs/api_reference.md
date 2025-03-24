# API Reference

This document provides detailed information about the API for each module in the YouTube Shorts AI Pipeline.

## Text Generation Module

The text generation module uses Rytr to create engaging scripts for YouTube Shorts.

### TextGenerator Class

```python
from src.text_generation import TextGenerator
```

#### Initialization

```python
generator = TextGenerator(api_key=None)
```

- `api_key` (str, optional): Rytr API key. If not provided, will look for RYTR_API_KEY in environment variables.

#### Methods

##### generate_short_script

```python
result = generator.generate_short_script(
    topic,
    target_duration=30,
    output_file=None,
    tone="Enthusiastic",
    use_case="Script Writing"
)
```

- `topic` (str): The topic or idea for the YouTube Short
- `target_duration` (int, optional): Target duration in seconds. Defaults to 30.
- `output_file` (str, optional): Path to save the script. Defaults to None.
- `tone` (str, optional): Tone of the script. Defaults to "Enthusiastic".
- `use_case` (str, optional): Rytr use case. Defaults to "Script Writing".

**Returns**: dict with keys:
- `text`: The generated script
- `output_path`: Path to the saved script file (if output_file was provided)
- `metadata`: Dictionary with generation details

## Audio Generation Module

The audio generation module uses ElevenLabs to convert scripts to natural-sounding voiceovers.

### AudioGenerator Class

```python
from src.audio_generation import AudioGenerator
```

#### Initialization

```python
generator = AudioGenerator(api_key=None)
```

- `api_key` (str, optional): ElevenLabs API key. If not provided, will look for ELEVENLABS_API_KEY in environment variables.

#### Methods

##### list_voices

```python
voices = generator.list_voices()
```

**Returns**: list of available voices with their details

##### find_voice

```python
voice = generator.find_voice(gender=None, name=None, accent=None)
```

- `gender` (str, optional): Voice gender ("male" or "female")
- `name` (str, optional): Voice name
- `accent` (str, optional): Voice accent

**Returns**: dict with voice details or None if no match

##### generate_speech

```python
result = generator.generate_speech(
    text,
    output_path,
    voice_id=None,
    model_id="eleven_monolingual_v1",
    stability=0.5,
    similarity_boost=0.75
)
```

- `text` (str): Text to convert to speech
- `output_path` (str): Path to save the audio file
- `voice_id` (str, optional): Voice ID to use. Defaults to None (auto-select).
- `model_id` (str, optional): TTS model ID. Defaults to "eleven_monolingual_v1".
- `stability` (float, optional): Voice stability. Defaults to 0.5.
- `similarity_boost` (float, optional): Voice similarity boost. Defaults to 0.75.

**Returns**: dict with keys:
- `output_path`: Path to the saved audio file
- `metadata`: Dictionary with generation details

##### optimize_script_for_tts

```python
optimized_text = generator.optimize_script_for_tts(text)
```

- `text` (str): Original script text

**Returns**: str: Optimized text for TTS

## Video Generation Module

The video generation module uses Runway to create visually appealing videos.

### VideoGenerator Class

```python
from src.video_generation import VideoGenerator
```

#### Initialization

```python
generator = VideoGenerator(api_key=None)
```

- `api_key` (str, optional): Runway API key. If not provided, will look for RUNWAY_API_KEY in environment variables.

#### Methods

##### generate_video_from_text

```python
result = generator.generate_video_from_text(
    prompt,
    output_path,
    duration=10,
    width=768,
    height=1344
)
```

- `prompt` (str): The text prompt describing the video
- `output_path` (str): The path to save the video file to
- `duration` (int, optional): Duration in seconds. Defaults to 10.
- `width` (int, optional): Video width. Defaults to 768.
- `height` (int, optional): Video height. Defaults to 1344 (9:16 aspect ratio for Shorts).

**Returns**: dict with keys:
- `output_path`: Path to the saved video file
- `metadata`: Dictionary with generation details

##### generate_video_from_image

```python
result = generator.generate_video_from_image(
    image_path,
    prompt,
    output_path,
    duration=10
)
```

- `image_path` (str): Path to the input image
- `prompt` (str): The text prompt describing the video
- `output_path` (str): The path to save the video file to
- `duration` (int, optional): Duration in seconds. Defaults to 10.

**Returns**: dict with keys:
- `output_path`: Path to the saved video file
- `metadata`: Dictionary with generation details

##### add_audio_to_video

```python
output_path = generator.add_audio_to_video(
    video_path,
    audio_path,
    output_path
)
```

- `video_path` (str): Path to the input video
- `audio_path` (str): Path to the audio file
- `output_path` (str): The path to save the combined video file to

**Returns**: str: The path to the saved video file

##### add_text_overlay

```python
output_path = generator.add_text_overlay(
    video_path,
    text,
    output_path,
    font_size=40,
    color='white',
    position='bottom'
)
```

- `video_path` (str): Path to the input video
- `text` (str): Text to overlay
- `output_path` (str): The path to save the video file to
- `font_size` (int, optional): Font size. Defaults to 40.
- `color` (str, optional): Text color. Defaults to 'white'.
- `position` (str, optional): Text position ('top', 'center', 'bottom'). Defaults to 'bottom'.

**Returns**: str: The path to the saved video file

##### create_youtube_short

```python
result = generator.create_youtube_short(
    prompt,
    audio_path=None,
    output_path=None,
    add_captions=False,
    caption_text=None
)
```

- `prompt` (str): The text prompt describing the video
- `audio_path` (str, optional): Path to the audio file. Defaults to None.
- `output_path` (str, optional): The path to save the final video. Defaults to None.
- `add_captions` (bool, optional): Whether to add captions. Defaults to False.
- `caption_text` (str, optional): Text for captions. Defaults to None.

**Returns**: dict with keys:
- `output_path`: Path to the saved video file
- `metadata`: Dictionary with generation details

## Music Generation Module

The music generation module uses Suno to create background music.

### MusicGenerator Class

```python
from src.music_generation import MusicGenerator
```

#### Initialization

```python
generator = MusicGenerator(api_key=None)
```

- `api_key` (str, optional): Suno API key. If not provided, will look for SUNO_API_KEY in environment variables.

#### Methods

##### generate_background_music

```python
result = generator.generate_background_music(
    prompt,
    output_path,
    duration=30,
    genre=None,
    mood=None,
    tempo=None
)
```

- `prompt` (str): The text prompt describing the music
- `output_path` (str): The path to save the audio file to
- `duration` (int, optional): Approximate duration in seconds. Defaults to 30.
- `genre` (str, optional): Music genre. Defaults to None.
- `mood` (str, optional): Mood of the music. Defaults to None.
- `tempo` (str, optional): Tempo of the music. Defaults to None.

**Returns**: dict with keys:
- `output_path`: Path to the saved audio file
- `metadata`: Dictionary with generation details

##### adjust_music_duration

```python
output_path = generator.adjust_music_duration(
    music_path,
    target_duration,
    output_path=None
)
```

- `music_path` (str): Path to the input music file
- `target_duration` (float): Target duration in seconds
- `output_path` (str, optional): Path to save the adjusted music. Defaults to None (overwrites input).

**Returns**: str: Path to the adjusted music file

##### adjust_music_volume

```python
output_path = generator.adjust_music_volume(
    music_path,
    volume_adjustment_db,
    output_path=None
)
```

- `music_path` (str): Path to the input music file
- `volume_adjustment_db` (float): Volume adjustment in decibels (negative values reduce volume)
- `output_path` (str, optional): Path to save the adjusted music. Defaults to None (overwrites input).

**Returns**: str: Path to the adjusted music file

##### create_music_for_voiceover

```python
result = generator.create_music_for_voiceover(
    prompt,
    voiceover_path,
    output_path,
    volume_reduction_db=-10
)
```

- `prompt` (str): The text prompt describing the music
- `voiceover_path` (str): Path to the voiceover audio file
- `output_path` (str): Path to save the music file
- `volume_reduction_db` (float, optional): Volume reduction in decibels. Defaults to -10.

**Returns**: dict with keys:
- `output_path`: Path to the saved audio file
- `metadata`: Dictionary with generation details

## Pipeline Integration

The pipeline integration module combines all components into a seamless workflow.

### YouTubeShortsCreator Class

```python
from src.pipeline_integration import YouTubeShortsCreator
```

#### Initialization

```python
creator = YouTubeShortsCreator(config=None)
```

- `config` (dict, optional): Configuration dictionary. Defaults to None.

#### Methods

##### create_short

```python
result = creator.create_short(
    topic,
    output_name=None,
    voice_id=None,
    duration=30,
    add_captions=True
)
```

- `topic` (str): The topic or idea for the YouTube Short
- `output_name` (str, optional): Base name for output files. Defaults to timestamp.
- `voice_id` (str, optional): Voice ID for TTS. Defaults to None (auto-select).
- `duration` (int, optional): Target duration in seconds. Defaults to 30.
- `add_captions` (bool, optional): Whether to add captions. Defaults to True.

**Returns**: dict with keys:
- `output_path`: Path to the final video file
- `metadata_path`: Path to the metadata JSON file
- `metadata`: Dictionary with all generation details
