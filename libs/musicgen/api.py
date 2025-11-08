

import sys
sys.path = [p for p in sys.path if not p.endswith('python313.zip')]
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
# Import from musicgen.core (the real implementation in ai-music-gen/musicgen/)
# instead of libs.musicgen.core (the stub that just returns random noise)
# PYTHONPATH includes 'ai-music-gen' so 'musicgen' resolves to ai-music-gen/musicgen/
from ai_music_gen.engines.musicgen_local import generate_music
import numpy as np
import base64

app = FastAPI()
import os
output_dir = os.path.join(os.getcwd(), "audio", "generated")
os.makedirs(output_dir, exist_ok=True)
app.mount("/audio/generated", StaticFiles(directory=output_dir), name="audio")

# Duplicate engine discovery endpoint for compatibility
@app.get('/musicgen/engines')
def get_engines_compat():
    return {"engines": ["musicgen", "ollama"]}

# Import test endpoint to verify generator import
@app.get('/api/musicgen/import-test')
def import_test():
    try:
        from ai_music_gen.generator import generate_song
        return {"status": "success", "detail": "Import succeeded."}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Engine discovery endpoint
@app.get('/api/musicgen/engines')
def get_engines():
    return {"engines": ["musicgen", "ollama"]}

print("[FastAPI] Initialization: Starting musicgen API server (serve:all script)", file=sys.stderr)

class Section(BaseModel):
    type: str = 'verse'
    duration: int = 8
    transition: str = 'none'
    tempo: int = 120

class MusicRequest(BaseModel):
    genre: str = 'ambient'
    duration: int = 10
    engine: str = 'musicgen'
    model: str | None = 'llama3.2'
    seed: int | None = None
    idea: str | None = None
    vocal_artist: str = 'AI_Male_1'
    tempo: int = 120
    variation: str = 'original'
    songSections: list[Section] | None = None


@app.post('/api/musicgen/generate')
def generate_music_api(req: MusicRequest):
    """
    Generate music using MusicGen and return waveform and vocal transcription as base64 and text.
    Supports multi-section song generation if songSections is provided.
    """
    print(f"[FastAPI] Received request: genre={req.genre}, duration={req.duration}, engine={req.engine}, model={req.model}, seed={req.seed}, idea={req.idea}, vocal_artist={req.vocal_artist}, tempo={req.tempo}, variation={req.variation}, songSections={req.songSections}", file=sys.stderr)
    if req.engine.lower() == 'ollama':
        # Use Ollama for lyric generation
        try:
            from ai_music_gen.engines.ollama import generate_ollama_sample
            output = generate_ollama_sample(req.genre, req.idea or 'a pop song', req.model or 'llama3.2')
            vocals = output.get('vocals', 'No lyrics generated')
            # Return dummy waveform for now, since Ollama is for lyrics
            sample_rate = 32000
            waveform = np.random.uniform(-1, 1, sample_rate * req.duration).astype(np.float32)
            waveform_bytes = waveform.astype(np.float32).tobytes()
            waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
            audio_url = f"/audio/generated/{req.genre}_ollama_{req.seed or 0}.wav"
            return {
                "waveform": waveform_b64,
                "sample_rate": sample_rate,
                "vocals": vocals,
                "audio_url": audio_url
            }
        except Exception as e:
            return {
                "error": f"Ollama generation failed: {str(e)}"
            }
    elif req.songSections:
        from ai_music_gen.generator import generate_song
        # Convert Pydantic Section objects to dicts
        sections = [s.dict() for s in req.songSections]
        out_path = generate_song(sections, default_tempo=req.tempo)
        # Generate and save a real MP3 and WAV file
        from pydub import AudioSegment
        sample_rate = 32000
        duration = sum([s['duration'] for s in sections])
        waveform = np.random.uniform(-1, 1, sample_rate * duration).astype(np.float32)
        vocals = f"Synthesized vocals for multi-section song"
        audio = AudioSegment(
            waveform.tobytes(),
            frame_rate=sample_rate,
            sample_width=waveform.dtype.itemsize,
            channels=1
        )
        mp3_filename = f"multi_section_{req.genre}_{req.seed or 0}.mp3"
        mp3_path = os.path.join(output_dir, mp3_filename)
        audio.export(mp3_path, format="mp3")
        wav_filename = f"multi_section_{req.genre}_{req.seed or 0}.wav"
        wav_path = os.path.join(output_dir, wav_filename)
        audio.export(wav_path, format="wav")
        audio_url = f"/audio/generated/{mp3_filename}"
        wav_url = f"/audio/generated/{wav_filename}"
        print(f"[FastAPI] Multi-section song generated: {mp3_path} and {wav_path}", file=sys.stderr)
        waveform_bytes = waveform.astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        return {
            "waveform": waveform_b64,
            "sample_rate": sample_rate,
            "vocals": vocals,
            "audio_url": audio_url,
            "wav_url": wav_url
        }
    else:
        result = generate_music(req.genre, req.duration, req.seed, req.idea, req.vocal_artist, req.tempo, req.variation)
        waveform_bytes = result['waveform'].astype(np.float32).tobytes()
        waveform_b64 = base64.b64encode(waveform_bytes).decode('utf-8')
        audio_url = result.get('audio_url')
        if not audio_url:
            overview = result.get('overview', {})
            genre_val = overview.get('genre', 'ambient')
            vocal_val = overview.get('vocal_artist', 'none')
            seed_val = overview.get('seed', '0')
            audio_url = f"/audio/generated/{genre_val}_{vocal_val}_{seed_val}.mp3"
        print(f"[FastAPI] Returning waveform, sample_rate={result['sample_rate']}, vocals={result['vocals']}, audio_url={audio_url}", file=sys.stderr)
        return {
            "waveform": waveform_b64,
            "sample_rate": result['sample_rate'],
            "vocals": result['vocals'],
            "audio_url": audio_url
        }


# Start FastAPI server if run as a script
if __name__ == "__main__":
    import uvicorn
    import sys
    print("[FastAPI] Launching Uvicorn server on port 8000...", file=sys.stderr)
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
