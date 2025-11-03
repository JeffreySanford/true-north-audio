#!/usr/bin/env python3
"""
Convert Liberty Blues MIDI to WAV and MP3
Uses Python libraries for conversion (no external dependencies)
"""

import os
import sys
from pathlib import Path
import subprocess


def check_dependencies():
    """Check what tools are available."""
    tools = {}

    # Check for FluidSynth
    try:
        result = subprocess.run(['fluidsynth', '--version'],
                                capture_output=True, text=True)
        tools['fluidsynth'] = True
        print("✅ FluidSynth found")
    except BaseException:
        tools['fluidsynth'] = False
        print("⚠️  FluidSynth not found")

    # Check for FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                                capture_output=True, text=True)
        tools['ffmpeg'] = True
        print("✅ FFmpeg found")
    except BaseException:
        tools['ffmpeg'] = False
        print("⚠️  FFmpeg not found")

    # Check Python packages
    try:
        import mido
        tools['mido'] = True
        print("✅ mido (MIDI) found")
    except BaseException:
        tools['mido'] = False
        print("⚠️  mido not found")

    try:
        import numpy
        tools['numpy'] = True
        print("✅ numpy found")
    except BaseException:
        tools['numpy'] = False
        print("⚠️  numpy not found")

    try:
        from pydub import AudioSegment
        tools['pydub'] = True
        print("✅ pydub found")
    except BaseException:
        tools['pydub'] = False
        print("⚠️  pydub not found")

    try:
        from scipy.io import wavfile
        tools['scipy'] = True
        print("✅ scipy found")
    except BaseException:
        tools['scipy'] = False
        print("⚠️  scipy not found")

    return tools


def install_pydub():
    """Install pydub if not available."""
    print("\n📦 Installing pydub for audio conversion...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pydub'])


def convert_midi_to_wav_simple(midi_file, wav_file, duration=160):
    """
    Simple MIDI to WAV conversion using synthesized tones.
    Not perfect but works without external dependencies.
    """
    print(f"\n🎵 Converting MIDI to WAV (simple synthesis)...")

    import mido
    import numpy as np
    from scipy.io import wavfile

    # Load MIDI file
    mid = mido.MidiFile(midi_file)

    # Audio settings
    sample_rate = 48000
    duration_samples = int(duration * sample_rate)
    audio = np.zeros(duration_samples, dtype=np.float32)

    # Track time and active notes
    time = 0.0
    active_notes = {}
    tempo = 500000  # Default tempo (120 BPM)

    print(f"   Processing {len(mid.tracks)} MIDI tracks...")

    for i, track in enumerate(mid.tracks):
        time = 0.0

        for msg in track:
            # Update time
            time += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)

            if msg.type == 'set_tempo':
                tempo = msg.tempo

            elif msg.type == 'note_on' and msg.velocity > 0:
                # Start note
                active_notes[msg.note] = {
                    'start': time, 'velocity': msg.velocity}

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                # End note - generate tone
                if msg.note in active_notes:
                    note_info = active_notes[msg.note]
                    start_time = note_info['start']
                    end_time = time
                    velocity = note_info['velocity']

                    # Generate sine wave for this note
                    freq = 440 * (2 ** ((msg.note - 69) / 12))  # A4 = 440Hz

                    start_sample = int(start_time * sample_rate)
                    end_sample = int(end_time * sample_rate)

                    if end_sample > len(audio):
                        end_sample = len(audio)

                    if start_sample < len(audio):
                        duration_note = end_sample - start_sample
                        t = np.arange(duration_note) / sample_rate

                        # Simple ADSR envelope
                        attack = int(0.01 * sample_rate)
                        decay = int(0.1 * sample_rate)
                        release = int(0.2 * sample_rate)

                        envelope = np.ones(duration_note)
                        if duration_note > attack:
                            envelope[:attack] = np.linspace(0, 1, attack)
                        if duration_note > attack + decay:
                            envelope[attack:attack +
                                     decay] = np.linspace(1, 0.7, decay)
                        if duration_note > release:
                            envelope[-release:] = np.linspace(0.7, 0, release)

                        # Generate tone
                        amplitude = (velocity / 127.0) * 0.3
                        wave = amplitude * \
                            np.sin(2 * np.pi * freq * t) * envelope

                        # Add to audio
                        audio[start_sample:end_sample] += wave

                    del active_notes[msg.note]

    # Normalize audio
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.8

    # Convert to 16-bit PCM
    audio_int16 = (audio * 32767).astype(np.int16)

    # Save WAV file
    wavfile.write(wav_file, sample_rate, audio_int16)
    print(f"✅ Saved WAV: {wav_file}")

    return wav_file


