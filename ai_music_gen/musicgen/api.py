from fastapi import FastAPI
from pydantic import BaseModel
from .core import generate_music
from .engines.stable_audio import generate_stable_audio_sample
from .engines.riffusion import generate_riffusion_sample
from .engines.openai_jukebox import generate_openai_jukebox_sample
from .engines.ollama import generate_ollama_sample
import numpy as np
import base64
import sys

app = FastAPI()

@app.get('/api/musicgen/import-test')
def import_test():
    return {"status": "success", "detail": "Import succeeded."}

print(
    "[FastAPI] Initialization: Starting musicgen API server "
    "(serve:all script)",
    file=sys.stderr
)

class Section(BaseModel):
    type: str = 'verse'
    duration: int = 8
    transition: str = 'none'
    tempo: int = 120

class MusicRequest(BaseModel):
    genre: str = 'ambient'
    duration: int = 10
    engine: str = 'MusicGen (Audiocraft)'
    seed: int | None = None
    idea: str | None = None
    vocal_artist: str = 'AI_Male_1'
    tempo: int = 120
    variation: str = 'original'
    songSections: list[Section] | None = None
    lyrics: str | None = None
    vocal_style: str = 'spoken'


@app.post('/api/musicgen/generate')
def generate_music_api(req: MusicRequest):
    """
    Generate music using MusicGen, Jukebox, Stable Audio, Riffusion, Ollama, or other engines and return waveform and vocal transcription as base64 and text.
    Supports multi-section song generation if songSections is provided.
    """
    print(f"[FastAPI] Received request: genre={req.genre}", file=sys.stderr)
    print(f"engine={req.engine}", file=sys.stderr)
    engine = req.engine.lower() if req.engine else ''
    if 'jukebox' in engine:
        from ..jukebox.jukebox.generate_sample import generate_jukebox_sample
        result = generate_jukebox_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/jukebox_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif 'stable audio' in engine:
        result = generate_stable_audio_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/stable_audio_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif 'riffusion' in engine:
        result = generate_riffusion_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/riffusion_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif 'openai jukebox' in engine:
        result = generate_openai_jukebox_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/openai_jukebox_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif 'ollama' in engine:
        result = generate_ollama_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/ollama_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif req.songSections:
        from ..generator import generate_song
        sections = [s.dict() for s in req.songSections]
        out_path = generate_song(sections, default_tempo=req.tempo)
        sample_rate = 32000
        duration = sum([s['duration'] for s in sections])
        waveform = np.random.uniform(-1, 1, sample_rate * duration)
        waveform = waveform.astype(np.float32)
        vocals = "Synthesized vocals for multi-section song"
        audio_url = out_path if out_path else ""
        if not audio_url:
            audio_url = "/audio/generated/unknown_multi_section.mp3"
        print(
            f"[FastAPI] Multi-section song generated: {out_path}",
            file=sys.stderr
        )
        waveform_bytes = waveform.astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        return {
            "waveform": waveform_b64,
            "sample_rate": sample_rate,
            "vocals": vocals,
            "audio_url": audio_url
        }
    else:
        result = generate_music(
            req.genre,
            req.duration,
            req.seed,
            req.idea,
            req.vocal_artist,
            req.tempo,
            req.variation,
            req.lyrics,
            req.vocal_style
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url')
        if not audio_url:
            overview = result.get('overview', {})
            genre_val = overview.get('genre', 'ambient')
            vocal_val = overview.get('vocal_artist', 'none')
            seed_val = overview.get('seed', '0')
            audio_url = (
                f"/audio/generated/{genre_val}_"
                f"{vocal_val}_"
                f"{seed_val}.mp3"
            )
        print(
            f"[FastAPI] Returning waveform, sample_rate="
            f"{result['sample_rate']}, vocals={result['vocals']}, "
            f"audio_url={audio_url}",
            file=sys.stderr
        )
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }


@app.get('/musicgen/engines')
def get_engines():
    # TODO: Replace with actual engine detection logic
    return {
        "audiocraft": True,
        "bark": True,
        "midi": True,
        "ollama": True,  # Add ollama status here if needed
        "recommended": "audiocraft"
    }



# Ollama models endpoint (mock implementation)
@app.get('/ollama/models')
def get_ollama_models():
    # TODO: Replace with actual Ollama model detection logic
    return {
        "models": [
            {"name": "llama2", "installed": True},
            {"name": "mistral", "installed": True},
            {"name": "phi3", "installed": False}
        ]
    }


