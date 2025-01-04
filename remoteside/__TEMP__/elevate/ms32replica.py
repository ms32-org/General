import tkinter as tk
from threading import Thread
import keyboard
import time

blocking_active = True
root = None

def block_touch(event):
    global blocking_active
    if not blocking_active:
        return None
    return "break"

def create_overlay():
    global root
    global blocking_active
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.2)
    root.attributes("-topmost", True)

    root.bind("<ButtonPress>", block_touch)
    root.bind("<ButtonRelease>", block_touch)
    root.bind("<Motion>", block_touch)
    while blocking_active:
        root.update()
    root.quit() 
    root.destroy()
    root = None

def remote_controls():
    global blocking_active
    while True:
        Thread(target=create_overlay).start()
        keyboard.wait('ctrl+shift+up')
        print("unlocking")
        blocking_active = False

        time.sleep(3)

        blocking_active = True
        print("lock")
if __name__ == "__main__":
    remote_controls()
