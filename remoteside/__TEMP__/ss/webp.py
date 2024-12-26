import asyncio
import aiohttp
import io
from PIL import Image
import mss
import time

# Async function to send the screenshot
async def send_screenshot(session, url, buffer):
    retries = 3
    for attempt in range(retries):
        try:
            async with session.post(url, data=buffer.getvalue(), timeout=5) as response:
                if response.status == 200:
                    return True
                else:
                    print(f"Attempt {attempt + 1}: Server responded with {response.status}")
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error: {e}")
        await asyncio.sleep(2 ** attempt)  # Exponential backoff for retries
    return False

# Async function to capture and send screen frames
async def capture_screen(session, url):
    # Initialize mss for screen capture
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        frame_count = 0
        fps_start_time = time.time()

        while True:
            start_time = time.time()

            # Capture a specific portion of the screen (e.g., reduce resolution)
            monitor = {"top": 0, "left": 0, "width": 1280, "height": 720}  # Capture a portion of the screen
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            # Optionally reduce the image size (adjust based on your needs)
            img = img.resize((640, 360), Image.Resampling.LANCZOS)  # Resize to lower resolution for faster upload

            # Save image to buffer with JPEG (try different formats)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=30)  # JPEG for better speed vs WebP

            # Send the screenshot asynchronously
            success = await send_screenshot(session, url, buffer)
            if success:
                frame_count += 1

            # Calculate FPS
            if time.time() - fps_start_time >= 1.0:
                avg_fps = frame_count / (time.time() - fps_start_time)
                print(f"FPS: {avg_fps:.2f}")
                frame_count = 0
                fps_start_time = time.time()

            # Calculate time spent processing the frame
            frame_time = time.time() - start_time
            target_fps = 30  # Target FPS (adjust for your needs)
            sleep_time = max(0, (1 / target_fps) - frame_time)

            # Sleep for the remaining time to maintain target FPS
            await asyncio.sleep(sleep_time)  # Non-blocking sleep

# Main async function to run everything
async def main():
    url = "https://server-20zy.onrender.com/screenshot"  # Use your server URL
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(keepalive_timeout=10)) as session:
        await capture_screen(session, url)

# Run the main function inside asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())  # Start the asyncio event loop
