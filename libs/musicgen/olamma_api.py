"""
Olamma in-memory server scaffold for musicgen integration.
This FastAPI app starts/stops Olamma in-memory for dev/test, and exposes endpoints for music generation.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import subprocess
import requests
import os

app = FastAPI(title="Olamma In-Memory MusicGen API")

# Configurable Olamma server params
OLAMMA_PORT = int(os.environ.get("OLAMMA_PORT", 11434))
OLAMMA_HOST = os.environ.get("OLAMMA_HOST", "localhost")
OLAMMA_MODEL = os.environ.get("OLAMMA_MODEL", "musicgen")  # Replace with actual model name
OLAMMA_BIN = os.environ.get("OLAMMA_BIN", "ollama")  # Path to ollama binary

class MusicGenRequest(BaseModel):
    prompt: str
    seed: Optional[int] = None
    tempo: Optional[int] = None

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
        print(f"Failed to start Olamma: {e}")

@app.on_event("shutdown")
def stop_olamma():
    global olamma_process
    if olamma_process:
        olamma_process.terminate()
        olamma_process = None

@app.post("/musicgen", response_model=MusicGenResponse)
def generate_music(request: MusicGenRequest):
    """
    Proxy request to Olamma server for music generation.
    """
    try:
        # Example: POST to Olamma REST API (replace with actual endpoint/model)
        response = requests.post(
            f"http://{OLAMMA_HOST}:{OLAMMA_PORT}/api/generate",
            json={
                "model": OLAMMA_MODEL,
                "prompt": request.prompt,
                "seed": request.seed,
                "tempo": request.tempo
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        # Assume Olamma returns audio_url or similar
        return MusicGenResponse(audio_url=data.get("audio_url"))
    except Exception as e:
        return MusicGenResponse(error=str(e))

@app.get("/olamma/status")
def olamma_status():
    """
    Check if Olamma server is running.
    """
    try:
        response = requests.get(f"http://{OLAMMA_HOST}:{OLAMMA_PORT}/api/status", timeout=5)
        response.raise_for_status()
        return {"status": "running"}
    except Exception:
        return {"status": "not running"}
