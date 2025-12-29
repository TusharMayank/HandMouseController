"""
Cursor Effects Module
Creates visual feedback overlays for gesture detection
"""

import tkinter as tk
import pyautogui
from utils.config import (
	GESTURE_NONE,
	GESTURE_MOVE,
	GESTURE_CLICK,
	GESTURE_DOUBLE_CLICK,
	GESTURE_RIGHT_CLICK,
	GESTURE_DRAG,
	GESTURE_SCROLL
)


class CursorEffects:
	"""Creates visual overlay effects around cursor for gesture feedback"""
	
	def __init__(self):
		self.overlay_window = None
		self.canvas = None
		self.current_gesture = GESTURE_NONE
		self.is_active = False
		self.update_id = None
		
		# Effect settings
		self.ring_radius = 30
		self.ring_width = 4
		
		# Gesture colors (RGB format for tkinter)
		self.colors = {
			GESTURE_CLICK: "#00BFFF",  # Deep Sky Blue
			GESTURE_RIGHT_CLICK: "#FF4500",  # Orange Red
			GESTURE_DOUBLE_CLICK: "#FFD700",  # Gold
			GESTURE_DRAG: "#FF00FF",  # Magenta
			GESTURE_SCROLL: "#00FFFF",  # Cyan
			GESTURE_MOVE: None,  # No effect
			GESTURE_NONE: None  # No effect
		}
	
	def start(self):
		"""Start the cursor effects overlay"""
		if self.overlay_window is not None:
			return  # Already running
		
		# Create transparent overlay window
		self.overlay_window = tk.Tk()
		self.overlay_window.withdraw()  # Hide initially
		
		# Configure window properties
		self.overlay_window.overrideredirect(True)  # No window decorations
		self.overlay_window.attributes('-topmost', True)  # Always on top
		self.overlay_window.attributes('-transparentcolor', 'black')  # Black is transparent
		
		# Make window fullscreen but invisible
		screen_width = self.overlay_window.winfo_screenwidth()
		screen_height = self.overlay_window.winfo_screenheight()
		self.overlay_window.geometry(f"{screen_width}x{screen_height}+0+0")
		
		# Create canvas for drawing
		self.canvas = tk.Canvas(
			self.overlay_window,
			width=screen_width,
			height=screen_height,
			bg='black',
			highlightthickness=0
		)
		self.canvas.pack()
		
		# Show window
		self.overlay_window.deiconify()
		self.overlay_window.update()
		
		# Make window click-through using Windows API (for Windows OS)
		try:
			import ctypes
			hwnd = ctypes.windll.user32.GetParent(self.overlay_window.winfo_id())
			# Get current window styles
			styles = ctypes.windll.user32.GetWindowLongW(hwnd, -20)
			# Add WS_EX_TRANSPARENT and WS_EX_LAYERED flags
			styles = styles | 0x00080000 | 0x00000020
			# Apply new styles
			ctypes.windll.user32.SetWindowLongW(hwnd, -20, styles)
		except Exception as e:
			print(f"Warning: Could not make overlay click-through: {e}")
			print("Overlay may interfere with gestures")
		
		self.is_active = True
		self._update_overlay()
	
	def stop(self):
		"""Stop and close the overlay"""
		self.is_active = False
		
		if self.update_id:
			self.overlay_window.after_cancel(self.update_id)
			self.update_id = None
		
		if self.overlay_window:
			self.overlay_window.destroy()
			self.overlay_window = None
			self.canvas = None
	
	def set_gesture(self, gesture):
		"""Update current gesture"""
		self.current_gesture = gesture
	
	def _update_overlay(self):
		"""Update overlay effects"""
		if not self.is_active or not self.canvas:
			return
		
		# Clear canvas
		self.canvas.delete("all")
		
		# Get cursor position
		try:
			cursor_x, cursor_y = pyautogui.position()
		except:
			# If can't get cursor position, skip this frame
			self.update_id = self.overlay_window.after(16, self._update_overlay)
			return
		
		# Draw effect based on current gesture
		color = self.colors.get(self.current_gesture)
		
		if color:
			# Draw ring around cursor
			self.canvas.create_oval(
				cursor_x - self.ring_radius,
				cursor_y - self.ring_radius,
				cursor_x + self.ring_radius,
				cursor_y + self.ring_radius,
				outline=color,
				width=self.ring_width
			)
			
			# Special effects for specific gestures
			if self.current_gesture == GESTURE_DOUBLE_CLICK:
				# Pulsing effect for double-click
				self.canvas.create_oval(
					cursor_x - self.ring_radius - 10,
					cursor_y - self.ring_radius - 10,
					cursor_x + self.ring_radius + 10,
					cursor_y + self.ring_radius + 10,
					outline=color,
					width=2
				)
			
			elif self.current_gesture == GESTURE_DRAG:
				# Filled circle for drag
				self.canvas.create_oval(
					cursor_x - 8,
					cursor_y - 8,
					cursor_x + 8,
					cursor_y + 8,
					fill=color,
					outline=color
				)
			
			elif self.current_gesture == GESTURE_SCROLL:
				# Cross indicator for scroll
				self.canvas.create_line(
					cursor_x, cursor_y - self.ring_radius,
					cursor_x, cursor_y + self.ring_radius,
					fill=color,
					width=3
				)
				self.canvas.create_line(
					cursor_x - self.ring_radius, cursor_y,
					cursor_x + self.ring_radius, cursor_y,
					fill=color,
					width=3
				)
		
		# Schedule next update (60 FPS)
		self.update_id = self.overlay_window.after(16, self._update_overlay)