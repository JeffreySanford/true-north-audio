import copy
import datetime
import math
import random
from typing import Dict, List, Sequence, Optional

import numpy as np

# Import vocal synthesis engine
try:
    from engines.vocals import (
        generate_vocals_placeholder,
        mix_vocals_with_music,
        parse_lyrics_with_timing,
        should_add_vocals,
        get_default_lyrics
    )
    VOCALS_AVAILABLE = True
except ImportError:
    VOCALS_AVAILABLE = False
    print("[MusicGen] Warning: Vocal engine not available. Install vocals module for vocal synthesis.")

# Expose generate_music for import
__all__ = ["generate_music", "generate_melody"]


NOTE_TO_SEMITONE = {
    "C": 0,
    "C#": 1,
    "DB": 1,
    "D": 2,
    "D#": 3,
    "EB": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "GB": 6,
    "G": 7,
    "G#": 8,
    "AB": 8,
    "A": 9,
    "A#": 10,
    "BB": 10,
    "B": 11,
}


SCALE_PATTERNS: Dict[str, List[int]] = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
}


GENRE_PROFILES: Dict[str, Dict[str, object]] = {
    "default": {
        "root": "C3",
        "scale": "major",
        "progressions": [[1, 5, 6, 4]],
        "melody_degrees": [1, 2, 3, 5, 6],
        "pad_waves": ["sine", "triangle"],
        "melody_waves": ["sine"],
        "bass_wave": "sine",
        "percussion": False,
        "percussion_density": 0.4,
        "tempo_hint": 110,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.01, 4.0),
        "melody_rest_prob": 0.18,
    },
    "ambient": {
        "root": "C3",
        "scale": "major",
        "progressions": [[1, 4, 5, 6], [1, 6, 4, 5]],
        "melody_degrees": [1, 2, 3, 5, 6],
        "pad_waves": ["sine", "triangle"],
        "melody_waves": ["sine", "triangle"],
        "bass_wave": "sine",
        "percussion": False,
        "tempo_hint": 75,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.015, 3.0),
        "melody_rest_prob": 0.25,
    },
    "rock": {
        "root": "E3",
        "scale": "minor",
        "progressions": [[1, 5, 6, 4], [1, 4, 5, 4]],
        "melody_degrees": [1, 3, 4, 5, 6],
        "pad_waves": ["saw", "square"],
        "melody_waves": ["square", "saw"],
        "bass_wave": "square",
        "percussion": True,
        "percussion_density": 0.85,
        "tempo_hint": 130,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.02, 5.0),
        "melody_rest_prob": 0.12,
    },
    "jazz": {
        "root": "F3",
        "scale": "mixolydian",
        "progressions": [[2, 5, 1, 6], [1, 6, 2, 5]],
        "melody_degrees": [1, 2, 3, 5, 6, 7],
        "pad_waves": ["sine", "triangle"],
        "melody_waves": ["sine"],
        "bass_wave": "sine",
        "percussion": True,
        "percussion_density": 0.6,
        "tempo_hint": 105,
        "melody_octave": 1,
        "chord_octave": 1,
        "bass_offset": -12,
        "melody_vibrato": (0.018, 5.5),
        "melody_rest_prob": 0.2,
    },
    "electronic": {
        "root": "A2",
        "scale": "minor",
        "progressions": [[1, 6, 3, 7], [1, 5, 6, 5]],
        "melody_degrees": [1, 3, 4, 5, 7],
        "pad_waves": ["saw", "triangle"],
        "melody_waves": ["saw", "square"],
        "bass_wave": "saw",
        "percussion": True,
        "percussion_density": 0.95,
        "tempo_hint": 128,
        "melody_octave": 2,
        "chord_octave": 1,
        "bass_offset": -12,
        "melody_vibrato": (0.01, 6.5),
        "melody_rest_prob": 0.08,
    },
    "hiphop": {
        "root": "D3",
        "scale": "minor",
        "progressions": [[1, 4, 1, 5], [6, 1, 4, 5]],
        "melody_degrees": [1, 4, 5, 6, 7],
        "pad_waves": ["sine", "square"],
        "melody_waves": ["sine", "triangle"],
        "bass_wave": "square",
        "percussion": True,
        "percussion_density": 0.9,
        "tempo_hint": 92,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.012, 4.2),
        "melody_rest_prob": 0.22,
    },
    "classical": {
        "root": "C3",
        "scale": "major",
        "progressions": [[1, 4, 6, 5], [1, 3, 4, 5]],
        "melody_degrees": [1, 2, 3, 4, 5, 6],
        "pad_waves": ["sine"],
        "melody_waves": ["sine"],
        "bass_wave": "sine",
        "percussion": False,
        "tempo_hint": 90,
        "melody_octave": 1,
        "chord_octave": 1,
        "bass_offset": -12,
        "melody_vibrato": (0.008, 3.5),
        "melody_rest_prob": 0.3,
    },
    "pop": {
        "root": "C3",
        "scale": "major",
        "progressions": [[1, 5, 6, 4], [6, 4, 1, 5]],
        "melody_degrees": [1, 2, 3, 5, 6],
        "pad_waves": ["sine", "saw"],
        "melody_waves": ["sine", "square"],
        "bass_wave": "sine",
        "percussion": True,
        "percussion_density": 0.75,
        "tempo_hint": 118,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.012, 4.5),
        "melody_rest_prob": 0.14,
    },
    "folk": {
        "root": "G3",
        "scale": "major",
        "progressions": [[1, 4, 5, 1], [1, 6, 4, 5]],
        "melody_degrees": [1, 2, 3, 5, 6],
        "pad_waves": ["triangle", "sine"],
        "melody_waves": ["sine"],
        "bass_wave": "triangle",
        "percussion": False,
        "tempo_hint": 96,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.01, 3.5),
        "melody_rest_prob": 0.32,
    },
    "blues": {
        "root": "A3",
        "scale": "minor",
        "progressions": [[1, 1, 1, 1, 4, 4, 1, 1, 5, 4, 1, 1]],
        "melody_degrees": [1, 3, 4, 5, 7],
        "pad_waves": ["sine", "square"],
        "melody_waves": ["square", "triangle"],
        "bass_wave": "square",
        "percussion": True,
        "percussion_density": 0.7,
        "tempo_hint": 88,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.018, 5.2),
        "melody_rest_prob": 0.26,
    },
    "metal": {
        "root": "D3",
        "scale": "minor",
        "progressions": [[1, 6, 7, 5], [1, 4, 3, 6]],
        "melody_degrees": [1, 3, 4, 5, 6, 7],
        "pad_waves": ["saw", "square"],
        "melody_waves": ["saw"],
        "bass_wave": "saw",
        "percussion": True,
        "percussion_density": 0.98,
        "tempo_hint": 150,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.025, 6.5),
        "melody_rest_prob": 0.06,
    },
    "country": {
        "root": "A3",
        "scale": "major",
        "progressions": [[1, 4, 5, 1], [1, 5, 6, 4]],
        "melody_degrees": [1, 2, 3, 5, 6],
        "pad_waves": ["triangle", "sine"],
        "melody_waves": ["sine", "triangle"],
        "bass_wave": "triangle",
        "percussion": True,
        "percussion_density": 0.68,
        "tempo_hint": 104,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.011, 4.1),
        "melody_rest_prob": 0.24,
    },
    "reggae": {
        "root": "B2",
        "scale": "major",
        "progressions": [[1, 4, 5, 4], [6, 7, 1, 5]],
        "melody_degrees": [1, 2, 3, 5, 6],
        "pad_waves": ["sine", "triangle"],
        "melody_waves": ["sine", "square"],
        "bass_wave": "sine",
        "percussion": True,
        "percussion_density": 0.65,
        "tempo_hint": 78,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.016, 3.8),
        "melody_rest_prob": 0.35,
    },
    "soul": {
        "root": "E3",
        "scale": "minor",
        "progressions": [[1, 4, 3, 6], [2, 5, 1, 6]],
        "melody_degrees": [1, 2, 3, 5, 6, 7],
        "pad_waves": ["sine", "triangle"],
        "melody_waves": ["sine", "square"],
        "bass_wave": "sine",
        "percussion": True,
        "percussion_density": 0.72,
        "tempo_hint": 100,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.017, 4.8),
        "melody_rest_prob": 0.28,
    },
    "funk": {
        "root": "D3",
        "scale": "mixolydian",
        "progressions": [[1, 7, 6, 5], [1, 4, 1, 5]],
        "melody_degrees": [1, 2, 3, 5, 6, 7],
        "pad_waves": ["sine", "square"],
        "melody_waves": ["square", "saw"],
        "bass_wave": "square",
        "percussion": True,
        "percussion_density": 0.9,
        "tempo_hint": 112,
        "melody_octave": 1,
        "chord_octave": 0,
        "bass_offset": -12,
        "melody_vibrato": (0.02, 5.8),
        "melody_rest_prob": 0.18,
    },
}


