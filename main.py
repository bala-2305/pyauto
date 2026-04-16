import mcp.server.fastmcp as fastmcp
import pyautogui
from PIL import ImageGrab
import os
import tempfile
import time
import base64
import io
import subprocess
import psutil
import pygetwindow as gw

# Initialize FastMCP server
mcp_server = fastmcp.FastMCP("PyAutoControl")

@mcp_server.tool()
def get_active_window_info() -> str:
    """
    Retrieve the title and process name of the window currently in focus.
    """
    try:
        window = gw.getActiveWindow()
        if window:
            return f"Active Window: {window.title} (Location: {window.topleft})"
        return "No active window found."
    except Exception as e:
        return f"Error retrieving window info: {str(e)}"

@mcp_server.tool()
def kill_process(process_name: str) -> str:
    """
    Force-close a specific process by its name (e.g., 'notepad.exe').
    """
    try:
        count = 0
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == process_name:
                proc.kill()
                count += 1
        if count > 0:
            return f"Successfully killed {count} instance(s) of {process_name}."
        return f"Process {process_name} not found."
    except Exception as e:
        return f"Error killing process: {str(e)}"

@mcp_server.tool()
def get_system_health() -> str:
    """
    Get CPU usage, memory usage, and battery status.
    """
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        
        health = f"CPU Usage: {cpu}% | Memory Usage: {mem}%"
        if battery:
            health += f" | Battery: {battery.percent}% ({'Charging' if battery.power_plugged else 'Discharging'})"
        
        return health
    except Exception as e:
        return f"Error retrieving system health: {str(e)}"

@mcp_server.tool()
def launch_application(app_name_or_path: str) -> str:
    """
    Launch an application by its name (if in PATH) or absolute file path.
    Example: 'notepad', 'calc', or 'C:/Program Files/Inkscape/bin/inkscape.exe'
    """
    try:
        # Using subprocess.Popen allows the app to run independently of the MCP server
        subprocess.Popen(app_name_or_path, shell=True)
        return f"Successfully initiated launch for: {app_name_or_path}"
    except Exception as e:
        return f"Error launching application: {str(e)}"

@mcp_server.tool()
def get_screen_size() -> str:
    """Get the primary monitor resolution."""
    width, height = pyautogui.size()
    return f"Screen size: {width}x{height}"

@mcp_server.tool()
def mouse_click(x: int, y: int, button: str = "left") -> str:
    """Click at specific coordinates."""
    pyautogui.click(x, y, button=button)
    return f"Clicked {button} at ({x}, {y})"

@mcp_server.tool()
def click_element(image_path: str, confidence: float = 0.8) -> str:
    """
    Search for an element on screen using an image template and click it.
    The image_path should be a path to a small template image of the element.
    """
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.click(location)
            return f"Successfully clicked element found at {location}"
        else:
            return f"Could not find element on screen matching {image_path}"
    except Exception as e:
        return f"Error clicking element: {str(e)}"

@mcp_server.tool()
def type_text(text: str, interval: float = 0.1) -> str:
    """Type text at current focus."""
    pyautogui.typewrite(text, interval=interval)
    return f"Typed: {text}"

@mcp_server.tool()
def take_screenshot() -> str:
    """
    Capture the current screen and return it as a base64 PNG data URI.
    USE THIS FIRST to see the screen state and identify coordinates or elements.
    """
    try:
        screenshot = ImageGrab.grab()
        
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"

@mcp_server.tool()
def list_directory(path: str = ".") -> str:
    """List files and directories in a given path."""
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@mcp_server.tool()
def read_file_content(path: str) -> str:
    """Read the text content of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp_server.tool()
def write_to_file(path: str, content: str) -> str:
    """Write text content to a file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp_server.tool()
def move_mouse(x: int, y: int, duration: float = 0.5) -> str:
    """Move mouse to coordinates."""
    pyautogui.moveTo(x, y, duration=duration)
    return f"Moved mouse to ({x}, {y})"

if __name__ == "__main__":
    mcp_server.run()

