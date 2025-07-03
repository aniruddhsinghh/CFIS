# 🔍 Criminal Face Identification System (CFIS)

CFIS is an AI-based facial recognition system for criminal identification. It combines OpenCV, Mediapipe, and face recognition libraries with a web dashboard and real-time alert system.

## 🚀 Features

- 🎯 Face Detection & Recognition
- 🧠 468 Landmark Extraction (Mediapipe)
- 📸 Live Webcam Integration
- 🗂 SQLite-based Criminal Database
- 💬 Telegram Bot for Alerts
- 🌐 Flask Web Dashboard
- 🧊 (Planned) 3D Face Model Support

## 📁 Project Structure

├── cfis_recognition.py # Core recognition logic
├── cfis_recognition_mediapipe.py # Landmark detection module
├── register_face.py # Face registration
├── main.py # Entry point
├── cfis_web/ # Flask web dashboard
├── registered_faces/ # Stored face images
├── faces.db # SQLite database
├── test_landmarks.py # Test scripts
└── 3d_model/ # (Planned) 3D model logic

## 💻 Run Instructions

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the main program
python main.py

# 3. Start the web dashboard
cd cfis_web
python app.py