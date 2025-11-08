#!/usr/bin/env python3
"""Quick WAV to MP3 converter using lameenc"""

import sys
from pathlib import Path


def convert_wav_to_mp3_simple(wav_file, mp3_file):
    """Convert WAV to MP3 using scipy and lameenc."""
    import time
    start_time = time.time()
    print(f"Converting {wav_file} to MP3...")

    try:
        import lameenc
        from scipy.io import wavfile
        import math

        sample_rate, audio_data = wavfile.read(wav_file)
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)

        encoder = lameenc.Encoder()
        encoder.set_bit_rate(320)
        encoder.set_in_sample_rate(sample_rate)
        encoder.set_channels(1)
        encoder.set_quality(2)

        # Progress bar setup
        total_samples = len(audio_data)
        chunk_size = 44100 * 10  # 10 seconds per chunk
        mp3_data = b''
        for i in range(0, total_samples, chunk_size):
            chunk = audio_data[i:i+chunk_size]
            mp3_data += encoder.encode(chunk.tobytes())
            percent = (i + chunk_size) / total_samples
            percent = min(percent, 1.0)
            bar = ('#' * int(percent * 40)).ljust(40)
            print(f"\rProgress: [{bar}] {percent*100:.1f}%", end='')
        mp3_data += encoder.flush()
        print("\rProgress: [########################################] 100.0%")

        with open(mp3_file, 'wb') as f:
            f.write(mp3_data)

        end_time = time.time()
        elapsed = end_time - start_time
        size_mb = Path(mp3_file).stat().st_size / (1024 * 1024)
        print(f"\n✅ Saved: {mp3_file}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Time: {elapsed:.2f} seconds")
        print(f"   Speed: {size_mb/elapsed:.2f} MB/sec")

    except ImportError:
        print("⚠️  lameenc not installed. Installing...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'lameenc'])
        print("✅ lameenc installed! Run this script again.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Alternative: Restart your terminal and use:")
        print(f"   ffmpeg -i {wav_file} -codec:a libmp3lame -qscale:a 2 {mp3_file}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        wav_file = sys.argv[1]
        mp3_file = sys.argv[2]
    else:
        wav_file = "../backend/src/assets/generated/liberty_blues_backing.wav"
        mp3_file = "../backend/src/assets/generated/liberty_blues_backing.mp3"

    if not Path(wav_file).exists():
        print(f"❌ WAV file not found: {wav_file}")
        sys.exit(1)

    convert_wav_to_mp3_simple(wav_file, mp3_file)
