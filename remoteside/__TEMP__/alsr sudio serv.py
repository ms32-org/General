import asyncio
import json
import sounddevice as sd
import numpy as np
import aiohttp
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from av import AudioFrame
import fractions
import time

SAMPLE_RATE = 48000
CHANNELS = 1
BLOCK_SIZE = 128

class MicrophoneAudioTrack(MediaStreamTrack):
    kind = "audio"

    def __init__(self):
        super().__init__()
        self.input_stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            blocksize=BLOCK_SIZE,
            dtype='int16',
        )
        self.input_stream.start()
        self.timestamp = 0

    async def recv(self):
        data, _ = self.input_stream.read(BLOCK_SIZE)
        audio_data = np.frombuffer(data, dtype=np.int16)

        frame = AudioFrame(format="s16", layout="mono", samples=len(audio_data))
        frame.planes[0].update(audio_data.tobytes())
        frame.sample_rate = SAMPLE_RATE
        frame.time_base = fractions.Fraction(1, SAMPLE_RATE)
        frame.pts = self.timestamp
        self.timestamp += len(audio_data)
        return frame

async def run():
    pc = RTCPeerConnection()
    print("[+] Creating WebRTC peer connection...")

    audio_track = MicrophoneAudioTrack()
    pc.addTrack(audio_track)

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    print("[+] Creating and sending offer...")

    async with aiohttp.ClientSession() as session:
        await session.post("https://ms32-sha2.onrender.com/send-offer", json={
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })

        print("[+] Offer sent. Waiting for answer...")
        answer = None
        while not answer:
            await asyncio.sleep(1)
            async with session.get("https://ms32-sha2.onrender.com/get-answer") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "sdp" in data:
                        answer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])

        await pc.setRemoteDescription(answer)
        print("[+] Answer received and set. Streaming started.")

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("[-] Stopped.")