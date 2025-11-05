#!/usr/bin/env python3
"""
Test script for vocal synthesis integration.
Demonstrates how to generate music with your custom lyrics using Bark TTS.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from musicgen.core import generate_music

# Your "Liberty Vote Blues" lyrics
LIBERTY_VOTE_BLUES_LYRICS = """
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


def test_basic_vocal_generation():
    """Test basic vocal generation with default settings."""
    print("\n=== Test 1: Basic Vocal Generation ===")
    print("Generating blues track with Liberty Vote Blues lyrics...")
    
    result = generate_music(
        genre='blues',
        duration=120,  # 2 minutes for full song
        tempo=90,      # Slow blues tempo
        lyrics=LIBERTY_VOTE_BLUES_LYRICS,
        vocal_style='spoken',
        vocal_artist='AI_Male_1',
        seed=42
    )
    
    print(f"✓ Generated track: {result['overview']['duration']} seconds")
    print(f"✓ Audio URL: {result['audio_url']}")
    print(f"✓ Vocal info: {result.get('vocals')}")
    
    if result.get('vocal_segments'):
        print(f"✓ Vocal segments parsed: {len(result['vocal_segments'])}")
        for seg in result['vocal_segments']:
            print(f"  - {seg['type']}: {seg['start']}s - {seg['end']}s")
    
    if result.get('warning'):
        print(f"⚠ Warning: {result['warning']}")
    
    return result


def test_instrumental_only():
    """Test that instrumental generation still works without lyrics."""
    print("\n=== Test 2: Instrumental Only (No Lyrics) ===")
    print("Generating instrumental blues track...")
    
    result = generate_music(
        genre='blues',
        duration=30,
        tempo=90,
        seed=123
    )
    
    print(f"✓ Generated instrumental: {result['overview']['duration']} seconds")
    print(f"✓ Audio URL: {result['audio_url']}")
    print(f"✓ No vocal segments: {result.get('vocal_segments') is None}")
    
    return result


def test_different_vocal_styles():
    """Test different vocal style options."""
    print("\n=== Test 3: Different Vocal Styles ===")
    
    short_lyrics = """
(Verse 1 – 0:00 – 0:10)
This is a test of the vocal system,
Listen closely to the rhythm.
"""
    
    for style in ['spoken', 'sung', 'rap']:
        print(f"\nTesting vocal_style='{style}'...")
        result = generate_music(
            genre='pop',
            duration=15,
            tempo=120,
            lyrics=short_lyrics,
            vocal_style=style,
            seed=999
        )
        print(f"✓ Generated with {style} style")
        if result.get('vocals'):
            vocal_data = result['vocals']
            if isinstance(vocal_data, dict):
                print(f"  Style recorded: {vocal_data.get('style')}")


def main():
    """Run all vocal tests."""
    print("=" * 60)
    print("VOCAL SYNTHESIS TEST SUITE")
    print("=" * 60)
    
    try:
        # Test 1: Full song with lyrics
        result1 = test_basic_vocal_generation()
        
        # Test 2: Instrumental (backward compatibility)
        result2 = test_instrumental_only()
        
        # Test 3: Different styles
        test_different_vocal_styles()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED")
        print("=" * 60)
        
        print("\n📝 NEXT STEPS TO ADD REAL VOCALS:")
        print("1. Install a TTS library:")
        print("   pip install bark-tts  # Best for singing")
        print("   # OR")
        print("   pip install TTS  # Coqui TTS for speech")
        
        print("\n2. Update engines/vocals.py:")
        print("   - Replace generate_vocals_placeholder() with real TTS")
        print("   - Add timing sync to match lyric segments")
        print("   - Adjust pitch/tempo to match instrumental")
        
        print("\n3. For production vocals:")
        print("   - Use Bark for natural singing: github.com/suno-ai/bark")
        print("   - Or commercial API: Suno, Chirp, ElevenLabs")
        
        print("\n4. Test your song:")
        print("   python ai-music-gen/test_vocals.py")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
