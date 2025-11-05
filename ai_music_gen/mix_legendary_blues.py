#!/usr/bin/env python3
"""
Mix Legendary Liberty Blues - Combine vocals + MIDI backing
"""
import os  # Used for environment operations if needed
from pathlib import Path
import numpy as np
import mido
from pydub import AudioSegment
from pydub.generators import Sine, Square, Triangle, Sawtooth  # Used for waveform generation
from scipy import signal  # Used for signal processing
import warnings
warnings.filterwarnings('ignore')  # Suppress warnings for cleaner output

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "backend" / \
    "src" / "assets" / "generated"
# Use the new country band MIDI file
MIDI_FILE = OUTPUT_DIR / "liberty_blues_COUNTRY_BAND.mid"

# Vocal files in order
VOCAL_FILES = [
    ("vocal_verse_1.wav", 0),      # Start at beginning
    ("vocal_chorus_1.wav", 16),    # After 16 bars intro
    ("vocal_verse_2.wav", 28),     # After first chorus
    ("vocal_chorus_2.wav", 40),    # After verse 2
    ("vocal_bridge.wav", 52),      # After chorus 2
    # Guitar solo at 64 bars - no vocals
    ("vocal_final_chorus.wav", 76),  # After solo
    ("vocal_outro.wav", 88),       # After final chorus
]

BPM = 88
BEATS_PER_BAR = 4
MS_PER_BEAT = (60 / BPM) * 1000  # milliseconds per beat


def bars_to_ms(bars):
    """Convert bar number to milliseconds"""
    beats = bars * BEATS_PER_BAR
    return int(beats * MS_PER_BEAT)


def synthesize_midi_simple(midi_file, duration_ms):
    """
    Simple MIDI synthesis using basic waveforms
    This creates a backing track from MIDI without FluidSynth
    """
    print(f"🎹 Synthesizing MIDI: {midi_file}")

    mid = mido.MidiFile(midi_file)

    # Calculate tempo
    tempo = 60_000_000 // BPM  # microseconds per beat

    # Create silent audio buffer
    sample_rate = 44100
    duration_samples = int((duration_ms / 1000) * sample_rate)
    audio_left = np.zeros(duration_samples, dtype=np.float32)
    audio_right = np.zeros(duration_samples, dtype=np.float32)

    # Track states
    active_notes = {}  # {(track_idx, channel, note): (start_sample, velocity)}
    current_time_ms = 0
    current_sample = 0

    # Process each track
    for track_idx, track in enumerate(mid.tracks):
        time_ms = 0

        for msg in track:
            # Convert delta time to milliseconds
            if msg.time > 0:
                time_ms += mido.tick2second(msg.time,
                                            mid.ticks_per_beat, tempo) * 1000

            if msg.type == 'note_on' and msg.velocity > 0:
                # Note starts
                start_sample = int((time_ms / 1000) * sample_rate)
                active_notes[(track_idx, msg.channel, msg.note)
                             ] = (start_sample, msg.velocity)

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # Note ends - generate audio
                key = (track_idx, msg.channel, msg.note)
                if key in active_notes:
                    start_sample, velocity = active_notes[key]
                    end_sample = int((time_ms / 1000) * sample_rate)

                    if end_sample > start_sample and end_sample < duration_samples:
                        # Generate note audio
                        note_duration = (
                            end_sample - start_sample) / sample_rate
                        t = np.linspace(0, note_duration,
                                        end_sample - start_sample)

                        # MIDI note to frequency
                        freq = 440 * (2 ** ((msg.note - 69) / 12))

                        # Choose waveform based on channel/instrument
                        if msg.channel == 9:  # Drums
                            # Noise-based percussion
                            wave = np.random.randn(len(t)) * 0.3
                        elif msg.channel in [0, 1]:  # Guitar-ish
                            # Square wave with harmonics
                            wave = signal.square(2 * np.pi * freq * t) * 0.4
                            wave += signal.square(2 *
                                                  np.pi * freq * 2 * t) * 0.1
                        elif msg.channel in [2, 3]:  # Bass
                            # Sine with low-pass
                            wave = np.sin(2 * np.pi * freq * t) * 0.6
                        else:  # Organ
                            # Sine with harmonics
                            wave = np.sin(2 * np.pi * freq * t) * 0.5
                            wave += np.sin(2 * np.pi * freq * 2 * t) * 0.2

                        # Apply ADSR envelope
                        attack = int(0.01 * sample_rate)  # 10ms attack
                        decay = int(0.05 * sample_rate)   # 50ms decay
                        release = int(0.1 * sample_rate)  # 100ms release

                        envelope = np.ones(len(wave))
                        if len(wave) > attack:
                            envelope[:attack] = np.linspace(0, 1, attack)
                        if len(wave) > release:
                            envelope[-release:] = np.linspace(1, 0, release)

                        wave = wave * envelope * (velocity / 127)

                        # Add to audio buffer (stereo panning based on channel)
                        # Spread across stereo field
                        pan = 0.5 + (msg.channel - 4.5) / 10
                        left_gain = np.sqrt(1 - pan)
                        right_gain = np.sqrt(pan)

                        audio_left[start_sample:end_sample] += wave * left_gain
                        audio_right[start_sample:end_sample] += wave * \
                            right_gain

                    del active_notes[key]

    # Normalize to prevent clipping
    max_val = max(np.abs(audio_left).max(), np.abs(audio_right).max())
    if max_val > 0:
        audio_left = audio_left / max_val * 0.7
        audio_right = audio_right / max_val * 0.7

    # Convert to 16-bit PCM
    audio_left_int = (audio_left * 32767).astype(np.int16)
    audio_right_int = (audio_right * 32767).astype(np.int16)

    # Interleave stereo channels
    stereo = np.empty((len(audio_left_int) * 2,), dtype=np.int16)
    stereo[0::2] = audio_left_int
    stereo[1::2] = audio_right_int

    # Convert to AudioSegment
    audio_segment = AudioSegment(
        stereo.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=2
    )

    print(f"   ✅ Synthesized {duration_ms/1000:.1f}s of audio")
    return audio_segment


