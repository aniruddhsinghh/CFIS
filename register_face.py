import os
import sqlite3
import shutil
import face_recognition

# === DB SETUP ===
conn = sqlite3.connect('faces.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        image_path TEXT NOT NULL,
        crime TEXT
    )
''')
conn.commit()

# === CREATE FOLDER TO SAVE FACES ===
os.makedirs("registered_faces", exist_ok=True)

# === GET USER INFO ===
person_id = input("Enter Person ID: ")
name = input("Enter Name: ")
crime = input("Enter Associated Crime (leave blank if none): ")
source_path = input("Enter full path to face image (e.g. C:/Users/.../myface.jpg): ")

# === CHECK IF FACE EXISTS IN IMAGE ===
image = face_recognition.load_image_file(source_path)
encodings = face_recognition.face_encodings(image)

if not encodings:
    print("[ERROR] No face detected in the provided image. Try another one.")
    conn.close()
    exit()

# === COPY IMAGE TO PROJECT FOLDER ===
filename = f"{person_id}_{name}.jpg"
dest_path = os.path.join("registered_faces", filename)
shutil.copy(source_path, dest_path)

try:
    cursor.execute("ALTER TABLE persons ADD COLUMN crime TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

# === INSERT TO DB ===
cursor.execute("INSERT INTO persons (id, name, image_path, crime) VALUES (?, ?, ?, ?)",
               (person_id, name, dest_path, crime))
conn.commit()

print(f"[SUCCESS] Registered {name} with ID {person_id}")

conn.close()
