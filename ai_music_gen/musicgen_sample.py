# musicgen_sample.py
# Generates a sample audio file using Ollama (default engine)

from engines.ollama import generate_ollama_sample

# Generate music from a text prompt using Ollama
output = generate_ollama_sample(
    genre="pop",
    duration=10,
    idea="A happy pop melody with piano and drums"
)

# Save the generated audio (assuming output is a dict with waveform)
import numpy as np
from scipy.io.wavfile import write

write("ollama_sample.wav", output['sample_rate'], output['waveform'])
print("Sample audio generated: ollama_sample.wav")
