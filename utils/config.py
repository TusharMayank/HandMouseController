"""
Configuration settings for Hand Mouse Controller
All adjustable parameters in one place
"""

# Camera Settings
CAMERA_INDEX = 0  # Default camera (0 = primary webcam)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS = 30
USE_DSHOW = True  # Use DirectShow on Windows (faster initialization)


# Hand Detection Settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1  # Only track one hand


# Gesture Recognition Thresholds
PINCH_THRESHOLD = 0.045  # Distance ratio for detecting pinch
CLICK_COOLDOWN = 0.3  # Seconds between clicks
DOUBLE_CLICK_TIME = 0.7  # Maximum seconds between clicks for double-click



# Mouse Control Settings
SCREEN_REDUCTION_FACTOR = 0.7  # Use 70% of screen for safety margin
MOVEMENT_SENSITIVITY = 1.2  # Cursor speed multiplier
SMOOTHING_FACTOR = 0.7  # 0 = no smoothing, 1 = max smoothing


# Scroll Settings (Fist-based joystick scroll)
SCROLL_ACTIVATION_THRESHOLD = 20  # Pixels to move from neutral to start scrolling
SCROLL_SPEED_SLOW = 9  # Scroll steps per frame (slow scroll)
SCROLL_SPEED_MEDIUM = 11  # Scroll steps per frame (medium scroll)
SCROLL_SPEED_FAST = 13  # Scroll steps per frame (fast scroll)
SCROLL_ZONE_MEDIUM = 100  # Pixels from neutral for medium speed
SCROLL_ZONE_FAST = 150  # Pixels from neutral for fast speed


# UI Settings
PREVIEW_WIDTH = 480
PREVIEW_HEIGHT = 360
UI_UPDATE_INTERVAL = 30  # milliseconds


# Colors for visualization (BGR format for OpenCV)
# General states
COLOR_INACTIVE = (128, 128, 128)  # Gray - hand detected but not active
COLOR_ACTIVE = (0, 255, 0)        # Green - hand tracking active


# Gesture-specific colors
COLOR_MOVE = (255, 255, 0)        # Cyan - moving cursor
COLOR_LEFT_CLICK = (0, 255, 255)  # Yellow - left click gesture
COLOR_RIGHT_CLICK = (0, 0, 255)   # Red - right click gesture
COLOR_DOUBLE_CLICK = (0, 165, 255) # Orange - double click gesture
COLOR_DRAG = (255, 0, 255)        # Magenta - dragging
COLOR_SCROLL = (255, 128, 0)      # Blue-ish - scrolling


# Landmark/connection colors
COLOR_LANDMARK = (0, 255, 0)      # Green dots for hand points
COLOR_CONNECTION = (255, 255, 255) # White lines between points
COLOR_FINGERTIP = (0, 255, 255)   # Yellow for fingertips
COLOR_THUMB_INDEX = (255, 0, 0)   # Blue for thumb-index connection


# Gesture States
GESTURE_NONE = "none"
GESTURE_MOVE = "move"
GESTURE_CLICK = "click"
GESTURE_DOUBLE_CLICK = "double_click"
GESTURE_RIGHT_CLICK = "right_click"
GESTURE_DRAG = "drag"
GESTURE_SCROLL = "scroll"


# Advanced UI Features
ENABLE_SYSTEM_TRAY = True
ENABLE_ALWAYS_ON_TOP = True
ENABLE_PREVIEW_TOGGLE = True
START_MINIMIZED = False
START_IN_TRAY = False
COMPACT_MODE = False


# Window Settings
WINDOW_TITLE = "Hand Mouse Controller"
MIN_WINDOW_WIDTH = 400
MIN_WINDOW_HEIGHT = 700
DEFAULT_WINDOW_WIDTH = 800   # Add this line - initial window width
DEFAULT_WINDOW_HEIGHT = 650  # Add this line - initial window height


# Theme Colors (for CustomTkinter)
THEME_MODE = "dark"  # "dark", "light", or "system"
THEME_COLOR = "blue"  # "blue", "green", "dark-blue"


# Status Messages
STATUS_READY = "Ready"
STATUS_TRACKING = "Tracking Active"
STATUS_PAUSED = "Paused"
STATUS_NO_CAMERA = "Camera Not Found"
STATUS_NO_HAND = "No Hand Detected"