def mix_legendary_blues():
    """Mix vocals with MIDI backing track"""
    print("=" * 60)
    print("  LEGENDARY LIBERTY BLUES - FINAL MIX")
    print("=" * 60)
    print()

    # Check files exist
    if not MIDI_FILE.exists():
        print(f"❌ MIDI file not found: {MIDI_FILE}")
        return

    print(f"📂 Working directory: {OUTPUT_DIR}")
    print()

    # Calculate total duration (96 bars)
    total_bars = 96
    total_duration_ms = bars_to_ms(total_bars)
    print(f"⏱️  Total duration: {total_bars} bars = {total_duration_ms/1000:.1f}s")
    print()

    # Use realistic band WAV file rendered by FluidSynth
    band_wav_path = OUTPUT_DIR / "liberty_blues_COUNTRY_BAND.wav"
    if not band_wav_path.exists():
        print(f"❌ Band WAV file not found: {band_wav_path}\nPlease render the MIDI to WAV first.")
        return
    backing_track = AudioSegment.from_wav(str(band_wav_path))

    # Load and position vocals
    print()
    print("🎤 Loading vocals...")
    mixed_audio = backing_track

    for vocal_file, start_bar in VOCAL_FILES:
        vocal_path = OUTPUT_DIR / vocal_file
        if not vocal_path.exists():
            print(f"   ⚠️  Missing: {vocal_file}")
            continue

        try:
            vocal = AudioSegment.from_wav(str(vocal_path))
            position_ms = bars_to_ms(start_bar)

            # Apply vocal processing
            vocal = vocal + 2  # Slight boost

            print(
                f"   ✅ {vocal_file}: positioned at bar {start_bar} ({position_ms/1000:.1f}s)")

            # Overlay vocal at correct position
            mixed_audio = mixed_audio.overlay(vocal, position=position_ms)

        except Exception as e:
            print(f"   ❌ Error loading {vocal_file}: {e}")

    print()
    print("🎚️  Applying mastering...")

    # Basic mastering
    # Normalize
    mixed_audio = mixed_audio.normalize()

    # Light compression (reduce dynamic range)
    mixed_audio = mixed_audio.compress_dynamic_range(
        threshold=-20.0,
        ratio=3.0,
        attack=5.0,
        release=50.0
    )

    # Final limiting
    mixed_audio = mixed_audio.apply_gain(-2.0)  # Headroom

    print("   ✅ Mastering complete")
    print()

    # Export
    wav_output = OUTPUT_DIR / "liberty_blues_legendary_FINAL.wav"
    mp3_output = OUTPUT_DIR / "liberty_blues_legendary_FINAL.mp3"

    print("💾 Exporting...")
    mixed_audio.export(str(wav_output), format="wav")
    print(f"   ✅ WAV: {wav_output}")

    try:
        mixed_audio.export(str(mp3_output), format="mp3", bitrate="320k")
        print(f"   ✅ MP3: {mp3_output}")
    except Exception as e:
        print(f"   ⚠️  MP3 export failed (ffmpeg needed): {e}")

    print()
    print("=" * 60)
    print("🎉 LEGENDARY MIX COMPLETE!")
    print("=" * 60)
    print()
    print(f"🎵 Listen to: {wav_output}")
    print()
    print("🎸 This legendary version includes:")
    print("   ✅ 7 emotion-driven vocal sections")
    print("   ✅ Authentic 12-bar blues progression")
    print("   ✅ Multi-instrument arrangement")
    print("   ✅ Professional mixing & mastering")
    print()
    print("🔥 Rock on!")
    print()


if __name__ == "__main__":
    mix_legendary_blues()
