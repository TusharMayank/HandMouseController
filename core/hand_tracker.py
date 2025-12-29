"""
Hand Tracking Module
Uses MediaPipe to detect hand landmarks and calculate finger positions
"""

import cv2
import mediapipe as mp
import numpy as np
from utils.config import (
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    MAX_NUM_HANDS
)


class HandTracker:
	"""Detects and tracks hand landmarks using MediaPipe"""
	
	def __init__(self):
		# Initialize MediaPipe Hands
		self.mp_hands = mp.solutions.hands
		self.mp_draw = mp.solutions.drawing_utils
		self.mp_drawing_styles = mp.solutions.drawing_styles
		
		# Create hands detector
		self.hands = self.mp_hands.Hands(
			static_image_mode=False,
			max_num_hands=MAX_NUM_HANDS,
			min_detection_confidence=MIN_DETECTION_CONFIDENCE,
			min_tracking_confidence=MIN_TRACKING_CONFIDENCE
		)
		
		# Store latest hand landmarks
		self.landmarks = None
		self.hand_detected = False
	
	def process_frame(self, frame):
		"""
		Process a video frame to detect hands

		Args:
			frame: BGR image from camera (OpenCV format)

		Returns:
			Processed frame with hand landmarks drawn
		"""
		# Convert BGR to RGB (MediaPipe uses RGB)
		rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		
		# Process the frame to find hands
		results = self.hands.process(rgb_frame)
		
		# Check if any hands were detected
		# noinspection PyUnresolvedReferences
		if results.multi_hand_landmarks:
			self.hand_detected = True
			# Take first hand (we only track one hand)
			# noinspection PyUnresolvedReferences
			self.landmarks = results.multi_hand_landmarks[0]
			
			# Draw hand landmarks on the frame
			self.mp_draw.draw_landmarks(
				frame,
				self.landmarks,
				self.mp_hands.HAND_CONNECTIONS,
				self.mp_drawing_styles.get_default_hand_landmarks_style(),
				self.mp_drawing_styles.get_default_hand_connections_style()
			)
		else:
			self.hand_detected = False
			self.landmarks = None
		
		return frame
	
	def get_landmark_position(self, landmark_id, frame_width, frame_height):
		"""
		Get screen coordinates of a specific landmark

		Args:
			landmark_id: Which point (0-20)
			frame_width: Width of camera frame
			frame_height: Height of camera frame

		Returns:
			Tuple (x, y) in pixel coordinates, or None if not detected
		"""
		if not self.hand_detected or self.landmarks is None:
			return None
		
		# Get the landmark
		landmark = self.landmarks.landmark[landmark_id]
		
		# Convert normalized coordinates (0.0-1.0) to pixel coordinates
		x = int(landmark.x * frame_width)
		y = int(landmark.y * frame_height)
		
		return (x, y)
	
	def calculate_distance(self, landmark1_id, landmark2_id):
		"""
		Calculate distance between two landmarks
		Used for pinch detection

		Args:
			landmark1_id: First landmark (e.g., thumb tip = 4)
			landmark2_id: Second landmark (e.g., index tip = 8)

		Returns:
			Distance as ratio (0.0-1.0), or None if not detected
		"""
		if not self.hand_detected or self.landmarks is None:
			return None
		
		# Get both landmarks
		lm1 = self.landmarks.landmark[landmark1_id]
		lm2 = self.landmarks.landmark[landmark2_id]
		
		# Calculate Euclidean distance (straight line)
		# Using normalized coordinates (0.0-1.0), so no frame dimensions needed
		distance = np.sqrt(
			(lm1.x - lm2.x) ** 2 +
			(lm1.y - lm2.y) ** 2
		)
		
		return distance
	
	def get_fingertip_positions(self, frame_width, frame_height):
		"""
		Get positions of all 5 fingertips

		Returns:
			Dictionary with fingertip positions or None
		"""
		if not self.hand_detected:
			return None
		
		fingertips = {
			'thumb': self.get_landmark_position(4, frame_width, frame_height),
			'index': self.get_landmark_position(8, frame_width, frame_height),
			'middle': self.get_landmark_position(12, frame_width, frame_height),
			'ring': self.get_landmark_position(16, frame_width, frame_height),
			'pinky': self.get_landmark_position(20, frame_width, frame_height)
		}
		
		return fingertips
	
	def is_fist_closed(self):
		"""
		Detect if hand is making a fist (all fingers closed)

		Returns:
			Boolean - True if fist is closed
		"""
		if not self.hand_detected or self.landmarks is None:
			return False
		
		# Get wrist position (landmark 0) as reference
		wrist = self.landmarks.landmark[0]
		
		# Get fingertip positions
		thumb_tip = self.landmarks.landmark[4]
		index_tip = self.landmarks.landmark[8]
		middle_tip = self.landmarks.landmark[12]
		ring_tip = self.landmarks.landmark[16]
		pinky_tip = self.landmarks.landmark[20]
		
		# Get knuckle positions (base of fingers)
		index_knuckle = self.landmarks.landmark[5]
		middle_knuckle = self.landmarks.landmark[9]
		ring_knuckle = self.landmarks.landmark[13]
		pinky_knuckle = self.landmarks.landmark[17]
		
		# Check if fingertips are below or at same level as knuckles (closed fingers)
		# In camera coordinates, Y increases downward
		index_closed = index_tip.y >= index_knuckle.y
		middle_closed = middle_tip.y >= middle_knuckle.y
		ring_closed = ring_tip.y >= ring_knuckle.y
		pinky_closed = pinky_tip.y >= pinky_knuckle.y
		
		# Thumb check - should be close to palm
		thumb_to_wrist_dist = np.sqrt(
			(thumb_tip.x - wrist.x) ** 2 +
			(thumb_tip.y - wrist.y) ** 2
		)
		thumb_closed = thumb_to_wrist_dist < 0.15  # Threshold for thumb
		
		# Fist is closed if at least 4 out of 5 fingers are closed
		closed_count = sum([index_closed, middle_closed, ring_closed, pinky_closed, thumb_closed])
		
		return closed_count >= 4
	
	def release(self):
		"""Clean up resources"""
		if self.hands:
			self.hands.close()

