import asyncio
import numpy as np
import mss
import aiohttp
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, RTCIceCandidate
from aiortc import RTCConfiguration, RTCIceServer
from av import VideoFrame
import json
import time
import fractions
from mouse import move, click, wheel, double_click
from keyboard import send
from time import sleep
from pyautogui import size, mouseDown, mouseUp
import datetime
import requests

width, height = size()
url = "https://ms32-sha2.onrender.com"
# url = "http://192.168.29.154:5000"

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {msg}")

class ScreenShareTrack(VideoStreamTrack):
    kind = "video"

    def __init__(self):
        super().__init__()
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

    async def recv(self):
        await asyncio.sleep(1 / 30)
        img = np.array(self.sct.grab(self.monitor))
        frame = VideoFrame.from_ndarray(img[..., :3], format="bgr24")
        frame.pts = int(time.time() * 90000)
        frame.time_base = fractions.Fraction(1, 90000)
        return frame

async def run():
    response = requests.get("https://ms32-org.metered.live/api/v1/turn/credentials?apiKey=63c45333b770b8e79c79e77c970b3e79a7af")
    data = response.json()
    ice_server_list = data
    rtc_ice_servers = [RTCIceServer(**server) for server in ice_server_list]
    rtc_ice_servers.append(RTCIceServer(urls="stun:stun.l.google.com:19302"))
    config = RTCConfiguration(iceServers=rtc_ice_servers)

    pc = RTCPeerConnection(configuration=config)
    data_channel = pc.createDataChannel("control")

    @pc.on("iceconnectionstatechange")
    def on_ice_state_change():
        log(f"[ICE] State changed: {pc.iceConnectionState}")

    @pc.on("icecandidate")
    def on_ice_candidate(candidate):
        if candidate:
            requests.post(f"{url}/send-candidate", json=candidate.to_dict())

    @data_channel.on("open")
    def on_open():
        log("[*] Data channel opened")

    @data_channel.on("message")
    def on_message(data):
        log(f"[+] Message received: {data}")
        data = json.loads(data)
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
            btns = []
            for key in data["button"]:
                btns.append(chr(key)) if type(key) == int else btns.append(key)
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

    # Add screen track
    screen_track = ScreenShareTrack()
    pc.addTrack(screen_track)

    # Create and send offer
    log("Creating offer...")
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    log("Offer created and local description set.")

    async with aiohttp.ClientSession() as session:
        log("Sending offer to server...")
        await session.post(f"{url}/send-offer", json={
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })
        log("Offer sent. Waiting for answer...")

        # Wait for answer
        while True:
            try:
                async with session.get(f"{url}/get-answer") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        log("Answer received.")
                        break
            except Exception:
                pass
            await asyncio.sleep(0.3)

        await pc.setRemoteDescription(RTCSessionDescription(
            sdp=data["sdp"],
            type=data["type"]
        ))
        log("Remote description set. Connection should establish soon.")
        async def fetch_remote_candidates():
            log("Fetching remote ICE candidates...")
            while True:
                try:
                    async with session.get(f"{url}/get-candidates") as res:
                        if res.status == 200:
                            candidates = await res.json()
                            for c in candidates:
                                log(f"[Candidate] {c}")
                                try:
                                    # Extract only the required keys
                                    candidate_string = c.get('candidate')
                                    sdp_mid = c.get('sdpMid')
                                    sdp_m_line_index = c.get('sdpMLineIndex')

                                    # Ensure all required keys are present
                                    if candidate_string and sdp_mid is not None and sdp_m_line_index is not None:
                                        # Create and add the RTCIceCandidate
                                        candidate = RTCIceCandidate(
                                            candidate=candidate_string,
                                            sdpMid=sdp_mid,
                                            sdpMLineIndex=sdp_m_line_index
                                        )
                                        try:
                                            await pc.addIceCandidate(candidate)
                                        except Exception as e:
                                            log(f"[ICE] Failed to add candidate: {e}")
                                        log("[+] Candidate added.")
                                    else:
                                        log("[!] Incomplete candidate data received.")
                                except Exception as e:
                                    log(f"[!] Error adding candidate: {e}")
                except Exception as e:
                    log(f"[!] Error fetching candidates: {e}")
                await asyncio.sleep(1)
        asyncio.create_task(fetch_remote_candidates())

        log("Screen streaming with data channel active...")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
