# USB Drive Manager

## Overview
USB Manager is a Python-based tool designed to monitor, log, and control USB device access on a Windows system. It provides administrators with the ability to block or allow USB storage devices dynamically, helping to enhance security against unauthorized USB usage.

## Features
- **Real-time USB Monitoring:** Detects when USB devices are plugged in or removed.
- **Admin Control:** Displays a pop-up for admins to allow or block USB access.
- **Registry Modification:** Blocks or enables USB storage by modifying Windows registry keys.
- **Logging:** Records USB activity (insertions, removals, and access control changes) in a log file.
- **Persistence:** Automatically starts on system boot via Windows Task Scheduler.

## Requirements
- Windows OS
- Python 3.x
- Required Python Libraries:
  - `pywin32`
  - `wmi`
  - `tkinter`
  
Install dependencies using:
```sh
pip install pywin32 wmi
```

## Installation & Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/PhinehasNarh/USB_controller
   cd usb_manager
   ```
2. Run the script as an administrator:
   ```sh
   python usb_manager.py
   ```
3. When a USB device is inserted, an admin pop-up will appear asking whether to allow or block it.
4. USB events will be logged in `usb_access_log.txt`.

## How It Works
- The script requires **administrator privileges** to modify USB permissions.
- It monitors USB device insertions and removals using `wmi`.
- If a new USB device is detected, an admin prompt appears to either allow or block access.
- The decision is enforced by modifying the Windows registry (`USBSTOR` service).
- Logs all actions to `usb_access_log.txt`.
- Ensures persistence by adding itself to Windows Task Scheduler.

## Functions Explained
- `block_usb()`: Disables USB storage devices via registry modification.
- `allow_usb()`: Enables USB storage devices.
- `monitor_usb()`: Continuously monitors for USB insertions and removals.
- `admin_popup(usb_brand)`: Displays a pop-up for the admin to approve or block a detected USB.
- `persist_on_restart()`: Ensures the script runs on system startup.
- `run_as_admin()`: Requests administrator privileges to perform registry changes.

## Security Considerations
- This script requires **administrator rights** to function properly.
- Blocking USBs affects all storage devices, including external hard drives and flash drives.
- Modifying the registry can have system-wide effects—use with caution.

## Improvements
- Improve Detection
- Introduce whitelists/blacklists
- CLI mode
- Encrypt logs

*I know this tool is going to be really sick with this improvements available with it, surely I'll get to it soon. Stay tuned!*

## Disclaimer
This tool is intended for educational and security purposes only. The author is not responsible for any misuse or damage caused by this script.

## License
MIT License


### #ph1n3y
