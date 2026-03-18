import tkinter as tk
from tkinter import Label, Button, Entry, messagebox, Toplevel, StringVar, OptionMenu
import os
import cv2
import subprocess
import time
import pyttsx3

# === CONFIG ===
face_db_path = "image database"  # Ensure this path exists
embedding_script = "embedding.py"

# === Initialize TTS ===
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# === Capture and Save Image ===
def capture_and_save_image(user_folder, user_name, window):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Webcam Error", "Could not open webcam.")
        speak("Webcam not accessible.")
        return

    messagebox.showinfo("Instructions", "Press 'C' to capture image. Press 'Q' to cancel.")
    speak("Press C to capture image")

    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Webcam Error", "Failed to read from webcam.")
            break

        cv2.imshow("Capture Face", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            existing_images = [f for f in os.listdir(user_folder) if f.endswith(".jpg")]
            img_count = len(existing_images) + 1
            image_path = os.path.join(user_folder, f"{user_name}_{img_count}.jpg")
            cv2.imwrite(image_path, frame)
            messagebox.showinfo("Success", f"Image saved at {image_path}")
            speak("Image saved successfully")
            break
        elif key == ord('q'):
            speak("Cancelled")
            break

    cap.release()
    cv2.destroyAllWindows()
    window.destroy()
    update_embeddings()

# === Update Embeddings ===
def update_embeddings():
    try:
        subprocess.run(["python", embedding_script], check=True)
        messagebox.showinfo("Success", "Embeddings updated successfully.")
        speak("Embeddings updated successfully")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to update embeddings.")
        speak("Failed to update embeddings")

# === Add New or Existing Face ===
def open_add_face_window():
    choice_window = Toplevel(root)
    choice_window.title("Add Face")
    choice_window.geometry("400x300")
    choice_window.configure(bg="cadet blue")

    Label(choice_window, text="Select Option", font=("Arial", 18, "bold italic"), fg="white", bg="cadet blue")\
        .pack(pady=20)

    def new_user():
        choice_window.destroy()
        open_capture_window(new_user=True)

    def existing_user():
        choice_window.destroy()
        open_capture_window(new_user=False)

    Button(choice_window, text="Add New User", command=new_user, width=20, font=("Arial", 12)).pack(pady=10)
    Button(choice_window, text="Add to Existing User", command=existing_user, width=20, font=("Arial", 12)).pack(pady=10)

# === Window to Capture Image ===
def open_capture_window(new_user=True):
    capture_window = Toplevel(root)
    capture_window.title("Capture Face")
    capture_window.geometry("500x400")
    capture_window.configure(bg="cadet blue")

    Label(capture_window, text="Enter Name:" if new_user else "Select User:",
          font=("Arial", 18, "bold italic"), bg="cadet blue", fg="white").pack(pady=20)

    name_var = StringVar()

    if new_user:
        name_entry = Entry(capture_window, textvariable=name_var, font=("Arial", 14), width=30)
        name_entry.pack(pady=10)
    else:
        users = os.listdir(face_db_path)
        if not users:
            messagebox.showwarning("No Users", "No existing users found.")
            speak("No existing users found")
            capture_window.destroy()
            return
        name_var.set(users[0])
        OptionMenu(capture_window, name_var, *users).pack(pady=10)

    Button(capture_window, text="Capture",
           command=lambda: proceed_to_capture(name_var.get(), capture_window),
           font=("Arial", 12), bg="#2C3E50", fg="white", width=15).pack(pady=20)

# === Start Capture Process ===
def proceed_to_capture(user_name, window):
    if not user_name:
        messagebox.showwarning("Input Error", "Name cannot be empty.")
        return
    user_folder = os.path.join(face_db_path, user_name)
    os.makedirs(user_folder, exist_ok=True)
    capture_and_save_image(user_folder, user_name, window)

# === Main Window ===
root = tk.Tk()
root.title("AttendiFY")
root.geometry("600x500")
root.configure(bg="#2C3E50")

try:
    bg_img = tk.PhotoImage(file="background.png")
    Label(root, image=bg_img).place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

Label(root, text="AttendiFY", font=("Arial", 30, "bold italic"), fg="white", bg="#2C3E50")\
    .place(relx=0.5, rely=0.2, anchor="center")

button_style = {
    "font": ("Arial", 12, "bold italic"),
    "fg": "white",
    "bg": "#3498DB",
    "activebackground": "#2980B9",
    "width": 15,
    "height": 2,
    "bd": 5,
    "relief": "groove"
}

Button(root, text="Add Face", command=open_add_face_window, **button_style)\
    .place(relx=0.5, rely=0.5, anchor="center")

Button(root, text="Detect Face", command=lambda: subprocess.run(["python", "main.py"]), **button_style)\
    .place(relx=0.5, rely=0.7, anchor="center")

root.mainloop()
