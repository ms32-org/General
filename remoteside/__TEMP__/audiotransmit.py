import asyncio
import websockets
import mss
from PIL import Image
import io
from mouse import move, click, wheel, double_click
from keyboard import send
import json
from time import sleep
from pyautogui import size, mouseDown, mouseUp
import time

width, height = size()

async def handle_message(data):
    try:
        data = json.loads(data)
        print("[INPUT]", data)
        if data["type"] == "click":
            x = data["x"] * (width / data["width"])
            y = data["y"] * (height / data["height"])
            move(x, y)
            if data["button"] == 0:
                click()
            elif data["button"] == 1:
                click(button="middle")
            elif data["button"] == 2:
                click(button="right")

        elif data["type"] == "key" and data["button"]:
            btns = [chr(k) if isinstance(k, int) else k for k in data["button"]]
            keys = "+".join(btns)
            send(keys.lower())

        elif data["type"] == "scroll":
            wheel(delta=-(data["deltaY"]))

        elif data["type"] == "dbclick":
            x = data["x"] * (width / data["width"])
            y = data["y"] * (height / data["height"])
            move(x, y)
            double_click()

        elif data["type"] == "drag":
            x1 = data["x1"] * (width / data["width"])
            y1 = data["y1"] * (height / data["height"])
            x2 = data["x2"] * (width / data["width"])
            y2 = data["y2"] * (height / data["height"])
            move(x1, y1)
            sleep(0.01)
            mouseDown()
            sleep(0.01)
            move(x2, y2)
            sleep(0.01)
            mouseUp()

    except Exception as e:
        print(f"[INPUT ERROR] {e}")

async def receive_messages(websocket):
    async for message in websocket:
        await handle_message(message)

async def send_screen(websocket):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        frame_count = 0
        start_time = time.time()

        while True:
            frame_start = time.time()
            img = sct.grab(monitor)
            img_pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            img_pil = img_pil.resize((960, 540),Image.BOX) 

            buf = io.BytesIO()
            img_pil.save(buf, format='JPEG', quality=50,optimize=True)
            jpeg_bytes = buf.getvalue()

            try:
                await websocket.send(jpeg_bytes) 
            except Exception as e:
                print(f"[SEND ERROR] {e}")
                break

            frame_count += 1
            elapsed = time.time() - start_time
            if elapsed >= 1.0:
                print(f"[FPS] {frame_count} fps")
                frame_count = 0
                start_time = time.time()

            await asyncio.sleep(max(0, 0.05 - (time.time() - frame_start)))


async def main():
    uri = "wss://screenshare-server.onrender.com"
    try:
        async with websockets.connect(uri, max_size=None) as websocket:

            await websocket.send("sender")
            print("[INFO] Connected to server as sender")

            await asyncio.gather(
                send_screen(websocket),
                receive_messages(websocket)
            )

    except Exception as e:
        print(f"[ERROR] {e}")

asyncio.run(main())