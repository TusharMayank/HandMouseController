"""
Settings Window
Allows user to adjust sensitivity, speed, and other parameters
"""

import customtkinter as ctk
import json
import os


class SettingsWindow(ctk.CTkToplevel):
	"""Settings dialog with sliders for adjustable parameters"""
	
	def __init__(self, parent, config_callback):
		super().__init__(parent)
		
		self.config_callback = config_callback  # Function to update main app config
		self.settings_file = "user_settings.json"
		self.config_callback = config_callback
		self.settings_file = "user_settings.json"
		
		# Initialize attributes (will be set properly in methods)
		self.settings = {}
		self.scroll_frame = None
		self.movement_slider = None
		self.smoothing_slider = None
		self.pinch_slider = None
		self.double_click_slider = None
		self.scroll_activation_slider = None
		self.scroll_slow_slider = None
		self.scroll_medium_slider = None
		self.scroll_fast_slider = None
		
		# Value labels for sliders (to update on reset)
		self.movement_value_label = None
		self.smoothing_value_label = None
		self.pinch_value_label = None
		self.double_click_value_label = None
		self.scroll_activation_value_label = None
		self.scroll_slow_value_label = None
		self.scroll_medium_value_label = None
		self.scroll_fast_value_label = None
		
		# Window configuration
		self.title("Hand Mouse Controller - Settings")
		self.geometry("600x700")
		self.resizable(False, False)
		
		# Make window modal (stays on top of parent)
		self.transient(parent)
		self.grab_set()
		
		# Center window on screen
		self.center_window()
		
		# Load saved settings or use defaults
		self.load_settings()
		
		# Create UI
		self.create_widgets()
	
	def center_window(self):
		"""Position settings window at top-center of screen"""
		self.update_idletasks()
		width = self.winfo_width()
		height = self.winfo_height()
		x = (self.winfo_screenwidth() // 2) - (width // 2)  # Centered horizontally
		y = 0  # Touch the top of screen
		self.geometry(f"{width}x{height}+{x}+{y}")
	
	def load_settings(self):
		"""Load settings from file or use defaults"""
		default_settings = {
			'movement_sensitivity': 40,  # → 2.2x speed (more reasonable)
			'smoothing': 70,  # unchanged
			'scroll_speed_slow': 20,  # → 6 steps (slower start)
			'scroll_speed_medium': 30,  # → 7 steps (similar to old)
			'scroll_speed_fast': 40,  # → 14 steps (moderate)
			'scroll_activation': 50,  # unchanged
			'pinch_sensitivity': 50,  # unchanged
			'double_click_time': 50  # unchanged
		}
		
		try:
			if os.path.exists(self.settings_file):
				with open(self.settings_file, 'r') as f:
					self.settings = json.load(f)
				# Merge with defaults in case new settings were added
				for key, value in default_settings.items():
					if key not in self.settings:
						self.settings[key] = value
			else:
				self.settings = default_settings
		except Exception as e:
			print(f"Error loading settings: {e}")
			self.settings = default_settings
	
	def save_settings(self):
		"""Save settings to file"""
		try:
			with open(self.settings_file, 'w') as f:
				json.dump(self.settings, f, indent=4)
		except Exception as e:
			print(f"Error saving settings: {e}")
	
	def create_widgets(self):
		"""Create all settings widgets"""
		
		# Main container with scrollable frame
		self.scroll_frame = ctk.CTkScrollableFrame(self, width=560, height=600)
		self.scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)
		
		# Title
		title_label = ctk.CTkLabel(
			self.scroll_frame,
			text="Adjust Settings",
			font=("Arial", 20, "bold")
		)
		title_label.pack(pady=(0, 20))
		
		# Mouse Control Section
		self.create_section_header("Mouse Control")
		
		self.movement_slider, self.movement_value_label = self.create_slider(
			"Movement Sensitivity",
			"How fast the cursor moves",
			self.settings['movement_sensitivity'],
			lambda v: self.update_setting('movement_sensitivity', v)
		)
		
		self.smoothing_slider, self.smoothing_value_label = self.create_slider(
			"Cursor Smoothing",
			"Higher = smoother but slightly delayed",
			self.settings['smoothing'],
			lambda v: self.update_setting('smoothing', v)
		)
		
		# Gesture Recognition Section
		self.create_section_header("Gesture Recognition")
		
		self.pinch_slider, self.pinch_value_label = self.create_slider(
			"Pinch Sensitivity",
			"Lower = easier to trigger pinch gestures",
			self.settings['pinch_sensitivity'],
			lambda v: self.update_setting('pinch_sensitivity', v)
		)
		
		self.double_click_slider, self.double_click_value_label = self.create_slider(
			"Double-Click Speed",
			"Higher = more time allowed between clicks",
			self.settings['double_click_time'],
			lambda v: self.update_setting('double_click_time', v)
		)
		
		# Scroll Settings Section
		self.create_section_header("Scroll Settings")
		
		self.scroll_activation_slider, self.scroll_activation_value_label = self.create_slider(
			"Scroll Activation Distance",
			"How far to move fist before scrolling starts",
			self.settings['scroll_activation'],
			lambda v: self.update_setting('scroll_activation', v)
		)
		
		self.scroll_slow_slider, self.scroll_slow_value_label = self.create_slider(
			"Scroll Speed - Slow Zone",
			"Speed when slightly away from neutral",
			self.settings['scroll_speed_slow'],
			lambda v: self.update_setting('scroll_speed_slow', v)
		)
		
		self.scroll_medium_slider, self.scroll_medium_value_label = self.create_slider(
			"Scroll Speed - Medium Zone",
			"Speed when moderately away from neutral",
			self.settings['scroll_speed_medium'],
			lambda v: self.update_setting('scroll_speed_medium', v)
		)
		
		self.scroll_fast_slider, self.scroll_fast_value_label = self.create_slider(
			"Scroll Speed - Fast Zone",
			"Speed when far from neutral",
			self.settings['scroll_speed_fast'],
			lambda v: self.update_setting('scroll_speed_fast', v)
		)
		
		# Buttons
		button_frame = ctk.CTkFrame(self)
		button_frame.pack(pady=10, fill="x", padx=20)
		
		apply_button = ctk.CTkButton(
			button_frame,
			text="Apply & Save",
			command=self.apply_settings,
			fg_color="green",
			hover_color="darkgreen",
			width=150
		)
		apply_button.pack(side="left", padx=5)
		
		reset_button = ctk.CTkButton(
			button_frame,
			text="Reset to Defaults",
			command=self.reset_to_defaults,
			fg_color="orange",
			hover_color="darkorange",
			width=150
		)
		reset_button.pack(side="left", padx=5)
		
		close_button = ctk.CTkButton(
			button_frame,
			text="Close",
			command=self.close_window,
			fg_color="gray",
			hover_color="darkgray",
			width=150
		)
		close_button.pack(side="right", padx=5)
	
	def create_section_header(self, text):
		"""Create a section header label"""
		header = ctk.CTkLabel(
			self.scroll_frame,
			text=text,
			font=("Arial", 16, "bold"),
			anchor="w"
		)
		header.pack(pady=(20, 10), padx=10, fill="x")
		
		# Separator line
		separator = ctk.CTkFrame(self.scroll_frame, height=2, fg_color="gray")
		separator.pack(fill="x", padx=10, pady=(0, 10))
	
	def create_slider(self, title, description, initial_value, command):
		"""Create a labeled slider with value display"""
		# Container frame
		container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
		container.pack(pady=10, padx=10, fill="x")
		
		# Title and value label
		header_frame = ctk.CTkFrame(container, fg_color="transparent")
		header_frame.pack(fill="x", pady=(0, 5))
		
		title_label = ctk.CTkLabel(
			header_frame,
			text=title,
			font=("Arial", 13, "bold"),
			anchor="w"
		)
		title_label.pack(side="left")
		
		value_label = ctk.CTkLabel(
			header_frame,
			text=f"{int(initial_value)}",
			font=("Arial", 13),
			anchor="e",
			width=40
		)
		value_label.pack(side="right")
		
		# Description
		desc_label = ctk.CTkLabel(
			container,
			text=description,
			font=("Arial", 10),
			text_color="gray",
			anchor="w"
		)
		desc_label.pack(fill="x", pady=(0, 5))
		
		# Slider
		slider = ctk.CTkSlider(
			container,
			from_=10,
			to=100,
			number_of_steps=90,
			command=lambda v: self.slider_changed(v, value_label, command)
		)
		slider.set(initial_value)
		slider.pack(fill="x", pady=(0, 5))
		
		# Min/Max labels
		range_frame = ctk.CTkFrame(container, fg_color="transparent")
		range_frame.pack(fill="x")
		
		min_label = ctk.CTkLabel(range_frame, text="10 (Slow)", font=("Arial", 9), text_color="gray")
		min_label.pack(side="left")
		
		max_label = ctk.CTkLabel(range_frame, text="100 (Fast)", font=("Arial", 9), text_color="gray")
		max_label.pack(side="right")
		
		return slider, value_label
	
	# noinspection PyMethodMayBeStatic
	def slider_changed(self, value, value_label, command):
		"""Called when slider value changes"""
		value_label.configure(text=f"{int(value)}")
		command(int(value))
	
	def update_setting(self, key, value):
		"""Update a setting value"""
		self.settings[key] = value
	
	def apply_settings(self):
		"""Apply settings and notify main app"""
		# Save to file
		self.save_settings()
		
		# Convert slider values (10-100) to actual config values
		actual_values = self.convert_to_actual_values()
		
		# Notify main app
		if self.config_callback:
			self.config_callback(actual_values)
		
		# Show confirmation
		self.show_confirmation()
	
	def convert_to_actual_values(self):
		"""Convert slider values (10-100) to actual configuration values"""
		return {
			# Movement sensitivity: 10-100 → 0.8-5.0
			'MOVEMENT_SENSITIVITY': 0.8 + (self.settings['movement_sensitivity'] - 10) * (5.0 - 0.8) / 90,
			
			# Smoothing: 10-100 → 0.5-0.9 (unchanged)
			'SMOOTHING_FACTOR': 0.5 + (self.settings['smoothing'] - 10) * (0.9 - 0.5) / 90,
			
			# Scroll speeds: Updated ranges
			'SCROLL_SPEED_SLOW': 1 + int((self.settings['scroll_speed_slow'] - 10) * 49 / 90),  # 1-50
			'SCROLL_SPEED_MEDIUM': 1 + int((self.settings['scroll_speed_medium'] - 10) * 29 / 90),  # 1-30
			'SCROLL_SPEED_FAST': 1 + int((self.settings['scroll_speed_fast'] - 10) * 39 / 90),  # 1-40
			
			# Scroll activation: 10-100 → 20-100 pixels (unchanged)
			'SCROLL_ACTIVATION_THRESHOLD': 20 + int((self.settings['scroll_activation'] - 10) * 80 / 90),
			
			# Pinch sensitivity: 10-100 → 0.1-0.01 (inverted - lower slider = harder pinch)
			'PINCH_THRESHOLD': 0.1 - (self.settings['pinch_sensitivity'] - 10) * (0.1 - 0.01) / 90,
			
			# Double-click time: 10-100 → 0.1-1.0 seconds
			'DOUBLE_CLICK_TIME': 0.1 + (self.settings['double_click_time'] - 10) * (1.0 - 0.1) / 90,
		}
	
	def reset_to_defaults(self):
		"""Reset all settings to default values"""
		defaults = {
			'movement_sensitivity': 60,
			'smoothing': 70,
			'scroll_speed_slow': 30,
			'scroll_speed_medium': 50,
			'scroll_speed_fast': 60,
			'scroll_activation': 50,
			'pinch_sensitivity': 50,
			'double_click_time': 50
		}
		
		# Update settings dictionary
		self.settings.clear()
		self.settings.update(defaults)
		
		# Update all sliders AND their value labels
		self.movement_slider.set(defaults['movement_sensitivity'])
		self.movement_value_label.configure(text=f"{defaults['movement_sensitivity']}")
		
		self.smoothing_slider.set(defaults['smoothing'])
		self.smoothing_value_label.configure(text=f"{defaults['smoothing']}")
		
		self.scroll_slow_slider.set(defaults['scroll_speed_slow'])
		self.scroll_slow_value_label.configure(text=f"{defaults['scroll_speed_slow']}")
		
		self.scroll_medium_slider.set(defaults['scroll_speed_medium'])
		self.scroll_medium_value_label.configure(text=f"{defaults['scroll_speed_medium']}")
		
		self.scroll_fast_slider.set(defaults['scroll_speed_fast'])
		self.scroll_fast_value_label.configure(text=f"{defaults['scroll_speed_fast']}")
		
		self.scroll_activation_slider.set(defaults['scroll_activation'])
		self.scroll_activation_value_label.configure(text=f"{defaults['scroll_activation']}")
		
		self.pinch_slider.set(defaults['pinch_sensitivity'])
		self.pinch_value_label.configure(text=f"{defaults['pinch_sensitivity']}")
		
		self.double_click_slider.set(defaults['double_click_time'])
		self.double_click_value_label.configure(text=f"{defaults['double_click_time']}")
		
		# Save and apply
		self.apply_settings()
	
	def show_confirmation(self):
		"""Show settings saved confirmation"""
		# Create temporary label
		confirm_label = ctk.CTkLabel(
			self,
			text="✓ Settings Saved Successfully!",
			font=("Arial", 12, "bold"),
			text_color="green"
		)
		confirm_label.place(relx=0.5, rely=0.95, anchor="center")
		
		# Remove after 2 seconds
		self.after(2000, confirm_label.destroy)
	
	def close_window(self):
		"""Close the settings window"""
		self.grab_release()
		self.destroy()