from flask import Flask, Response, render_template
import io
import wave
import time

app = Flask(__name__)

# Sample audio data for testing (replace this with your actual audio data source)
audio_data = b""  # Replace with actual audio data (e.g., a WAV file in memory)

@app.route('/')
def index():
    # Serve the HTML for audio playback
    return render_template("alsraudio.html")

@app.route('/stream')
def stream_audio_live():
    if not audio_data:
        return "No audio available to stream.", 400
    
    def generate_audio():
        # This function will yield audio chunks continuously
        wav_buffer = io.BytesIO(audio_data)
        with wave.open(wav_buffer, 'rb') as wf:
            while True:
                chunk = wf.readframes(1024)
                if not chunk:
                    break
                yield chunk
    
    return Response(generate_audio(), content_type="audio/wav", status=200)

if __name__ == '__main__':
    app.run(debug=True)
