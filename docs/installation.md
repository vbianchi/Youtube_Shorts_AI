# Installation Guide

This guide provides detailed instructions for installing and setting up the YouTube Shorts AI Pipeline.

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
- **Python**: Version 3.10 or higher
- **Storage**: At least 2GB of free disk space
- **RAM**: Minimum 8GB recommended
- **Internet Connection**: Required for API access

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-shorts-pipeline.git
cd youtube-shorts-pipeline
```

### 2. Set Up Python Environment

#### Using venv (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Using conda

```bash
conda create -n youtube-shorts python=3.10
conda activate youtube-shorts
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

You'll need to obtain API keys from the following services:

#### Rytr (Text Generation)
1. Sign up at [Rytr](https://rytr.me/)
2. Navigate to your account settings
3. Generate an API key

#### ElevenLabs (Text-to-Speech)
1. Create an account at [ElevenLabs](https://elevenlabs.io/)
2. Go to your profile settings
3. Find or generate your API key

#### Runway (Video Generation)
1. Sign up at [Runway](https://runwayml.com/)
2. Access your account settings
3. Create an API key

#### Suno (Music Generation)
1. Create an account at [Suno](https://suno.ai/)
2. Navigate to API settings
3. Generate a new API key

### 5. Configure Environment Variables

Create a `.env` file in the project root directory with the following content:

```
RYTR_API_KEY=your_rytr_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
RUNWAY_API_KEY=your_runway_api_key
SUNO_API_KEY=your_suno_api_key
```

Replace `your_*_api_key` with the actual API keys you obtained.

### 6. Verify Installation

Run the test script to verify that everything is set up correctly:

```bash
python test_pipeline.py
```

If all tests pass, your installation is complete and working correctly.

## Troubleshooting

### Common Issues

#### ModuleNotFoundError
If you encounter a "ModuleNotFoundError", ensure that:
1. Your virtual environment is activated
2. All dependencies are installed: `pip install -r requirements.txt`
3. You're running commands from the project root directory

#### API Authentication Errors
If you encounter API authentication errors:
1. Verify that your API keys are correct
2. Check that the `.env` file is in the correct location
3. Ensure the environment variables are being loaded properly

#### Video Generation Issues
If video generation fails:
1. Check your Runway API quota
2. Verify that your prompt is clear and descriptive
3. Try reducing the video duration for testing

### Getting Help

If you encounter issues not covered here:
1. Check the [GitHub Issues](https://github.com/yourusername/youtube-shorts-pipeline/issues) for similar problems
2. Create a new issue with detailed information about your problem
3. Include error messages and steps to reproduce the issue
