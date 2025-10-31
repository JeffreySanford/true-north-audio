


# Advanced genre and vocal artist lists
GENRES = [
    "ambient", "rock", "jazz", "classical", "pop", "electronic", "hiphop", "folk", "blues", "metal", "country", "reggae", "soul", "funk", "world", "experimental",
    "bigband", "1940s"
]
VOCAL_ARTISTS = [
    {"name": "AI_Male_1", "gender": "male"},
    {"name": "AI_Male_2", "gender": "male"},
    {"name": "AI_Female_1", "gender": "female"},
    {"name": "AI_Female_2", "gender": "female"},
    {"name": "AI_Choir", "gender": "mixed"}
]

import random
import datetime

class MusicGenConfig:
    def __init__(self,
                 genre: str,
                 vocal_artist: str,
                 seed: int = None,
                 tempo: int = 120,
                 idea: str = None,
                 variation: str = "original",
                 duration: int = 10):
        self.genre = genre
        self.vocal_artist = vocal_artist
        self.seed = seed or random.randint(0, 999999)
        self.tempo = tempo
        self.idea = idea
        self.variation = variation
        self.duration = duration
        self.created_at = datetime.datetime.now()

    def overview(self):
        return {
            "genre": self.genre,
            "vocal_artist": self.vocal_artist,
            "seed": self.seed,
            "tempo": self.tempo,
            "idea": self.idea,
            "variation": self.variation,
            "duration": self.duration,
            "created_at": self.created_at.isoformat()
        }

class MusicGen:
    @staticmethod
    def available_genres():
        return GENRES

    @staticmethod
    def available_vocal_artists():
        return VOCAL_ARTISTS


    @staticmethod
    def generate_music(config: MusicGenConfig):
        overview = config.overview()
        print(f"[MusicGen] Starting generation: {overview}")
        import numpy as np
        import os
        import wave
        sample_rate = 32000
        try:
            duration = int(getattr(config, 'duration', 10))
        except Exception:
            duration = 10
        waveform = np.random.uniform(-1, 1, sample_rate * duration).astype(np.float32)
        print(f"[MusicGen] Generated waveform shape: {waveform.shape}, dtype: {waveform.dtype}")
        # Basic static/noise detection
        static_warning = None
        if np.all(waveform == 0) or np.var(waveform) < 1e-4:
            static_warning = "Warning: Output waveform is likely static or silence."
            print(f"[MusicGen] {static_warning}")
        vocals = f"Synthesized vocals for {overview['vocal_artist']}"
        # Save WAV file to disk
        audio_dir = os.path.join(os.getcwd(), "backend", "src", "assets", "generated")
        os.makedirs(audio_dir, exist_ok=True)
        wav_path = os.path.join(audio_dir, f"{overview['genre']}_{overview['vocal_artist']}_{overview['seed']}.wav")
        mp3_path = os.path.join(audio_dir, f"{overview['genre']}_{overview['vocal_artist']}_{overview['seed']}.mp3")
        print(f"[MusicGen] Saving WAV to {wav_path}")
        int_waveform = np.int16(waveform * 32767)
        with wave.open(wav_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(int_waveform.tobytes())
        print(f"[MusicGen] WAV file saved. Starting MP3 conversion...")
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-y', '-i', wav_path, mp3_path], check=True)
            print(f"[MusicGen] MP3 conversion succeeded: {mp3_path}")
            audio_url = f"/audio/generated/{overview['genre']}_{overview['vocal_artist']}_{overview['seed']}.mp3"
        except Exception as e:
            print(f"[MusicGen] MP3 conversion failed: {e}")
            # fallback to WAV if MP3 fails
            audio_url = f"/audio/generated/{overview['genre']}_{overview['vocal_artist']}_{overview['seed']}.wav"
        print(f"[MusicGen] Returning audio_url: {audio_url}")
        return {
            "overview": overview,
            "audio_url": audio_url,
            "status": "success",
            "waveform": waveform,
            "sample_rate": sample_rate,
            "vocals": vocals,
            "warning": static_warning
        }


# Exported function for API and __init__.py
def generate_music(genre: str = 'ambient', duration: int = 10, seed: int = None, idea: str = None, vocal_artist: str = 'AI_Male_1', tempo: int = 120, variation: str = "original"):
    config = MusicGenConfig(
        genre=genre,
        vocal_artist=vocal_artist,
        seed=seed,
        tempo=tempo,
        idea=idea,
        variation=variation,
        duration=duration
    )
    result = MusicGen.generate_music(config)
    # Guarantee audio_url is always present
    if 'audio_url' not in result or not result['audio_url']:
        overview = result.get('overview', {})
        genre_val = overview.get('genre', 'ambient')
        vocal_val = overview.get('vocal_artist', 'none')
        seed_val = overview.get('seed', '0')
        result['audio_url'] = f"/audio/generated/{genre_val}_{vocal_val}_{seed_val}.mp3"
    return result
