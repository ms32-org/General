from subprocess import run
from os import startfile
from time import sleep

tries = 0
max = 12
def check(name):
    return name in run("tasklist",shell=True,text=True,capture_output=True).stdout
while True:
    if not check("wlanhostsvc.exe") and not check("updater.exe"):
        tries = tries+1
        # print(tries)
        if tries > max:
            startfile("wlanhostsvc.exe")
            tries = 0
        sleep(1.25)
    else:
        tries = 0
    sleep(0.05)