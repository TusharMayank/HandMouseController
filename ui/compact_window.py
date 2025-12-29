import customtkinter as ctk


class CompactWindow(ctk.CTkToplevel):
    """
    Compact Window Mode
    Small window with essential controls
    """

    def __init__(self, parent, callbacks, initial_states):
        super().__init__(parent)
        self.callbacks = callbacks
        self.parent = parent

        # Window Setup
        self.title("Hand Mouse")
        self.geometry("300x230")  # Slightly wider for the new toggle
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        x_pos = screen_width - 310
        y_pos = 0

        self.geometry(f"+{x_pos}+{y_pos}")

        # Keep on top
        self.attributes('-topmost', True)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets(initial_states)

        # Handle closing
        self.protocol("WM_DELETE_WINDOW", parent.on_closing)

    def create_widgets(self, initial_states):
        # 1. Start/Stop Tracking Button
        self.tracking_btn = ctk.CTkButton(
            self,
            text="Start Tracking",
            command=self._on_tracking_toggle,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.tracking_btn.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # 2. Settings Button
        self.settings_btn = ctk.CTkButton(
            self,
            text="Settings",
            command=self.callbacks['settings']
        )
        self.settings_btn.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Separator
        ctk.CTkFrame(self, height=2, fg_color="gray").grid(row=2, column=0, padx=10, pady=(0, 15), sticky="ew")

        # 3. Speak Aloud Toggle
        self.speech_var = ctk.BooleanVar(value=initial_states.get('speech_enabled', True))
        self.speech_switch = ctk.CTkSwitch(
            self,
            text="Speak Aloud",
            variable=self.speech_var,
            command=self._on_speech_toggle
        )
        self.speech_switch.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="w")

        # 4. Custom Mode Toggle (Developer vs Compact)
        # Create a container frame for the custom look
        toggle_frame = ctk.CTkFrame(self, fg_color="transparent")
        toggle_frame.grid(row=4, column=0, padx=10, pady=(0, 20))

        # Left Label
        dev_label = ctk.CTkLabel(toggle_frame, text="DEVELOPER WINDOW", font=("Arial", 10, "bold"), text_color="gray")
        dev_label.pack(side="left", padx=(0, 5))

        # The Switch
        # value=1 (ON) means Compact Mode (Green)
        # value=0 (OFF) means Developer Mode (Blue)
        self.mode_var = ctk.IntVar(value=1)  # Starts in Compact Mode

        self.mode_switch = ctk.CTkSwitch(
            toggle_frame,
            text="",  # No text on the switch itself
            variable=self.mode_var,
            command=self._on_mode_toggle,
            fg_color="#3B8ED0",  # Blue when OFF (Left/Developer)
            progress_color="#2CC985",  # Green when ON (Right/Compact)
            button_color="white",
            button_hover_color="gray90",
            width=50
        )
        self.mode_switch.pack(side="left")

        # Right Label
        compact_label = ctk.CTkLabel(toggle_frame, text="COMPACT WINDOW", font=("Arial", 10, "bold"))
        compact_label.pack(side="left", padx=(5, 0))

        # Initialize button state
        self.update_tracking_state(initial_states.get('is_tracking', False))

    def _on_tracking_toggle(self):
        if self.tracking_btn.cget('text') == "Start Tracking":
            self.callbacks['start']()
        else:
            self.callbacks['stop']()

    def update_tracking_state(self, is_tracking):
        if is_tracking:
            self.tracking_btn.configure(text="Stop Tracking", fg_color="red", hover_color="darkred")
        else:
            self.tracking_btn.configure(text="Start Tracking", fg_color="green", hover_color="darkgreen")

    def _on_speech_toggle(self):
        if 'toggle_speech' in self.callbacks:
            self.callbacks['toggle_speech'](self.speech_var.get())

    def _on_mode_toggle(self):
        # If user switches to OFF (0), it means they want Developer Mode
        if self.mode_var.get() == 0:
            self.callbacks['switch_to_full']()
        # If they try to switch back to ON (1) while here, nothing happens (already compact)