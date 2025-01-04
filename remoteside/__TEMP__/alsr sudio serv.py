from flask import Flask, request
import pyaudio
import wave
import io
import threading

app = Flask(__name__)

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Set up PyAudio for playback
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# Buffer to store incoming audio chunks
audio_buffer = []
buffer_lock = threading.Lock()

@app.route('/audio', methods=['POST'])
def stream_audio():
    try:
        # Get the WAV audio data from the client
        audio_data = request.data
        
        # Create a BytesIO buffer from the received WAV data
        wav_buffer = io.BytesIO(audio_data)
        
        # Open the WAV data with wave module to read it
        with wave.open(wav_buffer, 'rb') as wf:
            # Verify the format of the audio (channels, rate, etc.)
            if wf.getnchannels() != CHANNELS or wf.getframerate() != RATE:
                return "Invalid audio format", 400

            # Read frames from the WAV file and add to the buffer
            frames = wf.readframes(wf.getnframes())
            with buffer_lock:
                audio_buffer.append(frames)
        
        return "Audio received", 200
    except Exception as e:
        print(f"Error receiving audio: {e}")
        return "Error", 500

def audio_playback():
    global audio_buffer
    while True:
        if audio_buffer:
            with buffer_lock:
                # Get the next audio chunk
                chunk = audio_buffer.pop(0)
            # Play the audio chunk
            stream.write(chunk)

# Start the audio playback in a separate thread
playback_thread = threading.Thread(target=audio_playback, daemon=True)
playback_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
