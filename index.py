import pyautogui
import keyboard
import random
import time
import threading

# Global variables to manage state
is_typing = False
current_position = 0
min_wpm = 40
max_wpm = 60

def auto_type(text):
    """Types the given text with random intervals based on WPM."""
    global is_typing, current_position, min_wpm, max_wpm
    try:
        while current_position < len(text):  # Keep typing until the end of the text
            if not is_typing:  # Stop typing if toggled off
                break
            pyautogui.typewrite(text[current_position])  # Type the current character
            current_position += 1  # Move to the next character
            # Calculate random delay based on WPM range
            delay = 60 / random.randint(min_wpm, max_wpm) / 5  # 5 characters per word
            time.sleep(delay)
    except Exception as e:
        print(f"Error while typing: {e}")

def toggle_typing(text):
    """Toggles typing state and starts/stops the typing process."""
    global is_typing
    if is_typing:
        print("Typing paused.")
        is_typing = False
    else:
        print("Typing started.")
        is_typing = True
        threading.Thread(target=auto_type, args=(text,), daemon=True).start()

def increase_speed():
    """Increases typing speed by 1.5x."""
    global min_wpm, max_wpm
    min_wpm = int(min_wpm * 1.5)
    max_wpm = int(max_wpm * 1.5)
    print(f"Speed increased: min WPM = {min_wpm}, max WPM = {max_wpm}")

def main():
    global min_wpm, max_wpm, current_position, is_typing
    # Read text from a .txt file
    with open("text_to_type.txt", "r", encoding="utf-8") as file:
        text_to_type = file.read().strip()  # Read and strip any extra whitespace

    # Set initial speed
    min_wpm = int(200)
    max_wpm = int(300)
    print("Press 'Esc' to start/pause typing, 'F1' to increase speed, 'Ctrl+Shift+X' to exit.")

    # Register hotkeys
    keyboard.add_hotkey('esc', toggle_typing, args=(text_to_type,))
    keyboard.add_hotkey('ctrl+shift+a', increase_speed)
    keyboard.add_hotkey('ctrl+shift+b', exit)
    
    # Keep the script running
    keyboard.wait('ctrl+shift+b')
    print("Script exited.")

if __name__ == "__main__":
    main()
