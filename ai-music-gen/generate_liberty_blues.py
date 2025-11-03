#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Liberty Vote Blues with full vocals using Bark TTS
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from musicgen.core import generate_music

# Liberty Vote Blues lyrics
lyrics = """
(Verse 1 – 0:00 – 0:15)
Lost my job in the summer of '09,
Factory closed, said they'd be just fine,
Sent my resume to a thousand doors,
No one's hiring for folks like us no more.

(Chorus – 0:15 – 0:35)
It's the Liberty Vote Blues, can't shake it away,
Promises made but they never stay,
From the heartland to the coast, it's the same old song,
We keep voting for hope, but it all goes wrong.

(Verse 2 – 0:35 – 0:50)
Politicians smile, shake your hand real tight,
Say they'll fight for you with all their might,
But come November when the votes are cast,
They disappear just like the past.

(Chorus – 0:50 – 1:10)
It's the Liberty Vote Blues, can't shake it away,
Promises made but they never stay,
From the heartland to the coast, it's the same old song,
We keep voting for hope, but it all goes wrong.

(Bridge – 1:10 – 1:25)
My daddy told me, "Son, don't lose your faith,"
But how much longer can I keep this pace?
The American Dream feels like a lie,
Just trying to survive, not asking why.

(Chorus – 1:25 – 1:45)
It's the Liberty Vote Blues, can't shake it away,
Promises made but they never stay,
From the heartland to the coast, it's the same old song,
We keep voting for hope, but it all goes wrong.

(Outro – 1:45 – 2:00)
So here's my vote, here's my voice tonight,
Maybe someday we'll make it right,
Till then I'll sing these Liberty Blues,
For all of us who've paid our dues.
"""

if __name__ == "__main__":
    print("=" * 70)
    print("🎵 GENERATING LIBERTY VOTE BLUES")
    print("=" * 70)
    print("")
    print("Configuration:")
    print("  Genre:       Blues")
    print("  Tempo:       90 BPM")
    print("  Duration:    2:00 (120 seconds)")
    print("  Vocal Style: Sung (Musical blues voice)")
    print("  Voice:       Bark v2/en_speaker_9 (best for blues)")
    print("  Segments:    7 (Verse, Chorus, Bridge, Outro)")
    print("")
    print("🎸 Instruments:")
    print("   - Synthesized blues guitar, bass, piano")
    print("   - Real instrument samples coming in next update!")
    print("")
    print("⚠️  Note: This will take 10-20 minutes on CPU")
    print("   Bark generates ~2-3 minutes per vocal segment")
    print("")
    print("🎤 Starting generation with Bark vocals...\n")
    
    result = generate_music(
        genre='blues',
        duration=120,
        tempo=90,
        lyrics=lyrics,
        vocal_style='sung',  # Use singing voice instead of spoken
        vocal_artist='AI_Male_1',
        seed=2025
    )
    
    print("\n" + "=" * 70)
    print("✅ GENERATION COMPLETE!")
    print("=" * 70)
    
    print(f"\n📊 Song Details:")
    print(f"   URL:      {result['audio_url']}")
    print(f"   Duration: {result['overview']['rendered_duration']} seconds")
    print(f"   Scale:    {result['overview']['rendered_scale']}")
    print(f"   Tempo:    {result['overview']['rendered_tempo']} BPM")
    
    if result.get('vocal_segments'):
        print(f"\n🎤 Vocal Segments: {len(result['vocal_segments'])}")
        for seg in result['vocal_segments']:
            print(f"   {seg['type']:12} {seg['start']:5.1f}s - {seg['end']:5.1f}s  ({seg['duration']:2.0f}s)")
    
    print(f"\n📂 Files Saved:")
    print(f"   MP3: backend/src/assets/generated/blues_AI_Male_1_2025.mp3")
    print(f"   WAV: backend/src/assets/generated/blues_AI_Male_1_2025.wav")
    
    print(f"\n▶️  Play Now:")
    print(f"   start backend/src/assets/generated/blues_AI_Male_1_2025.mp3")
    print(f"   # or")
    print(f"   ffplay backend/src/assets/generated/blues_AI_Male_1_2025.mp3")
    
    if result.get('warning'):
        print(f"\n⚠️  Warning: {result['warning']}")
    
    print("")
