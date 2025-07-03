import mediapipe as mp
import cv2

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for i, lm in enumerate(face_landmarks.landmark):
                x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                confidence = lm.visibility if lm.HasField('visibility') else lm.z  # z can be used as proxy
                color = (0, 255, 0) if confidence > 0.5 else (0, 0, 255)
                cv2.circle(frame, (x, y), 1, color, -1)

    cv2.imshow("Landmark Confidence Heatmap", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