def note_to_midi(note: str) -> int:
    note = note.strip().upper()
    if not note:
        return 60
    if len(note) > 2 and note[1] in {"#", "B"}:
        name = note[:2]
        octave_part = note[2:]
    else:
        name = note[0]
        octave_part = note[1:]
    semitone = NOTE_TO_SEMITONE.get(name, 0)
    try:
        octave = int(octave_part)
    except ValueError:
        octave = 4
    return semitone + (octave + 1) * 12


def midi_to_freq(midi_note: int) -> float:
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def resolve_profile(genre: str) -> Dict[str, object]:
    profile = copy.deepcopy(GENRE_PROFILES["default"])
    if not genre:
        return profile
    override = GENRE_PROFILES.get(genre.lower())
    if not override:
        return profile
    for key, value in override.items():
        if isinstance(value, list):
            profile[key] = copy.deepcopy(value)
        elif isinstance(value, dict):
            profile[key] = value.copy()
        else:
            profile[key] = value
    return profile


def expand_scale(root_midi: int, scale_name: str, octaves: int = 5) -> List[int]:
    pattern = SCALE_PATTERNS.get(scale_name.lower(), SCALE_PATTERNS["major"])
    notes: List[int] = []
    for octave in range(octaves):
        base = root_midi + 12 * octave
        for interval in pattern:
            notes.append(base + interval)
    notes.append(root_midi + 12 * octaves)
    return notes


