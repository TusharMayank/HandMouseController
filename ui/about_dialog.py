"""
About dialog showing application information
"""

import customtkinter as ctk
from app_info import APP_NAME, APP_VERSION, APP_AUTHOR, APP_DESCRIPTION, APP_LICENSE


class AboutDialog(ctk.CTkToplevel):
	"""About dialog window"""
	
	def __init__(self, parent):
		super().__init__(parent)
		
		self.title("About")
		self.geometry("450x500")
		self.resizable(False, False)
		
		# Center on parent
		self.transient(parent)
		self.grab_set()
		
		# Center window
		self.update_idletasks()
		parent_x = parent.winfo_x()
		parent_y = parent.winfo_y()
		parent_width = parent.winfo_width()
		parent_height = parent.winfo_height()
		
		x = parent_x + (parent_width - 450) // 2
		y = parent_y + (parent_height - 500) // 2
		self.geometry(f"450x500+{x}+{y}")
		
		# Create content
		self.create_widgets()
	
	def create_widgets(self):
		"""Create about dialog content"""
		# App name
		name_label = ctk.CTkLabel(
			self,
			text=APP_NAME,
			font=("Arial", 28, "bold")
		)
		name_label.pack(pady=(30, 10))
		
		# Version
		version_label = ctk.CTkLabel(
			self,
			text=f"Version {APP_VERSION}",
			font=("Arial", 14)
		)
		version_label.pack(pady=5)
		
		# Description
		desc_label = ctk.CTkLabel(
			self,
			text=APP_DESCRIPTION,
			font=("Arial", 11),
			wraplength=380
		)
		desc_label.pack(pady=20)
		
		# Features frame
		features_frame = ctk.CTkFrame(self)
		features_frame.pack(pady=10, padx=30, fill="both")
		
		features_title = ctk.CTkLabel(
			features_frame,
			text="Features:",
			font=("Arial", 12, "bold")
		)
		features_title.pack(pady=(10, 5))
		
		features = [
			"• 6 Gesture Controls",
			"• Real-time AI Hand Tracking (30 FPS)",
			"• 8 Customizable Settings",
			"• Visual Gesture Feedback",
			"• System Tray Support",
			"• Always on Top Mode",
			"• Performance Optimization"
		]
		
		for feature in features:
			feature_label = ctk.CTkLabel(
				features_frame,
				text=feature,
				font=("Arial", 10),
				anchor="w"
			)
			feature_label.pack(anchor="w", padx=20, pady=2)
		
		ctk.CTkLabel(features_frame, text="").pack(pady=5)  # Spacer
		
		# Author
		author_label = ctk.CTkLabel(
			self,
			text=f"Developed by {APP_AUTHOR}",
			font=("Arial", 11),
			text_color="gray"
		)
		author_label.pack(pady=10)
		
		# License
		license_label = ctk.CTkLabel(
			self,
			text=APP_LICENSE,
			font=("Arial", 10),
			text_color="gray"
		)
		license_label.pack(pady=5)
		
		# Close button
		close_button = ctk.CTkButton(
			self,
			text="Close",
			command=self.destroy,
			width=120
		)
		close_button.pack(pady=20)