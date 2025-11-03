#!/usr/bin/env python3
"""
Simple mixer using scipy.io.wavfile (no ffmpeg needed)
"""
import os
from pathlib import Path
import numpy as np
from scipy.io import wavfile
import warnings
warnings.filterwarnings('ignore')

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "backend" / \
    "src" / "assets" / "generated"

# Vocal files
VOCAL_FILES = [
    "vocal_verse_1.wav",
    "vocal_chorus_1.wav",
    "vocal_verse_2.wav",
    "vocal_chorus_2.wav",
    "vocal_bridge.wav",
    "vocal_final_chorus.wav",
    "vocal_outro.wav"
]


def load_wav(filepath):
    """Load WAV file using scipy"""
    try:
        rate, data = wavfile.read(str(filepath))
        # Convert to float32
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
        elif data.dtype == np.int32:
            data = data.astype(np.float32) / 2147483648.0
        return rate, data
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None, None


def save_wav(filepath, rate, data):
    """Save WAV file using scipy"""
    # Convert to int16
    data = np.clip(data, -1.0, 1.0)
    data_int16 = (data * 32767).astype(np.int16)
    wavfile.write(str(filepath), rate, data_int16)


def concatenate_vocals():
    """Concatenate all vocal files into one"""
    print("=" * 60)
    print("  VOCAL CONCATENATION")
    print("=" * 60)
    print()
    print(f"📂 Directory: {OUTPUT_DIR}")
    print()

    all_audio = []
    sample_rate = None

    for vocal_file in VOCAL_FILES:
        vocal_path = OUTPUT_DIR / vocal_file
        if not vocal_path.exists():
            print(f"   ⚠️  Missing: {vocal_file}")
            continue

        print(f"   📥 Loading: {vocal_file}")
        rate, data = load_wav(vocal_path)

        if rate is None:
            continue

        if sample_rate is None:
            sample_rate = rate

        # Convert mono to stereo if needed
        if len(data.shape) == 1:
            data = np.column_stack([data, data])

        all_audio.append(data)
        print(f"       Duration: {len(data)/rate:.2f}s, Shape: {data.shape}")

    if not all_audio:
        print("❌ No audio loaded!")
        return

    print()
    print("🎵 Concatenating...")
    combined = np.vstack(all_audio)

    print(f"   Total duration: {len(combined)/sample_rate:.2f}s")
    print(f"   Sample rate: {sample_rate} Hz")
    print(
        f"   Channels: {combined.shape[1] if len(combined.shape) > 1 else 1}")
    print()

    # Save
    output_file = OUTPUT_DIR / "liberty_blues_vocals_COMPLETE.wav"
    print(f"💾 Saving: {output_file}")
    save_wav(output_file, sample_rate, combined)

    print()
    print("=" * 60)
    print("✅ DONE!")
    print("=" * 60)
    print()
    print(f"🎵 Listen to: {output_file}")
    print()

    return output_file


if __name__ == "__main__":
    output = concatenate_vocals()

    # Play it!
    if output and output.exists():
        print("🔊 Playing audio...")
        os.system(
            f'powershell -c "(New-Object Media.SoundPlayer \\"{output}\\").PlaySync()"')
