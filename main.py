"""
Hand Mouse Controller - Main Entry Point
Control your mouse using hand gestures captured by webcam

Author: TUSHAR MAYANK
Date: 2025
"""

import sys
from ui.main_window import MainWindow


def main():
	"""
	Main entry point for the application
	"""
	try:
		# Create and run the application
		app = MainWindow()
		app.mainloop()
	
	except KeyboardInterrupt:
		print("\nApplication interrupted by user")
		sys.exit(0)
	
	except Exception as e:
		print(f"Fatal error: {e}")
		import traceback
		traceback.print_exc()
		sys.exit(1)


if __name__ == "__main__":
	main()