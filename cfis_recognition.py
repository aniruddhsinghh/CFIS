import cv2
import face_recognition
import sqlite3
import numpy as np
import os

# Load data from DB
conn = sqlite3.connect("faces.db")
cursor = conn.cursor()

cursor.execute("SELECT name, crime, image_path FROM persons")
known_face_encodings = []
known_face_names = []
known_face_crimes = []

for name, crime, image_path in cursor.fetchall():
    if os.path.exists(image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
            known_face_crimes.append(crime)
        else:
            print(f"[connecting to server]")

        alerted_names = set()  # Keeps track of already alerted names


# Webcam
video_capture = cv2.VideoCapture(0)

print(">> Press 'q' to quit")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                crime = known_face_crimes[best_match_index]

            else:
                crime = "Unknown"

              # Avoid duplicate alerts
            alerted_names = set()  # place this ABOVE the loop

# inside the while loop after identifying a match
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            crime = known_face_crimes[best_match_index]

    # Avoid duplicate alerts
        if name not in alerted_names:
            print(f"[ALERT] {name} detected. Crime: {crime}")
            alerted_names.add(name)

        # === Telegram Alert ===
        try:
            import requests

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


        top *= 4
        right *= 5
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        label = f"{name} | {crime}"
        cv2.putText(frame, label, (left + 6, bottom - 6),
            cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 1)

    cv2.imshow("CFIS - Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
