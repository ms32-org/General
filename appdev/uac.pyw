import ctypes
import sys
import winreg as reg

def disable_uac():
    try:
        # Path to UAC registry key
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        uac_keys = {
            "EnableLUA": 0,  # Disables UAC
            "ConsentPromptBehaviorAdmin": 0,  # No prompt for admin
            "ConsentPromptBehaviorUser": 0,  # No prompt for standard users
        }

        # Open the registry key for modification
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key_path, 0, reg.KEY_SET_VALUE) as key:
            for name, value in uac_keys.items():
                reg.SetValueEx(key, name, 0, reg.REG_DWORD, value)
                print(f"{name} set to {value}")
        
        print("UAC has been disabled. You may need to restart your system for the changes to take effect.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if is_admin():
        disable_uac()
    else:
        # Relaunch the script with administrative privileges
        print("Requesting administrative privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )