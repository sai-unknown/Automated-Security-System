import cv2
import numpy as np


def find_camera():
    print("[INFO]: Searching for available cameras...")
    for index in range(5):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
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
    if camera_index is None:
        camera_index = find_camera()
    if camera_index is None:
        return None

    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(camera_index)

    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

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


def detect_motion(frame, first_frame):
    if frame is None:
        return first_frame, False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        return gray, False

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

    return gray, motion_detected
