import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import platform
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key, Controller as Controller_Keyboard


# Action to perform options
BUTTON_OPTIONS = {
    "Left": Button.left,
    "Right": Button.right,
    "Middle": Button.middle
}

# Detect platform
IS_MACOS = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"

# Keyboard modifier options (Rename Alt to Option on macOS for clarity)
MODIFIER_OPTIONS = {
    "None": None,
    "Shift": Key.shift,
    "Ctrl": Key.ctrl,
    "Alt" if not IS_MACOS else "Option": Key.alt
}


class ClickMouse(threading.Thread):
    def __init__(self, delay, button, modifier=None):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.modifier = modifier
        self.running = False
        self.program_running = True
        self.daemon = True
        self.keyboard = Controller_Keyboard()

    def update_settings(self, delay, button, modifier=None):
        self.delay = delay
        self.button = button
        self.modifier = modifier

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                if self.modifier:
                    with self.keyboard.pressed(self.modifier):
                        mouse.click(self.button)
                else:
                    mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)


class AutoClickerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("300x340" if IS_MACOS or IS_LINUX else "300x320")
        self.root.resizable(True, True)
        self.root.wm_attributes("-topmost", 1)
        self.root.minsize(300, 340 if IS_MACOS or IS_LINUX else 320)

        # Base dimensions for font scaling
        self.base_width = 300
        self.base_height = 340 if IS_MACOS or IS_LINUX else 320

        # Default settings
        self.delay_var = tk.DoubleVar(value=0.001)
        self.button_var = tk.StringVar(value="Left")
        self.modifier_var = tk.StringVar(value="None")
        self.start_stop_key_var = tk.StringVar(value="s")

        # Global variables for keys (synced with vars)
        self.start_stop_key = KeyCode(char=self.start_stop_key_var.get())

        self.setup_ui()

        # Shared resources
        self.click_thread = ClickMouse(
            self.delay_var.get(), 
            BUTTON_OPTIONS[self.button_var.get()],
            MODIFIER_OPTIONS[self.modifier_var.get()]
        )
        self.click_thread.start()

        # Keyboard listener
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        # UI Update loop
        self.update_status()

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure columns for resizing
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        # Configure rows for resizing
        for i in range(8):
            self.main_frame.rowconfigure(i, weight=1)

        # Delay
        self.delay_label = ttk.Label(self.main_frame, text="Delay (seconds):")
        self.delay_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.delay_entry = ttk.Entry(self.main_frame, textvariable=self.delay_var, width=10)
        self.delay_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

        # Mouse Button
        self.button_label = ttk.Label(self.main_frame, text="Mouse Button:")
        self.button_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.button_combo = ttk.Combobox(self.main_frame, textvariable=self.button_var, values=list(BUTTON_OPTIONS.keys()), state="readonly", width=8)
        self.button_combo.grid(row=1, column=1, sticky=tk.EW, pady=5)

        # Modifier
        self.modifier_label = ttk.Label(self.main_frame, text="Modifier Key:")
        self.modifier_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.modifier_combo = ttk.Combobox(self.main_frame, textvariable=self.modifier_var, values=list(MODIFIER_OPTIONS.keys()), state="readonly", width=8)
        self.modifier_combo.grid(row=2, column=1, sticky=tk.EW, pady=5)

        # Start/Stop Key
        self.key_label = ttk.Label(self.main_frame, text="Start/Stop Key:")
        self.key_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.key_entry = ttk.Entry(self.main_frame, textvariable=self.start_stop_key_var, width=5)
        self.key_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)

        # Apply Button
        self.apply_button = ttk.Button(self.main_frame, text="Apply Settings", command=self.apply_settings_with_hotkey)
        self.apply_button.grid(row=4, column=0, pady=10, sticky=tk.NSEW)

        # Exit Button
        self.exit_button = ttk.Button(self.main_frame, text="Exit Program", command=self.exit_program)
        self.exit_button.grid(row=4, column=1, pady=10, sticky=tk.NSEW)

        # Status
        self.status_label = ttk.Label(self.main_frame, text="Status: Stopped", foreground="red", anchor="center")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.NSEW)

        # Start/Stop Button
        self.toggle_button = ttk.Button(self.main_frame, text="Start Auto-Clicker", command=self.toggle_clicking)
        self.toggle_button.grid(row=6, column=0, columnspan=2, pady=5, sticky=tk.NSEW)

        # Instructions
        instruction_text = "Press the shortcut key to toggle.\nUse 'Exit Program' button to close."
        if IS_MACOS:
            instruction_text += "\nNote: Accessibility permissions required."
        elif IS_LINUX:
            instruction_text += "\nNote: May require X11 or uinput permissions."
            
        self.instructions_label = ttk.Label(self.main_frame, text=instruction_text, font=("", 8), justify="center")
        self.instructions_label.grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.NSEW)

    def on_resize(self, event):
        # We only care about root window resize
        if event.widget == self.root:
            width = event.width
            height = event.height
            
            # Calculate scale factor (use the smaller scale to maintain readability)
            scale_w = width / self.base_width
            scale_h = height / self.base_height
            scale = min(scale_w, scale_h)
            
            # Update fonts
            base_font_size = 9
            new_size = max(int(base_font_size * scale), 6)
            
            small_font_size = 8
            new_small_size = max(int(small_font_size * scale), 5)

            font_style = ("", new_size)
            small_font_style = ("", new_small_size)

            # Apply fonts to widgets
            # ttk widgets use styles, but some support font option directly or via style
            style = ttk.Style()
            style.configure("TLabel", font=font_style)
            style.configure("TButton", font=font_style)
            style.configure("TEntry", font=font_style)
            style.configure("TCombobox", font=font_style)
            
            # Custom fonts for specific labels if needed
            self.instructions_label.configure(font=small_font_style)
            
            # For entries and comboboxes, we also want to update the font of the internal entry
            # In ttk, this is usually handled by the style, but sometimes needs explicit setting
            # for some themes. Let's try standard style first.
            self.delay_entry.configure(font=font_style)
            self.key_entry.configure(font=font_style)
            self.root.option_add("*TCombobox*Listbox.font", font_style) # Update listbox font

    def toggle_clicking(self):
        if self.click_thread.running:
            self.click_thread.stop_clicking()
            print("[INFO] Auto-clicker stopped.")
        else:
            self.click_thread.start_clicking()
            print("[INFO] Auto-clicker started.")

    def apply_settings_with_hotkey(self):
        self.apply_settings()
        self.update_hotkey()

    def apply_settings(self, event=None):
        try:
            delay = float(self.delay_var.get())
            if delay < 0.0001:
                delay = 0.0001
                self.delay_var.set(delay)
            button = BUTTON_OPTIONS[self.button_var.get()]
            modifier = MODIFIER_OPTIONS[self.modifier_var.get()]
            self.click_thread.update_settings(delay, button, modifier)
            print("[INFO] Settings applied.")
        except ValueError:
            messagebox.showerror("Error", "Invalid delay value. Please enter a number.")

    def update_hotkey(self, event=None):
        key_str = self.start_stop_key_var.get().lower()
        if len(key_str) == 1:
            self.start_stop_key = KeyCode(char=key_str)
        else:
            messagebox.showwarning("Warning", "Hotkey must be a single character.")
            self.start_stop_key_var.set(self.start_stop_key.char)

    def update_status(self):
        if self.click_thread.running:
            self.status_label.config(text="Status: Running", foreground="green")
            self.toggle_button.config(text="Stop Auto-Clicker")
        else:
            self.status_label.config(text="Status: Stopped", foreground="red")
            self.toggle_button.config(text="Start Auto-Clicker")
        
        if not self.click_thread.program_running:
            self.root.destroy()
            return

        self.root.after(100, self.update_status)

    def on_press(self, key):
        if key == self.start_stop_key:
            self.toggle_clicking()

    def exit_program(self):
        self.click_thread.exit()
        self.listener.stop()
        print("[INFO] Exiting...")


if __name__ == "__main__":
    mouse = Controller()
    root = tk.Tk()
    app = AutoClickerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.exit_program)
    root.mainloop()