def chord_from_degree(scale_notes: Sequence[int], degree: int, chord_size: int = 3,
                      octave_offset: int = 0) -> List[int]:
    if not scale_notes:
        return [60, 64, 67]
    deg = max(1, degree)
    base_idx = (deg - 1) + octave_offset * 7
    base_idx = base_idx % max(1, len(scale_notes))
    chord: List[int] = []
    for step in range(chord_size):
        idx = base_idx + step * 2
        if idx >= len(scale_notes):
            idx = len(scale_notes) - 1
        chord.append(scale_notes[idx])
    return chord


def adsr_envelope(length_samples: int, sample_rate: int,
                  attack: float = 0.02, decay: float = 0.12,
                  sustain_level: float = 0.7, release: float = 0.18) -> np.ndarray:
    if length_samples <= 0:
        return np.zeros(0, dtype=np.float32)
    env = np.ones(length_samples, dtype=np.float32) * sustain_level
    attack_samples = max(1, int(attack * sample_rate))
    decay_samples = max(1, int(decay * sample_rate))
    release_samples = max(1, int(release * sample_rate))
    total = attack_samples + decay_samples + release_samples
    if total > length_samples:
        scale = length_samples / float(total)
        attack_samples = max(1, int(attack_samples * scale))
        decay_samples = max(1, int(decay_samples * scale))
        release_samples = max(1, int(release_samples * scale))
        total = attack_samples + decay_samples + release_samples
        if total > length_samples:
            release_samples = max(1, length_samples - (attack_samples + decay_samples))
    env[:attack_samples] = np.linspace(0.0, 1.0, attack_samples, endpoint=False)
    env[attack_samples:attack_samples + decay_samples] = np.linspace(
        1.0, sustain_level, decay_samples, endpoint=False
    )
    env[-release_samples:] = np.linspace(sustain_level, 0.0, release_samples, endpoint=False)
    return env


def oscillator_from_phase(wave_type: str, phase: np.ndarray) -> np.ndarray:
    wrapped = np.mod(phase, 2 * np.pi)
    phase_ratio = wrapped / (2 * np.pi)
    if wave_type == "sine":
        return np.sin(wrapped)
    if wave_type == "square":
        return np.where(np.sin(wrapped) >= 0.0, 1.0, -1.0)
    if wave_type == "triangle":
        saw = 2.0 * phase_ratio - 1.0
        return 2.0 * np.abs(saw) - 1.0
    if wave_type == "saw":
        return 2.0 * phase_ratio - 1.0
    return np.sin(wrapped)


