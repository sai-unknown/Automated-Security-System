import os
import cv2
import numpy as np
import face_recognition
from datetime import datetime
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import pandas as pd
import random
import threading
import time

stop_flag = False  # Global flag to stop the detection
KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'

# Ensure directories exist
os.makedirs(UNKNOWN_FACES_DIR, exist_ok=True)
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)

# Load known faces once at startup
known_encodings = []
known_names = []
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.lower().endswith((".jpg", ".png")):
        path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(filename)[0])
        else:
            print(f"[Warning]: No faces found in {filename}. Skipping.")


def find_camera():
    """
    Test different camera indices to find a working camera.
    Returns the index of the first working camera, or None if none found.
    """
    print("[INFO]: Searching for available cameras...")
    for index in range(5):  # Test indices 0-4
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # Use DirectShow on Windows
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                print(f"[INFO]: Found working camera at index {index}")
                return index
        cap.release()
    
    print("[ERROR]: No working camera found!")
    return None


def open_camera(camera_index=None):
    """
    Open camera with the given index or auto-detect.
    Returns VideoCapture object or None if failed.
    """
    if camera_index is None:
        camera_index = find_camera()
        if camera_index is None:
            return None
    
    # Try with DirectShow backend on Windows (more reliable)
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        # Fallback to default backend
        cap = cv2.VideoCapture(camera_index)
    
    if cap.isOpened():
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Read a test frame
        ret, frame = cap.read()
        if ret and frame is not None:
            print(f"[INFO]: Camera opened successfully at index {camera_index}")
            return cap
        else:
            print(f"[ERROR]: Camera opened but cannot read frames")
            cap.release()
            return None
    
    print(f"[ERROR]: Failed to open camera at index {camera_index}")
    return None


def capture_and_save_face(name):
    """
    Opens the webcam and allows the user to save their face image by pressing 'S'.
    """
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

            # Display instructions on frame
            cv2.putText(frame, "Press 'S' to Save | 'Q' to Quit", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.imshow("Register New Face - Press 'S' to Save, 'Q' to Quit", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):  # Save face when 'S' is pressed
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)

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

            elif key == ord('q'):  # Quit when 'Q' is pressed
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


def register_new_face_threadsafe(root):
    """
    This function should be called from the main thread (GUI thread).
    It asks for the name using simpledialog, then starts the capture/save function in a new thread.
    """
    name = simpledialog.askstring("Register Face", "Enter your name for registration:", parent=root)
    if name:
        threading.Thread(target=capture_and_save_face, args=(name,), daemon=True).start()
    else:
        messagebox.showwarning("Input Error", "Name cannot be empty.")


def reload_known_faces():
    global known_encodings, known_names
    known_encodings = []
    known_names = []
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".png")):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    print("[INFO]: Reloaded known faces from directory.")


def detect_motion_and_faces(cap, first_frame):
    """
    Detects motion and faces in the current frame.
    Returns: frame, updated_first_frame, motion_detected, face_names
    """
    ret, frame = cap.read()
    if not ret or frame is None:
        print("[ERROR]: Failed to read frame from camera")
        return None, first_frame, False, None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        return frame, gray, False, None

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_fresh = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_fresh = cv2.dilate(thresh_fresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh_fresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    face_names = []
    if motion_detected:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = []
        
        if face_locations:
            try:
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            except Exception as e:
                print(f"[Error]: Face encoding failed: {e}")
                face_encodings = []

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            if known_encodings:
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(distances)
                if distances[best_match_index] < 0.4:
                    name = known_names[best_match_index]

            # Draw box and label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            face_names.append(name)

            # Save unknown faces
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

    return frame, gray, motion_detected, face_names


def log_motion_for_gui(update_frame_callback, update_status_callback):
    """
    Main detection loop for GUI integration.
    """
    global stop_flag
    
    # Open camera with auto-detection
    cap = open_camera()
    
    if cap is None:
        update_status_callback("❌ ERROR: Could not access camera! Check if it's connected and not in use.")
        messagebox.showerror("Camera Error", 
            "Could not access camera.\n\n" +
            "Possible solutions:\n" +
            "1. Check if camera is connected\n" +
            "2. Close other apps using the camera\n" +
            "3. Try restarting your computer\n" +
            "4. Check Windows camera privacy settings")
        return []
    
    first_frame = None
    motion_timestamps = []

    update_status_callback("✅ Camera opened. Starting detection...")
    
    # Give camera time to initialize
    time.sleep(1)

    try:
        frame_count = 0
        while not stop_flag:
            frame, first_frame, motion_detected, face_names = detect_motion_and_faces(cap, first_frame)
            
            if frame is None:
                update_status_callback("❌ Failed to read from webcam.")
                break

            frame_count += 1

            if motion_detected:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                motion_timestamps.append({
                    "Timestamp": timestamp,
                    "Faces": ", ".join(face_names) if face_names else "None"
                })
                update_status_callback(f"🚨 Motion at {timestamp} | Faces: {motion_timestamps[-1]['Faces']}")

                # Save log periodically
                if len(motion_timestamps) % 10 == 0:
                    try:
                        df = pd.DataFrame(motion_timestamps)
                        df.to_csv("motion_log.csv", index=False)
                    except Exception as e:
                        print(f"[Error]: Failed to write log: {e}")
            else:
                if frame_count % 30 == 0:  # Update status every 30 frames
                    update_status_callback("👁️ Monitoring... No motion detected.")

            update_frame_callback(frame)
            
            # Small delay to prevent CPU overload
            time.sleep(0.03)

    except Exception as loop_error:
        print(f"[Error]: Detection loop crashed: {loop_error}")
        update_status_callback(f"❌ Error: {loop_error}")

    finally:
        cap.release()
        update_status_callback("🛑 Detection stopped.")
        try:
            if motion_timestamps:
                df = pd.DataFrame(motion_timestamps)
                df.to_csv("motion_log.csv", index=False)
                print(f"[LOG]: Motion log saved with {len(motion_timestamps)} entries.")
            else:
                print("[LOG]: No motion was detected - no log to save.")
        except Exception as final_log_error:
            print(f"[Error]: Failed to save motion log: {final_log_error}")
        cv2.destroyAllWindows()
        print("[INFO]: Released webcam and destroyed all windows.")
    
    return motion_timestamps