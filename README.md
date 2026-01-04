# Automated Security System
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/sai-unknown/Automated-Security-System)
![Repo Size](https://img.shields.io/github/repo-size/sai-unknown/Automated-Security-System)


An AI-powered motion detection and face recognition system built with Python, OpenCV, and face_recognition library. This system monitors your camera feed in real-time, detects motion, and recognizes faces.

## ✨ Features

- 🎥 **Real-time Motion Detection**: Detects movement in camera feed using background subtraction
- 👤 **Face Recognition**: Recognizes known faces and saves unknown faces for review
- 📊 **Logging**: Automatically logs motion events with timestamps and detected faces
- 🖥️ **Modern GUI**: Beautiful, user-friendly interface built with Tkinter
- 📸 **Face Registration**: Easy face registration system for adding known faces

## 🛠 Tech Stack
- **Python**  
- **OpenCV**  
- **Haar Cascades**  
- **LBPH Face Recognizer**  
- **CSV logging** 

## 📂 Project Structure

```
Automated-Security-System/
│── src/
│   ├── motion_detection.py    # Motion detection and camera handling
│   ├── face_recognition.py    # Face recognition and registration
│   ├── logger.py              # Logging functionality
│   ├── main.py                # Main orchestration logic
│   └── gui.py                 # GUI application
│── data/                      # Data storage directory
│   ├── known_faces/           # Known face images
│   └── unknown_faces/         # Unknown face images (auto-saved)
│── demo/                      # Demo files
│   └── demo.gif
│── requirements.txt           # Python dependencies
│── README.md                  # This file
│── motion_log.csv             # Motion detection log (auto-generated)
```


## Demo
![demo](https://github.com/user-attachments/assets/ef29aa75-38f1-44fe-a07c-6b5490923523)


## 📦 Installation

1. **Clone or download this repository**
   ```bash
      git clone https://github.com/sai-unknown/Automated-Security-System.git
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure you have a webcam connected to your computer**

## Usage

### Running the Application

```bash
python -m src.gui
```

Or if you're in the `src` directory:

```bash
python gui.py
```

### Registering Faces

1. Click the **"👤 Register New Face"** button
2. Enter the name for the person
3. Position yourself in front of the camera
4. Press **'S'** to save your face
5. Press **'Q'** to quit without saving

**Note:** Face images are saved in the `data/known_faces/` directory. Make sure to place face images there with the format `{name}.jpg` or `{name}.png`.

### Starting Detection

1. Click **"▶ Start Detection"** to begin monitoring
2. The system will:
   - Detect motion in the camera feed
   - Recognize faces when motion is detected
   - Save unknown faces automatically
   - Log all motion events to `motion_log.csv`

3. Click **"⬛ Stop Detection"** to stop monitoring

## Configuration

### Camera Settings

The system automatically detects available cameras. Camera settings can be adjusted in `src/motion_detection.py`:

- Frame width: 640px
- Frame height: 480px
- FPS: 30

### Face Recognition Threshold

The face recognition threshold (default: 0.4) can be adjusted in `src/face_recognition.py`. Lower values are more strict, higher values are more lenient.

### Motion Detection Sensitivity

Motion detection sensitivity can be adjusted in `src/motion_detection.py`:

- Contour area threshold: 1000 pixels
- Delta threshold: 30

## Requirements

- Python 3.8 or higher
- Webcam/Camera
- Windows, macOS, or Linux

## Dependencies

- `opencv-python`: Computer vision and camera handling
- `face-recognition`: Face recognition library
- `numpy`: Numerical operations
- `pandas`: Data logging
- `Pillow`: Image processing for GUI

## 🔨 Troubleshooting

### Camera Not Found

- Ensure your camera is connected and not being used by another application
- Check Windows camera privacy settings
- Try restarting your computer
- Close other applications that might be using the camera

### No Faces Detected

- Ensure good lighting conditions
- Face the camera directly
- Make sure your face is clearly visible
- Check that known face images are in the `data/known_faces/` directory

### Performance Issues

- Reduce camera resolution in `motion_detection.py`
- Increase the delay between frames in `main.py`
- Close other resource-intensive applications

## 📝 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

This is a group project of team 4 members. 
- Emma Vaishnavi ("Team Lead/ Manager")
- Rakesh.L ("Testing/ Reporting")
- Rafi ("Testing /Reporting ")
- Sandeep Rathod.B ("Developer")

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Acknowledgments

- Built with [OpenCV](https://opencv.org/)
- Face recognition powered by [face_recognition](https://github.com/ageitgey/face_recognition)
- GUI built with Tkinter

