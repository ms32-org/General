import pyaudio
import wave
import io
import requests

CHUNK = 1024  
FORMAT = pyaudio.paInt16  
CHANNELS = 1  
RATE = 44100  
SERVER_URL = "http://127.0.0.1:5000/audio" 

def send_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("Recording and sending audio as WAV... Press Ctrl+C to stop.")
    
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

            # Send the WAV data to the server
            wav_buffer.seek(0)
            response = requests.post(SERVER_URL, data=wav_buffer.read(), headers={"Content-Type": "audio/wav"})
            wav_buffer.close()
            if response.status_code != 200:
                print(f"Failed to send audio: {response.status_code}, {response.text}")
            else:
                print("done")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

# Run the function
send_audio()