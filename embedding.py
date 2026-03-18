import os
import pickle
from deepface import DeepFace

# Path to your face database
face_db_path = "C:\\Users\\SANDINI KANNANGARA\\Desktop\\Face Based Attendance System\\image database"
embedding_file = "face_embeddings.pkl"

def generate_and_save_embeddings():
    known_faces = {}
    for person_name in os.listdir(face_db_path):
        person_folder = os.path.join(face_db_path, person_name)
        if os.path.isdir(person_folder):
            for filename in os.listdir(person_folder):
                img_path = os.path.join(person_folder, filename)
                try:
                    embedding = DeepFace.represent(img_path, model_name="Facenet", enforce_detection=False)[0]['embedding']
                    known_faces[person_name] = embedding
                    print(f"Saved embedding for: {person_name}")
                    break  # Only one image per person
                except Exception as e:
                    print(f"Error with {filename}: {e}")

    # Save embeddings to file
    with open(embedding_file, "wb") as f:
        pickle.dump(known_faces, f)
    print("All embeddings saved to file successfully.")

if __name__ == "__main__":
    generate_and_save_embeddings()
