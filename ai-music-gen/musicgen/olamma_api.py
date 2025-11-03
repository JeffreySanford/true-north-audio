"""
Olamma in-memory server scaffold for musicgen integration.
This FastAPI app provides a lightweight Ollama-compatible API for dev/test and
proxies requests to our FastAPI backend. It does NOT start the real `ollama serve`
process to avoid conflicts with its own Uvicorn server.
"""


from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import subprocess
import requests
import os

app = FastAPI(title="Olamma In-Memory MusicGen API")

# Configurable params (kept for compatibility)
OLAMMA_PORT = int(os.environ.get("OLAMMA_PORT", 11434))
OLAMMA_HOST = os.environ.get("OLAMMA_HOST", "localhost")
OLAMMA_MODEL = os.environ.get("OLAMMA_MODEL", "musicgen")
OLAMMA_BIN = os.environ.get("OLAMMA_BIN", "ollama")  # Not used here


class MusicGenRequest(BaseModel):
    genre: str
    duration: Optional[int] = 10
    engine: str
    model: Optional[str] = "llama3.2"
    seed: Optional[int] = None
    idea: Optional[str] = None
    vocal_artist: Optional[str] = None
    tempo: Optional[int] = 120


class MusicGenResponse(BaseModel):
    audio_url: Optional[str] = None
    error: Optional[str] = None


"""
Note: We intentionally do NOT spawn `ollama serve` from this proxy. The proxy
itself binds to port 11434 via Uvicorn; launching the real Ollama on the same port
would lead to a port collision and can stall the overall start script.
"""


@app.post("/musicgen", response_model=MusicGenResponse)
def generate_music(request: MusicGenRequest):
    """
    Proxy request to FastAPI backend for music generation.
    """
    try:
        response = requests.post(
            "http://localhost:8000/api/musicgen/generate",
            json={
                "genre": request.genre,
                "duration": request.duration,
                "engine": request.engine,
                "model": request.model,
                "seed": request.seed,
                "idea": request.idea,
                "vocal_artist": request.vocal_artist,
                "tempo": request.tempo
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        # Return audio_url or error from backend
        return MusicGenResponse(
            audio_url=data.get("audio_url"),
            error=data.get("error")
        )
    except Exception as e:
        # F541 fix: no f-string, use concatenation
        err_msg = "MusicGen request failed: " + str(e)
        if len(err_msg) > 79:
            err_msg = err_msg[:76] + "..."
        return MusicGenResponse(error=err_msg)


@app.get("/olamma/status")
def olamma_status():
    """
    Check if Olamma server is running.
    """
    # Since this is a proxy, consider it "running" if this service is up
    return {"status": "running"}


if __name__ == "__main__":
    import uvicorn
    print("[Ollama Proxy] Starting on port 11434...")
    uvicorn.run(app, host="0.0.0.0", port=11434)
