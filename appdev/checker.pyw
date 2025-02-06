from subprocess import check_output
from os import startfile
from time import sleep
tries = 0
max = 5
while True:
    if "ms32.exe" not in check_output("tasklist").decode("utf-8"):
        sleep(1)
        tries = tries+1
        print(tries)
        if tries == max:break
        continue
    continue
startfile("ms32.exe")