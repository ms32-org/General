import asyncio
import aiohttp
import io
from PIL import Image
import mss
import time

async def share(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(keepalive_timeout=10)) as session:
        with mss.mss() as sct:
            frame_count = 0
            total_time = 0
            fps_start_time = time.time()

            monitor = sct.monitors[1]  # Assuming you want the primary screen (adjust if multiple monitors)
            full_screen_width = monitor['width']
            full_screen_height = monitor['height']

            while True:
                try:
                    # Start time for the frame
                    start_time = time.time()

                    # Capture the full screen
                    screenshot = sct.grab(monitor)
                    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

                    # Optional: Downscale the image if performance is an issue
                    target_width = 1280  # Target width for downscaling
                    target_height = int(target_width * full_screen_height / full_screen_width)  # Maintain aspect ratio
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)  # Use LANCZOS for downsampling

                    # Save the image to a buffer
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=30)  # Lower quality for better performance
                    buffer.seek(0)

                    # Send the screenshot
                    success = await send_screenshot(session, url, buffer)
                    if success:
                        frame_count += 1

                    # Calculate elapsed time for this frame
                    frame_time = time.time() - start_time
                    total_time += frame_time

                    # Calculate and log FPS every second
                    if time.time() - fps_start_time >= 1.0:
                        avg_fps = frame_count / (time.time() - fps_start_time)
                        print(f"FPS: {avg_fps:.2f}")
                        frame_count = 0
                        total_time = 0
                        fps_start_time = time.time()

                    # Control the frame rate based on the processing time
                    target_fps = 30  # Target FPS (you can adjust this as needed)
                    sleep_time = max(0, 1 / target_fps - frame_time)
                    await asyncio.sleep(sleep_time)

                except Exception as e:
                    print(f"Error: {e}")

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

async def main():
    url = "https://server-20zy.onrender.com/screenshot"  # Use your server URL
    await share(url)

if __name__ == "__main__":
    asyncio.run(main())
