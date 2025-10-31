"""
Olamma in-memory server scaffold for musicgen integration.
This FastAPI app starts/stops Olamma in-memory for dev/test,
and exposes endpoints for music generation.
"""


from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import subprocess
import requests
import os

app = FastAPI(title="Olamma In-Memory MusicGen API")

# Configurable Olamma server params
OLAMMA_PORT = int(os.environ.get("OLAMMA_PORT", 11434))
OLAMMA_HOST = os.environ.get("OLAMMA_HOST", "localhost")
# Replace with actual model name
OLAMMA_MODEL = os.environ.get("OLAMMA_MODEL", "musicgen")
OLAMMA_BIN = os.environ.get("OLAMMA_BIN", "ollama")  # Path to ollama binary


class MusicGenRequest(BaseModel):
    genre: str
    duration: Optional[int] = 10
    seed: Optional[int] = None
    idea: Optional[str] = None
    vocal_artist: Optional[str] = None
    tempo: Optional[int] = 120


class MusicGenResponse(BaseModel):
    audio_url: Optional[str] = None
    error: Optional[str] = None


olamma_process = None


@app.on_event("startup")
def start_olamma():
    global olamma_process
    # Start Olamma server in-memory (subprocess)
    try:
        olamma_process = subprocess.Popen([
            OLAMMA_BIN, "serve", "--port", str(OLAMMA_PORT)
        ])
    except Exception as e:
        print("Failed to start Olamma: " + str(e))


@app.on_event("shutdown")
def stop_olamma():
    global olamma_process
    if olamma_process:
        olamma_process.terminate()
        olamma_process = None


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
    try:
        url = "http://{}:{}/api/status".format(OLAMMA_HOST, OLAMMA_PORT)
        response = requests.get(
            url,
            timeout=5
        )
        response.raise_for_status()
        return {"status": "running"}
    except Exception:
        return {"status": "not running"}