# Start FastAPI server if run as a script
if __name__ == "__main__":
    import uvicorn
    print(
        "[FastAPI] Launching Uvicorn server on port 8000...",
        file=sys.stderr
    )
    uvicorn.run(
        "musicgen.api:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
from fastapi import FastAPI
from pydantic import BaseModel
from .core import generate_music
from .engines.stable_audio import generate_stable_audio_sample
from .engines.riffusion import generate_riffusion_sample
from .engines.openai_jukebox import generate_openai_jukebox_sample
from .engines.ollama import generate_ollama_sample
import numpy as np
import base64
import sys

app = FastAPI()


@app.get('/api/musicgen/import-test')
def import_test():
    return {"status": "success", "detail": "Import succeeded."}


print(
    "[FastAPI] Initialization: Starting musicgen API server "
    "(serve:all script)",
    file=sys.stderr
)


class Section(BaseModel):
    type: str = 'verse'
    duration: int = 8
    transition: str = 'none'
    tempo: int = 120


class MusicRequest(BaseModel):
    genre: str = 'ambient'
    duration: int = 10
    engine: str = 'MusicGen (Audiocraft)'
    seed: int | None = None
    idea: str | None = None
    vocal_artist: str = 'AI_Male_1'
    tempo: int = 120
    variation: str = 'original'
    songSections: list[Section] | None = None
    lyrics: str | None = None
    vocal_style: str = 'spoken'


@app.post('/api/musicgen/generate')
def generate_music_api(req: MusicRequest):
    """
    Generate music using MusicGen or Jukebox and return waveform and
    vocal transcription as base64 and text.
    Supports multi-section song generation if songSections is provided.
    """
    print(f"[FastAPI] Received request: genre={req.genre}", file=sys.stderr)
    print(f"engine={req.engine}", file=sys.stderr)
    engine = req.engine.lower() if req.engine else ''
    if 'jukebox' in engine:
        # Use Jukebox backend
        from ..jukebox.jukebox.generate_sample import generate_jukebox_sample
        result = generate_jukebox_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/jukebox_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif 'stable audio' in engine:
        result = generate_stable_audio_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/stable_audio_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif 'riffusion' in engine:
        result = generate_riffusion_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/riffusion_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif 'openai jukebox' in engine:
        result = generate_openai_jukebox_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/openai_jukebox_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif 'ollama' in engine:
        result = generate_ollama_sample(
            genre=req.genre,
            duration=req.duration,
            seed=req.seed,
            idea=req.idea,
            vocal_artist=req.vocal_artist,
            tempo=req.tempo,
            variation=req.variation,
            songSections=req.songSections
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url', '/audio/generated/ollama_sample.mp3')
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }
    elif req.songSections:
        # Only import if actually used
        from ..generator import generate_song
        sections = [s.dict() for s in req.songSections]
        out_path = generate_song(sections, default_tempo=req.tempo)
        sample_rate = 32000
        duration = sum([s['duration'] for s in sections])
        waveform = np.random.uniform(-1, 1, sample_rate * duration)
        waveform = waveform.astype(np.float32)
        vocals = "Synthesized vocals for multi-section song"
        audio_url = out_path if out_path else ""
        if not audio_url:
            audio_url = "/audio/generated/unknown_multi_section.mp3"
        print(
            f"[FastAPI] Multi-section song generated: {out_path}",
            file=sys.stderr
        )
        waveform_bytes = waveform.astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        return {
            "waveform": waveform_b64,
            "sample_rate": sample_rate,
            "vocals": vocals,
            "audio_url": audio_url
        }
    else:
        result = generate_music(
            req.genre,
            req.duration,
            req.seed,
            req.idea,
            req.vocal_artist,
            req.tempo,
            req.variation,
            req.lyrics,
            req.vocal_style
        )
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url')
        if not audio_url:
            overview = result.get('overview', {})
            genre_val = overview.get('genre', 'ambient')
            vocal_val = overview.get('vocal_artist', 'none')
            seed_val = overview.get('seed', '0')
            audio_url = (
                f"/audio/generated/{genre_val}_"
                f"{vocal_val}_"
                f"{seed_val}.mp3"
            )
        print(
            f"[FastAPI] Returning waveform, sample_rate="
            f"{result['sample_rate']}, vocals={result['vocals']}, "
            f"audio_url={audio_url}",
            file=sys.stderr
        )
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }


# Start FastAPI server if run as a script
if __name__ == "__main__":
    import uvicorn
    print(
        "[FastAPI] Launching Uvicorn server on port 8000...",
        file=sys.stderr
    )
    uvicorn.run(
        "musicgen.api:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
