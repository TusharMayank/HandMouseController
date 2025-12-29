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
import os
import ctypes
import customtkinter as ctk


def show_instance_warning():
    """Display a warning window indicating the app is already running"""
    # Create a small isolated window
    warning_app = ctk.CTk()
    warning_app.title("Warning")

    # Center the window
    width, height = 400, 150
    screen_width = warning_app.winfo_screenwidth()
    screen_height = warning_app.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    warning_app.geometry(f"{width}x{height}+{x}+{y}")

    # Keep on top
    warning_app.attributes('-topmost', True)

    # UI Elements
    label = ctk.CTkLabel(
        warning_app,
        text="ANOTHER INSTANCE OF THE APP IS OPEN",
        font=("Arial", 16, "bold"),
        text_color="red"
    )
    label.pack(expand=True, pady=(20, 10))

    btn = ctk.CTkButton(
        warning_app,
        text="OK",
        command=lambda: sys.exit(0),
        width=100
    )
    btn.pack(pady=(0, 20))

    warning_app.mainloop()


def check_single_instance():
    """Check if an instance is already running using a named mutex (Windows only)"""
    if os.name == 'nt':
        mutex_name = "Global\\HandMouseController_Unique_Mutex"
        kernel32 = ctypes.windll.kernel32

        # Try to create a named mutex
        mutex = kernel32.CreateMutexW(None, False, mutex_name)

        # Error 183 means ERROR_ALREADY_EXISTS
        if kernel32.GetLastError() == 183:
            return None

        return mutex
    return "Non-Windows-Mutex"


def main():
    """
    Main entry point for the application
    """
    # Check for existing instance
    app_mutex = check_single_instance()

    if app_mutex is None:
        # If mutex is None, it means another instance is running
        try:
            show_instance_warning()
        except:
            pass  # Failsafe if GUI fails
        sys.exit(0)

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