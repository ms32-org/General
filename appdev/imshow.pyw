from tkinter import Tk, Canvas, NW
from PIL import Image, ImageTk
from pyautogui import screenshot
from cv2 import imread, resize, cvtColor, COLOR_BGR2RGB
from os import path
import sys
def get_path(name):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = path.abspath('.')
    return path.join(base_path, name)
# Create main window
root = Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.title("NOESCAPE.EXE")
root.iconbitmap(get_path("defender.ico"))
root.configure(bg="black")
root.update_idletasks()

# Get screen size
screen_width = root.winfo_width()
screen_height = root.winfo_height()

# Screenshot background
ss = screenshot().resize((screen_width, screen_height))
ss_img = ImageTk.PhotoImage(ss)

# Load and process foreground image
img_path = sys.argv[1]  # Replace with your actual file
if not path.exists(img_path):
    print("Image not found:", img_path)
    root.destroy()
    exit()

img = imread(img_path)
rgb = cvtColor(img, COLOR_BGR2RGB)
img_height, img_width = rgb.shape[:2]
img_aspect = img_width / img_height
screen_aspect = screen_width / screen_height

# Fit image to screen size while keeping aspect ratio
if img_aspect > screen_aspect:
    new_width = screen_width
    new_height = int(screen_width / img_aspect)
else:
    new_height = screen_height
    new_width = int(screen_height * img_aspect)

resized = resize(rgb, (new_width, new_height))
pil_img = Image.fromarray(resized)
fg_img = ImageTk.PhotoImage(pil_img)

# Create canvas
canvas = Canvas(root, width=screen_width, height=screen_height, highlightthickness=0)
canvas.pack()

# Draw screenshot (background)
canvas.create_image(0, 0, anchor=NW, image=ss_img)

# Draw foreground image centered
x_offset = (screen_width - new_width) // 2
y_offset = (screen_height - new_height) // 2
canvas.create_image(x_offset, y_offset, anchor=NW, image=fg_img)

# Prevent garbage collection
canvas.bg_ref = ss_img
canvas.fg_ref = fg_img

# Auto-close after 7.5 seconds or ESC
# root.bind("<Escape>", lambda e: root.destroy())
root.after(7500, root.destroy)
root.mainloop()
