# Contributing to YouTube Shorts AI Pipeline

Thank you for considering contributing to the YouTube Shorts AI Pipeline project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful, inclusive, and considerate in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

For feature requests or enhancements:
- Use a clear, descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- Include any relevant examples or mockups

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add or update tests as necessary
5. Update documentation as needed
6. Commit your changes (`git commit -m 'Add some feature'`)
7. Push to the branch (`git push origin feature/your-feature-name`)
8. Open a Pull Request

## Development Setup

1. Clone your fork of the repository
2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development dependencies
```

3. Create a `.env` file with your API keys for testing

## Coding Standards

- Follow PEP 8 style guidelines
- Write docstrings for all functions, classes, and modules
- Include type hints where appropriate
- Write unit tests for new functionality
- Ensure all tests pass before submitting a pull request

## Testing

Run tests using pytest:
```bash
pytest
```

## Documentation

- Update documentation for any changes to functionality
- Follow the existing documentation style
- Include examples for new features

## Versioning

We use Semantic Versioning (SemVer) for this project:
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
