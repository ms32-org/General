import tkinter as tk
from time import sleep
import pyttsx3
from threading import Thread



engine = pyttsx3.init()
rate = engine.getProperty('rate')
rate -= 40 
engine.setProperty("rate", rate)
engine.setProperty("volume", 1)

root = tk.Tk()

root.configure(bg="blue")

root.attributes("-fullscreen", True)

root.bind("<Escape>", lambda event: root.destroy())

say_msg = "Hello, this is your message with a typing animation!"

message_label = tk.Label(
    root,
    text="",                      
    font=("Courier", 28, "bold"), 
    bg="blue",                    
    fg="white"                    
)
message_label.pack(expand=True)

def speak_and_type(message, rate):

    engine.say(message)
    engine.runAndWait()

def type_message(message, label, typing_speed):
    current_text = ""
    for char in message:
        current_text += char
        label.config(text=current_text + "_")
        root.update()
        sleep(typing_speed) 
    blink_cursor(label, current_text)

def blink_cursor(label, message):
    cursor_visible = True
    while True:
        if cursor_visible:
            label.config(text=message + "_") 
        else:
            label.config(text=message)
        cursor_visible = not cursor_visible
        root.update()
        sleep(0.5) 
        if not cursor_visible:  
            break

    root.after(5000, close_window)

def close_window():
    root.destroy()

Thread(target=speak_and_type, args=(say_msg, rate)).start()

typing_speed = 0.05 * (150 / rate)  
Thread(target=type_message,args=(say_msg, message_label, typing_speed)).start()
root.mainloop()
