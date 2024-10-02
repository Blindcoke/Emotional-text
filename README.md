Emotions App
This project is an emotion recognition web application powered by FastAPI for the backend and ONNX with Roberta for text classification. The app processes user input (both text and voice) and predicts associated emotions. It uses GPU acceleration via Docker, leveraging NVIDIA drivers for efficient processing.

Table of Contents
Features
Architecture
Installation
Usage
API Endpoints
Contributing
License
Features
Text and voice input for emotion classification.
GPU-accelerated inference using ONNX and NVIDIA's TensorRT.
Emotion classification with Roberta model.
Real-time voice transcription and analysis.
CORS-enabled for integration with various frontends.
Dockerized setup for easy deployment with FastAPI.
Architecture
FastAPI: Backend for handling HTTP requests and API endpoints.
ONNXRuntime: Optimized model inference using Roberta model for sequence classification.
Whisper: Used for speech-to-text transcription.
Docker: Containerized app setup using NVIDIA GPU for optimized performance.
Installation
Prerequisites
Docker installed on your system.
NVIDIA GPU with drivers configured (for GPU-based inference).
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/emotions-app.git
cd emotions-app
Ensure your NVIDIA drivers and Docker are configured properly for GPU acceleration.

Build and start the containers using docker-compose:

bash
Copy code
docker-compose up --build
This will build the containers for the AI model and web services, and expose the application on port 80.

Docker Services
ai: The container running the AI emotion recognition model.
web: The frontend service for interacting with the app (if included).
Usage
After installation, you can access the app by navigating to:

arduino
Copy code
http://localhost:80
Text Prediction
Enter a sentence in the input field.
Click submit to see the emotion predictions.
Voice Prediction
Switch to "Voice Mode."
Click the recording button to start recording.
Click stop when finished. The app will transcribe the voice and predict emotions.
API Endpoints
/predict (POST)

Description: Analyzes the text and predicts emotions.
Request Body:
json
Copy code
{
  "text": "I am feeling great!"
}
Response:
json
Copy code
{
  "predictions": [
    {
      "label": "joy",
      "score": 0.98
    }
  ],
  "sentences": ["I am feeling great!"],
  "symbol_emojies": [""]
}
/transcribe (POST)

Description: Transcribes the voice from an uploaded audio file and predicts emotions.
Request: Upload audioFile in the form-data.
Response:
json
Copy code
{
  "predictions": [...],
  "sentences": [...],
  "symbol_emojies": [...]
}
Contributing
If you want to contribute to this project, feel free to create a pull request or submit an issue. We welcome all suggestions for improvement.

License
This project is licensed under the MIT License.
