from fastapi import FastAPI, Query
from pydantic import BaseModel
from musicgen import generate_music
import numpy as np
import base64

app = FastAPI()

class MusicRequest(BaseModel):
    genre: str = 'ambient'
    duration: int = 10
    seed: int | None = None

@app.post('/generate-music')
def generate_music_api(req: MusicRequest):
    waveform = generate_music(req.genre, req.duration, req.seed)
    # Encode waveform as base64 for transport (demo)
    waveform_bytes = waveform.astype(np.float32).tobytes()
    waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
    return {"waveform": waveform_b64, "sample_rate": 22050}
