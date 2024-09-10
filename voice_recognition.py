import os
import wave
import pyaudio
import json
from vosk import Model, KaldiRecognizer

# Path to your downloaded model
MODEL_PATH = "./vosk-model-small-en-us-0.15"

# Check if the model directory exists
if not os.path.exists(MODEL_PATH):
    print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as '{MODEL_PATH}'")
    exit(1)

# Load the Vosk model
model = Model(MODEL_PATH)

# Set up PyAudio to capture live audio from the microphone
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Initialize the recognizer
recognizer = KaldiRecognizer(model, 16000)

print("Listening...")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            print(f"Recognized Text: {result_dict['text']}")
        else:
            partial_result = recognizer.PartialResult()
            print(f"Partial Text: {json.loads(partial_result)['partial']}")
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
p.terminate()

print("Stopped listening.")
