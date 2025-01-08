from cv2 import imread,resize , cvtColor, COLOR_BGR2RGB
from PIL import Image, ImageTk
from requests import post
from os import listdir, path
from time import time
import tkinter as tk
import sys 
url = "https://ms32-sha2.onrender.com/logs"
user = "app"
root = tk.Tk()

root.title("NOESCAPE.EXE")
fp = path.join(sys._MEIPASS,"logo.png")
root.iconphoto(False,tk.PhotoImage(file=fp))
root.attributes("-fullscreen",True)
root.configure(bg="black")
root.attributes("-alpha",0.3)
root.attributes("-topmost",True)
root.update()
root.bind("<Escape>",lambda x: root.destroy())

def log(statement,state="SUCESS",terminal=False):
    try:
        statement = f"{state}   {statement}"
        post(url+"output",data={"user":user,"err":statement})
    except:
        pass
data = listdir("assets")
file_path = "assets/"+data[0] if data else None
if file_path and file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
    root.attributes("-alpha",1)
    root.update()
    canvas_height = root.winfo_height() 
    canvas_width = root.winfo_width() 
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()
    start_time = time()
    frame = imread(file_path)
    height, width = frame.shape[:2]
    aspect_ratio = width / height
    if aspect_ratio > 1:
        new_width = canvas_width
        new_height = int(canvas_width / aspect_ratio)
    else:
        new_height = canvas_height
        new_width = int(canvas_height * aspect_ratio)
    frame = resize(frame, (new_width, new_height))
    if frame is None:
        log("Invalid format of file",state="FATAL")
        raise ValueError("Invalid Format")
    rgb =  cvtColor(frame, COLOR_BGR2RGB)
    img = Image.fromarray(rgb)
    img_tk = ImageTk.PhotoImage(image=img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    # canvas.image = img_tk 
    while time() - start_time < 7.5:
        root.update()
    log("Showed Image")
    canvas.destroy() 
root.destroy()

