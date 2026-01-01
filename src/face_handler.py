import os
import cv2
import numpy as np
import face_recognition as face_recognition_lib

from datetime import datetime
import random
import tkinter.messagebox as messagebox

KNOWN_FACES_DIR = os.path.join('data', 'known_faces')
UNKNOWN_FACES_DIR = os.path.join('data', 'unknown_faces')

os.makedirs(UNKNOWN_FACES_DIR, exist_ok=True)
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

known_encodings = []
known_names = []


def load_known_faces():
    global known_encodings, known_names
    known_encodings = []
    known_names = []

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".png")):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition_lib.load_image_file(path)
            encodings = face_recognition_lib.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
            else:
                print(f"[Warning]: No faces found in {filename}. Skipping.")


def reload_known_faces():
    global known_encodings, known_names
    known_encodings = []
    known_names = []
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".png")):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition_lib.load_image_file(path)
            encodings = face_recognition_lib.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    print("[INFO]: Reloaded known faces from directory.")


def recognize_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition_lib.face_locations(rgb_frame)
    face_encodings = []

    if face_locations:
        try:
            face_encodings = face_recognition_lib.face_encodings(rgb_frame, face_locations)
        except Exception as e:
            print(f"[Error]: Face encoding failed: {e}")
            face_encodings = []

    face_names = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        if known_encodings:
            distances = face_recognition_lib.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(distances)
            if distances[best_match_index] < 0.4:
                name = known_names[best_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        face_names.append(name)

        if name == "Unknown":
            now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            top_c = max(0, top)
            bottom_c = min(frame.shape[0], bottom)
            left_c = max(0, left)
            right_c = min(frame.shape[1], right)

            if bottom_c > top_c and right_c > left_c:
                face_crop = frame[top_c:bottom_c, left_c:right_c]
                if face_crop.size > 0:
                    filename = f"unknown_{now_str}_{random.randint(1000, 9999)}.jpg"
                    save_path = os.path.join(UNKNOWN_FACES_DIR, filename)
                    success = cv2.imwrite(save_path, face_crop)
                    if success:
                        print(f"[INFO]: Saved unknown face to {save_path}.")

    return frame, face_names


def capture_and_save_face(name):
    from motion_detection import open_camera

    cap = open_camera()
    if cap is None:
        messagebox.showerror("Camera Error", "Could not access camera. Please check if it's connected and not being used by another application.")
        return

    cv2.namedWindow("Register New Face - Press 'S' to Save, 'Q' to Quit")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[Error]: Failed to capture image from webcam.")
                break

            cv2.putText(frame, "Press 'S' to Save | 'Q' to Quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow("Register New Face - Press 'S' to Save, 'Q' to Quit", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition_lib.face_locations(rgb_frame)
                if face_locations:
                    top, right, bottom, left = face_locations[0]
                    face_image = frame[top:bottom, left:right]
                    path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
                    cv2.imwrite(path, face_image)
                    print(f"[INFO]: Registered {name} successfully at {path}.")
                    messagebox.showinfo("Success", f"Face registered for {name}!")
                    reload_known_faces()
                else:
                    messagebox.showwarning("No Face", "No face detected in the frame.")
                break
            elif key == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


load_known_faces()
