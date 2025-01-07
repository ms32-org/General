import pyaudio
import wave
import io
import asyncio
import ssl
from aiohttp import ClientSession

CHUNK = 1024*5  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)
SERVER_URL = "https://ms32-sha2.onrender.com/audio"  # POST endpoint

async def send_audio():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False  # Disable SSL certificate verification
    ssl_context.verify_mode = ssl.CERT_NONE
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording and sending audio via POST request... Press Ctrl+C to stop.")

    async with ClientSession() as session:
        try:
            while True:
                frames = []

                # Record audio for ~0.23 seconds (10 chunks)
                for _ in range(10):
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)

                # Create a WAV file in memory
                wav_buffer = io.BytesIO()
                with wave.open(wav_buffer, 'wb') as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(audio.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))

                # Send the WAV data to the server via POST request
                wav_buffer.seek(0)
                headers = {'Content-Type': 'audio/wav'}  # Set appropriate content type for audio data

                async with session.post(SERVER_URL, data=wav_buffer.read(), ssl=ssl_context, headers=headers) as response:
                    if response.status == 200:
                        print("Audio chunk sent successfully.")
                    else:
                        print(f"Failed to send audio chunk. Status code: {response.status}")

                wav_buffer.close()

                # Introduce a small delay to prevent overwhelming the server
                await asyncio.sleep(0.05)  # 50 ms delay between chunks

        except KeyboardInterrupt:
            print("Stopping...")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

# Run the function
asyncio.run(send_audio())
