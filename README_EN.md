# Port Monitor

## Project Overview
Port Monitor is a tool for monitoring the status of local ports. It periodically checks whether specified ports are available and notifies the user via a notification window when the port status changes.

## Features
- Periodically checks port status (default every 2 seconds).
- Supports asynchronous port detection for high performance.
- Displays a notification window when port status changes.
- Allows specifying ports to monitor via the `config.json` configuration file.

## Usage

### 1. Configuration File
Ensure the `config.json` file exists in the project directory with the following format:
```json
{
  "ports": {
    "Service A": "5000",
    "Service B": "5011",
    "Service C": "5012"
  }
}
```
- Keys represent service names, and values represent corresponding port numbers.

### 2. Running the Program
#### Direct Execution
Run the script using Python:
```bash
python port_monitor.py
```

#### Packaging as an Executable
Use the following command to package the program into a single executable file:
```bash
pyinstaller --onefile --noconsole --add-data "config.json;." port_monitor.py
```
- The `--noconsole` flag ensures the program runs in the background without displaying a console window.
- The `--add-data` flag ensures the configuration file is included in the same directory as the executable.

### 3. Running the Executable
Double-click the generated `.exe` file to run the program.

## Notes
- Ensure the `config.json` file is in the same directory as the executable.
- During runtime, the program will display a notification window in the bottom-right corner of the screen. Clicking the notification window will close it.

## Dependencies
- Python 3.7 or higher
- Required Python libraries:
  - `asyncio`
  - `tkinter`
  - `socket`

## Contributions
Feel free to submit issues and feature requests!

[中文版](./README.md)
