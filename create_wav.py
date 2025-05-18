import math
import wave

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

fs = 16000  # Sample rate
channels = 1  # Mono
seconds = 10  # Duration of recording
filename = "output_16kHz_mono.wav"

print("Recording...")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=channels, dtype=np.int16)
sd.wait()  # Wait until recording is finished
write(filename, fs, recording)  # Save as WAV file in 16-bit format
print(f"Saved as {filename}")