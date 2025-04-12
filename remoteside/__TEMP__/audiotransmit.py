import asyncio
import json
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, AudioStreamTrack
import sounddevice as sd
import numpy as np
import requests

# WebRTC Peer Connection to handle the communication
class AudioSenderStream(AudioStreamTrack):
    def __init__(self, pcm_stream):
        super().__init__()
        self.pcm_stream = pcm_stream  # Audio stream from microphone

    async def recv(self):
        # Generate audio frame and return it for sending via WebRTC
        pcm_data = next(self.pcm_stream)
        return pcm_data  # Send audio frame

# Function to capture microphone audio and return audio data
def audio_stream():
    # Setup for microphone capture using sounddevice
    samplerate = 16000
    channels = 1
    blocksize = 1024

    # A generator to stream microphone data in blocks
    def generate_pcm_data():
        with sd.InputStream(samplerate=samplerate, channels=channels, blocksize=blocksize) as stream:
            while True:
                # Read the microphone input and return it in WebRTC-compatible format
                pcm_data, overflowed = stream.read(blocksize)
                yield pcm_data

    return generate_pcm_data()

# Create WebRTC offer and send it to the server
async def send_offer_to_server():
    # Create the RTC connection and offer
    pc = RTCPeerConnection()
    pc.on('iceconnectionstatechange', lambda: print(f'ICE connection state: {pc.iceConnectionState}'))
    pc.on('track', lambda track: print(f"Track: {track.kind}"))

    # Set up the audio stream
    audio_stream_track = AudioSenderStream(audio_stream())
    pc.addTrack(audio_stream_track)

    # Create the offer
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)

    # Send offer to the server
    offer_data = {
        'sdp': offer.sdp,
        'type': offer.type
    }
    response = requests.post('https://ms32-sha2.onrender.com/offer', json=offer_data)
    answer = response.json()

    # Set remote description (answer from server)
    await pc.setRemoteDescription(RTCSessionDescription(sdp=answer['sdp'], type=answer['type']))

    print("Offer sent, answer received, connection established.")

    # Keep the connection alive
    await asyncio.sleep(3600)  # Keep running for 1 hour (for testing purposes)


# Run the offer creation and sending in an asyncio event loop
asyncio.run(send_offer_to_server())