def convert_wav_to_mp3(wav_file, mp3_file):
    """Convert WAV to MP3 using pydub."""
    print(f"\n🎵 Converting WAV to MP3...")

    try:
        from pydub import AudioSegment

        # Load WAV
        audio = AudioSegment.from_wav(wav_file)

        # Export as MP3
        audio.export(mp3_file, format='mp3', bitrate='320k')

        print(f"✅ Saved MP3: {mp3_file}")
        return mp3_file

    except Exception as e:
        print(f"❌ Error converting to MP3: {e}")
        print("   You can convert manually with: ffmpeg -i input.wav output.mp3")
        return None


def main():
    print("=" * 60)
    print("🎸 LIBERTY BLUES - MIDI to WAV/MP3 Converter")
    print("=" * 60)

    # Check dependencies
    print("\n📋 Checking dependencies...")
    tools = check_dependencies()

    # File paths
    midi_file = Path(
        "../backend/src/assets/generated/liberty_blues_backing.mid")
    wav_file = Path(
        "../backend/src/assets/generated/liberty_blues_backing.wav")
    mp3_file = Path(
        "../backend/src/assets/generated/liberty_blues_backing.mp3")

    if not midi_file.exists():
        print(f"\n❌ Error: MIDI file not found: {midi_file}")
        print("   Run generate_liberty_blues_bark.py first!")
        return

    print(f"\n📂 Input:  {midi_file}")
    print(f"📂 Output: {wav_file}")
    print(f"📂 Output: {mp3_file}")

    # Convert MIDI to WAV
    if not tools['mido'] or not tools['numpy'] or not tools['scipy']:
        print("\n❌ Missing required packages!")
        print("   Install with: pip install mido numpy scipy")
        return

    try:
        convert_midi_to_wav_simple(str(midi_file), str(wav_file))
    except Exception as e:
        print(f"\n❌ Error converting MIDI to WAV: {e}")
        import traceback
        traceback.print_exc()
        return

    # Convert WAV to MP3
    if not tools['pydub']:
        print("\n⚠️  pydub not installed. Installing now...")
        install_pydub()
        tools['pydub'] = True

    if tools['pydub']:
        try:
            convert_wav_to_mp3(str(wav_file), str(mp3_file))
        except Exception as e:
            print(f"\n⚠️  MP3 conversion failed: {e}")
            print("   WAV file is still available!")

    # Summary
    print("\n" + "=" * 60)
    print("✅ CONVERSION COMPLETE!")
    print("=" * 60)

    if wav_file.exists():
        size_mb = wav_file.stat().st_size / (1024 * 1024)
        print(f"\n✅ WAV: {wav_file.name} ({size_mb:.2f} MB)")

    if mp3_file.exists():
        size_mb = mp3_file.stat().st_size / (1024 * 1024)
        print(f"✅ MP3: {mp3_file.name} ({size_mb:.2f} MB)")

    print("\n▶️  Play with:")
    print(f"   start {wav_file}")
    print(f"   # or")
    print(f"   start {mp3_file}")

    print("\n💡 Note: This uses simple synthesis. For better quality:")
    print("   1. Install FluidSynth: winget install FluidSynth")
    print("   2. Download a soundfont (e.g., FluidR3_GM.sf2)")
    print("   3. Use: fluidsynth -F output.wav soundfont.sf2 input.mid")


if __name__ == "__main__":
    main()
