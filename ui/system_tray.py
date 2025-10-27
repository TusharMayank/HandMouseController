"""
System Tray Component
Allows application to run in system tray
"""

import pystray
from PIL import Image
import os
from utils.config import WINDOW_TITLE


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
		Load custom icon or create fallback icon for system tray

		Returns:
			PIL Image object
		"""
		# Try to load custom icon
		icon_paths = [
			'app_icon.ico',
			'app_icon.png',
			os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_icon.ico'),
			os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_icon.png')
		]
		
		for icon_path in icon_paths:
			try:
				if os.path.exists(icon_path):
					img = Image.open(icon_path)
					# Resize to 64x64 for system tray
					img = img.resize((64, 64), Image.Resampling.LANCZOS)
					# Convert to RGB if needed
					if img.mode != 'RGB':
						# Create white background for transparency
						bg = Image.new('RGB', (64, 64), (255, 255, 255))
						if img.mode == 'RGBA':
							bg.paste(img, mask=img.split()[3])  # Use alpha channel as mask
						else:
							bg.paste(img)
						return bg
					return img
			except Exception as e:
				print(f"Could not load icon from {icon_path}: {e}")
				continue
		
		# Fallback: Create simple hand icon if custom icon not found
		print("Using fallback icon for system tray")
		return self._create_fallback_icon()
	
	def _create_fallback_icon(self):
		"""
		Create simple hand icon as fallback

		Returns:
			PIL Image object
		"""
		from PIL import ImageDraw
		
		width = 64
		height = 64
		image = Image.new('RGB', (width, height), color='white')
		draw = ImageDraw.Draw(image)
		
		# Draw a simple hand shape
		# Palm
		draw.rectangle((20, 35, 45, 55), fill='dodgerblue')
		
		# Fingers
		draw.rectangle((20, 25, 25, 35), fill='dodgerblue')  # Thumb
		draw.rectangle((28, 20, 32, 35), fill='dodgerblue')  # Index
		draw.rectangle((35, 18, 39, 35), fill='dodgerblue')  # Middle
		draw.rectangle((42, 22, 46, 35), fill='dodgerblue')  # Ring
		
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