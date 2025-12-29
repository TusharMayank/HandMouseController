"""
Smoothing utilities for stable cursor movement
Reduces jitter from hand tracking
"""

from collections import deque
from utils.config import SMOOTHING_FACTOR


class MovementSmoother:
	"""Applies exponential moving average to smooth cursor movement"""
	
	def __init__(self, smoothing_factor=SMOOTHING_FACTOR):
		self.smoothing_factor = smoothing_factor
		self.prev_x = None
		self.prev_y = None
	
	def smooth_position(self, x, y):
		"""
		Apply exponential smoothing to coordinates

		Args:
			x, y: Current raw coordinates from hand tracking

		Returns:
			Tuple of smoothed (x, y) coordinates
		"""
		if self.prev_x is None:
			# First time - no previous position to smooth with
			self.prev_x = x
			self.prev_y = y
			return x, y
		
		# Exponential moving average formula
		smooth_x = self.smoothing_factor * self.prev_x + (1 - self.smoothing_factor) * x
		smooth_y = self.smoothing_factor * self.prev_y + (1 - self.smoothing_factor) * y
		
		# Save for next frame
		self.prev_x = smooth_x
		self.prev_y = smooth_y
		
		return int(smooth_x), int(smooth_y)
	
	def reset(self):
		"""Reset smoothing history"""
		self.prev_x = None
		self.prev_y = None


class GestureStabilizer:
	"""Prevents gesture flickering by requiring consistent detection"""
	
	def __init__(self, buffer_size=5):
		self.buffer = deque(maxlen=buffer_size)
	
	def add_gesture(self, gesture):
		"""Add gesture to buffer"""
		self.buffer.append(gesture)
		
	def get_stable_gesture(self):
		"""
		Return gesture only if it appears consistently

		Returns:
			Most common gesture in buffer, or None if inconsistent
		"""
		if len(self.buffer) < self.buffer.maxlen:
			# Buffer not full yet - wait for more data
			return None
		
		# Count how many times each gesture appears
		gesture_counts = {}
		for g in self.buffer:
			gesture_counts[g] = gesture_counts.get(g, 0) + 1
		
		# Find most common gesture
		most_common = max(gesture_counts, key=gesture_counts.get)
		
		# Require at least 60% consistency (3 out of 5)
		if gesture_counts[most_common] >= len(self.buffer) * 0.6:
			return most_common
		return None
	
	def clear(self):
		"""Clear the buffer"""
		self.buffer.clear()
		
	