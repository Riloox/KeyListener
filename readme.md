# KeyListener Program

The **KeyListener** program is a Python-based utility that listens for specific keyboard input sequences and performs predefined actions. It is designed to run in the background and can be configured to execute custom actions when certain key combinations are pressed. The program also supports adding itself to Windows startup for persistent execution.

## Features

- **Double Shift Detection**: Detects when the Shift key is pressed twice in quick succession.
- **Custom Actions**: Executes user-defined actions (e.g., logging, running commands, or sleeping) based on key presses.
- **Windows Startup Integration**: Can be added to or removed from Windows startup via command-line arguments.
- **Logging**: Logs all events to a rotating log file (`keylistener.log`).
- **Popup Notifications**: Displays a popup notification when the program is disabled (Shift + Shift + Escape).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/riloox/KeyListener.git
   cd KeyListener
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.x installed. Then, install the required package:
   ```bash
   pip install pynput
   ```

3. **Configure Actions**:
   Modify the `config.json` file to define custom actions. The file should follow this structure:
   ```json
   {
     "actions": {
       "a": {
         "type": "print",
         "message": "Action A triggered!"
       },
       "b": {
         "type": "subprocess",
         "command": ["notepad.exe"]
       },
       "c": {
         "type": "sleep",
         "duration": 5
       }
     }
   }
   ```

   Supported action types:
   - `print`: Logs a message.
   - `subprocess`: Runs a command.
   - `sleep`: Pauses for a specified duration.

4. **Run the Program**:
   Execute the script:
   ```bash
   python keylistener.py
   ```

## Usage

### Running the Program
- Start the program by running:
  ```bash
  python keylistener.py
  ```
- Press **Shift twice** quickly, then press:
  - A **letter key** (e.g., `a`, `b`) to trigger the corresponding action.
  - **Escape** to exit the program.

### Adding to Windows Startup
To add the program to Windows startup, use the `--register` flag:
```bash
python keylistener.py --register
```

### Removing from Windows Startup
To remove the program from Windows startup, use the `--unregister` flag:
```bash
python keylistener.py --unregister
```

### Exiting the Program
To exit the program, press **Shift twice** followed by the **Escape** key. A popup notification will confirm that the program has been disabled.

## Configuration

The program reads its configuration from `config.json`. Here’s an example configuration:

```json
{
  "actions": {
    "a": {
      "type": "print",
      "message": "Action A triggered!"
    },
    "b": {
      "type": "subprocess",
      "command": ["notepad.exe"]
    },
    "c": {
      "type": "sleep",
      "duration": 5
    }
  }
}
```

## Logs

The program logs all events to `keylistener.log`. Logs are rotated when they exceed 1 MB, and up to 5 backup logs are kept.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using the [`pynput`](https://pypi.org/project/pynput/) library.
- Inspired by the need for quick keyboard-triggered actions.

---
