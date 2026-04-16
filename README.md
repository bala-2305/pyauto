# PyAutoControl MCP Server

A Model Context Protocol (MCP) server that provides autonomous GUI automation capabilities to LLM clients (like Claude Desktop). This tool allows an AI to interact directly with your computer's screen, mouse, and keyboard.

## Features

- **Screen Resolution**: Retrieve primary monitor dimensions.
- **Mouse Control**: Perform clicks and precise cursor movements.
- **Keyboard Automation**: Type text and hotkeys into active windows.
- **Screen Capture**: Take and save screenshots for visual context.

## Setup Instructions

### 1. Environment Requirements
- Python 3.12 or higher
- Windows (recommended for PyAutoGUI compatibility)

### 2. Installation
The project uses a virtual environment and `pyproject.toml` for dependency management.

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
pip install mcp[cli] pyautogui opencv-python pillow
```

### 3. Claude Desktop Configuration
To use this with Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "PyAutoControl": {
      "command": "d:/pyauto/.venv/Scripts/python.exe",
      "args": ["D:/pyauto/main.py"]
    }
  }
}
```

## Available Tools

- `get_screen_size`: Returns the width and height of the primary monitor.
- `mouse_click(x, y, button)`: Clicks the specified mouse button at the given coordinates.
- `type_text(text, interval)`: Types a string of text with a configurable delay between keystrokes.
- `take_screenshot(filename)`: Captures the current screen and saves it as a file.
- `move_mouse(x, y, duration)`: Moves the cursor to a specific location over a set duration.

## Security Warning
**Giving an LLM control over your mouse and keyboard is powerful but risky.** Only run this server with prompts you trust, and never leave the automation unattended while active.
