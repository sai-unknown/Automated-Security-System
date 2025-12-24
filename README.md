# Automated Security System

![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/sai-unknown/Automated-Security-System)
![Repo Size](https://img.shields.io/github/repo-size/sai-unknown/Automated-Security-System)

> **Automated Security System** – A smart surveillance system using Python, OpenCV, and face recognition that triggers alerts only on motion detection, making security monitoring efficient and intelligent.

---

## 📋 Table of Contents
- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## 🧠 About
This project is a **motion-triggered face recognition system**.  
It continuously monitors the camera feed, detects motion, and runs face recognition **only when movement occurs**. This reduces unnecessary CPU usage and improves monitoring efficiency.

---

## ✨ Features
- 🚶 **Motion Detection** – Detects movement before running face recognition.  
- 🧑 **Face Recognition** – Recognizes faces using LBPH or Haar Cascades.  
- ⚡ **Efficient Processing** – Avoids running recognition when there’s no movement.  
- 📄 **Event Logging** – Logs detection events in `motion_log.csv`.  

---

## 🛠 Tech Stack
- **Python**  
- **OpenCV**  
- **Haar Cascades**  
- **LBPH Face Recognizer**  
- **CSV logging**  

---

## 📦 Installation

1. Clone the repository:
```bash
   git clone https://github.com/sai-unknown/Automated-Security-System.git
```
2. Navigate into the project folder:
```bash
   cd Automated-Security-System
```
3. Create a Python virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
```
4. Install dependencies:
```bash
   pip install -r requirements.txt
```
---

## ▶️ Usage


1. Run main program:
```bash
   python main.py
```
2. The system will:
-Monitor the camera feed
-Detect motion
-Run face recognition only when motion is detected
-Log events in motion_log.csv

---

## 🧠 How It Works

1. Motion Detection:
   Continuously checks video frames for changes.
2. Face Recognition:
   Triggered only on motion detection using LBPH/Haar Cascades.
3. Event Logging:
   Detection events are recorded in motion_log.csv for auditing.

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome!
Please open an issue or submit a pull request.

---

## 📝 License

This project is licensed under the MIT License. See LICENSE for details.
