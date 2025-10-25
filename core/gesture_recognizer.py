"""
Gesture Recognition Module
Identifies hand gestures based on finger positions and timing
"""

import time
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


class GestureRecognizer:
	"""Recognizes gestures from hand landmark data"""
	
	def __init__(self, hand_tracker):
		self.hand_tracker = hand_tracker
		
		# Timing trackers
		self.pinch_start_time = None
		self.last_click_time = None
		self.click_count = 0
		
		# State trackers
		self.is_dragging = False
		self.was_pinched = False
		self.last_pinch_type = None
		self.current_gesture = GESTURE_NONE
		
		# Scroll state (fist-based)
		self.is_scrolling = False
		self.scroll_neutral_y = None  # Y position where fist was clenched
		
		# Drag stability
		self.drag_pinch_frames = 0  # Count consecutive pinch frames
		self.drag_release_frames = 0  # Count consecutive release frames
		self.DRAG_START_FRAMES = 3  # Need 3 frames to start drag
		self.DRAG_STOP_FRAMES = 5  # Need 5 frames to stop drag
		
		# Landmark IDs for fingertips
		self.THUMB_TIP = 4
		self.INDEX_TIP = 8
		self.MIDDLE_TIP = 12
		self.RING_TIP = 16
		self.PINKY_TIP = 20
	
	def _reset_state(self):
		"""Reset all gesture tracking state"""
		self.pinch_start_time = None
		self.is_dragging = False
		self.was_pinched = False
		self.last_pinch_type = None
		self.current_gesture = GESTURE_NONE
		self.is_scrolling = False
		self.scroll_neutral_y = None
		self.drag_pinch_frames = 0
		self.drag_release_frames = 0
	
	def is_pinching(self, finger1_id, finger2_id):
		"""
		Check if two fingers are pinching together

		Args:
			finger1_id: First finger landmark ID
			finger2_id: Second finger landmark ID

		Returns:
			Boolean - True if pinching, False otherwise
		"""
		distance = self.hand_tracker.calculate_distance(finger1_id, finger2_id)
		
		if distance is None:
			return False
		
		return distance < config.PINCH_THRESHOLD
	
	def recognize_gesture(self):
		"""
		Main method to identify current gesture

		Returns:
			String representing the detected gesture
		"""
		if not self.hand_tracker.hand_detected:
			self._reset_state()
			return GESTURE_NONE
		
		current_time = time.time()
		
		# Check for different pinch combinations
		thumb_index_pinch = self.is_pinching(self.THUMB_TIP, self.INDEX_TIP)
		thumb_middle_pinch = self.is_pinching(self.THUMB_TIP, self.MIDDLE_TIP)
		thumb_ring_pinch = self.is_pinching(self.THUMB_TIP, self.RING_TIP)
		thumb_pinky_pinch = self.is_pinching(self.THUMB_TIP, self.PINKY_TIP)
		
		# Priority 1: Right-click (thumb + middle)
		if thumb_middle_pinch:
			if not self.was_pinched:
				self.current_gesture = GESTURE_RIGHT_CLICK
				self.was_pinched = True
				self.last_pinch_type = "middle"
				return GESTURE_RIGHT_CLICK
			return GESTURE_NONE
		
		# Priority 2: Scroll (clenched fist)
		is_fist = self.hand_tracker.is_fist_closed()
		
		if is_fist:
			if not self.is_scrolling:
				# Just clenched fist - record neutral position (wrist Y)
				self.is_scrolling = True
			# Neutral position will be set in mouse controller
			
			self.current_gesture = GESTURE_SCROLL
			return GESTURE_SCROLL
		else:
			# Fist opened - stop scrolling
			if self.is_scrolling:
				self.is_scrolling = False
				self.scroll_neutral_y = None
		
		# Priority 3: Drag (thumb + pinky) - STABLE DRAG
		if thumb_pinky_pinch:
			# Pinch detected - increment counter, reset release counter
			self.drag_pinch_frames += 1
			self.drag_release_frames = 0
			
			# If not dragging yet, check if we've held pinch long enough
			if not self.is_dragging:
				if self.drag_pinch_frames >= self.DRAG_START_FRAMES:
					# Held pinch for required frames - start drag
					self.is_dragging = True
					self.was_pinched = True
					self.last_pinch_type = "pinky"
					self.current_gesture = GESTURE_DRAG
					return GESTURE_DRAG
				else:
					# Still building up to drag
					return GESTURE_NONE
			else:
				# Already dragging, continue
				self.current_gesture = GESTURE_DRAG
				return GESTURE_DRAG
		
		# Pinch NOT detected - handle drag release
		if self.is_dragging and self.last_pinch_type == "pinky":
			# Increment release counter
			self.drag_release_frames += 1
			self.drag_pinch_frames = 0
			
			# Check if released long enough to stop drag
			if self.drag_release_frames >= self.DRAG_STOP_FRAMES:
				# Released for required frames - stop drag
				self.is_dragging = False
				self.was_pinched = False
				self.last_pinch_type = None
				self.drag_pinch_frames = 0
				self.drag_release_frames = 0
				self.current_gesture = GESTURE_NONE
				return GESTURE_NONE
			else:
				# Might be temporary loss - keep dragging
				self.current_gesture = GESTURE_DRAG
				return GESTURE_DRAG
		
		# Priority 4: Click (thumb + index) - SIMPLIFIED, no timing
		if thumb_index_pinch:
			if not self.was_pinched:
				self.was_pinched = True
				self.last_pinch_type = "index"
				self.pinch_start_time = current_time
			# Don't return click yet - wait for release
			return GESTURE_NONE
		
		# No pinch currently active - check if we just released one
		if self.was_pinched:
			# Released from click (index)
			if self.last_pinch_type == "index":
				# Check for double-click
				if self.last_click_time and (current_time - self.last_click_time) < config.DOUBLE_CLICK_TIME:
					# Double-click detected!
					self.current_gesture = GESTURE_DOUBLE_CLICK
					self.last_click_time = None
					self.was_pinched = False
					self.last_pinch_type = None
					return GESTURE_DOUBLE_CLICK
				else:
					# Single click
					self.current_gesture = GESTURE_CLICK
					self.last_click_time = current_time
					self.was_pinched = False
					self.last_pinch_type = None
					return GESTURE_CLICK
			
			# Released from middle or ring pinch - just reset
			else:
				self.was_pinched = False
				self.last_pinch_type = None
		
		# No gesture detected - just move cursor
		self.current_gesture = GESTURE_MOVE
		return GESTURE_MOVE
		
	def get_current_gesture(self):
		"""
		Get the most recently recognized gesture

		Returns:
			String representing current gesture state
		"""
		return self.current_gesture
		