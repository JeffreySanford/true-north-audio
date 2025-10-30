import mido
import time
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
        track.append(mido.Message('note_off', note=note, velocity=64, time=120))
    out_path = f"melody_{int(start)}.mid"
    mid.save(out_path)
    elapsed = time.time() - start
    print(f"Melody generated in {elapsed:.2f} seconds. Saved to {out_path}.")
    return out_path
