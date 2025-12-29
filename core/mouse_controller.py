"""
Mouse Controller Module
Executes mouse actions based on recognized gestures
"""

import pyautogui
import numpy as np
from utils.smoothing import MovementSmoother
from utils import config
from utils.config import (
    GESTURE_NONE,
    GESTURE_MOVE,
    GESTURE_CLICK,
    GESTURE_DOUBLE_CLICK,
    GESTURE_RIGHT_CLICK,
    GESTURE_DRAG,
    GESTURE_SCROLL
)


class MouseController:
	"""Controls mouse based on hand gestures"""
	
	def __init__(self, hand_tracker, gesture_recognizer, camera_width, camera_height):
		self.hand_tracker = hand_tracker
		self.gesture_recognizer = gesture_recognizer
		self.camera_width = camera_width
		self.camera_height = camera_height
		
		# Get screen dimensions
		self.screen_width, self.screen_height = pyautogui.size()
		
		# Initialize movement smoother
		self.smoother = MovementSmoother()
		
		# Scroll state (fist-based joystick)
		self.scroll_neutral_y = None  # Neutral position when fist clenched
		self.is_scroll_active = False
		
		# Drag state tracking
		self.is_mouse_button_down = False
		
		# Safety settings
		pyautogui.FAILSAFE = True  # Move mouse to corner to abort
		pyautogui.PAUSE = 0.01  # Small pause between actions
	
	def map_hand_to_screen(self, hand_x, hand_y):
		"""
		Convert hand coordinates from camera space to screen space

		Args:
			hand_x: X position in camera frame
			hand_y: Y position in camera frame

		Returns:
			Tuple of (screen_x, screen_y)
		"""
		# Define the active area in camera view (reduced for comfort)
		active_width = self.camera_width * config.SCREEN_REDUCTION_FACTOR
		active_height = self.camera_height * config.SCREEN_REDUCTION_FACTOR
		
		# Center the active area
		offset_x = (self.camera_width - active_width) / 2
		offset_y = (self.camera_height - active_height) / 2
		
		# Normalize hand position within active area
		normalized_x = (hand_x - offset_x) / active_width
		normalized_y = (hand_y - offset_y) / active_height
		
		# Clamp to 0-1 range
		normalized_x = np.clip(normalized_x, 0, 1)
		normalized_y = np.clip(normalized_y, 0, 1)
		
		# Map to screen coordinates
		screen_x = normalized_x * self.screen_width
		screen_y = normalized_y * self.screen_height
		
		return int(screen_x), int(screen_y)
	
	def move_cursor(self):
		"""Move cursor based on index finger position"""
		# Get index fingertip position (landmark 8)
		index_pos = self.hand_tracker.get_landmark_position(8, self.camera_width, self.camera_height)
		
		if index_pos is None:
			return None
		
		hand_x, hand_y = index_pos
		
		# Map to screen coordinates
		screen_x, screen_y = self.map_hand_to_screen(hand_x, hand_y)
		
		# Apply smoothing
		smooth_x, smooth_y = self.smoother.smooth_position(screen_x, screen_y)
		
		# Move the cursor
		pyautogui.moveTo(smooth_x, smooth_y, duration=0)
		return None
	
	# noinspection PyMethodMayBeStatic
	def execute_click(self, click_type):
		"""
		Execute a mouse click

		Args:
			click_type: 'left', 'right', or 'double'
		"""
		if click_type == 'left':
			pyautogui.click()
		elif click_type == 'right':
			pyautogui.rightClick()
		elif click_type == 'double':
			pyautogui.doubleClick()
	
	# noinspection PyMethodMayBeStatic
	def start_drag(self):
		"""Start a drag operation"""
		pyautogui.mouseDown()
	
	# noinspection PyMethodMayBeStatic
	def stop_drag(self):
		"""Stop a drag operation"""
		pyautogui.mouseUp()
	
	def handle_scroll(self):
		"""Handle continuous scrolling based on fist position (joystick style)"""
		# Get wrist position (landmark 0) as fist position reference
		wrist_pos = self.hand_tracker.get_landmark_position(0, self.camera_width, self.camera_height)
		
		if wrist_pos is None:
			self.scroll_neutral_y = None
			self.is_scroll_active = False
			return
		
		_, current_y = wrist_pos
		
		# Set neutral position on first frame of scrolling
		if self.scroll_neutral_y is None:
			self.scroll_neutral_y = current_y  # ← This records where you clenched
			self.is_scroll_active = False
			return  # ← Important: Don't scroll on first frame
		
		# Calculate offset from neutral position (where fist was clenched)
		offset_y = current_y - self.scroll_neutral_y
		
		# Check if moved beyond activation threshold
		if abs(offset_y) < config.SCROLL_ACTIVATION_THRESHOLD:
			# Within neutral zone - no scrolling
			self.is_scroll_active = False
			return
		
		# Determine scroll direction and speed
		self.is_scroll_active = True
		
		# Calculate scroll speed based on distance from neutral
		abs_offset = abs(offset_y)
		
		if abs_offset >= config.SCROLL_ZONE_FAST:
			scroll_speed = config.SCROLL_SPEED_FAST
		elif abs_offset >= config.SCROLL_ZONE_MEDIUM:
			scroll_speed = config.SCROLL_SPEED_MEDIUM
		else:
			scroll_speed = config.SCROLL_SPEED_SLOW
		
		# Scroll direction: positive offset = moved down = scroll down (negative)
		if offset_y > 0:
			# Hand moved down → scroll down
			pyautogui.scroll(-scroll_speed)
		else:
			# Hand moved up → scroll up
			pyautogui.scroll(scroll_speed)
	
	def update(self):
		"""
		Main update loop - called every frame
		Executes appropriate action based on current gesture
		"""
		gesture = self.gesture_recognizer.recognize_gesture()
		
		if gesture == GESTURE_MOVE:
			self.move_cursor()
		
		elif gesture == GESTURE_CLICK:
			self.execute_click('left')
		
		elif gesture == GESTURE_DOUBLE_CLICK:
			self.execute_click('double')
		
		elif gesture == GESTURE_RIGHT_CLICK:
			self.execute_click('right')
		
		elif gesture == GESTURE_DRAG:
			# Start drag if mouse button not already down
			if not self.is_mouse_button_down:
				self.start_drag()
				self.is_mouse_button_down = True
			# Continue moving cursor while dragging
			self.move_cursor()
		
		elif gesture == GESTURE_SCROLL:
			self.handle_scroll()
		
		elif gesture == GESTURE_NONE:
			# If we were dragging, stop it
			if self.is_mouse_button_down:
				self.stop_drag()
				self.is_mouse_button_down = False
			# Reset scroll tracking (when fist opens)
			self.scroll_neutral_y = None
			self.is_scroll_active = False
	
	def update_settings(self, movement_sensitivity=None, smoothing_factor=None):
		"""
		Update controller settings dynamically

		Args:
			movement_sensitivity: New sensitivity value
			smoothing_factor: New smoothing value
		"""
		if smoothing_factor is not None:
			self.smoother.smoothing_factor = smoothing_factor
		
	def reset(self):
		"""Reset controller state"""
		self.smoother.reset()
		self.scroll_neutral_y = None
		self.is_scroll_active = False
		self.is_mouse_button_down = False
		
		# Make sure mouse button isn't stuck down
		try:
			pyautogui.mouseUp()
		except Exception as e:
			pass
