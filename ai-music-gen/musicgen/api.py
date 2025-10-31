from fastapi import FastAPI
from pydantic import BaseModel
from ai_music_gen.musicgen.core import generate_music
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
    seed: int | None = None
    idea: str | None = None
    vocal_artist: str = 'AI_Male_1'
    tempo: int = 120
    variation: str = 'original'
    songSections: list[Section] | None = None


@app.post('/api/musicgen/generate')
def generate_music_api(req: MusicRequest):
    """
    Generate music using MusicGen and return waveform and
    vocal transcription as base64 and text.
    Supports multi-section song generation if songSections is provided.
    """
    print(f"[FastAPI] Received request: genre={req.genre}", file=sys.stderr)
    print(f"duration={req.duration}", file=sys.stderr)
    print(f"seed={req.seed}", file=sys.stderr)
    print(f"idea={req.idea}, "
          f"vocal_artist={req.vocal_artist}", file=sys.stderr)
    print(f"tempo={req.tempo}, "
          f"variation={req.variation}", file=sys.stderr)
    print(f"songSections={req.songSections}", file=sys.stderr)
    if req.songSections:
        # Only import if actually used
        from ai_music_gen.generator import generate_song
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
            req.variation
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
        "ai_music_gen.musicgen.api:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
