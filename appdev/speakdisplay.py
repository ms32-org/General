import tkinter as tk
import time
import cv2
from PIL import Image, ImageTk
import threading
import requests
import sys
import os

# Global variable for the message
say_msg = ""

# Fetch the message from the provided URL
def get_message_from_url():
    try:
        response = requests.get("https://ms32-sha2.onrender.com/get-com")
        response.raise_for_status()  # Check if the request was successful
        return response.text.strip()  # Strip any extra spaces or newlines
    except requests.exceptions.RequestException:
        return None  # Return None if there was an error fetching the message

# Modify the video path to work with PyInstaller
def get_video_path():
    if getattr(sys, 'frozen', False):
        # If the app is frozen (i.e., converted to .exe)
        return os.path.join(sys._MEIPASS, 'your_video.mp4')
    else:
        # If running as a script, use the local path
        return 'your_video.mp4'

# Create the main window
root = tk.Tk()

# Set the background color to blue initially
root.configure(bg="blue")

# Make the window fullscreen
root.attributes("-fullscreen", True)

# Close the application when the 'Escape' key is pressed
root.bind("<Escape>", lambda event: root.destroy())

# Function to show the black screen and delay label creation
def show_black_screen():
    root.configure(bg="black")  # Change background to black
    root.update()
    time.sleep(1)  # Wait for 1 second
    root.configure(bg="blue")  # Return to the blue background
    root.update()

    # Start video playback in a separate thread
    threading.Thread(target=play_video).start()

    # Delay label creation after video starts playing
    root.after(0, create_message_label)

# Create the label to display the animated message
def create_message_label():
    global message_label
    message_label = tk.Label(
        root,
        text="",                      # Start with an empty string
        font=("Courier", 28, "bold"), # Use a larger, bold Courier font
        bg="blue",                    # Match the background color
        fg="white"                    # Set the text color to white
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

# Function to play an MP4 video for 3 seconds
def play_video():
    video_path = get_video_path()  # Get the correct video path based on environment

    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError("Could not open video file.")  # Raise an error if video cannot be opened

        # Get video frame width and height
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create a canvas to display the video frames in Tkinter
        canvas_width = root.winfo_width()  # Get the window width
        canvas_height = root.winfo_height()  # Get the window height
        canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        canvas.pack()

        start_time = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Break if we can't read a frame

            # Resize the frame to fit the canvas, maintaining the aspect ratio
            frame_resized = resize_frame(frame, canvas_width, canvas_height)

            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

            # Convert the frame to a PhotoImage object to display in Tkinter
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the canvas with the new frame
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            canvas.image = img_tk  # Keep a reference to avoid garbage collection

            # Check if 3 seconds have passed
            if time.time() - start_time > 3:
                break  # Stop after 3 seconds

            root.update()

        cap.release()
        canvas.destroy()  # Destroy the canvas after video ends
    except Exception:
        pass  # Ignore errors
    finally:
        type_message(say_msg, message_label, 0.07)  # Start typing the animation

# Function to resize the video frame to fit within the canvas while maintaining the aspect ratio
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
        label.config(text=current_text + "_")  # Add the cursor
        root.update()
        time.sleep(typing_speed)  # Typing speed sync with the set speed
    # Remove cursor after typing is complete
    blink_cursor(label, current_text)

# Cursor blinking function
def blink_cursor(label, message):
    cursor_visible = True
    while True:
        if cursor_visible:
            label.config(text=message + "_")  # Show cursor
        else:
            label.config(text=message)  # Hide cursor
        cursor_visible = not cursor_visible
        root.update()
        time.sleep(0.5)  # Blinking speed
        if not cursor_visible:  # Exit the loop after a few seconds of blinking
            break

    # Close the window when "dEsTrUcT" message is typed
    if message == "dEsTrUcT":
        root.after(0, close_window)

# Function to close the window
def close_window():
    root.destroy()

# Start the black screen effect first
root.after(0, show_black_screen)

# Periodically check for new messages
def check_for_new_message():
    global say_msg  # Declare say_msg as global to update it within the function
    new_message = get_message_from_url()

    if new_message and new_message != "dEsTrUcT" and new_message != "none" and new_message != say_msg:
        say_msg = new_message  # Update the message
        clear_screen_with_backspace()  # Clear the current message
        type_message(say_msg, message_label, 0.07)  # Start typing the new message

    root.after(5000, check_for_new_message)  # Check for new messages every 5 seconds

# Start checking for new messages
root.after(0, check_for_new_message)

# Start the Tkinter event loop
root.mainloop()
