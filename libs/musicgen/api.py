
from fastapi import FastAPI, Query
from pydantic import BaseModel
from libs.musicgen.core import generate_music
import numpy as np
import base64
import sys

app = FastAPI()

print("[FastAPI] Initialization: Starting musicgen API server (serve:all script)", file=sys.stderr)

class MusicRequest(BaseModel):
    genre: str = 'ambient'
    duration: int = 10
    seed: int | None = None
    idea: str | None = None


@app.post('/api/musicgen/generate')
def generate_music_api(req: MusicRequest):
    """
    Generate music using Magenta and return waveform and vocal transcription as base64 and text.
    """
    print(f"[FastAPI] Received request: genre={req.genre}, duration={req.duration}, seed={req.seed}, idea={req.idea}", file=sys.stderr)
    result = generate_music(req.genre, req.duration, req.seed, req.idea)
    waveform_bytes = result['waveform'].astype(np.float32).tobytes()
    waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
    print(f"[FastAPI] Returning waveform, sample_rate={result['sample_rate']}, vocals={result['vocals']}", file=sys.stderr)
    return {
        "waveform": waveform_b64,
        "sample_rate": result['sample_rate'],
        "vocals": result['vocals']
    }


# Start FastAPI server if run as a script
if __name__ == "__main__":
    import uvicorn
    import sys
    print("[FastAPI] Launching Uvicorn server on port 8000...", file=sys.stderr)
    uvicorn.run("libs.musicgen.api:app", host="0.0.0.0", port=8000, reload=False)
