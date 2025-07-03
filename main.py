import cv2
import sqlite3
from datetime import datetime

# === DATABASE SETUP ===
conn = sqlite3.connect('faces.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS face_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT
    )
''')
conn.commit()

# === FACE DETECTION SETUP ===
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

print("Press 'q' to quit.")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles around faces and log to database
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Insert face detection timestamp into DB
        cursor.execute("INSERT INTO face_log (timestamp) VALUES (?)", (datetime.now().isoformat(),))
        conn.commit()

    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()
conn.close()
