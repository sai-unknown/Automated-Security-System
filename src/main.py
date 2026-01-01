import os
import cv2
import numpy as np
from datetime import datetime
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import threading
import time

from motion_detection import open_camera, detect_motion
from face_handler import recognize_faces, reload_known_faces, capture_and_save_face
from logger import save_log

stop_flag = False


def detect_motion_and_faces(cap, first_frame):
    ret, frame = cap.read()
    if not ret or frame is None:
        print("[ERROR]: Failed to read frame from camera")
        return None, first_frame, False, None

    updated_first_frame, motion_detected = detect_motion(frame, first_frame)

    face_names = []
    if motion_detected:
        frame, face_names = recognize_faces(frame)

    return frame, updated_first_frame, motion_detected, face_names


def log_motion_for_gui(update_frame_callback, update_status_callback):
    global stop_flag

    cap = open_camera()
    if cap is None:
        update_status_callback("❌ ERROR: Could not access camera! Check if it's connected and not in use.")
        messagebox.showerror("Camera Error", "Could not access camera.\n\n" +
                            "Possible solutions:\n" +
                            "1. Check if camera is connected\n" +
                            "2. Close other apps using the camera\n" +
                            "3. Try restarting your computer\n" +
                            "4. Check Windows camera privacy settings")
        return []

    first_frame = None
    motion_timestamps = []
    update_status_callback("✅ Camera opened. Starting detection...")

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

                if len(motion_timestamps) % 10 == 0:
                    try:
                        save_log(motion_timestamps)
                    except Exception as e:
                        print(f"[Error]: Failed to write log: {e}")
            else:
                if frame_count % 30 == 0:
                    update_status_callback("👁️ Monitoring... No motion detected.")

            update_frame_callback(frame)

            time.sleep(0.03)

    except Exception as loop_error:
        print(f"[Error]: Detection loop crashed: {loop_error}")
        update_status_callback(f"❌ Error: {loop_error}")
    finally:
        cap.release()
        update_status_callback("🛑 Detection stopped.")

        try:
            if motion_timestamps:
                save_log(motion_timestamps)
                print(f"[LOG]: Motion log saved with {len(motion_timestamps)} entries.")
            else:
                print("[LOG]: No motion was detected - no log to save.")
        except Exception as final_log_error:
            print(f"[Error]: Failed to save motion log: {final_log_error}")

        cv2.destroyAllWindows()
        print("[INFO]: Released webcam and destroyed all windows.")

    return motion_timestamps


def register_new_face_threadsafe(root):
    name = simpledialog.askstring("Register Face", "Enter your name for registration:", parent=root)
    if name:
        threading.Thread(target=capture_and_save_face, args=(name,), daemon=True).start()
    else:
        messagebox.showwarning("Input Error", "Name cannot be empty.")


if __name__ == "__main__":
    print("Please run the GUI application using: python -m src.gui")
    print("Or import this module from your GUI application.")
