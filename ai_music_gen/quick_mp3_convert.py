#!/usr/bin/env python3
"""Quick WAV to MP3 converter using lameenc"""

import sys
from pathlib import Path


def convert_wav_to_mp3_simple(wav_file, mp3_file):
    """Convert WAV to MP3 using scipy and lameenc."""
    print(f"Converting {wav_file} to MP3...")

    try:
        # Try using lameenc
        import lameenc
        from scipy.io import wavfile

        # Read WAV
        sample_rate, audio_data = wavfile.read(wav_file)

        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)

        # Create MP3 encoder
        encoder = lameenc.Encoder()
        encoder.set_bit_rate(320)
        encoder.set_in_sample_rate(sample_rate)
        encoder.set_channels(1)
        encoder.set_quality(2)  # High quality

        # Encode
        mp3_data = encoder.encode(audio_data.tobytes())
        mp3_data += encoder.flush()

        # Write MP3
        with open(mp3_file, 'wb') as f:
            f.write(mp3_data)

        print(f"✅ Saved: {mp3_file}")
        size_mb = Path(mp3_file).stat().st_size / (1024 * 1024)
        print(f"   Size: {size_mb:.2f} MB")

    except ImportError:
        print("⚠️  lameenc not installed. Installing...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'lameenc'])
        print("✅ lameenc installed! Run this script again.")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Alternative: Restart your terminal and use:")
        print(
            f"   ffmpeg -i {wav_file} -codec:a libmp3lame -qscale:a 2 {mp3_file}")


if __name__ == "__main__":
    wav_file = "../backend/src/assets/generated/liberty_blues_backing.wav"
    mp3_file = "../backend/src/assets/generated/liberty_blues_backing.mp3"

    if not Path(wav_file).exists():
        print(f"❌ WAV file not found: {wav_file}")
        sys.exit(1)

    convert_wav_to_mp3_simple(wav_file, mp3_file)
