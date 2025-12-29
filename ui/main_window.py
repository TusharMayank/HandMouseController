"""
Main Window
Central application window that coordinates all components
"""

import customtkinter as ctk
import threading
from core.hand_tracker import HandTracker
from core.gesture_recognizer import GestureRecognizer
from core.mouse_controller import MouseController
from ui.camera_view import CameraView
from ui.control_panel import ControlPanel
from ui.system_tray import SystemTray
from ui.settings_window import SettingsWindow
from ui.cursor_effects import CursorEffects
from ui.about_dialog import AboutDialog
from utils.speech import SpeechAnnouncer
from ui.compact_window import CompactWindow
from utils.config import (
    WINDOW_TITLE,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT,
    DEFAULT_WINDOW_WIDTH,
    DEFAULT_WINDOW_HEIGHT,
    THEME_MODE,
    THEME_COLOR,
    UI_UPDATE_INTERVAL,
    ENABLE_SYSTEM_TRAY,
    STATUS_READY,
    STATUS_PAUSED,
    STATUS_NO_HAND
)


class MainWindow(ctk.CTk):
	"""Main application window"""

	def __init__(self):
		super().__init__()

		# Set theme
		ctk.set_appearance_mode(THEME_MODE)
		ctk.set_default_color_theme(THEME_COLOR)

		# Window configuration
		self.title(WINDOW_TITLE)

		# Get screen dimensions
		screen_width = self.winfo_screenwidth()
		screen_height = self.winfo_screenheight()

		# Calculate position (centered horizontally, top vertically)
		center_x = int((screen_width - DEFAULT_WINDOW_WIDTH) / 2)
		top_y = 0  # 20 pixels from top (small padding)

		# Set geometry with size and position (width*height+x+y)
		self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}+{center_x}+{top_y}")

		# Set minimum size
		self.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

		# Set window icon
		try:
			import os
			icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_icon.ico')
			if os.path.exists(icon_path):
				self.iconbitmap(icon_path)
		except Exception as e:
			pass  # Continue without icon if not found

		# Tracking state
		self.is_tracking = False
		self.is_running = False
		self.update_id = None
		self.tracking_thread = None
		self.thread_lock = threading.Lock()

		# Settings window reference
		self.settings_window = None

		# Cursor visual effects
		self.cursor_effects = CursorEffects()

		# Text-to-Speech Engine
		self.speech_announcer = SpeechAnnouncer()  # <--- INITIALIZE SPEECH ENGINE

		# Compact Window Reference
		self.compact_window = None

		# Initialize core components
		self.hand_tracker = HandTracker()
		self.gesture_recognizer = GestureRecognizer(self.hand_tracker)
		self.mouse_controller = None  # Created after camera starts
		self.current_frame = None

		# Create UI components
		self.camera_view = CameraView(self, self.hand_tracker)
		self.camera_view.pack(padx=10, pady=10)

		# Create control panel with callbacks
		callbacks = {
			'start': self.start_tracking,
			'stop': self.stop_tracking,
			'always_on_top': self.toggle_always_on_top,
			'hide_preview': self.toggle_hide_preview,
			'minimize_to_tray': self.minimize_to_tray,
			'settings': self.open_settings,
			'about': self.open_about,
			'compact_mode': self.toggle_compact_mode_from_main
		}
		self.control_panel = ControlPanel(self, callbacks)
		self.control_panel.pack(padx=10, pady=10, fill="both", expand=True)

		# System tray (if enabled)
		self.system_tray = None
		if ENABLE_SYSTEM_TRAY:
			tray_callbacks = {
				'show_window': self.show_window,
				'pause': self.pause_tracking,
				'resume': self.resume_tracking,
				'exit': self.quit_application
			}
			self.system_tray = SystemTray(tray_callbacks)
			self.system_tray.start()

		# Force the window to hide before the first draw and open Compact Mode
		self.withdraw()
		self.after(10, self.switch_to_compact_mode)

		# Handle window close event
		self.protocol("WM_DELETE_WINDOW", self.on_closing)

	def switch_to_compact_mode(self):
		"""Hide main window and show compact window"""
		self.withdraw()

		if self.compact_window is None or not self.compact_window.winfo_exists():
			callbacks = {
				'start': self.start_tracking,
				'stop': self.stop_tracking,
				'settings': self.open_settings,
				'toggle_speech': self.toggle_speech,
				'switch_to_full': self.switch_to_full_mode
			}

			from utils import config
			initial_states = {
				'is_tracking': self.is_tracking,
				'speech_enabled': config.ENABLE_SPEECH
			}

			self.compact_window = CompactWindow(self, callbacks, initial_states)
		else:
			# Show the window
			self.compact_window.deiconify()
			self.compact_window.update_tracking_state(self.is_tracking)

			# RESET TOGGLE: Ensure it is set to 1 (Compact Mode/Green)
			# when returning to this window
			self.compact_window.mode_var.set(1)

	def switch_to_full_mode(self):
		"""Hide compact window and show main window"""
		self.deiconify()

		if self.compact_window:
			self.compact_window.withdraw()

		# RESET TOGGLE: Ensure Main Window switch is set to 0 (Developer Mode/Blue)
		if hasattr(self.control_panel, 'mode_var'):
			self.control_panel.mode_var.set(0)

	def toggle_compact_mode_from_main(self, is_enabled):
		"""Callback from Main Window 'Compact Mode' toggle"""
		if is_enabled:
			self.switch_to_compact_mode()

	# If disabled, we stay in Main Window (already handled by switch logic)

	def toggle_speech(self, enabled):
		"""Callback for speech toggle"""
		from utils import config
		config.ENABLE_SPEECH = enabled
		if self.speech_announcer:
			self.speech_announcer.toggle(enabled)

		# Update settings window if open
		if self.settings_window and self.settings_window.winfo_exists():
			if hasattr(self.settings_window, 'speech_switch'):
				if enabled:
					self.settings_window.speech_switch.select()
				else:
					self.settings_window.speech_switch.deselect()

	def start_tracking(self):
		"""Start hand tracking and mouse control"""

		if self.is_tracking:
			return  # Already tracking

		self.control_panel.update_status("Starting camera...")
		self.update()  # Force UI update

		# Start tracking flags first
		self.is_tracking = True
		self.is_running = True
		if self.system_tray:
			self.system_tray.set_tracking_state(True)

