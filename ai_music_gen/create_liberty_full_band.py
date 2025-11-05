#!/usr/bin/env python3
"""
Liberty Blues - FULL BAND Chicago Version
Take existing vocals and create massive band arrangement with:
- Lead Guitar, Rhythm Guitar, Bass, Drums (existing)
- PLUS: Hammond B3 Organ, Piano, Harmonica, Saxophone
"""
from pathlib import Path
import numpy as np
from mido import MidiFile, MidiTrack, Message, MetaMessage
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = Path(__file__).parent.parent / "backend" / \
    "src" / "assets" / "generated"

BPM = 88
BEATS_PER_BAR = 4
TICKS_PER_BEAT = 480
SAMPLE_RATE = 24000

print("=" * 70)
print("  🎸 LIBERTY BLUES - FULL BAND CHICAGO VERSION 🎸")
print("=" * 70)
print()


def create_full_band_midi():
    """Create MASSIVE Chicago blues band arrangement"""
    print("🎵 Creating COUNTRY BAND arrangement with 5 instruments...\n")

    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    tempo = int(60_000_000 / BPM)

    # Channel assignments (General MIDI)
    LEAD_GUITAR = 0  # Acoustic Guitar (Steel) - Program 25
    RHYTHM_GUITAR = 1  # Acoustic Guitar (Nylon) - Program 24
    BASS = 2  # Acoustic Bass - Program 33
    BRASS = 3  # Trumpet - Program 57
    DRUMS = 9  # Standard Drum Kit

    # Create tracks
    tracks = {
        'lead_guitar': MidiTrack(),
        'rhythm_guitar': MidiTrack(),
        'bass': MidiTrack(),
        'brass': MidiTrack(),
        'drums': MidiTrack()
    }

    # Assign realistic instrument program numbers
    tracks['lead_guitar'].append(Message('program_change', program=25, channel=LEAD_GUITAR, time=0))
    tracks['rhythm_guitar'].append(Message('program_change', program=24, channel=RHYTHM_GUITAR, time=0))
    tracks['bass'].append(Message('program_change', program=33, channel=BASS, time=0))
    tracks['brass'].append(Message('program_change', program=57, channel=BRASS, time=0))
    # Drums do not need program_change
    for track in tracks.values():
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        mid.tracks.append(track)

    # E major country scale for Liberty Blues
    country_scale = [52, 54, 56, 57, 59, 61, 64, 66, 68, 71]  # E major scale

    # 12-bar country progression in E major
    chord_progression = [
        ('E', [52, 56, 59]),  # E-G#-B (bars 1-4)
        ('E', [52, 56, 59]),
        ('E', [52, 56, 59]),
        ('E', [52, 56, 59]),
        ('A', [57, 61, 64]),  # A-C#-E (bars 5-6)
        ('A', [57, 61, 64]),
        ('E', [52, 56, 59]),  # Back to E (bars 7-8)
        ('E', [52, 56, 59]),
        ('B', [59, 63, 66]),  # B-D#-F# (bar 9)
        ('A', [57, 61, 64]),  # A (bar 10)
        ('E', [52, 56, 59]),  # E (bar 11)
        ('B', [59, 63, 66]),  # B turnaround (bar 12)
    ]

    bars_per_beat = TICKS_PER_BEAT
    bars_per_bar = bars_per_beat * BEATS_PER_BAR

    # Song structure: 9 choruses (same as original)
    num_choruses = 9
    total_bars = num_choruses * 12 + 16  # +16 for intro

    print("🎸 Lead Guitar - Country licks and fills...")
    # Lead guitar - simple country licks, humanized
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            # Play root and fifth, add fills at ends
            for beat in range(4):
                note = notes[0] + 12 if beat % 2 == 0 else notes[2] + 12
                vel = 95 + np.random.randint(-10, 10)
                time_offset = bars_per_beat // 2 + np.random.randint(-10, 10)
                tracks['lead_guitar'].append(
                    Message('note_on', note=note, velocity=vel, time=time, channel=LEAD_GUITAR))
                tracks['lead_guitar'].append(
                    Message('note_off', note=note, velocity=0, time=time_offset, channel=LEAD_GUITAR))
                time = bars_per_beat - time_offset
            # Simple fill at end of phrase
            if bar_num in [3, 7, 11]:
                fill_note = country_scale[np.random.randint(0, len(country_scale))] + 12
                tracks['lead_guitar'].append(
                    Message('note_on', note=fill_note, velocity=100, time=time, channel=LEAD_GUITAR))
                tracks['lead_guitar'].append(
                    Message('note_off', note=fill_note, velocity=0, time=bars_per_beat // 2, channel=LEAD_GUITAR))
                time = bars_per_beat // 2
            else:
                time += bars_per_bar

    print("🎸 Rhythm Guitar - Country strumming...")
    # Rhythm guitar - simple strumming pattern
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for chord, notes in chord_progression:
            for beat in range(4):
                for note in notes:
                    vel = 80 + np.random.randint(-10, 10)
                    time_offset = bars_per_beat // 3 + np.random.randint(-5, 5)
                    tracks['rhythm_guitar'].append(
                        Message('note_on', note=note + 12, velocity=vel, time=time, channel=RHYTHM_GUITAR))
                    tracks['rhythm_guitar'].append(
                        Message('note_off', note=note + 12, velocity=0, time=time_offset, channel=RHYTHM_GUITAR))
                    time = bars_per_beat - time_offset
                time += bars_per_beat

    # ...existing code...

    print(" Bass - Country walking bass...")
    # Bass - simple walking pattern, humanized
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for chord, notes in chord_progression:
            root = notes[0]
            pattern = [root, root + 2, notes[2], root + 4]
            for note in pattern:
                vel = 90 + np.random.randint(-10, 10)
                time_offset = bars_per_beat // 2 + np.random.randint(-10, 10)
                tracks['bass'].append(
                    Message('note_on', note=note - 12, velocity=vel, time=time, channel=BASS))
                tracks['bass'].append(
                    Message('note_off', note=note - 12, velocity=0, time=time_offset, channel=BASS))
                time = bars_per_beat - time_offset

    # ...existing code...

    print("� Brass - Simple horn stabs...")
    # Brass - simple stabs on chord changes
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [0, 4, 8]:
                for note in notes:
                    vel = 100 + np.random.randint(-10, 10)
                    time_offset = bars_per_beat // 2 + np.random.randint(-10, 10)
                    tracks['brass'].append(
                        Message('note_on', note=note + 12, velocity=vel, time=time, channel=BRASS))
                    tracks['brass'].append(
                        Message('note_off', note=note + 12, velocity=0, time=time_offset, channel=BRASS))
                    time = bars_per_beat - time_offset
            else:
                time += bars_per_bar

    print("🥁 Drums - Country groove...")
    # Drums - simple country groove, humanized
    kick, snare, hihat = 36, 38, 42
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar in range(12):
            for beat in range(4):
                # Kick on 1 and 3
                if beat in [0, 2]:
                    vel = 100 + np.random.randint(-10, 10)
                    tracks['drums'].append(
                        Message('note_on', note=kick, velocity=vel, time=time, channel=DRUMS))
                    tracks['drums'].append(
                        Message('note_off', note=kick, velocity=0, time=bars_per_beat // 4, channel=DRUMS))
                    time = bars_per_beat // 2
                # Snare on 2 and 4
                if beat in [1, 3]:
                    vel = 90 + np.random.randint(-10, 10)
                    tracks['drums'].append(
                        Message('note_on', note=snare, velocity=vel, time=time, channel=DRUMS))
                    tracks['drums'].append(
                        Message('note_off', note=snare, velocity=0, time=bars_per_beat // 4, channel=DRUMS))
                    time = bars_per_beat // 2
                # Hi-hat on all beats
                vel = 80 + np.random.randint(-10, 10)
                tracks['drums'].append(
                    Message('note_on', note=hihat, velocity=vel, time=time, channel=DRUMS))
                tracks['drums'].append(
                    Message('note_off', note=hihat, velocity=0, time=bars_per_beat // 8, channel=DRUMS))
                time = bars_per_beat // 2

    # Write MIDI file
    output_file = OUTPUT_DIR / "liberty_blues_COUNTRY_BAND.mid"
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    mid.save(str(output_file))

    print(f"\n✅ Saved: {output_file}")
    print(f"   {total_bars} bars at {BPM} BPM")
    print(f"   5 INSTRUMENTS: Lead Guitar, Rhythm Guitar, Bass, Brass, Drums")
    print("\n💡 For realistic playback, use a high-quality country soundfont or virtual instrument.")
    print("   (General MIDI program numbers are set for each instrument.)")
    print()
    return output_file


if __name__ == "__main__":
    create_full_band_midi()
