AttendiFY is an AI-powered face recognition-based attendance system designed to automate attendance marking using real-time computer vision. It replaces traditional methods such as manual entry, ID cards, or biometric scanners with a smart, contactless solution.
The system uses a webcam to detect and recognize faces, verify identity, and record attendance while preventing duplicate entries and spoofing attempts.

* Features

 Real-time face detection using webcam
 Face recognition using deep learning (FaceNet via DeepFace)
 Liveness detection (eye detection to prevent spoofing)
 Duplicate attendance prevention (same person cannot mark twice per day)
 CSV-based attendance logging with date & time
 Voice feedback using text-to-speech
 User-friendly GUI built with Tkinter
 Add new users or update existing users easily

 Project Structure
 project/
│
├── main.py              # Core attendance logic
├── embedding.py         # Face embedding generation
├── UI.py                # GUI interface
├── Add.py               # Add/update user functionality
│
├── image_database/
│   ├── User1/
│   │   ├── img1.jpg
│   │   └── img2.jpg
│   └── User2/
│       ├── img1.jpg
│       └── img2.jpg
│
├── embeddings.pkl       # Stored face embeddings
├── attendance.csv       # Attendance records

How it works
The system stores facial embeddings of users
When a face is detected, a new embedding is generated
It compares the new embedding with stored ones using similarity
If matched, attendance is recorded with timestamp
If already marked, duplicate entry is prevented

 How to Run
01.Clone the repository
02.Install dependencies
03.Run the system
