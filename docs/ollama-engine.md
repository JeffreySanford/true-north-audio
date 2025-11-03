# Ollama Engine Integration

## Overview
Ollama is the default engine for music generation in True North Audio. It is designed for exclusive local AI music generation and can be extended to use your own models or APIs.

## Usage
- The UI defaults to Ollama for music generation.
- Backend requests with engine='Ollama (Exclusive AI)' are routed to `musicgen/engines/ollama.py`.
- The sample script `ai-music-gen/ollama_song_sample.py` demonstrates generating a full song (e.g., modern hiphop version of "The Best Is Yet To Come" by Dean Martin).

## Implementation
- The engine function `generate_ollama_sample` can be customized to call your local Ollama model or API.
- Example stub uses Python's `subprocess` to demonstrate how to invoke a local model.
- Update the command and parsing logic to match your actual Ollama setup.

## Example Script
```python
from musicgen.engines.ollama import generate_ollama_sample

if __name__ == "__main__":
    genre = "hiphop"
    duration = 180
    idea = "Modern hiphop version of 'The Best Is Yet To Come' by Dean Martin"
    vocal_artist = "AI_Male_1"
    tempo = 90
    variation = "remix"
    songSections = [
        {"type": "intro", "duration": 16, "transition": "fade"},
        {"type": "verse", "duration": 32, "transition": "drum_fill"},
        {"type": "chorus", "duration": 32, "transition": "cut"},
        {"type": "bridge", "duration": 16, "transition": "fade"},
        {"type": "outro", "duration": 16, "transition": "fade"}
    ]
    result = generate_ollama_sample(
        genre=genre,
        duration=duration,
        idea=idea,
        vocal_artist=vocal_artist,
        tempo=tempo,
        variation=variation,
        songSections=songSections
    )
    print("Ollama Song Sample Result:")
    print(f"Sample Rate: {result['sample_rate']}")
    print(f"Waveform (first 32): {result['waveform'][:32]}")
    print(f"Vocals: {result['vocals']}")
    print(f"Audio URL: {result['audio_url']}")
```

## Extending Ollama
- Replace the stub logic with your real model or API call.
- Ensure the output matches the expected format for the frontend and backend.
- Document any customizations for future portability.
