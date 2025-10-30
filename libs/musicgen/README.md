# musicgen

Basic AI-powered music generation library for True North Audio.

## Features
- `generate_music(genre, duration, seed)`: Generates a dummy music waveform (sine wave + noise) for prototyping.
- Extensible for real ML models (Magenta, PyTorch, etc.)

## Usage
```python
from musicgen import generate_music
waveform = generate_music(genre='ambient', duration=10)
```

## Roadmap
- Integrate real music generation models
- Add genre/style controls
- Export to audio file formats
- REST API integration
