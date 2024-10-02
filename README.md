# Emotions App

This project is an emotion recognition web application powered by FastAPI for the backend and ONNX with Roberta for text classification. The app processes user input (both text and voice) and predicts associated emotions. It uses GPU acceleration via Docker, leveraging NVIDIA drivers for efficient processing.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Text and voice input for emotion classification.
- GPU-accelerated inference using ONNX and NVIDIA's TensorRT.
- Emotion classification with Roberta model.
- Real-time voice transcription and analysis.
- CORS-enabled for integration with various frontends.
- Dockerized setup for easy deployment with FastAPI.

## Architecture
- FastAPI: Backend for handling HTTP requests and API endpoints.
- ONNXRuntime: Optimized model inference using Roberta model for sequence classification.
- Whisper: Used for speech-to-text transcription.
- Docker: Containerized app setup using NVIDIA GPU for optimized performance.

## Installation

### Prerequisites
- Docker installed on your system.
- NVIDIA GPU with drivers configured (for GPU-based inference).

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/emotions-app.git
   cd emotions-app
2. Ensure your NVIDIA drivers and Docker are configured properly for GPU acceleration.
3. Build and start the containers using docker-compose:

   ```bash
   docker-compose up --build
This will build the containers for the AI model and web services, and expose the application on port 80.

## Docker Services
* ai: The container running the AI emotion recognition model.
* web: The frontend service for interacting with the app (if included).

## Usage
After installation, you can access the app by navigating to: http://localhost:80

### Text Prediction
1. Enter a sentence in the input field.
2. Click submit to see the emotion predictions.

### Voice Prediction
1. Switch to "Voice Mode."
2. Click the recording button to start recording.
3. Click stop when finished.
4. The app will transcribe the voice and predict emotions.

# Contributing

If you want to contribute to this project, feel free to create a pull request or submit an issue. We welcome all suggestions for improvement.

# License

This project is licensed under the MIT License.

---

This Markdown-formatted content is ready to be added directly to your GitHub `README.md` file. It includes all the sections you provided, properly formatted with headers, code blocks, and lists.