def add_note(buffer: np.ndarray, freq: float, start_time: float, length: float,
             sample_rate: int, wave_pool: Sequence[str], volume: float,
             rng: np.random.Generator, vibrato: Sequence[float] | None = None) -> None:
    start_idx = int(start_time * sample_rate)
    if start_idx >= buffer.shape[0]:
        return
    length_samples = max(1, int(length * sample_rate))
    end_idx = min(buffer.shape[0], start_idx + length_samples)
    if end_idx <= start_idx:
        return
    note_length = end_idx - start_idx
    wave_type = wave_pool[int(rng.integers(len(wave_pool)))] if wave_pool else "sine"
    if wave_type == "noise":
        waveform = rng.uniform(-1.0, 1.0, note_length)
    else:
        freq_curve = np.full(note_length, freq, dtype=np.float32)
        if vibrato and len(vibrato) == 2:
            depth, rate = vibrato
            t = np.arange(note_length, dtype=np.float32) / sample_rate
            freq_curve *= 1.0 + depth * np.sin(2 * np.pi * rate * t)
        phase = np.cumsum((2 * np.pi * freq_curve) / sample_rate, dtype=np.float32)
        waveform = oscillator_from_phase(wave_type, phase)
    envelope = adsr_envelope(note_length, sample_rate)
    buffer[start_idx:end_idx] += (waveform * envelope * volume).astype(np.float32)


def add_chord_layer(buffer: np.ndarray, chord_notes: Sequence[int], start_time: float,
                    chord_length: float, sample_rate: int, wave_pool: Sequence[str],
                    rng: np.random.Generator, vibrato: Sequence[float] | None,
                    intensity: float) -> None:
    for midi_note in chord_notes:
        freq = midi_to_freq(midi_note)
        add_note(
            buffer,
            freq,
            start_time,
            chord_length,
            sample_rate,
            wave_pool,
            intensity,
            rng,
            vibrato,
        )


def generate_percussion_track(duration: float, sample_rate: int, tempo: int,
                              rng: np.random.Generator, density: float) -> np.ndarray:
    total_samples = max(1, int(duration * sample_rate))
    track = np.zeros(total_samples, dtype=np.float32)
    seconds_per_beat = 60.0 / max(1, tempo)
    total_beats = int(math.ceil(duration / seconds_per_beat)) + 1
    for beat in range(total_beats):
        start_time = beat * seconds_per_beat
        if start_time >= duration:
            break
        if beat % 4 == 0:
            add_percussion_hit(track, start_time, sample_rate, rng,
                               kind="kick", strength=0.9)
        if beat % 4 == 2:
            add_percussion_hit(track, start_time, sample_rate, rng,
                               kind="snare", strength=0.7)
        if rng.random() < 0.65 * density:
            add_percussion_hit(track, start_time, sample_rate, rng,
                               kind="hihat", strength=0.5)
        if rng.random() < 0.3 * density:
            add_percussion_hit(track, start_time + seconds_per_beat / 2.0,
                               sample_rate, rng, kind="hihat", strength=0.45)
    return track


def add_percussion_hit(buffer: np.ndarray, start_time: float, sample_rate: int,
                       rng: np.random.Generator, kind: str, strength: float) -> None:
    start_idx = int(start_time * sample_rate)
    if start_idx >= buffer.shape[0]:
        return
    if kind == "kick":
        length = 0.4
        freq_start = 60.0
        envelope_rate = 6.0
        add_idx = min(buffer.shape[0], start_idx + int(length * sample_rate))
        t = np.arange(add_idx - start_idx) / sample_rate
        phase = 2 * np.pi * (freq_start * t - 20.0 * t * t)
        wave = np.sin(phase) * np.exp(-envelope_rate * t)
        buffer[start_idx:add_idx] += (wave * strength).astype(np.float32)
        return
    if kind == "snare":
        length = 0.25
        add_idx = min(buffer.shape[0], start_idx + int(length * sample_rate))
        t = np.arange(add_idx - start_idx) / sample_rate
        noise = rng.uniform(-1.0, 1.0, add_idx - start_idx)
        envelope = np.exp(-12.0 * t)
        buffer[start_idx:add_idx] += (noise * envelope * strength).astype(np.float32)
        return
    length = 0.18
    add_idx = min(buffer.shape[0], start_idx + int(length * sample_rate))
    t = np.arange(add_idx - start_idx) / sample_rate
    noise = rng.uniform(-1.0, 1.0, add_idx - start_idx)
    envelope = np.exp(-20.0 * t)
    buffer[start_idx:add_idx] += (noise * envelope * strength).astype(np.float32)


