

import numpy as np
import pretty_midi
from magenta.music import melodies_lib
from magenta.music import sequences_lib
from magenta.music import midi_synth

# Genre to MIDI program mapping (General MIDI)
GENRE_PROGRAMS = {
    'ambient': 89,   # Pad 1 (new age)
    'pop': 4,       # Electric Piano
    'rock': 30,     # Overdriven Guitar
    'jazz': 65,     # Alto Sax
    'classical': 0, # Acoustic Grand Piano
    'electronic': 81, # Lead 2 (sawtooth)
    'hiphop': 25,   # Acoustic Guitar
    'folk': 24,     # Nylon Guitar
}

def generate_melody(genre: str = 'ambient', duration: int = 10, seed: int = None, idea: str = None) -> melodies_lib.Melody:
    """
    Generate a genre-based melody using Magenta's Melody class.
    """
    if seed is not None:
        np.random.seed(seed)
    # Use idea to vary starting note
    start_note = 60  # Middle C
    if idea:
        start_note += sum(ord(c) for c in idea) % 12
    # Genre-based scale
    scale = {
        'ambient': [60, 62, 65, 69, 72],
        'pop': [60, 64, 67, 69, 71],
        'rock': [55, 59, 62, 64, 67],
        'jazz': [60, 63, 65, 68, 70],
        'classical': [60, 62, 64, 65, 67, 69, 71],
        'electronic': [60, 63, 67, 70, 74],
        'hiphop': [48, 50, 53, 55, 58],
        'folk': [60, 62, 64, 67, 69],
    }.get(genre, [60, 62, 64, 65, 67])
    melody = melodies_lib.Melody()
    notes = [start_note + (scale[i % len(scale)] - 60) for i in range(duration)]
    melody.from_event_list(notes)
    return melody

def generate_vocals(idea: str = None, duration: int = 10) -> str:
    """
    Generate a simple vocal transcription from the idea prompt.
    """
    if not idea:
        return "(No vocals)"
    # Simulate vocal transcription by repeating the idea
    words = idea.split()
    transcription = ' '.join(words * max(1, duration // max(1, len(words))))
    return transcription

def melody_to_waveform(melody: melodies_lib.Melody, genre: str = 'ambient', duration: int = 10, sample_rate: int = 22050) -> np.ndarray:
    """
    Convert a Magenta Melody to audio waveform using pretty_midi and numpy.
    """
    pm = pretty_midi.PrettyMIDI()
    program = GENRE_PROGRAMS.get(genre, 0)
    instrument = pretty_midi.Instrument(program=program)
    for i, note_num in enumerate(melody.event_list):
        start = i * (duration / len(melody.event_list))
        end = start + (duration / len(melody.event_list))
        note = pretty_midi.Note(velocity=100, pitch=note_num, start=start, end=end)
        instrument.notes.append(note)
    pm.instruments.append(instrument)
    audio = pm.fluidsynth(fs=sample_rate)
    return audio

def generate_music(genre: str = 'ambient', duration: int = 10, seed: int = None, idea: str = None):
    """
    Generate music using Magenta and return waveform and vocal transcription.
    Returns:
        dict: { 'waveform': np.ndarray, 'sample_rate': int, 'vocals': str }
    """
    melody = generate_melody(genre, duration, seed, idea)
    waveform = melody_to_waveform(melody, genre, duration)
    vocals = generate_vocals(idea, duration)
    return {
        'waveform': waveform,
        'sample_rate': 22050,
        'vocals': vocals
    }
