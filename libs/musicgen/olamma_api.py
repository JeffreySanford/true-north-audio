"""
Olamma in-memory server scaffold for musicgen integration.
This FastAPI app exposes a lightweight Ollama-compatible API surface for dev/test
and proxies requests to our FastAPI backend for actual work. It does NOT start the
real `ollama serve` process to avoid port conflicts with the proxy itself.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import subprocess
import requests
import os

app = FastAPI(title="Olamma In-Memory MusicGen API")

# Configurable proxy params (kept for compatibility)
OLAMMA_PORT = int(os.environ.get("OLAMMA_PORT", 11434))
OLAMMA_HOST = os.environ.get("OLAMMA_HOST", "localhost")
OLAMMA_MODEL = os.environ.get("OLAMMA_MODEL", "musicgen")  # Placeholder default
OLAMMA_BIN = os.environ.get("OLAMMA_BIN", "ollama")  # Unused here; do not auto-start real Ollama

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

"""
Note: We intentionally do NOT start `ollama serve` here. This module is the
proxy service that binds to port 11434 via Uvicorn. Spawning the real Ollama
on the same port would immediately conflict and can prevent the frontend from
ever starting in the combined serve script.
"""

@app.post("/musicgen", response_model=MusicGenResponse)
def generate_music(request: MusicGenRequest):
    """
    Proxy request to FastAPI backend for music generation.
    """
    try:
        response = requests.post(
            f"http://localhost:8000/api/musicgen/generate",
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
        return MusicGenResponse(audio_url=data.get("audio_url"), error=data.get("error"))
    except Exception as e:
        return MusicGenResponse(error=str(e))

@app.get("/api/tags")
def get_models():
    """
    Return available Ollama models for the frontend selector.
    """
    # Return some common models that might be available
    return {
        "models": [
            {"name": "llama3.2", "size": "2.0 GB", "digest": "llama3.2"},
            {"name": "llama3.1", "size": "4.7 GB", "digest": "llama3.1"},
            {"name": "codellama", "size": "3.8 GB", "digest": "codellama"}
        ]
    }

@app.get("/api/status")
def get_status():
    """
    Return Ollama server status.
    """
    # This proxy itself is considered the "Ollama" for dev purposes
    return {"status": "running"}

# Back-compat endpoint used by validate scripts
@app.get("/olamma/status")
def get_status_compat():
    return {"status": "running"}
