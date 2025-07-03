import cv2
import face_recognition
import sqlite3
import numpy as np
import os
import mediapipe as mp
import requests

# Initialize Mediapipe for facial landmark detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Load data from DB
conn = sqlite3.connect("faces.db")
cursor = conn.cursor()

cursor.execute("SELECT id, name, image_path, crime FROM persons")
known_face_encodings = []
known_face_names = []
known_face_crimes = []

for id, name, image_path, crime in cursor.fetchall():
    if os.path.exists(image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
            known_face_crimes.append(crime)

# Webcam
video_capture = cv2.VideoCapture(0)
alerted_names = set()

print(">> Press 'q' to quit")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces using face_recognition (for encoding comparison)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Detect face landmarks using Mediapipe
    results = face_mesh.process(rgb_small_frame)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        crime = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                crime = known_face_crimes[best_match_index]

        # Check the confidence of the face landmarks
        confidence = 0
        if results.multi_face_landmarks:
            for landmarks in results.multi_face_landmarks:
                # Calculate confidence based on landmarks (you can define your logic here)
                confidence = len(landmarks.landmark) / 468  # Normalize confidence (based on total landmarks)

        # If confidence is high, send an alert and avoid duplicate alerts
        if confidence > 0.8 and name not in alerted_names:
            print(f"[ALERT] {name} detected. Crime: {crime}")
            alerted_names.add(name)

            # === Telegram Alert ===
            try:
                bot_token = '7465077112:AAG3ko00l1gqv0t0GhKLb05O8vbHU7yjoJ8'
                chat_id = '1334229039'
                message = f"⚠️ ALERT: {name} detected.\nCrime: {crime}"

                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                params = {
                    "chat_id": chat_id,
                    "text": message
                }

                response = requests.get(url, params=params)

                if response.status_code == 200:
                    print("[ALERT SENT on Telegram]")
                else:
                    print("[ERROR] Telegram responded:", response.text)
            except Exception as e:
                print("[ERROR] Failed to send Telegram alert:", str(e))

        # Draw the detected face bounding box
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 1)

    cv2.imshow("CFIS - Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