def apply_reverb(signal: np.ndarray, sample_rate: int,
                 delay_seconds: float = 0.28, decay: float = 0.35,
                 repeats: int = 3) -> np.ndarray:
    delay_samples = int(delay_seconds * sample_rate)
    if delay_samples <= 0:
        return signal
    output = signal.copy()
    for n in range(1, repeats + 1):
        offset = delay_samples * n
        if offset >= signal.shape[0]:
            break
        output[offset:] += signal[:-offset] * (decay / n)
    return output


def create_song_waveform(config: "MusicGenConfig", sample_rate: int) -> tuple[np.ndarray, Dict[str, object]]:
    rng = np.random.default_rng(config.seed)
    profile = resolve_profile(config.genre)
    tempo_hint = profile.get("tempo_hint", 120)
    tempo = int(config.tempo or tempo_hint)
    tempo = max(48, min(172, tempo))
    duration_seconds = max(2.0, float(config.duration))
    seconds_per_beat = 60.0 / tempo
    measure_duration = 4 * seconds_per_beat
    scale_name = str(profile.get("scale", "major"))

    idea_text = (config.idea or "").lower()
    if any(word in idea_text for word in ["dark", "minor", "melancholy"]):
        scale_name = "minor"
    if any(word in idea_text for word in ["bright", "uplift", "hope"]):
        scale_name = "major"
    if "slow" in idea_text:
        tempo = max(48, tempo - 15)
    if "fast" in idea_text or "energetic" in idea_text:
        tempo = min(172, tempo + 15)

    if config.variation and config.variation.lower() in {"remix", "alternate", "extended"}:
        duration_seconds *= 1.1

    total_samples = max(1, int(sample_rate * duration_seconds))
    pad_track = np.zeros(total_samples, dtype=np.float32)
    melody_track = np.zeros(total_samples, dtype=np.float32)
    bass_track = np.zeros(total_samples, dtype=np.float32)

    root_midi = note_to_midi(str(profile.get("root", "C3")))
    scale_notes = expand_scale(root_midi, scale_name, octaves=6)
    progressions: List[List[int]] = profile.get("progressions", [[1, 5, 6, 4]])
    progression = progressions[int(rng.integers(len(progressions)))]
    if config.variation and config.variation.lower() == "extended":
        progression = progression + progression[:2]

    vibrato = profile.get("melody_vibrato")
    chord_octave = int(profile.get("chord_octave", 0))
    melody_octave = int(profile.get("melody_octave", 1))
    bass_offset = int(profile.get("bass_offset", -12))

    pad_waves = profile.get("pad_waves", ["sine"])
    melody_waves = profile.get("melody_waves", ["sine"])
    bass_wave = [str(profile.get("bass_wave", "sine"))]

    num_measures = max(2, int(math.ceil(duration_seconds / measure_duration)))
    for measure in range(num_measures):
        start_time = measure * measure_duration
        if start_time >= duration_seconds:
            break
        degree = progression[measure % len(progression)]
        chord_notes = chord_from_degree(scale_notes, degree, chord_size=4,
                                        octave_offset=chord_octave)
        add_chord_layer(
            pad_track,
            chord_notes,
            start_time,
            measure_duration + seconds_per_beat,
            sample_rate,
            pad_waves,
            rng,
            vibrato,
            intensity=0.35,
        )
        bass_note = chord_notes[0] + bass_offset
        add_note(
            bass_track,
            midi_to_freq(bass_note),
            start_time,
            measure_duration,
            sample_rate,
            bass_wave,
            volume=0.42,
            rng=rng,
            vibrato=None,
        )

    melody_degrees: List[int] = profile.get("melody_degrees", [1, 2, 3, 5, 6])
    total_beats = int(math.ceil(duration_seconds / seconds_per_beat))
    rest_prob = float(profile.get("melody_rest_prob", 0.2))
    if total_beats < 4:
        total_beats = 4
    for beat in range(total_beats):
        start_time = beat * seconds_per_beat
        if start_time >= duration_seconds:
            break
        if rng.random() < rest_prob:
            continue
        if beat % 4 == 0 and beat // 4 < len(progression):
            base_degree = progression[beat // 4 % len(progression)]
        else:
            base_degree = rng.choice(melody_degrees)
        if rng.random() < 0.35:
            base_degree = rng.choice(melody_degrees)
        degree = ((base_degree - 1) % 7) + 1
        melody_idx = degree - 1 + melody_octave * 7
        melody_idx = min(melody_idx, len(scale_notes) - 1)
        note_length = seconds_per_beat * (1.5 if rng.random() < 0.25 else 1.0)
        volume = 0.35 + 0.1 * rng.random()
        add_note(
            melody_track,
            midi_to_freq(scale_notes[melody_idx]),
            start_time,
            note_length,
            sample_rate,
            melody_waves,
            volume,
            rng,
            vibrato,
        )

    percussion_track = np.zeros(total_samples, dtype=np.float32)
    if profile.get("percussion", False):
        percussion_track = generate_percussion_track(
            duration_seconds,
            sample_rate,
            tempo,
            np.random.default_rng(config.seed + 7),
            float(profile.get("percussion_density", 0.8)),
        )

    combined = pad_track * 0.55 + melody_track * 0.85 + bass_track * 0.75 + percussion_track * 0.5
    combined = apply_reverb(combined, sample_rate)
    max_val = float(np.max(np.abs(combined)))
    if max_val > 0:
        combined = combined / max_val * 0.92
    combined = np.clip(combined, -0.99, 0.99).astype(np.float32)

    target_samples = max(1, int(sample_rate * max(2.0, float(config.duration))))
    if combined.shape[0] > target_samples:
        combined = combined[:target_samples]
    elif combined.shape[0] < target_samples:
        combined = np.pad(combined, (0, target_samples - combined.shape[0]))

    metadata = {
        "tempo": tempo,
        "scale": scale_name,
        "progression": progression,
        "duration_seconds": len(combined) / sample_rate,
        "melody_rest_prob": rest_prob,
    }
    return combined, metadata


def generate_melody(*args, **kwargs):
    # Map 'length' to 'duration' for test compatibility
    if 'length' in kwargs:
        kwargs['duration'] = kwargs.pop('length')

    return generate_music(*args, **kwargs)


GENRES = [
    "ambient", "rock", "jazz", "classical", "pop", "electronic",
    "hiphop", "folk", "blues", "metal", "country", "reggae",
    "soul", "funk", "world", "experimental", "bigband", "1940s"
]
VOCAL_ARTISTS = [
    {"name": "AI_Male_1", "gender": "male"},
    {"name": "AI_Male_2", "gender": "male"},
    {"name": "AI_Female_1", "gender": "female"},
    {"name": "AI_Female_2", "gender": "female"},
    {"name": "AI_Choir", "gender": "mixed"}
]


class MusicGenConfig:
    def __init__(self,
                 genre: str,
                 vocal_artist: str,
                 seed: int = None,
                 tempo: int = 120,
                 idea: str = None,
                 variation: str = "original",
                 duration: int = 10,
                 lyrics: Optional[str] = None,
                 vocal_style: str = "spoken"):
        self.genre = genre
        self.vocal_artist = vocal_artist
        self.seed = seed or random.randint(0, 999999)
        self.tempo = tempo
        self.idea = idea
        self.variation = variation
        self.duration = duration
        self.lyrics = lyrics
        self.vocal_style = vocal_style
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
            "lyrics": self.lyrics if self.lyrics else None,
            "vocal_style": self.vocal_style,
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
        print(
            f"[MusicGen] Starting generation: {overview}"
        )
        import os
        import wave
        sample_rate = 32000
        waveform, song_metadata = create_song_waveform(config, sample_rate)
        print(
            f"[MusicGen] Generated waveform shape: {waveform.shape}, "
            f"dtype: {waveform.dtype}"
        )
        static_warning = None
        variance = float(np.var(waveform))
        if variance < 1e-5:
            static_warning = (
                "Warning: Output waveform variance is low; track may sound flat. "
                f"Var: {variance:.6f}"
            )
            print(f"[MusicGen] {static_warning}")
        
        # === VOCAL SYNTHESIS INTEGRATION ===
        vocal_segments = []
        if VOCALS_AVAILABLE and config.lyrics:
            print(f"[MusicGen] Adding vocals with style: {config.vocal_style}")
            try:
                vocal_result = generate_vocals_placeholder(
                    lyrics=config.lyrics,
                    duration=config.duration,
                    sample_rate=sample_rate,
                    vocal_style=config.vocal_style
                )
                
                vocal_waveform = vocal_result['waveform']
                vocal_segments = vocal_result.get('segments', [])
                
                # Mix vocals with instrumental
                print(f"[MusicGen] Mixing vocals with instrumental track")
                waveform = mix_vocals_with_music(
                    music_waveform=waveform,
                    vocal_waveform=vocal_waveform,
                    music_volume=0.65,  # Lower music when vocals present
                    vocal_volume=1.0
                )
                print(f"[MusicGen] Vocals mixed successfully. Segments: {len(vocal_segments)}")
            except Exception as e:
                print(f"[MusicGen] Warning: Vocal synthesis failed: {e}")
                static_warning = f"Vocal synthesis error: {str(e)}"
        elif config.lyrics and not VOCALS_AVAILABLE:
            print("[MusicGen] Lyrics provided but vocal engine not available")
            static_warning = "Vocal engine not installed. Install Bark or TTS library for vocals."
        
        rendered_duration = len(waveform) / sample_rate
        scale_desc = song_metadata.get("scale") or "modal"
        overview.update({
            "rendered_tempo": song_metadata.get("tempo"),
            "rendered_scale": scale_desc,
            "progression": song_metadata.get("progression"),
            "rendered_duration": round(rendered_duration, 2),
            "melody_rest_prob": song_metadata.get("melody_rest_prob"),
        })
        vocals = (
            f"Melodic lead for {overview['vocal_artist']} over a "
            f"{scale_desc} palette"
        )
        audio_dir = os.path.join(
            os.getcwd(),
            "backend",
            "src",
            "assets",
            "generated"
        )
        os.makedirs(audio_dir, exist_ok=True)
        wav_path = os.path.join(
            audio_dir,
            f"{overview['genre']}_"
            f"{overview['vocal_artist']}_"
            f"{overview['seed']}.wav"
        )
        mp3_path = os.path.join(
            audio_dir,
            f"{overview['genre']}_"
            f"{overview['vocal_artist']}_"
            f"{overview['seed']}.mp3"
        )
        print(
            f"[MusicGen] Saving WAV to {wav_path}"
        )
        int_waveform = np.int16(waveform * 32767)
        with wave.open(wav_path, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(int_waveform.tobytes())
        print(
            "[MusicGen] WAV file saved. Starting MP3 conversion..."
        )
        try:
            import subprocess
            subprocess.run(
                ['ffmpeg', '-y', '-i',
                 wav_path, mp3_path], check=True)
            print(
                f"[MusicGen] MP3 conversion succeeded: {mp3_path}"
            )
            audio_url = (
                "/audio/generated/" + overview['genre'] + "_" +
                overview['vocal_artist'] + "_" + str(overview['seed'])
            )
            audio_url += ".mp3"
        except Exception as e:
            print("[MusicGen] MP3 conversion failed: {}".format(e))
            audio_url = (
                f"/audio/generated/{overview['genre']}_"
                f"{overview['vocal_artist']}_"
                f"{overview['seed']}.wav"
            )
        print(
            f"[MusicGen] Returning audio_url: {audio_url}"
        )
        
        # Prepare vocal info for response
        vocal_info = vocals
        if vocal_segments:
            vocal_info = {
                "description": vocals,
                "segments": vocal_segments,
                "style": config.vocal_style,
                "has_lyrics": True
            }
        
        return {
            "overview": overview,
            "audio_url": audio_url,
            "status": "success",
            "waveform": waveform,
            "sample_rate": sample_rate,
            "vocals": vocal_info,
            "vocal_segments": vocal_segments if vocal_segments else None,
            "warning": static_warning
        }


def generate_music(
    genre: str = 'ambient',
    duration: int = 10,
    seed: int = None,
    idea: str = None,
    vocal_artist: str = 'AI_Male_1',
    tempo: int = 120,
    variation: str = "original",
    lyrics: Optional[str] = None,
    vocal_style: str = "spoken"
):
    config = MusicGenConfig(
        genre=genre,
        vocal_artist=vocal_artist,
        seed=seed,
        tempo=tempo,
        idea=idea,
        variation=variation,
        duration=duration,
        lyrics=lyrics,
        vocal_style=vocal_style
    )
    result = MusicGen.generate_music(config)
    if 'audio_url' not in result or not result['audio_url']:
        overview = result.get('overview', {})
        genre_val = overview.get('genre', 'ambient')
        vocal_val = overview.get('vocal_artist', 'none')
        seed_val = overview.get('seed', '0')
        result['audio_url'] = (
            f"/audio/generated/{genre_val}_{vocal_val}_{seed_val}.mp3"
        )
    return result