<<<<<<< HEAD
		self.control_panel.set_tracking_state(True)

=======
>>>>>>> aa99d67b2636327b6d36232f448c24af70f8cb91
		# Start camera and tracking in separate thread
		self.tracking_thread = threading.Thread(target=self._initialize_and_track, daemon=True)
		self.tracking_thread.start()

		# Start cursor visual effects
		self.cursor_effects.start()

		# Start UI update loop
		self._update_ui()

		# Update Compact Window Button
		if self.compact_window and self.compact_window.winfo_exists():
			self.compact_window.update_tracking_state(True)

	def _initialize_and_track(self):
		"""Initialize camera and start tracking (runs in background thread)"""
		try:
			# Start camera in background
			if not self.camera_view.start_camera():
				print("ERROR: Camera failed to start")
				self.after(0, lambda: self.control_panel.update_status("Error: Could not start camera"))
				self.is_tracking = False
				self.is_running = False
				return

			self.after(0, lambda: self.control_panel.update_status("Camera started, initializing..."))

			# Get camera dimensions and create mouse controller
			cam_width, cam_height = self.camera_view.get_frame_size()

			self.mouse_controller = MouseController(
				self.hand_tracker,
				self.gesture_recognizer,
				cam_width,
				cam_height
			)

			self.after(0, lambda: self.control_panel.update_status("Tracking started"))

			# Start the tracking loop
			self._tracking_loop()

		except Exception as e:
			print(f"Error in initialization: {e}")
			import traceback
			traceback.print_exc()
			self.after(0, lambda: self.control_panel.update_status(f"Error: {e}"))
			self.is_tracking = False
			self.is_running = False

	def _tracking_loop(self):
		"""Background thread for camera capture and hand tracking"""

		while self.is_running:
			try:
				# Get and process frame
				frame = self.camera_view.update_frame()

				if frame is not None:
					# Store frame for UI display (thread-safe)
					with self.thread_lock:
						self.current_frame = frame

					# Update mouse control (this is the heavy processing)
					self.mouse_controller.update()

				# Small delay to prevent CPU overload
				import time
				time.sleep(0.01)  # 10ms delay = ~100 FPS max

			except Exception as e:
				print(f"Error in tracking loop: {e}")
				break


	def stop_tracking(self):
		"""Stop hand tracking and mouse control"""
		if not self.is_tracking:
			return  # Not tracking

		# Stop tracking flags
		self.is_tracking = False
		self.is_running = False  # Signals thread to stop
		if self.system_tray:
			self.system_tray.set_tracking_state(False)

		# Wait for tracking thread to finish
		if self.tracking_thread and self.tracking_thread.is_alive():
			self.tracking_thread.join(timeout=2.0)  # Wait max 2 seconds

		# Cancel UI update loop
		if self.update_id:
			self.after_cancel(self.update_id)
			self.update_id = None

		# Stop camera
		self.camera_view.stop_camera()

		# Reset mouse controller
		if self.mouse_controller:
			self.mouse_controller.reset()

		# Stop cursor effects
		self.cursor_effects.stop()

		# Update UI
		self.control_panel.update_gesture("None")
