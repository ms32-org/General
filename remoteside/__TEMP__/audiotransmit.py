import pyaudio
import wave
import io
import asyncio
import websockets
import ssl

CHUNK = 2048  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)
SERVER_URL = "wss://server-20zy.onrender.com/"  # WebSocket server URL

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

    print("Recording and sending audio via WebSocket... Press Ctrl+C to stop.")
    
    # Connect to WebSocket server
    async with websockets.connect(SERVER_URL,ssl=ssl_context) as websocket:
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

                # Send the WAV data to the WebSocket server
                wav_buffer.seek(0)
                await websocket.send(wav_buffer.read())  # Send audio data as binary
                
                wav_buffer.close()
                print("Audio chunk sent.")
                
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
