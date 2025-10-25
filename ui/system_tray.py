"""
System Tray Component
Allows application to run in system tray
"""

import pystray
from PIL import Image, ImageDraw
from utils.config import (
    STATUS_TRACKING,
    STATUS_PAUSED,
    WINDOW_TITLE
)


class SystemTray:
	"""Manages system tray icon and menu"""
	
	def __init__(self, callbacks):
		self.callbacks = callbacks
		self.icon = None
		self.is_tracking = False
		
		# Create tray icon image
		self.icon_image = self._create_icon_image()
	
	# noinspection PyMethodMayBeStatic
	def _create_icon_image(self):
		"""
		Create a simple hand icon for system tray

		Returns:
			PIL Image object
		"""
		# Create a 64x64 image
		width = 64
		height = 64
		image = Image.new('RGB', (width, height), color='black')
		draw = ImageDraw.Draw(image)
		
		# Draw a simple hand shape (rectangle palm + fingers)
		# Palm
		draw.rectangle((20, 35, 45, 55), fill='white')
		
		# Fingers
		draw.rectangle((20, 25, 25, 35), fill='white')  # Thumb
		draw.rectangle((28, 20, 32, 35), fill='white')  # Index
		draw.rectangle((35, 18, 39, 35), fill='white')  # Middle
		draw.rectangle((42, 22, 46, 35), fill='white')  # Ring
		
		return image
	
	def _create_menu(self):
		"""Create the right-click context menu"""
		return pystray.Menu(
			pystray.MenuItem(
				"Show Window",
				self._on_show,
				default=True  # Double-click action
			),
			pystray.Menu.SEPARATOR,
			pystray.MenuItem(
				"Pause Tracking",
				self._on_pause,
				checked=lambda item: not self.is_tracking,
				visible=lambda item: self.is_tracking
			),
			pystray.MenuItem(
				"Resume Tracking",
				self._on_resume,
				visible=lambda item: not self.is_tracking
			),
			pystray.Menu.SEPARATOR,
			pystray.MenuItem(
				"Exit",
				self._on_exit
			)
		)
	
	def _on_show(self, _icon, _item):
		"""Show the main window"""
		if 'show_window' in self.callbacks:
			self.callbacks['show_window']()
	
	def _on_pause(self, _icon, _item):
		"""Pause tracking"""
		if 'pause' in self.callbacks:
			self.callbacks['pause']()
			self.is_tracking = False
			self._update_menu()
	
	def _on_resume(self, _icon, _item):
		"""Resume tracking"""
		if 'resume' in self.callbacks:
			self.callbacks['resume']()
			self.is_tracking = True
			self._update_menu()
	
	def _on_exit(self, _icon, _item):
		"""Exit application"""
		self.stop()
		if 'exit' in self.callbacks:
			self.callbacks['exit']()
	
	def _update_menu(self):
		"""Update the menu to reflect current state"""
		if self.icon:
			self.icon.menu = self._create_menu()
	
	def start(self):
		"""Start the system tray icon"""
		if self.icon is not None:
			return  # Already running
		
		self.icon = pystray.Icon(
			name=WINDOW_TITLE,
			icon=self.icon_image,
			title=WINDOW_TITLE,
			menu=self._create_menu()
		)
		
		# Run in separate thread (non-blocking)
		self.icon.run_detached()
	
	def stop(self):
		"""Stop and remove the system tray icon"""
		if self.icon:
			self.icon.stop()
			self.icon = None
	
	def set_tracking_state(self, is_tracking):
		"""
		Update tracking state

		Args:
			is_tracking: Boolean - is tracking currently active
		"""
		self.is_tracking = is_tracking
		self._update_menu()