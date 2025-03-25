# YouTube Shorts AI Pipeline

A comprehensive pipeline to assemble text, audio, video, and music AI-generated content for creating YouTube Shorts videos.

## Overview

This project provides an end-to-end solution for creating YouTube Shorts videos using AI tools. The pipeline integrates multiple AI services to handle different aspects of content creation:

- **Text Generation**: Creates engaging scripts using Rytr
- **Audio Generation**: Converts text to natural-sounding speech using ElevenLabs
- **Video Generation**: Creates visually appealing videos using Runway
- **Music Generation**: Generates background music using Suno

The entire process is automated, allowing you to create professional-quality short videos by simply providing a topic.

## Features

- **Fully Automated Pipeline**: Generate complete YouTube Shorts with minimal input
- **Modular Architecture**: Each component can be used independently or as part of the pipeline
- **Customizable Output**: Control video duration, voice selection, and caption options
- **Web Interface**: User-friendly website for creating and managing shorts
- **API Access**: Programmatic access for integration with other tools

## Installation

### Prerequisites

- Python 3.10+
- Node.js 16+
- API keys for:
  - Rytr (text generation)
  - ElevenLabs (voice generation)
  - Runway (video generation)
  - Suno (music generation)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/vbianchi/youtube_shorts_ai.git
   cd youtube_shorts_ai
   ```

2. Install Python dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to add your API keys.

4. For the web interface, install Node.js dependencies:
   ```bash
   cd website
   npm install
   ```

## Usage

### Command Line

Generate a YouTube Short from the command line:

```bash
python -m src.pipeline_integration.pipeline --topic "The future of AI in content creation" --duration 30 --add-captions
```

### Python API

```python
from src.pipeline_integration import YouTubeShortsCreator

# Initialize the pipeline
creator = YouTubeShortsCreator()

# Create a short
result = creator.create_short(
    topic="Amazing facts about space",
    duration=30,
    add_captions=True
)

print(f"Short created: {result['output_path']}")
```

### Web Interface

1. Start the web server:
   ```bash
   cd website
   npm start
   ```

2. Open your browser and navigate to `http://localhost:3000`

3. Use the web interface to create and manage your YouTube Shorts

## API Key Configuration

Each AI service requires its own API key for authentication:

### Rytr (Text Generation)
- Sign up at https://rytr.me/
- Go to your account settings
- Find the API section and generate a new API key
- Add it to your .env file as `RYTR_API_KEY=your_key_here`

### ElevenLabs (Voice Generation)
- Create an account at https://elevenlabs.io/
- Navigate to your profile settings
- Copy your API key
- Add it to your .env file as `ELEVENLABS_API_KEY=your_key_here`

### Runway (Video Generation)
- Sign up at https://runwayml.com/
- Go to your account settings > API
- Generate a new API key
- Add it to your .env file as `RUNWAY_API_KEY=your_key_here`

### Suno (Music Generation)
- Create an account at https://suno.ai/
- Access your account settings
- Copy your API key
- Add it to your .env file as `SUNO_API_KEY=your_key_here`

## Customization Options

### Script Customization
- Modify the `tone` parameter in `text_generator.py` to change the writing style
- Adjust the `max_length` parameter to control script length
- Change the `language` parameter for different languages

### Voice Customization
- Change the `voice_id` in `audio_generator.py` to use different voices
- Adjust `stability` and `similarity_boost` for voice characteristics
- Modify `model_id` to use different TTS models

### Video Customization
- Change the `style` parameter in `video_generator.py` for different visual styles
- Adjust `resolution` for different video dimensions
- Modify `fps` to change frame rate
- Set `duration` to control video length

### Music Customization
- Change the `mood` parameter in `music_generator.py`
- Adjust `tempo` for faster or slower music
- Modify `genre` for different music styles

## Extending the Pipeline

The modular architecture makes it easy to extend:

### Add New AI Services
- Create a new client class in the appropriate module
- Implement the required API methods
- Update the generator class to use your new client

### Add Post-Processing Features
- Implement video effects in the `video_generator.py`
- Add caption generation in the pipeline integration
- Implement thumbnail generation for YouTube

### Add Analytics
- Track generation metrics
- Implement A/B testing for different styles
- Add performance analytics for video engagement

### Add Multi-Platform Support
- Extend the pipeline to support TikTok format
- Add Instagram Reels support
- Implement Facebook Shorts compatibility

## Permanent Deployment

For a permanent website deployment:

### Frontend Deployment (Vercel)
- Sign up at https://vercel.com/
- Connect your GitHub repository
- Select the website directory as the project root
- Configure build settings (if needed)
- Deploy

### Backend Deployment (Heroku)
- Create an account at https://heroku.com/
- Install Heroku CLI
- Run `heroku create your-app-name`
- Add environment variables for API keys
- Deploy with `git push heroku main`

### Database Setup (MongoDB Atlas)
- Sign up at https://www.mongodb.com/cloud/atlas
- Create a new cluster
- Set up database user and network access
- Connect your application using the connection string

## Documentation

For detailed documentation, see the [docs](./docs) directory:

- [Installation Guide](./docs/installation.md)
- [Usage Guide](./docs/usage.md)
- [API Reference](./docs/api_reference.md)
- [Examples](./docs/examples.md)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
