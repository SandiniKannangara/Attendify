import cv2
import os
import datetime
import pyttsx3
import pandas as pd
from deepface import DeepFace
from scipy.spatial.distance import cosine
import pickle

# -------------------------------
# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -------------------------------
# Paths
face_db_path = "C:\\Users\\SANDINI KANNANGARA\\Desktop\\Face Based Attendance System\\image database"
attendance_file = "attendance.csv"
embedding_file = "face_embeddings.pkl"

# -------------------------------
# Load known embeddings
known_faces = {}

def load_known_faces():
    global known_faces
    if os.path.exists(embedding_file):
        with open(embedding_file, "rb") as f:
            known_faces = pickle.load(f)
        print("Loaded face embeddings.")
        speak("Loaded face embeddings.")
    else:
        print("Embeddings not found.")
        speak("Embeddings not found. Please run the embedding generator.")

# -------------------------------
# Check if already marked today
def has_already_marked(name):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(attendance_file):
        df = pd.read_csv(attendance_file)
        return any((df["Name"] == name) & (df["Time"].str.startswith(today)))
    return False

# -------------------------------
# Mark attendance
def mark_attendance(name):
    if has_already_marked(name):
        print(f"{name} already marked today.")
        speak(f"{name} already marked today.")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(attendance_file) if os.path.exists(attendance_file) else pd.DataFrame(columns=["Name", "Time"])
    df = pd.concat([df, pd.DataFrame([{"Name": name, "Time": timestamp}])], ignore_index=True)
    df.to_csv(attendance_file, index=False)
    print(f"Attendance marked for {name}.")
    speak(f"Attendance marked for {name} at {timestamp}.")

# -------------------------------
# Face recognition using DeepFace
def recognize_face(image):
    try:
        embedding = DeepFace.represent(image, model_name="Facenet", enforce_detection=False)[0]['embedding']
        for name, stored_embedding in known_faces.items():
            similarity = cosine(embedding, stored_embedding)
            if similarity < 0.4:
                return name
    except Exception as e:
        print(f"Recognition error: {e}")
    return None

# -------------------------------
# Liveness check: eye detection
def is_live_face(gray_frame, faces):
    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3)
        if len(eyes) >= 1:
            return True
    return False

# -------------------------------
# Capture and process one live image
def capture_and_process_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        speak("Webcam not found.")
        return

    print("Press 'c' to capture image for attendance.")
    speak("Press C to capture image for attendance.")

    captured_img = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.")
            break

        display = frame.copy()
        cv2.putText(display, "Press 'c' to capture | 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
        cv2.imshow("Face Attendance System", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            captured_img = frame
            print("Image captured.")
            speak("Image captured.")
            break
        elif key == ord('q'):
            print("Cancelled.")
            speak("Attendance cancelled.")
            cap.release()
            cv2.destroyAllWindows()
            return

    cap.release()
    cv2.destroyAllWindows()

    if captured_img is None:
        print("No image captured.")
        return

    # Process image
    gray = cv2.cvtColor(captured_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        print("No face detected.")
        speak("No face detected. Please try again.")
        return

    if not is_live_face(gray, faces):
        print("Spoofing detected!")
        speak("Liveness detection failed. Please use a real face.")
        return

    name = recognize_face(captured_img)
    if name:
        mark_attendance(name)
    else:
        print("Face not recognized.")
        speak("Face not recognized. Please try again.")

# -------------------------------
# Load classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# -------------------------------
# Main program
load_known_faces()
capture_and_process_image()
