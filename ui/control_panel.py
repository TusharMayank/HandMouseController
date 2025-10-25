"""
Control Panel Widget
Contains buttons, toggles, and status indicators
"""

import customtkinter as ctk
from utils.config import (
    STATUS_READY,
    STATUS_TRACKING,
    ENABLE_ALWAYS_ON_TOP,
    ENABLE_PREVIEW_TOGGLE
)


class ControlPanel(ctk.CTkScrollableFrame):
	"""Control panel with buttons and settings"""
	
	def __init__(self, parent, callbacks):
		super().__init__(parent)
		
		self.callbacks = callbacks
		self.is_tracking = False
		
		# Configure grid
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		
		self._create_widgets()
	
	def _create_widgets(self):
		"""Create all control panel widgets"""
		
		# Gesture indicator
		self.gesture_label = ctk.CTkLabel(
			self,
			text="Gesture: None",
			font=("Arial", 16, "bold")
		)
		self.gesture_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")
		
		# Status indicator
		self.status_label = ctk.CTkLabel(
			self,
			text=f"Status: {STATUS_READY}",
			font=("Arial", 12)
		)
		self.status_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
		
		# Start button
		self.start_button = ctk.CTkButton(
			self,
			text="Start Tracking",
			command=self._on_start,
			fg_color="green",
			hover_color="darkgreen"
		)
		self.start_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
		
		# Stop button
		self.stop_button = ctk.CTkButton(
			self,
			text="Stop Tracking",
			command=self._on_stop,
			fg_color="red",
			hover_color="darkred",
			state="disabled"
		)
		self.stop_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
		
		# Always on top toggle (if enabled)
		if ENABLE_ALWAYS_ON_TOP:
			self.always_on_top_var = ctk.BooleanVar(value=False)
			self.always_on_top_switch = ctk.CTkSwitch(
				self,
				text="Always on Top",
				variable=self.always_on_top_var,
				command=self._on_always_on_top_toggle
			)
			self.always_on_top_switch.grid(row=3, column=0, padx=10, pady=10, sticky="w")
		
		# Hide preview toggle (if enabled)
		if ENABLE_PREVIEW_TOGGLE:
			self.hide_preview_var = ctk.BooleanVar(value=False)
			self.hide_preview_switch = ctk.CTkSwitch(
				self,
				text="Hide Preview",
				variable=self.hide_preview_var,
				command=self._on_hide_preview_toggle
			)
			self.hide_preview_switch.grid(row=3, column=1, padx=10, pady=10, sticky="w")
		
		# Minimize to tray button
		self.tray_button = ctk.CTkButton(
			self,
			text="Minimize to Tray",
			command=self._on_minimize_to_tray,
			fg_color="gray",
			hover_color="darkgray"
		)
		self.tray_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
		
		# Settings button
		self.settings_button = ctk.CTkButton(
			self,
			text="Settings",
			command=self._on_settings,
			fg_color="blue",
			hover_color="darkblue"
		)
		self.settings_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
	
	def _on_start(self):
		"""Called when Start button is clicked"""
		if 'start' in self.callbacks:
			self.callbacks['start']()
		self._set_tracking_state(True)
	
	def _on_stop(self):
		"""Called when Stop button is clicked"""
		if 'stop' in self.callbacks:
			self.callbacks['stop']()
		self._set_tracking_state(False)
	
	def _on_always_on_top_toggle(self):
		"""Called when Always on Top is toggled"""
		if 'always_on_top' in self.callbacks:
			self.callbacks['always_on_top'](self.always_on_top_var.get())
	
	def _on_hide_preview_toggle(self):
		"""Called when Hide Preview is toggled"""
		if 'hide_preview' in self.callbacks:
			self.callbacks['hide_preview'](self.hide_preview_var.get())
	
	def _on_minimize_to_tray(self):
		"""Called when Minimize to Tray is clicked"""
		if 'minimize_to_tray' in self.callbacks:
			self.callbacks['minimize_to_tray']()
	
	def _on_settings(self):
		"""Called when Settings button is clicked"""
		if 'settings' in self.callbacks:
			self.callbacks['settings']()
	
	def _set_tracking_state(self, is_tracking):
		"""Update button states based on tracking status"""
		self.is_tracking = is_tracking
		
		if is_tracking:
			self.start_button.configure(state="disabled")
			self.stop_button.configure(state="normal")
			self.update_status(STATUS_TRACKING)
		else:
			self.start_button.configure(state="normal")
			self.stop_button.configure(state="disabled")
			self.update_status(STATUS_READY)
	
	def update_gesture(self, gesture):
		"""
		Update gesture display

		Args:
			gesture: Current gesture string
		"""
		self.gesture_label.configure(text=f"Gesture: {gesture.upper()}")
	
	def update_status(self, status):
		"""
		Update status display

		Args:
			status: Status message string
		"""
		self.status_label.configure(text=f"Status: {status}")
	
	def get_always_on_top(self):
		"""Get Always on Top state"""
		if ENABLE_ALWAYS_ON_TOP:
			return self.always_on_top_var.get()
		return False
	
	def get_hide_preview(self):
		"""Get Hide Preview state"""
		if ENABLE_PREVIEW_TOGGLE:
			return self.hide_preview_var.get()
		return False
	