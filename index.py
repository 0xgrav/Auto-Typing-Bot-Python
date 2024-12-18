import tkinter as tk
from tkinter import scrolledtext
from pynput.keyboard import Controller
import threading
import random
import time

# Globals
is_typing = False
current_position = 0
min_wpm = 40
max_wpm = 60
typing_thread = None
keyboard = Controller()

def auto_type(text_widget):
    """Simulates typing with optimized speed using pynput."""
    global is_typing, current_position, min_wpm, max_wpm
    text = text_widget.get("1.0", tk.END).strip()  # Get text from the text widget
    while current_position < len(text):
        if not is_typing:
            break
        keyboard.type(text[current_position])  # Type the current character
        current_position += 1  # Move to the next character

        # WPM delay: Convert WPM to delay per character (5 characters per word)
        delay = 60 / (random.uniform(min_wpm, max_wpm) * 5)
        time.sleep(delay)

def start_typing(text_widget, min_wpm_input, max_wpm_input):
    """Starts the typing process."""
    global is_typing, typing_thread, min_wpm, max_wpm
    if is_typing:
        return  # Prevent starting again if already typing
    try:
        min_wpm = int(min_wpm_input.get())
        max_wpm = int(max_wpm_input.get())
        update_status("Starting in 2 seconds...")
        time.sleep(2)  # Delay to allow focusing on another UI
        is_typing = True
        if typing_thread is None or not typing_thread.is_alive():  # Start a new thread
            typing_thread = threading.Thread(
                target=auto_type, args=(text_widget,), daemon=True
            )
            typing_thread.start()
        update_status("Typing started.")
    except ValueError:
        update_status("Please enter valid WPM values.")

def pause_typing():
    """Pauses the typing process."""
    global is_typing
    if is_typing:
        is_typing = False
        update_status("Typing paused.")

def continue_typing():
    """Continues the typing process."""
    global is_typing, typing_thread
    if not is_typing:
        update_status("Continuing in 2 seconds...")
        time.sleep(2)  # Delay to allow focusing on another UI
        is_typing = True
        if typing_thread is None or not typing_thread.is_alive():  # Resume the thread
            typing_thread = threading.Thread(
                target=auto_type, args=(text_widget,), daemon=True
            )
            typing_thread.start()
        update_status("Typing continued.")

def stop_typing():
    """Stops the typing process and resets progress."""
    global is_typing, current_position
    is_typing = False
    current_position = 0
    update_status("Typing stopped. Progress reset.")

def increase_speed(min_wpm_input, max_wpm_input):
    """Increases typing speed by 1.5x."""
    global min_wpm, max_wpm
    try:
        min_wpm = int(min_wpm_input.get())
        max_wpm = int(max_wpm_input.get())
        min_wpm = int(min_wpm * 1.5)
        max_wpm = int(max_wpm * 1.5)
        min_wpm_input.delete(0, tk.END)
        min_wpm_input.insert(0, str(min_wpm))
        max_wpm_input.delete(0, tk.END)
        max_wpm_input.insert(0, str(max_wpm))
        update_status(f"Speed increased: Min WPM = {min_wpm}, Max WPM = {max_wpm}")
    except ValueError:
        update_status("Please enter valid WPM values.")

def update_status(message):
    """Updates the status label."""
    status_label.config(text=message)

# Create the GUI
root = tk.Tk()
root.title("Auto Typing Tool")

# Min WPM and Max WPM Inputs
tk.Label(root, text="Min WPM:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
min_wpm_input = tk.Entry(root, width=10)
min_wpm_input.grid(row=0, column=1, padx=10, pady=5)
min_wpm_input.insert(0, "40")

tk.Label(root, text="Max WPM:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
max_wpm_input = tk.Entry(root, width=10)
max_wpm_input.grid(row=0, column=3, padx=10, pady=5)
max_wpm_input.insert(0, "60")

# Text Area for Main Text
tk.Label(root, text="Main Text:").grid(row=1, column=0, columnspan=4, padx=10, pady=5)
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
text_widget.grid(row=2, column=0, columnspan=4, padx=10, pady=5)

def focus_handler(event):
    """Ensure editor field gets focus only when explicitly clicked."""
    event.widget.focus_set()

# Bind text widget focus to mouse click
text_widget.bind("<FocusIn>", focus_handler)

# Buttons
start_button = tk.Button(
    root, text="Start", command=lambda: start_typing(text_widget, min_wpm_input, max_wpm_input)
)
start_button.grid(row=3, column=0, padx=10, pady=10)

pause_button = tk.Button(root, text="Pause", command=pause_typing)
pause_button.grid(row=3, column=1, padx=10, pady=10)

continue_button = tk.Button(root, text="Continue", command=continue_typing)
continue_button.grid(row=3, column=2, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop_typing)
stop_button.grid(row=3, column=3, padx=10, pady=10)

increase_speed_button = tk.Button(
    root, text="Increase Speed", command=lambda: increase_speed(min_wpm_input, max_wpm_input)
)
increase_speed_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

# Status Label
status_label = tk.Label(root, text="Status: Ready", fg="blue")
status_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

# Run the GUI
root.mainloop()
