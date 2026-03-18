import os
import cv2
import subprocess
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# === CONFIG ===
face_db_path = "C:\\Users\\SANDINI KANNANGARA\\Desktop\\Face Based Attendance System\\image database"
embedding_script = "embedding.py"  # Your existing embedding generator

# === Function to Capture and Save Face Image ===
def capture_and_save_image(user_folder, user_name):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not accessible.")
        speak("Webcam not accessible.")
        return

    print("Press 'c' to capture image. Press 'q' to cancel.")
    speak("Press C to capture image.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from webcam.")
            break

        cv2.imshow("Capture Face", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            # Count existing images to name the new one correctly
            existing_images = [f for f in os.listdir(user_folder) if f.endswith(".jpg")]
            img_count = len(existing_images) + 1
            image_path = os.path.join(user_folder, f"{user_name}_{img_count}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image saved at {image_path}")
            speak("Image saved successfully.")
            break
        elif key == ord('q'):
            print("Cancelled.")
            speak("Cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()

# === Function to Trigger Embedding Script ===
def update_embeddings():
    try:
        subprocess.run(["python", embedding_script], check=True)
        print("Embeddings updated successfully.")
        speak("Embeddings updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating embeddings: {e}")
        speak("Failed to update embeddings.")

# === MAIN ===
if __name__ == "__main__":
    print("\n1. Add New User")
    print("2. Add Image to Existing User")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == '1':
        user_name = input("Enter the name of the new user: ").strip()
        if user_name:
            user_folder = os.path.join(face_db_path, user_name)
            os.makedirs(user_folder, exist_ok=True)
            capture_and_save_image(user_folder, user_name)
            update_embeddings()
        else:
            print("No name entered.")
            speak("No name entered.")

    elif choice == '2':
        users = os.listdir(face_db_path)
        if not users:
            print("No existing users found.")
            speak("No existing users found.")
        else:
            print("\nExisting Users:")
            for idx, user in enumerate(users, start=1):
                print(f"{idx}. {user}")
            try:
                selected = int(input("Select user by number: ").strip())
                if 1 <= selected <= len(users):
                    user_name = users[selected - 1]
                    user_folder = os.path.join(face_db_path, user_name)
                    capture_and_save_image(user_folder, user_name)
                    update_embeddings()
                else:
                    print("Invalid selection.")
                    speak("Invalid selection.")
            except ValueError:
                print("Invalid input.")
                speak("Invalid input.")
    else:
        print("Invalid choice.")
        speak("Invalid choice.")
