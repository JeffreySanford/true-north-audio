#!/usr/bin/env python3
"""
Liberty Blues - MASSIVE BLUES ORCHESTRA
Expanding to 15+ instruments for huge Chicago blues sound!
"""
import os
from pathlib import Path
import numpy as np
import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = Path(__file__).parent.parent / "backend" / \
    "src" / "assets" / "generated"

BPM = 88
BEATS_PER_BAR = 4
TICKS_PER_BEAT = 480

print("=" * 70)
print("  🎺 LIBERTY BLUES - MASSIVE ORCHESTRA VERSION 🎺")
print("=" * 70)
print()
print("Adding 15+ instruments for huge Chicago blues sound!")
print()


def create_massive_orchestra_midi():
    """Create MASSIVE blues orchestra arrangement"""

    mid = MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    tempo = int(60_000_000 / BPM)

    # MASSIVE Channel assignments (using all 16 MIDI channels!)
    LEAD_GUITAR = 0
    RHYTHM_GUITAR = 1
    ORGAN = 2
    PIANO = 3
    BASS = 4
    HARMONICA = 5
    SAX_TENOR = 6
    SAX_BARI = 7
    TRUMPET = 8
    DRUMS = 9          # Channel 9 is always drums
    TROMBONE = 10
    CONGA_BONGO = 11   # Percussion
    ELECTRIC_PIANO = 12
    SYNTH_PAD = 13      # Atmospheric pad
    BRASS_SECTION = 14  # Combined brass hits
    PERCUSSION = 15     # Extra percussion

    print("🎵 MASSIVE INSTRUMENT LINEUP:")
    print("   1. Lead Guitar (electric blues)")
    print("   2. Rhythm Guitar (choppy shuffle)")
    print("   3. Hammond B3 Organ (with Leslie)")
    print("   4. Acoustic Piano (bluesy comping)")
    print("   5. Electric Bass (walking)")
    print("   6. Harmonica (blues harp)")
    print("   7. Tenor Saxophone (lead horn)")
    print("   8. Baritone Sax (low horn)")
    print("   9. Trumpet (high horn)")
    print("   10. Full Drum Kit (shuffle groove)")
    print("   11. Trombone (mid horn)")
    print("   12. Congas/Bongos (latin percussion)")
    print("   13. Electric Piano (Rhodes-style)")
    print("   14. Synth Pad (atmospheric)")
    print("   15. Brass Section (horn hits)")
    print("   16. Extra Percussion (shaker, tambourine)")
    print()

    # Create tracks for ALL instruments
    tracks = {
        'lead_guitar': MidiTrack(),
        'rhythm_guitar': MidiTrack(),
        'organ': MidiTrack(),
        'piano': MidiTrack(),
        'bass': MidiTrack(),
        'harmonica': MidiTrack(),
        'sax_tenor': MidiTrack(),
        'sax_bari': MidiTrack(),
        'trumpet': MidiTrack(),
        'drums': MidiTrack(),
        'trombone': MidiTrack(),
        'conga_bongo': MidiTrack(),
        'electric_piano': MidiTrack(),
        'synth_pad': MidiTrack(),
        'brass_section': MidiTrack(),
        'percussion': MidiTrack()
    }

    for track in tracks.values():
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        mid.tracks.append(track)

    # E minor blues scale
    blues_scale = [52, 55, 57, 58, 59, 62, 64, 67, 69, 71]

    # 12-bar blues progression in E minor
    chord_progression = [
        ('Em7', [52, 55, 59, 62]),
        ('Em7', [52, 55, 59, 62]),
        ('Em7', [52, 55, 59, 62]),
        ('Em7', [52, 55, 59, 62]),
        ('Am7', [45, 48, 52, 55]),
        ('Am7', [45, 48, 52, 55]),
        ('Em7', [52, 55, 59, 62]),
        ('Em7', [52, 55, 59, 62]),
        ('Bm7', [47, 50, 54, 57]),
        ('Am7', [45, 48, 52, 55]),
        ('Em7', [52, 55, 59, 62]),
        ('Bm7', [47, 50, 54, 57]),
    ]

    bars_per_beat = TICKS_PER_BEAT
    bars_per_bar = bars_per_beat * BEATS_PER_BAR

    num_choruses = 9
    total_bars = num_choruses * 12 + 16

    print("🎸 Building massive arrangement...")

    # 1. LEAD GUITAR - Blues licks with bends
    print("   Adding Lead Guitar...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [3, 7, 11]:
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

    # 2. RHYTHM GUITAR - Choppy chords
    print("   Adding Rhythm Guitar...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for chord, notes in chord_progression:
            for beat in range(4):
                if beat in [1, 3]:
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

    # 3. HAMMOND B3 ORGAN - Sustained chords
    print("   Adding Hammond B3 Organ...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for chord, notes in chord_progression:
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

    # 4. ACOUSTIC PIANO - Comping
    print("   Adding Piano...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            for beat in [0, 2]:
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

    # 5. BASS - Walking pattern
    print("   Adding Bass...")
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

    # 6. HARMONICA - Wailing fills
    print("   Adding Harmonica...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num in range(12):
            if bar_num in [3, 7, 11]:
                for _ in range(3):
                    note = np.random.choice(blues_scale[4:]) + 24
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

    # 7. TENOR SAX - Lead horn lines
    print("   Adding Tenor Sax...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [0, 4, 8]:
                tracks['sax_tenor'].append(
                    Message(
                        'note_on',
                        note=notes[2] + 12,
                        velocity=95,
                        time=time,
                        channel=SAX_TENOR))
                time = bars_per_bar // 2
                tracks['sax_tenor'].append(
                    Message(
                        'note_off',
                        note=notes[2] + 12,
                        velocity=0,
                        time=time,
                        channel=SAX_TENOR))
                time = bars_per_bar // 2
            else:
                time += bars_per_bar

    # 8. BARITONE SAX - Low horn foundation
    print("   Adding Baritone Sax...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [0, 4, 8]:
                tracks['sax_bari'].append(
                    Message(
                        'note_on',
                        note=notes[0] + 12,
                        velocity=90,
                        time=time,
                        channel=SAX_BARI))
                time = bars_per_bar // 2
                tracks['sax_bari'].append(
                    Message(
                        'note_off',
                        note=notes[0] + 12,
                        velocity=0,
                        time=time,
                        channel=SAX_BARI))
                time = bars_per_bar // 2
            else:
                time += bars_per_bar

    # 9. TRUMPET - High horn accents
    print("   Adding Trumpet...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [0, 4, 8]:
                for beat in [0, 2]:
                    tracks['trumpet'].append(
                        Message(
                            'note_on',
                            note=notes[3] + 12,
                            velocity=100,
                            time=time,
                            channel=TRUMPET))
                    time = bars_per_beat // 4
                    tracks['trumpet'].append(
                        Message(
                            'note_off',
                            note=notes[3] + 12,
                            velocity=0,
                            time=time,
                            channel=TRUMPET))
                    time = (bars_per_beat * 3) // 4
            else:
                time += bars_per_bar

    # 10. DRUMS - Full shuffle kit
    print("   Adding Drums...")
    kick, snare, hihat, crash = 36, 38, 42, 49
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar in range(12):
            # Crash on first beat of new sections
            if bar in [0, 4, 8]:
                tracks['drums'].append(
                    Message(
                        'note_on',
                        note=crash,
                        velocity=110,
                        time=time,
                        channel=DRUMS))
                time = 20
                tracks['drums'].append(
                    Message(
                        'note_off',
                        note=crash,
                        velocity=0,
                        time=time,
                        channel=DRUMS))
                time = 0

            for beat in range(4):
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

    # 11. TROMBONE - Mid-range horn
    print("   Adding Trombone...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [0, 4, 8]:
                tracks['trombone'].append(
                    Message(
                        'note_on',
                        note=notes[1],
                        velocity=88,
                        time=time,
                        channel=TROMBONE))
                time = bars_per_bar // 2
                tracks['trombone'].append(
                    Message(
                        'note_off',
                        note=notes[1],
                        velocity=0,
                        time=time,
                        channel=TROMBONE))
                time = bars_per_bar // 2
            else:
                time += bars_per_bar

    # 12. CONGAS/BONGOS - Latin percussion accent
    print("   Adding Congas/Bongos...")
    conga_low, conga_high = 64, 65
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar in range(12):
            for beat in range(4):
                if beat in [1, 3]:  # Syncopated accents
                    note = conga_high if beat == 1 else conga_low
                    tracks['conga_bongo'].append(
                        Message(
                            'note_on',
                            note=note,
                            velocity=75,
                            time=time,
                            channel=CONGA_BONGO))
                    time = bars_per_beat // 4
                    tracks['conga_bongo'].append(
                        Message(
                            'note_off',
                            note=note,
                            velocity=0,
                            time=time,
                            channel=CONGA_BONGO))
                    time = (bars_per_beat * 3) // 4
                else:
                    time += bars_per_beat

    # 13. ELECTRIC PIANO (Rhodes) - Sparkly fills
    print("   Adding Electric Piano...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [5, 11]:  # Occasional fills
                for note in [notes[1], notes[2], notes[3]]:
                    tracks['electric_piano'].append(
                        Message(
                            'note_on',
                            note=note + 24,
                            velocity=70,
                            time=time,
                            channel=ELECTRIC_PIANO))
                    time = bars_per_beat // 6
                    tracks['electric_piano'].append(
                        Message(
                            'note_off',
                            note=note + 24,
                            velocity=0,
                            time=time,
                            channel=ELECTRIC_PIANO))
                    time = 0
            time += bars_per_bar

    # 14. SYNTH PAD - Atmospheric background
    print("   Adding Synth Pad...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for chord, notes in chord_progression:
            # Sustained pad notes
            for note in notes:
                tracks['synth_pad'].append(
                    Message(
                        'note_on',
                        note=note + 24,
                        velocity=40,
                        time=time,
                        channel=SYNTH_PAD))
            time = bars_per_bar - 100
            for note in notes:
                tracks['synth_pad'].append(
                    Message(
                        'note_off',
                        note=note + 24,
                        velocity=0,
                        time=time,
                        channel=SYNTH_PAD))
            time = 100

    # 15. BRASS SECTION - Big hits
    print("   Adding Brass Section...")
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar_num, (chord, notes) in enumerate(chord_progression):
            if bar_num in [0, 4, 8, 11]:  # Big section hits
                # Hit all chord tones
                for note in notes:
                    tracks['brass_section'].append(
                        Message(
                            'note_on',
                            note=note + 12,
                            velocity=105,
                            time=time,
                            channel=BRASS_SECTION))
                time = bars_per_beat
                for note in notes:
                    tracks['brass_section'].append(
                        Message(
                            'note_off',
                            note=note + 12,
                            velocity=0,
                            time=time,
                            channel=BRASS_SECTION))
                time = bars_per_bar - bars_per_beat
            else:
                time += bars_per_bar

    # 16. EXTRA PERCUSSION - Shaker, tambourine
    print("   Adding Extra Percussion...")
    shaker = 70
    time = bars_per_bar * 16
    for chorus in range(num_choruses):
        for bar in range(12):
            for beat in range(4):
                # Continuous 16th note shaker
                for _ in range(4):
                    tracks['percussion'].append(
                        Message(
                            'note_on',
                            note=shaker,
                            velocity=55,
                            time=time,
                            channel=PERCUSSION))
                    time = bars_per_beat // 4
                    tracks['percussion'].append(
                        Message(
                            'note_off',
                            note=shaker,
                            velocity=0,
                            time=time,
                            channel=PERCUSSION))
                    time = 0

    # Save
    output_file = OUTPUT_DIR / "liberty_blues_MASSIVE_ORCHESTRA.mid"
    mid.save(str(output_file))

    print()
    print("=" * 70)
    print(f"✅ SAVED: {output_file}")
    print(f"   {total_bars} bars at {BPM} BPM")
    print(f"   16 INSTRUMENTS - Massive blues orchestra!")
    print("=" * 70)
    return output_file


if __name__ == "__main__":
    create_massive_orchestra_midi()
    print("\n🎺 MASSIVE ORCHESTRA READY!")
    print("   Now update the masterpiece script to use this MIDI file!")
