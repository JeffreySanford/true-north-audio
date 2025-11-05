#!/usr/bin/env python3
"""
Quick test of Bark vocal synthesis.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engines.vocals import generate_vocals_placeholder

# Simple test lyrics
test_lyrics = """
(Verse 1 – 0:00 – 0:06)
Hello, this is a test.
Testing Bark vocal synthesis.
"""

print("=" * 60)
print("BARK VOCAL SYNTHESIS TEST")
print("=" * 60)
print("\nThis will:")
print("1. Download Bark models on first run (~1GB, takes 1-2 min)")
print("2. Generate vocals for test lyrics")
print("3. Save a WAV file\n")

input("Press Enter to start...")

print("\nGenerating vocals...")
result = generate_vocals_placeholder(
    lyrics=test_lyrics,
    duration=10,
    sample_rate=24000,  # Use Bark's native rate for faster processing
    vocal_style='spoken'
)

print(f"\n✅ Generation complete!")
print(f"   Waveform shape: {result['waveform'].shape}")
print(f"   Sample rate: {result['sample_rate']}Hz")
print(f"   Segments: {len(result['segments'])}")
print(f"   Note: {result['note']}")

# Check if audio is not silent
variance = result['waveform'].var()
print(f"   Variance: {variance:.6f} {'(has audio!)' if variance > 0.001 else '(silent)'}")

# Save to file
import wave
import numpy as np

output_path = "test_bark_output.wav"
int_waveform = np.int16(result['waveform'] * 32767)

with wave.open(output_path, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(result['sample_rate'])
    wf.writeframes(int_waveform.tobytes())

print(f"\n💾 Saved to: {output_path}")
print("\nPlay it with:")
print(f"   ffplay {output_path}")
print("   # or any audio player")
