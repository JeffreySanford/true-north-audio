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
    print("🎵 Creating FULL BAND arrangement with 8 instruments...\n")

    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    tempo = int(60_000_000 / BPM)

    # Channel assignments
    LEAD_GUITAR = 0
    RHYTHM_GUITAR = 1
    ORGAN = 2
    PIANO = 3
    BASS = 4
    HARMONICA = 5
    SAX = 6
    DRUMS = 9

    # Create tracks
    tracks = {
        'lead_guitar': MidiTrack(),
        'rhythm_guitar': MidiTrack(),
        'organ': MidiTrack(),
        'piano': MidiTrack(),
        'bass': MidiTrack(),
        'harmonica': MidiTrack(),
        'sax': MidiTrack(),
        'drums': MidiTrack()
    }

    for track in tracks.values():
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        mid.tracks.append(track)

    # E minor blues scale for Liberty Blues
    blues_scale = [52, 55, 57, 58, 59, 62, 64, 67, 69, 71]  # E blues scale

    # 12-bar blues progression in E minor
    chord_progression = [
        ('Em7', [52, 55, 59, 62]),  # E-G-B-D (bars 1-4)
        ('Em7', [52, 55, 59, 62]),
        ('Em7', [52, 55, 59, 62]),
        ('Em7', [52, 55, 59, 62]),
        ('Am7', [45, 48, 52, 55]),  # A-C-E-G (bars 5-6)
        ('Am7', [45, 48, 52, 55]),
        ('Em7', [52, 55, 59, 62]),  # Back to Em7 (bars 7-8)
        ('Em7', [52, 55, 59, 62]),
        ('Bm7', [47, 50, 54, 57]),  # B-D-F#-A (bar 9)
        ('Am7', [45, 48, 52, 55]),  # Am7 (bar 10)
        ('Em7', [52, 55, 59, 62]),  # Em7 (bar 11)
        ('Bm7', [47, 50, 54, 57]),  # Bm7 turnaround (bar 12)
    ]

    bars_per_beat = TICKS_PER_BEAT
    bars_per_bar = bars_per_beat * BEATS_PER_BAR

    # Song structure: 9 choruses (same as original)
    num_choruses = 9
    total_bars = num_choruses * 12 + 16  # +16 for intro

    print("🎸 Lead Guitar - Blues licks with bends...")
    # Lead guitar (existing style but enhanced)
    time = bars_per_bar * 16  # Skip intro
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [3, 7, 11]:  # Fills at phrase ends
                for _ in range(4):
                    note = np.random.choice(blues_scale) + 12
                    vel = np.random.randint(90, 110)
                    tracks['lead_guitar'].append(
                        Message(
                            'note_on',
                            note=note,
                            velocity=vel,
                            time=time,
                            channel=LEAD_GUITAR))
                    time = bars_per_beat // 2
                    tracks['lead_guitar'].append(
                        Message(
                            'note_off',
                            note=note,
                            velocity=0,
                            time=time,
                            channel=LEAD_GUITAR))
                    time = 0
                    # Random bends
                    if np.random.random() > 0.5:
                        tracks['lead_guitar'].append(
                            Message(
                                'pitchwheel',
                                pitch=4096,
                                time=0,
                                channel=LEAD_GUITAR))
                        time = bars_per_beat // 4
                        tracks['lead_guitar'].append(
                            Message(
                                'pitchwheel',
                                pitch=0,
                                time=time,
                                channel=LEAD_GUITAR))
                        time = 0
            else:
                time += bars_per_bar

    print("🎸 Rhythm Guitar - Choppy shuffle...")
    # Rhythm guitar chords on 2 and 4
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for chord, notes in chord_progression:
            for beat in range(4):
                if beat in [1, 3]:  # Backbeat
                    for note in notes[1:]:
                        tracks['rhythm_guitar'].append(
                            Message(
                                'note_on',
                                note=note + 12,
                                velocity=70,
                                time=time,
                                channel=RHYTHM_GUITAR))
                    time = bars_per_beat // 4
                    for note in notes[1:]:
                        tracks['rhythm_guitar'].append(
                            Message(
                                'note_off',
                                note=note + 12,
                                velocity=0,
                                time=time,
                                channel=RHYTHM_GUITAR))
                    time = bars_per_beat - (bars_per_beat // 4)
                else:
                    time += bars_per_beat

    print("🎹 Hammond B3 Organ - Sustained chords with Leslie...")
    # Organ - sustained chords throughout
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for chord, notes in chord_progression:
            # All chord notes sustained
            for note in notes:
                tracks['organ'].append(
                    Message(
                        'note_on',
                        note=note + 12,
                        velocity=65,
                        time=time,
                        channel=ORGAN))
            time = bars_per_bar - 100
            for note in notes:
                tracks['organ'].append(
                    Message(
                        'note_off',
                        note=note + 12,
                        velocity=0,
                        time=time,
                        channel=ORGAN))
            time = 100

    print("🎹 Piano - Bluesy comping and fills...")
    # Piano - comping with occasional runs
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            # Comp on beats 1 and 3
            for beat in [0, 2]:
                # Play root and fifth
                tracks['piano'].append(
                    Message(
                        'note_on',
                        note=notes[0],
                        velocity=75,
                        time=time,
                        channel=PIANO))
                tracks['piano'].append(
                    Message(
                        'note_on',
                        note=notes[2],
                        velocity=75,
                        time=0,
                        channel=PIANO))
                time = bars_per_beat // 2
                tracks['piano'].append(
                    Message(
                        'note_off',
                        note=notes[0],
                        velocity=0,
                        time=time,
                        channel=PIANO))
                tracks['piano'].append(
                    Message(
                        'note_off',
                        note=notes[2],
                        velocity=0,
                        time=0,
                        channel=PIANO))
                time = bars_per_beat // 2

            # Add bluesy run at end of some bars
            if bar_num in [7, 11]:
                for note in blues_scale[3:7]:
                    tracks['piano'].append(
                        Message(
                            'note_on',
                            note=note + 12,
                            velocity=80,
                            time=time,
                            channel=PIANO))
                    time = bars_per_beat // 8
                    tracks['piano'].append(
                        Message(
                            'note_off',
                            note=note + 12,
                            velocity=0,
                            time=time,
                            channel=PIANO))
                    time = 0

    print("🎵 Walking Bass - Strong foundation...")
    # Bass (same as before)
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for chord, notes in chord_progression:
            root = notes[0]
            pattern = [root, root + 2, notes[2], root + 4]
            for note in pattern:
                tracks['bass'].append(
                    Message(
                        'note_on',
                        note=note - 12,
                        velocity=100,
                        time=time,
                        channel=BASS))
                time = bars_per_beat
                tracks['bass'].append(
                    Message(
                        'note_off',
                        note=note - 12,
                        velocity=0,
                        time=time,
                        channel=BASS))
                time = 0

    print("🎺 Harmonica - Wailing blues harp...")
    # Harmonica - fills and accents
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num in range(12):
            if bar_num in [3, 7, 11]:  # Wailing fills
                for _ in range(3):
                    note = np.random.choice(
                        blues_scale[4:]) + 24  # High register
                    vel = np.random.randint(85, 100)
                    tracks['harmonica'].append(
                        Message(
                            'note_on',
                            note=note,
                            velocity=vel,
                            time=time,
                            channel=HARMONICA))
                    time = bars_per_beat // 3
                    tracks['harmonica'].append(
                        Message(
                            'note_off',
                            note=note,
                            velocity=0,
                            time=time,
                            channel=HARMONICA))
                    time = bars_per_beat // 3
            else:
                time += bars_per_bar

    print("🎷 Saxophone - Horn stabs and riffs...")
    # Sax - horn section stabs
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            # Horn stabs on strong beats
            if bar_num in [0, 4, 8]:  # Chord changes
                for beat in [0, 2]:
                    # Play third and fifth of chord
                    tracks['sax'].append(
                        Message(
                            'note_on',
                            note=notes[1] + 12,
                            velocity=95,
                            time=time,
                            channel=SAX))
                    tracks['sax'].append(
                        Message(
                            'note_on',
                            note=notes[2] + 12,
                            velocity=95,
                            time=0,
                            channel=SAX))
                    time = bars_per_beat // 2
                    tracks['sax'].append(
                        Message(
                            'note_off',
                            note=notes[1] + 12,
                            velocity=0,
                            time=time,
                            channel=SAX))
                    tracks['sax'].append(
                        Message(
                            'note_off',
                            note=notes[2] + 12,
                            velocity=0,
                            time=0,
                            channel=SAX))
                    time = bars_per_beat // 2
            else:
                time += bars_per_bar

    print("🥁 Drums - Full shuffle groove...")
    # Drums (enhanced)
    kick, snare, hihat = 36, 38, 42
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar in range(12):
            for beat in range(4):
                # Kick on 1 and 3
                if beat in [0, 2]:
                    tracks['drums'].append(
                        Message(
                            'note_on',
                            note=kick,
                            velocity=105,
                            time=time,
                            channel=DRUMS))
                    time = 20
                    tracks['drums'].append(
                        Message(
                            'note_off',
                            note=kick,
                            velocity=0,
                            time=time,
                            channel=DRUMS))
                    time = 0

                # Snare on 2 and 4 (backbeat)
                if beat in [1, 3]:
                    tracks['drums'].append(
                        Message(
                            'note_on',
                            note=snare,
                            velocity=100,
                            time=time,
                            channel=DRUMS))
                    time = 20
                    tracks['drums'].append(
                        Message(
                            'note_off',
                            note=snare,
                            velocity=0,
                            time=time,
                            channel=DRUMS))
                    time = 0

                # Shuffle hi-hat
                tracks['drums'].append(
                    Message(
                        'note_on',
                        note=hihat,
                        velocity=65,
                        time=time,
                        channel=DRUMS))
                time = bars_per_beat // 3
                tracks['drums'].append(
                    Message(
                        'note_off',
                        note=hihat,
                        velocity=0,
                        time=time,
                        channel=DRUMS))
                time = bars_per_beat // 6

                tracks['drums'].append(
                    Message(
                        'note_on',
                        note=hihat,
                        velocity=45,
                        time=time,
                        channel=DRUMS))
                time = bars_per_beat // 6
                tracks['drums'].append(
                    Message(
                        'note_off',
                        note=hihat,
                        velocity=0,
                        time=time,
                        channel=DRUMS))
                time = bars_per_beat // 3

    # Save
    output_file = OUTPUT_DIR / "liberty_blues_FULL_BAND.mid"
    mid.save(str(output_file))

    print(f"\n✅ Saved: {output_file}")
    print(f"   {total_bars} bars at {BPM} BPM")
    print(f"   8 INSTRUMENTS: Lead Guitar, Rhythm Guitar, Organ, Piano,")
    print(f"                  Bass, Harmonica, Sax, Drums")
    print()
    return output_file


if __name__ == "__main__":
    create_full_band_midi()
    print("=" * 70)
    print("🎉 FULL BAND VERSION READY!")
    print("=" * 70)
    print("\n💡 Now run the masterpiece mixer to combine with existing vocals!")
