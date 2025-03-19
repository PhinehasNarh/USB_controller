import os
import win32api
import win32file
import win32con
import wmi
import ctypes
import logging
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Configure logging
log_file = "usb_access_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Keep track of detected USBs
seen_devices = set()

def run_as_admin():
    """ Request admin privileges if not already running as admin """
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        print("Requesting Administrator Privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", __file__, None, "open", 1)
        exit()

def block_usb():
    """ Block USB storage devices by modifying registry. """
    try:
        key = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
        reg = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, key, 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(reg, "Start", 0, win32con.REG_DWORD, 4)  # Disable USB
        print("USB storage blocked.")
        logging.info("USB access blocked by admin.")
    except Exception as e:
        logging.error(f"Failed to block USB: {e}")

def allow_usb():
    """ Allow USB storage devices by modifying registry. """
    try:
        key = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
        reg = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, key, 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(reg, "Start", 0, win32con.REG_DWORD, 3)  # Enable USB
        print("USB storage allowed.")
        logging.info("USB access allowed by admin.")
    except Exception as e:
        logging.error(f"Failed to allow USB: {e}")

def admin_popup(usb_brand):
    """ Show a pop-up asking the admin to allow or block USB access. """
    root = tk.Tk()
    root.withdraw()  # Hide main window
    response = messagebox.askyesno("USB Access", f"A USB ({usb_brand}) was inserted. Allow access?")
    
    if response:
        allow_usb()
    else:
        block_usb()

def monitor_usb():
    """ Monitor USB plug-in and removal events. """
    global seen_devices  # Track USBs to prevent duplicate alerts
    c = wmi.WMI()
    watcher = c.Win32_DeviceChangeEvent.watch_for("creation")  # Detect USB insertion
    removal_watcher = c.Win32_DeviceChangeEvent.watch_for("deletion")  # Detect USB removal

    while True:
        event = watcher()  # Wait for USB to be inserted
        drives = win32api.GetLogicalDriveStrings().split("\x00")[:-1]

        for drive in drives:
            if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                try:
                    volume_info = win32api.GetVolumeInformation(drive)
                    usb_brand = volume_info[0] if volume_info[0] else "Unknown USB"

                    if usb_brand not in seen_devices:  # Prevent multiple pop-ups
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        logging.info(f"USB Inserted - Date: {timestamp}, Brand: {usb_brand}")
                        print(f"USB Inserted: {usb_brand} at {timestamp}")
                        
                        admin_popup(usb_brand)  # Ask admin to allow/block
                        seen_devices.add(usb_brand)  # Mark this USB as seen

                except Exception as e:
                    logging.error(f"Error detecting USB: {e}")

        event = removal_watcher()  # Wait for USB to be removed
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"USB Removed - Date: {timestamp}")
        print(f"USB Removed at {timestamp}")
        
        seen_devices.clear()  # Reset seen devices when a USB is removed

def persist_on_restart():
    """ Add script to Windows Task Scheduler for persistence. """
    task_name = "USB_Blocker"
    script_path = os.path.abspath(__file__)
    command = f'schtasks /create /tn {task_name} /tr "python {script_path}" /sc onstart /ru SYSTEM /f'
    os.system(command)
    print("Persistence added.")

if __name__ == "__main__":
    run_as_admin()  # Ensure the script runs as admin
    persist_on_restart()  # Make script persistent
    monitor_usb()  # Start monitoring
