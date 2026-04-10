# Auto Clicker

A cross-platform graphical auto-clicker built with Python, `tkinter`, and `pynput`. It supports customizable click intervals, mouse button selection, and keyboard modifiers (Shift, Ctrl, Alt/Option).

## Features

- **Customizable Delay**: Set the clicking interval in seconds (e.g., `0.001` for high speed).
- **Mouse Button Selection**: Choose between Left, Right, and Middle mouse buttons.
- **Keyboard Modifiers**: Combine clicks with Shift, Ctrl, or Alt (Option on macOS).
- **Custom Hotkey**: Set a custom key to start and stop the clicking process.
- **Always on Top**: The UI stays visible over other windows for easy access.
- **Responsive UI**: The window is resizable, and the text scales automatically.
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.

## Prerequisites

- **Python 3.x**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/).
- **pip**: Python's package installer, which usually comes with Python.

## Installation

1. **Clone the repository** (or download the source code):
   ```bash
   git clone https://github.com/your-username/AutoClicker.git
   cd AutoClicker
   ```

2. **Install the required dependencies**:
   ```bash
   pip install pynput
   ```

## Running the Application

To start the auto-clicker, run the following command in your terminal/command prompt:

```bash
python main.py
```

## Platform-Specific Setup

### Windows
No additional setup is usually required, provided Python and `pynput` are installed.

### macOS
- **Accessibility Permissions**: macOS requires explicit permission for applications to control the mouse and keyboard. 
- When you first run the script or toggle the clicker, you may be prompted to grant permissions. 
- Go to `System Settings > Privacy & Security > Accessibility` and ensure your Terminal (or IDE) is enabled.

### Linux
- **X11 vs. Wayland**: `pynput` works best on X11. If you are using Wayland, you might encounter issues.
- **Permissions**: You might need to add your user to the `input` group or run the script with root privileges to access `/dev/uinput` for keyboard/mouse simulation.
- **Tkinter**: On some Linux distributions, you may need to install `python3-tk` separately:
  ```bash
  sudo apt-get install python3-tk
  ```

## How to Use

1. **Configure Settings**:
   - Enter the desired **Delay** in seconds.
   - Select the **Mouse Button** to be clicked.
   - (Optional) Choose a **Modifier Key** (e.g., Shift + Click).
   - Enter a single character for the **Start/Stop Key** (default is `s`).
2. **Apply Settings**: Click the **Apply Settings** button to save your configuration.
3. **Toggle Clicker**: Press the configured hotkey (e.g., `s`) to start or stop clicking.
4. **Exit**: Press `e` on your keyboard or close the window to exit the application.

## Warning

Use this tool responsibly. Rapid clicking can cause unintended actions in games or applications. Avoid using it in competitive environments where it might violate terms of service.
