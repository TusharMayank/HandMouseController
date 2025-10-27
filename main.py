"""
Hand Mouse Controller - Main Entry Point
Control your mouse using hand gestures captured by webcam

Author: Tushar Mayank
Date: 2025
"""

import sys
from ui.main_window import MainWindow
from utils.logger import log_info, log_error
from app_info import APP_NAME, APP_VERSION


def main():
    """
    Main entry point for the application
    """
    log_info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    try:
        # Create and run the application
        app = MainWindow()
        log_info("Application window created successfully")
        app.mainloop()
        
    except KeyboardInterrupt:
        log_info("Application interrupted by user")
        print("\nApplication interrupted by user")
        sys.exit(0)
        
    except Exception as e:
        log_error("Fatal error", e)
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        log_info("Application shutdown complete")


if __name__ == "__main__":
    main()