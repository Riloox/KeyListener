from pynput.keyboard import Listener, Key
import subprocess
import time
import json
import winreg
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import ctypes  # For popup notification
import webbrowser  # For opening webpages

# Set up logging with rotation
log_handler = RotatingFileHandler(
    filename='keylistener.log',
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=5,         # Keep 5 backup files
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

logger = logging.getLogger('KeyListener')
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Log startup
logger.info("KeyListener started successfully!")

# Variables to track shift presses
last_shift_time = 0
shift_count = 0
waiting_for_input = False  # Tracks if we're waiting for a letter or Escape
actions = {}  # Will be populated from config

# Set the working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
logger.info(f"Working directory set to: {script_dir}")

# Load configuration from config.json
def load_config():
    global actions
    config_path = os.path.join(script_dir, 'config.json')
    logger.info(f"Loading config from: {config_path}")
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            actions = {
                key: create_action(value)
                for key, value in config['actions'].items()
            }
        logger.info("Config loaded successfully")
        logger.info(f"Loaded actions: {list(actions.keys())}")
    except FileNotFoundError:
        logger.warning("config.json not found! Using default actions.")
        actions = {
            'a': lambda: logger.info("Default Action A"),
            'b': lambda: logger.info("Default Action B"),
        }
    except json.JSONDecodeError:
        logger.warning("Invalid JSON in config.json! Using default actions.")
        actions = {
            'a': lambda: logger.info("Default Action A"),
            'b': lambda: logger.info("Default Action B"),
        }

def create_action(action_config):
    """Convert config action definition to executable function"""
    action_type = action_config.get('type', 'print')
    
    if action_type == 'print':
        return lambda: logger.info(action_config.get('message', 'No message defined'))
    elif action_type == 'subprocess':
        return lambda: subprocess.run(action_config.get('command', ['echo', 'No command']))
    elif action_type == 'sleep':
        return lambda: time.sleep(action_config.get('duration', 1))
    elif action_type == 'open_webpage':
        url = action_config.get('url', 'https://www.example.com')
        return lambda: open_webpage(url)
    elif action_type == 'execute_code':
        code = action_config.get('code', 'print("No code specified")')
        return lambda: execute_code(code)
    else:
        return lambda: logger.info(f"Unknown action type: {action_type}")

def open_webpage(url):
    """Open a webpage in the default web browser"""
    # Ensure the URL starts with 'http://' or 'https://'
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'  # Default to 'https://' if no protocol is specified
    
    logger.info(f"Opening webpage: {url}")
    webbrowser.open(url)

def execute_code(code):
    """Execute Python code"""
    logger.info(f"Executing code: {code}")
    try:
        exec(code)
    except Exception as e:
        logger.error(f"Error executing code: {e}")

def on_press(key):
    global last_shift_time, shift_count, waiting_for_input
    
    try:
        # Detect double shift
        if key in [Key.shift, Key.shift_r]:
            current_time = time.time()
            if current_time - last_shift_time < 0.5:
                shift_count += 1
                if shift_count == 2:
                    logger.info("Double shift detected! Waiting for input...")
                    waiting_for_input = True
                    shift_count = 0
            else:
                shift_count = 1
            last_shift_time = current_time
        
        # Handle input after double shift
        elif waiting_for_input:
            if key == Key.esc:
                logger.info("Escape pressed after double shift - stopping listener")
                show_popup("KeyListener Disabled", "The KeyListener program has been disabled.")
                return False  # Exit the program
            elif hasattr(key, 'char'):  # Check if it's a letter key
                handle_letter(key.char)
                waiting_for_input = False
            
    except AttributeError:
        # Ignore special keys (e.g., Ctrl, Alt)
        pass

def on_release(key):
    global waiting_for_input
    
    # Reset waiting state if a non-Shift key is released
    if waiting_for_input and key not in [Key.shift, Key.shift_r]:
        waiting_for_input = False
        logger.info("Waiting for input state reset due to non-shift key release")

def handle_letter(letter):
    """Handle the first letter pressed after double shift"""
    letter = letter.lower()
    logger.info(f"Handling letter: {letter}")
    action = actions.get(letter, lambda: logger.info(f"No action defined for letter '{letter}'"))
    action()

def show_popup(title, message):
    """Display a popup notification using ctypes"""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1000)  # 0x40 = Info icon, 0x1000 = Always on top

def add_to_startup():
    """Add the script to Windows startup via registry"""
    # Get the absolute path to the current script
    script_path = os.path.abspath(__file__)
    
    # Ensure the path is properly quoted to handle spaces
    script_path = f'"{script_path}"'
    
    # Find the path to pythonw.exe
    pythonw_path = sys.executable  # This gets the path to the current Python interpreter
    if "python.exe" in pythonw_path:
        pythonw_path = pythonw_path.replace("python.exe", "pythonw.exe")  # Use pythonw.exe to avoid a terminal window
    
    # Ensure the pythonw.exe path is properly quoted
    pythonw_path = f'"{pythonw_path}"'
    
    # Create the command to run the script
    command = f'{pythonw_path} {script_path}'
    
    # Log the command for debugging
    logger.info(f"Startup command: {command}")
    
    # Add to Windows startup via registry
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        reg_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "KeyListener", 0, winreg.REG_SZ, command)
        winreg.CloseKey(reg_key)
        logger.info("Added to startup successfully!")
        print("Added to startup successfully!")
    except WindowsError as e:
        logger.error(f"Failed to add to startup: {e}")
        print(f"Failed to add to startup: {e}")

def remove_from_startup():
    """Remove the script from Windows startup"""
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        reg_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(reg_key, "KeyListener")
        winreg.CloseKey(reg_key)
        logger.info("Removed from startup successfully!")
        print("Removed from startup successfully!")
    except WindowsError as e:
        logger.error(f"Failed to remove from startup: {e}")
        print(f"Failed to remove from startup: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--register":
            add_to_startup()
            sys.exit(0)
        elif sys.argv[1] == "--unregister":
            remove_from_startup()
            sys.exit(0)
    
    # Normal execution
    load_config()
    try:
        listener = Listener(on_press=on_press, on_release=on_release)
        logger.info("Starting keyboard listener...")
        listener.start()
        listener.join()
    except Exception as e:
        logger.error(f"Error in listener: {e}")