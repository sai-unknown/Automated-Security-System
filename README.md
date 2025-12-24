# Automated Security System

A smart surveillance system that uses motion detection to trigger face recognition, reducing unnecessary processing. This system uses OpenCV, Haar Cascades, and LBPH (Local Binary Patterns Histograms) to identify faces only when movement occurs, improving efficiency and making it ideal for secure, automated monitoring. :contentReference[oaicite:2]{index=2}

---

## 📋 Table of Contents
- [About](#about)
- [Features](#features)
- [Demo](#demo)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## 🧠 About
This project is a motion-triggered face recognition system designed for secure monitoring. Instead of running face recognition continuously, it uses motion detection to reduce CPU usage and eliminate false processing when there is no movement. :contentReference[oaicite:3]{index=3}

---

## ✨ Features
- 🚶 **Motion Detection** — Detects movement before face recognition begins. :contentReference[oaicite:4]{index=4}
- 🧑 **Face Recognition** — Uses trained models (LBPH or Haar cascades) to detect faces. :contentReference[oaicite:5]{index=5}
- ⚡ **Efficient Processing** — Reduces unnecessary computation and increases speed. :contentReference[oaicite:6]{index=6}

---

## 🛠 Tech Stack
- **Python**  
- **OpenCV**  
- **Haar Cascades**  
- **LBPH Face Recognizer**  
- **motion_log.csv** for logging detection events. :contentReference[oaicite:7]{index=7}

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sai-unknown/Automated-Security-System.git

2. Create a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # (Linux/macOS)
   venv\Scripts\activate     # (Windows)
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Usage:
   to run main.py:-
   ```bash
   python main.py

 to run gui.py:-
   ```bash
   python gui.py
