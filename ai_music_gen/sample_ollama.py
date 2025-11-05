# sample_ollama.py
# Generates a sample audio file using selected engine (defaults to Ollama)
# Music idea: A happy pop melody with piano and drums

import argparse
import numpy as np
from scipy.io.wavfile import write

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate sample audio using selected engine.')
parser.add_argument('--engine', type=str, default='ollama', help='Engine to use (ollama, openai_jukebox, riffusion, stable_audio)')
args = parser.parse_args()

# Engine mapping to functions
engine_functions = {
    'ollama': ('engines.ollama', 'generate_ollama_sample'),
    'openai_jukebox': ('engines.openai_jukebox', 'generate_openai_jukebox_sample'),
    'riffusion': ('engines.riffusion', 'generate_riffusion_sample'),
    'stable_audio': ('engines.stable_audio', 'generate_stable_audio_sample'),
}

if args.engine not in engine_functions:
    print(f"Unknown engine: {args.engine}. Available: {list(engine_functions.keys())}")
    exit(1)

module_name, func_name = engine_functions[args.engine]
module = __import__(module_name, fromlist=[func_name])
func = getattr(module, func_name)

# Generate music from a text prompt using selected engine
output = func(
    genre="pop",
    duration=10,
    idea="A happy pop melody with piano and drums"
)

# Save the generated audio
write(f"{args.engine}_sample.wav", output['sample_rate'], output['waveform'])
print(f"Sample audio generated: {args.engine}_sample.wav")
