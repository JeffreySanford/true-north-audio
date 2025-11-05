import os
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write

# Lyrics for each section
VOCALS = {
    "vocal_verse_1.wav": "Woke up this morning, feeling low and blue. The sun ain't shining, and I can't find my shoes.",
    "vocal_chorus_1.wav": "Liberty blues, rolling through my soul. Singing my story, letting the good times roll.",
    "vocal_verse_2.wav": "Walking down the alley, shadows on the wall. Dreaming of freedom, waiting for your call.",
    "vocal_chorus_2.wav": "Liberty blues, rolling through my soul. Singing my story, letting the good times roll.",
    "vocal_bridge.wav": "Oh, the night is cold, but my heart stays warm. With every note I sing, I weather the storm.",
    "vocal_final_chorus.wav": "Liberty blues, rolling through my soul. Singing my story, letting the good times roll.",
    "vocal_outro.wav": "Fade into the moonlight, my blues drifting away. Tomorrow brings hope, at the break of day."
}

# Bark voice preset for female, bluesy, vintage style
VOICE_PROMPT = "female_singer, blues, 1940s, vintage, expressive"

preload_models()

output_dir = os.path.join(os.path.dirname(__file__), '..', 'backend', 'src', 'assets', 'generated')
os.makedirs(output_dir, exist_ok=True)

for filename, lyrics in VOCALS.items():
    print(f"Generating {filename}...")
    audio_array = generate_audio(lyrics)
    out_path = os.path.join(output_dir, filename)
    write(out_path, SAMPLE_RATE, audio_array)
    print(f"✅ Saved: {out_path}")

print("\nAll vocals generated! You can now rerun the mixing script.")
