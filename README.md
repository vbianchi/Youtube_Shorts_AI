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
