"""
Text-to-Speech Utility
Announces detected gestures using the system's speech engine
"""

import pyttsx3
import threading


class SpeechAnnouncer:
    def __init__(self):
        self.engine = None
        self.last_gesture = None
        self.is_enabled = True

        try:
            # Initialize the TTS engine
            self.engine = pyttsx3.init()
            # Set properties (optional)
            self.engine.setProperty('rate', 150)  # Speed percent (can go over 100)
            self.engine.setProperty('volume', 0.9)  # Volume 0-1
        except Exception as e:
            print(f"Warning: Could not initialize Text-to-Speech engine: {e}")

    def announce_gesture(self, gesture_name):
        """
        Announce the gesture if it has changed since the last frame

        Args:
            gesture_name: The string ID of the current gesture (e.g., 'gesture_click')
        """
        if not self.is_enabled or not self.engine:
            return

        # normalize gesture name (e.g., "none" -> "None")
        if gesture_name is None:
            gesture_name = "none"

        # Only speak if the gesture has changed
        if gesture_name != self.last_gesture:
            self.last_gesture = gesture_name

            # Format the text to sound natural
            # e.g., "double_click" -> "Double Click"
            text_to_speak = gesture_name.replace("_", " ").title()

            # Don't announce "None" or "Move" excessively if desired,
            # but for this feature we will read everything as requested.
            self._speak_threaded(text_to_speak)

    def _speak_threaded(self, text):
        """Run speech in a separate thread to prevent UI blocking"""
        thread = threading.Thread(target=self._speak_task, args=(text,))
        thread.daemon = True
        thread.start()

    def _speak_task(self, text):
        """Internal task to run the engine"""
        try:
            # pyttsx3 needs its own loop in the thread or proper locking
            # This simple approach usually works for one-off utterances
            if self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")

    def toggle(self, enabled):
        """Enable or disable speech"""
        self.is_enabled = enabled