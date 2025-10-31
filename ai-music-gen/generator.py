
import mido
import time
import io
from .resources import check_resources


def generate_melody(length=16, tempo=120):
    """
    Generate a simple MIDI melody and return the file path.
    Warn if resources are low. Log generation time.
    """
    check_resources(min_ram_gb=2, min_cpu_ghz=2)
    start = time.time()
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    for i in range(length):
        note = 60 + (i % 12)
        track.append(mido.Message('note_on', note=note, velocity=64, time=120))
        track.append(mido.Message(
            'note_off', note=note, velocity=64, time=120))
    out_path = f"melody_{int(start)}.mid"
    mid.save(out_path)
    elapsed = time.time() - start
    print(f"Melody generated in {elapsed:.2f} seconds. Saved to {out_path}.")
    return out_path


def call_ollama_musicgen(genre, section_type, duration, prompt, tempo):
    import requests
    payload = {
        "genre": genre,
        "section_type": section_type,
        "duration": duration,
        "prompt": prompt,
        "tempo": tempo
    }
    response = requests.post(
        "http://localhost:11434/musicgen",
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    return response.content  # Should be WAV/MP3 bytes


def generate_song(sections, default_tempo=120):
    """
    Generate a multi-section song using Ollama/MusicGen API.
    sections: list of dicts with keys: type, duration, transition, tempo
    Returns the output WAV file path.
    """
    from pydub import AudioSegment
    start = time.time()
    song = AudioSegment.silent(duration=0)
    for idx, section in enumerate(sections):
        # Check resources before generating each section
        check_resources(min_ram_gb=2, min_cpu_ghz=2)
        sec_type = section.get('type', 'verse')
        sec_len = int(section.get('duration', 8))
        sec_tempo = int(section.get('tempo', default_tempo))
        prompt = section.get('prompt', None)
        genre = section.get('genre', 'ambient')
        print(
            f"[MusicGen] Generating section {idx+1}: {sec_type}, {sec_len}s, "
            f"tempo={sec_tempo}, genre={genre}"
        )
        audio_bytes = call_ollama_musicgen(
            genre,
            sec_type,
            sec_len,
            prompt,
            sec_tempo
        )
        section_audio = AudioSegment.from_file(
            io.BytesIO(audio_bytes),
            format="wav"
        )
        song += section_audio
        # Insert transition if specified
        transition = section.get('transition', 'none')
        if transition and transition != 'none':
            if transition == 'drum_fill':
                # Example: add a short drum fill
                # (could be a pre-generated sample)
                drum_fill = AudioSegment.silent(duration=500)
                song += drum_fill
            elif transition == 'fade':
                # Fade out last section
                song = song.fade_out(1000)
            elif transition == 'sfx':
                # Add SFX (could be a pre-generated sample)
                sfx = AudioSegment.silent(duration=250)
                song += sfx
            # Add other transitions as needed
    out_path = f"song_{int(start)}.wav"
    song.export(out_path, format="wav")
    elapsed = time.time() - start
    print("Song generated in %.2f seconds." % elapsed)
    print("Saved to:")
    print(out_path)
    return out_path
