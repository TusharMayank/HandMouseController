"""
Camera View Widget
Displays live camera feed with hand tracking overlay
"""

import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from utils.config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    PREVIEW_WIDTH,
    PREVIEW_HEIGHT,
    USE_DSHOW
)


class CameraView(ctk.CTkFrame):
	"""Widget that displays camera feed with hand tracking"""
	
	def __init__(self, parent, hand_tracker):
		super().__init__(parent)
		
		self.hand_tracker = hand_tracker
		self.camera = None
		self.is_running = False
		self.is_visible = True
		
		# Camera settings
		self.camera_width = CAMERA_WIDTH
		self.camera_height = CAMERA_HEIGHT
		self.preview_width = PREVIEW_WIDTH
		self.preview_height = PREVIEW_HEIGHT
	
		# Create preview label (displays camera feed)
		self.preview_label = ctk.CTkLabel(
			self,
			text="Camera Preview",
			width=self.preview_width,
			height=self.preview_height
		)
		self.preview_label.grid(row=0, column=0, padx=10, pady=10)
		
		# Placeholder image when no camera
		self.placeholder_image = self._create_placeholder()
		self.preview_label.configure(image=self.placeholder_image)
	
	def _create_placeholder(self):
		"""Create a placeholder image for when camera is off"""
		import numpy as np
		
		# Create gray image
		placeholder = np.ones((self.preview_height, self.preview_width, 3), dtype=np.uint8) * 50
		
		# Add text
		cv2.putText(
			placeholder,
			"Camera Off",
			(self.preview_width // 2 - 80, self.preview_height // 2),
			cv2.FONT_HERSHEY_SIMPLEX,
			1,
			(255, 255, 255),
			2
		)
		
		# Convert to PhotoImage
		placeholder_rgb = cv2.cvtColor(placeholder, cv2.COLOR_BGR2RGB)
		pil_image = Image.fromarray(placeholder_rgb)
		return ImageTk.PhotoImage(pil_image)
	
	def start_camera(self):
		"""Initialize and start camera capture"""
		if self.camera is not None:
			return  # Already running
		
		try:
			self.camera = cv2.VideoCapture(CAMERA_INDEX)
			self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
			self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
			
			# Check if camera opened successfully
			if not self.camera.isOpened():
				raise Exception("Could not open camera")
			
			self.is_running = True
			return True
		
		except Exception as e:
			print(f"Error starting camera: {e}")
			self.camera = None
			self.is_running = False
			return False
	
	def stop_camera(self):
		"""Stop camera capture and release resources"""
		self.is_running = False
		
		if self.camera is not None:
			self.camera.release()
			self.camera = None
		
		# Show placeholder
		self.preview_label.configure(image=self.placeholder_image)
	
	def update_frame(self):
		"""
		Capture and display a frame from camera
		Called repeatedly to create video effect

		Returns:
			The processed frame (for hand tracking), or None if error
		"""
		if not self.is_running or self.camera is None:
			return None
		
		# Capture frame
		ret, frame = self.camera.read()
		
		if not ret or frame is None:
			print("Failed to read frame")
			return None
		
		# Flip frame horizontally (mirror effect - more intuitive)
		frame = cv2.flip(frame, 1)
		
		# Process frame with hand tracker (draws hand skeleton)
		processed_frame = self.hand_tracker.process_frame(frame)
		
		return processed_frame
	
	def display_frame(self, frame):
		"""
		Display a frame in the preview label

		Args:
			frame: OpenCV image (BGR format)
		"""
		if not self.is_visible or frame is None:
			return
		
		# Resize frame to preview size
		frame_resized = cv2.resize(frame, (self.preview_width, self.preview_height))
		
		# Convert BGR to RGB
		frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
		
		# Convert to PIL Image
		pil_image = Image.fromarray(frame_rgb)
		
		# Convert to PhotoImage for tkinter
		photo = ImageTk.PhotoImage(image=pil_image)
		
		# Update label
		self.preview_label.configure(image=photo)
		self.preview_label.image = photo  # Keep reference to prevent garbage collection
	
	def show_preview(self):
		"""Show the camera preview"""
		self.is_visible = True
		self.preview_label.grid(row=0, column=0, padx=10, pady=10)
	
	def hide_preview(self):
		"""Hide the camera preview to save CPU"""
		self.is_visible = False
		self.preview_label.grid_remove()
	
	def get_frame_size(self):
		"""
		Get camera frame dimensions

		Returns:
			Tuple of (width, height)
		"""
		return (self.camera_width, self.camera_height)
	
	