<<<<<<< HEAD
		self.control_panel.set_tracking_state(False)
=======
		self.control_panel.update_status(STATUS_READY)
>>>>>>> aa99d67b2636327b6d36232f448c24af70f8cb91

		# Update Compact Window Button
		if self.compact_window and self.compact_window.winfo_exists():
			self.compact_window.update_tracking_state(False)

	def _update_ui(self):
		"""UI update loop - called every frame on main thread"""
		if not self.is_tracking:
			return

		try:
			# Display the frame if available
			if hasattr(self, 'current_frame') and self.current_frame is not None:
				with self.thread_lock:
					frame_to_display = self.current_frame.copy()

				self.camera_view.display_frame(frame_to_display)

				# Update gesture display
				if hasattr(self, 'gesture_recognizer') and self.gesture_recognizer:
					current_gesture = self.gesture_recognizer.get_current_gesture()
					self.control_panel.update_gesture(current_gesture)

					# Update cursor visual effects
					self.cursor_effects.set_gesture(current_gesture)

					# Update speech announcer <--- NEW BLOCK
					if self.speech_announcer:
						self.speech_announcer.announce_gesture(current_gesture)

				# Update status based on hand detection
				if self.hand_tracker.hand_detected:
					self.control_panel.update_status("Tracking: Hand Detected")
				else:
					self.control_panel.update_status(STATUS_NO_HAND)

		except Exception as e:
			print(f"Error in UI update: {e}")

		# Schedule next UI update
		self.update_id = self.after(UI_UPDATE_INTERVAL, self._update_ui)

	def pause_tracking(self):
		"""Pause tracking without stopping camera"""
		if self.is_tracking:
			self.is_tracking = False
			self.is_running = False  # Stops thread
			if self.system_tray:
				self.system_tray.set_tracking_state(False)
			self.control_panel.update_status(STATUS_PAUSED)

	def resume_tracking(self):
		"""Resume tracking"""
		if not self.is_tracking and self.camera_view.camera is not None:
			self.is_tracking = True
			self.is_running = True  # Starts thread
			if self.system_tray:
				self.system_tray.set_tracking_state(True)

			# Restart tracking thread
			self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
			self.tracking_thread.start()

			self._update_ui()

	def toggle_always_on_top(self, enabled):
		"""Toggle window always on top"""
		self.attributes('-topmost', enabled)

	def toggle_hide_preview(self, enabled):
		"""Toggle camera preview visibility"""
		if enabled:
			self.camera_view.hide_preview()
		else:
			self.camera_view.show_preview()

	def minimize_to_tray(self):
		"""Hide window to system tray"""
		if self.system_tray:
			self.withdraw()  # Hide window

	def show_window(self):
		"""Show window from system tray"""
		self.deiconify()  # Show window
		self.lift()  # Bring to front
		self.focus_force()  # Give focus

	# noinspection PyMethodMayBeStatic
	def open_settings(self):
		"""Open settings dialog"""
		# Check if settings window exists and is still open
		if self.settings_window is None or not self.settings_window.winfo_exists():
			self.settings_window = SettingsWindow(self, self.apply_new_settings)
		else:
			# Window already exists, just bring it to front
			self.settings_window.focus()

	def open_about(self):
		"""Open about dialog"""
		try:
			AboutDialog(self)
		except Exception as e:
			print(f"Error opening About dialog: {e}")

	def apply_new_settings(self, new_values):
		"""Apply settings from settings window"""
		from utils import config

		# Update config module values
		if 'MOVEMENT_SENSITIVITY' in new_values:
			config.MOVEMENT_SENSITIVITY = new_values['MOVEMENT_SENSITIVITY']

		if 'SMOOTHING_FACTOR' in new_values:
			config.SMOOTHING_FACTOR = new_values['SMOOTHING_FACTOR']

		if 'SCROLL_SPEED_SLOW' in new_values:
			config.SCROLL_SPEED_SLOW = new_values['SCROLL_SPEED_SLOW']

		if 'SCROLL_SPEED_MEDIUM' in new_values:
			config.SCROLL_SPEED_MEDIUM = new_values['SCROLL_SPEED_MEDIUM']

		if 'SCROLL_SPEED_FAST' in new_values:
			config.SCROLL_SPEED_FAST = new_values['SCROLL_SPEED_FAST']

		if 'SCROLL_ACTIVATION_THRESHOLD' in new_values:
			config.SCROLL_ACTIVATION_THRESHOLD = new_values['SCROLL_ACTIVATION_THRESHOLD']

		if 'PINCH_THRESHOLD' in new_values:
			config.PINCH_THRESHOLD = new_values['PINCH_THRESHOLD']

		if 'DOUBLE_CLICK_TIME' in new_values:
			config.DOUBLE_CLICK_TIME = new_values['DOUBLE_CLICK_TIME']

		# --- NEW: Speech Setting ---
		# --- AUDIO SETTINGS BLOCK ---
		# Update Speech Enable/Disable
		if 'ENABLE_SPEECH' in new_values:
			config.ENABLE_SPEECH = new_values['ENABLE_SPEECH']
			if self.speech_announcer:
				self.speech_announcer.toggle(config.ENABLE_SPEECH)

		# Update Speech Volume (Add this right here)
		if 'SPEECH_VOLUME' in new_values:
			config.SPEECH_VOLUME = new_values['SPEECH_VOLUME']
			if self.speech_announcer and self.speech_announcer.engine:
				# setProperty expects a float between 0.0 and 1.0
				self.speech_announcer.engine.setProperty('volume', config.SPEECH_VOLUME)

		# Update running components if they exist
		if self.mouse_controller:
			# Update smoother directly
			if 'SMOOTHING_FACTOR' in new_values:
				self.mouse_controller.smoother.smoothing_factor = new_values['SMOOTHING_FACTOR']

		print(f"Settings applied! Speech Enabled: {config.ENABLE_SPEECH}")

		# Sync Speech switch in Compact Window if settings changed it
		if 'ENABLE_SPEECH' in new_values:
			if self.compact_window and self.compact_window.winfo_exists():
				# Accessing public attribute
				if new_values['ENABLE_SPEECH']:
					self.compact_window.speech_switch.select()
				else:
					self.compact_window.speech_switch.deselect()

	def on_closing(self):
		"""Handle window close button"""
		if self.system_tray and self.is_tracking:
			# If tracking, minimize to tray instead of closing
			self.minimize_to_tray()
		else:
			# Otherwise, quit
			self.quit_application()

	def quit_application(self):
		"""Clean up and exit application"""
		# Stop tracking
		self.stop_tracking()

		# Stop cursor effects
		if hasattr(self, 'cursor_effects'):
			self.cursor_effects.stop()

		# Stop system tray
		if self.system_tray:
			self.system_tray.stop()

		# Release hand tracker
		self.hand_tracker.release()

		# Destroy window
		self.destroy()