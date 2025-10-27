# 🖐️ Hand Mouse Controller

> AI-powered touchless mouse control using hand gestures and computer vision.

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-v1.0.0-success.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Gesture Guide](#-gesture-guide)
- [Settings & Customization](#️-settings--customization)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 Overview
**Hand Mouse Controller** is a Python application that enables complete mouse control through hand gestures captured via a standard webcam. Using Google's MediaPipe AI framework, it tracks 21 hand landmarks in real-time to recognize six distinct gestures, providing a touchless, accessible, and innovative way to interact with your computer.

### Perfect For
- 🦾 **Accessibility**: An alternative input method for users with mobility challenges.
- 🧑‍💻 **Touchless Computing**: Ideal for hygiene-conscious or hands-free scenarios.
- 🎤 **Presentations**: Control slides and highlight content from across the room.
- 🧪 **Innovation**: A practical demonstration of real-time computer vision and AI.

---

## ✨ Features

### 🎮 Gesture Controls
| Gesture | Action | Visual Effect |
|:--- |:--- |:--- |
| 👆 **Index Finger** | Move Cursor | None |
| 🤏 **Thumb + Index** | Left Click | Blue Ring 🔵 |
| 🤌 **Thumb + Middle** | Right Click | Red Ring 🔴 |
| ✌️ **Double Pinch** | Double Click | Gold Ring 🟡 |
| 🤙 **Thumb + Pinky** | Drag & Drop | Magenta Ring 🟣 |
| ✊ **Clenched Fist** | Joystick Scroll | Cyan Ring 🔷 |

### 🎨 User Interface
- Modern dark-themed UI built with CustomTkinter.
- Live camera preview with hand skeleton overlay.
- Real-time gesture and status indicators.
- Scrollable settings panel with 8 adjustable sliders.
- System tray integration with pause/resume functionality.
- "Always on Top" and "Hide Preview" modes.

### ⚡ Performance & Stability
- **Real-Time Tracking**: 30 FPS hand detection with sub-100ms latency.
- **CPU Optimized**: 15-25% usage (preview on), dropping to 10-15% (preview hidden).
- **Stable Drag**: Anti-flicker system requires a multi-frame hold to start and stop dragging, preventing accidental drops.
- **Smart Scroll**: Joystick-style continuous scrolling with three speed zones and a neutral dead zone.
- **Multi-threaded Architecture**: Ensures the UI remains responsive while heavy AI processing runs in the background.

### 🛠️ Customization
- **Live Settings**: All 8 settings apply in real-time without needing to restart the application.
- **Persistent Preferences**: Your custom settings are saved to `user_settings.json` and loaded automatically on startup.
- **Adjustable Sensitivity**: Control everything from cursor speed (0.8x to 5.0x) to pinch detection thresholds.

---

## 🎥 Demo

### Gesture Showcase
<div align="center">
  <img src="https://i.imgur.com/your-demo-image-1.gif" alt="Gesture Demo" width="700">
  <p><em>(Replace with a GIF or image demonstrating the gestures)</em></p>
</div>

- **Move Cursor**: Point with your index finger to guide the cursor smoothly across the screen.
- **Click Actions**: Perform quick pinches for left-clicks (thumb+index), right-clicks (thumb+middle), and double-clicks.
- **Drag & Drop**: Securely drag files and select text by holding a thumb+pinky pinch.
- **Joystick Scroll**: Clench your fist and move it up or down for continuous, variable-speed scrolling.

---

## 💻 Installation

### System Requirements
- **Operating System**: Windows 10/11 (64-bit). macOS and Linux are experimental.
- **Python**: Version 3.10 or higher.
- **Webcam**: Any standard USB or built-in laptop camera.
- **RAM**: 4GB recommended.
- **Processor**: Dual-core CPU or better.

### Step-by-Step Installation
#### 1. Clone the Repository
```bash
git clone https://github.com/[Your-GitHub-Username]/HandMouseController.git
cd HandMouseController
```

#### 2. Create and Activate a Virtual Environment
```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
# source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Packages:**
- `opencv-python==4.10.0.84`
- `mediapipe==0.10.5`
- `pyautogui==0.9.54`
- `numpy>=2.0.0`
- `customtkinter==5.2.0`
- `Pillow==10.0.1`
- `pystray==0.19.5`

---

## 🚀 Quick Start

### Running the Application from Source
```bash
# Make sure your virtual environment is active
python main.py
```

### Running the Executable (from Releases)
1. Download the latest `HandMouseController_vX.X.X_Windows.zip` from the [Releases](../../releases) page.
2. Extract the ZIP file to a folder on your computer.
3. Double-click `HandMouseController.exe` to run.

### First-Time Use
1. **Launch**: Run the application and grant camera permissions if prompted.
2. **Start Tracking**: Click the green "Start Tracking" button.
3. **Position Hand**: Hold your hand 1-2 feet from the camera in good lighting. A green skeleton should appear.
4. **Test Gestures**: Point with your index finger to move the cursor. Try a few basic gestures.
5. **Customize**: Click "Settings" to adjust sensitivity and other parameters to your liking.

---

## 📚 Gesture Guide

### 1. 👆 Move Cursor
**How**: Point with your index finger.  
**Result**: Moves the cursor.  

---
### 2. 🤏 Left Click
**How**: A quick pinch and release of your thumb and index finger.  
**Visual**: Blue ring appears. 🔵

---
### 3. 🤌 Right Click
**How**: A quick pinch and release of your thumb and **middle** finger.  
**Visual**: Red/orange ring appears. 🔴

---
### 4. ✌️ Double Click
**How**: Two quick thumb+index pinches (within 0.5s).  
**Visual**: Pulsing gold/yellow ring appears. 🟡

---
### 5. 🤙 Drag & Drop
**How**: Pinch your thumb and **pinky** finger, hold for a moment, then move your hand. Release the pinch to drop.  
**Visual**: Magenta ring with a filled dot. 🟣  
*Note: This gesture is stabilized to prevent accidental drops from minor hand flickers.*

---
### 6. ✊ Scroll
**How**: Make a tight fist to activate "joystick mode." Move your fist up or down from its starting position to scroll. Open your hand to deactivate.  
**Visual**: Cyan ring with a crosshair. 🔷  
*Note: The farther you move your fist, the faster the page scrolls.*

---

## ⚙️ Settings & Customization
Click the "Settings" button to access 8 adjustable sliders that control the application's behavior. All changes are applied instantly.

| Setting | Range | Default | Description |
|:--- |:--- |:--- |:--- |
| **Movement Sensitivity** | 0.8x - 5.0x | ~2.2x | Cursor speed multiplier. |
| **Cursor Smoothing** | 0.5 - 0.9 | 0.77 | Reduces jitter. Higher is smoother but has slight lag. |
| **Pinch Sensitivity** | 0.1 - 0.01 | 0.06 | Gesture trigger threshold. Higher slider = easier to pinch. |
| **Double-Click Speed** | 0.1 - 1.0 sec | 0.46s | Max time allowed between clicks. |
| **Scroll Activation** | 20 - 100 px | 56 px | Dead zone before scroll starts. |
| **Scroll Speed - Slow**| 1 - 50 steps | 6 | Speed in the slow scroll zone. |
| **Scroll Speed - Medium**| 1 - 30 steps| 7 | Speed in the medium scroll zone. |
| **Scroll Speed - Fast** | 1 - 40 steps | 14 | Speed in the fast scroll zone. |

---

## 🐛 Troubleshooting

| Problem | Solution |
|:--- |:--- |
| **Camera Not Found** | Close other apps using the camera (Zoom, Skype). Check `CAMERA_INDEX` in `utils/config.py`. |
| **Hand Not Detected**| Improve room lighting. Sit 1-2 feet from the camera. Show your full palm. |
| **Gestures Inaccurate** | Open Settings and increase "Pinch Sensitivity." Make more deliberate gestures. |
| **Application is Laggy**| Toggle "Hide Preview" ON to save CPU. Close other resource-heavy programs. |
| **Drag is Unstable**| Increase `DRAG_STOP_FRAMES` in `core/gesture_recognizer.py` for more stability. |
| **App Freezes on Start**| Wait a few seconds for camera initialization. Run as Administrator. |
| **"Module Not Found"** | Activate your virtual environment (`venv\Scripts\activate`) and run `pip install -r requirements.txt`. |

---

## 📁 Project Structure
The project is organized into `core` functionality, `ui` components, and `utils` for configuration and shared tools.
```
HandMouseController/
├── core/               # AI and mouse control logic
├── ui/                 # All GUI components
├── utils/              # Configuration, logger, smoothing
├── main.py             # Application entry point
├── requirements.txt    # Dependencies
├── app_info.py         # Application metadata
└── README.md           # This file
```

---

## 🛠️ Technologies Used
- **Primary Language**: Python 3.10
- **AI/CV**: MediaPipe, OpenCV
- **UI**: CustomTkinter, Pillow
- **Automation**: PyAutoGUI, pystray
- **Architecture**: Multi-threading, State Machines

---

## 🤝 Contributing
Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, please feel free to fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

1.  **Fork** the repository.
2.  Create a **Feature Branch** (`git checkout -b feature/AmazingFeature`).
3.  **Commit** your Changes (`git commit -m 'Add: AmazingFeature'`).
4.  **Push** to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a **Pull Request**.

---

## 📜 License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

Copyright © 2024 Tushar Mayank

---

## 🙏 Acknowledgments
Special thanks to the creators and maintainers of:
- **[MediaPipe](https://google.github.io/mediapipe/)** by Google
- **[OpenCV](https://opencv.org/)**
- **[PyAutoGUI](https://pyautogui.readthedocs.io/)**
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)**
- **[pystray](https://github.com/moses-palmer/pystray)**

---

<div align="center">

### 💡 Built with Python | Powered by AI | Made for Accessibility

**[⬆ Back to Top](#-hand-mouse-controller)**

---

**Made with ❤️ by Tushar Mayank**

*Last Updated: 2024*

</div>