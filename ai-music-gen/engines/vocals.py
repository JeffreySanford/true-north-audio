"""
Vocal synthesis engine using TTS (text-to-speech) for spoken/sung lyrics.
Integrates with the music generation pipeline.

Uses Bark for realistic vocal synthesis.
"""

import numpy as np
from typing import Optional, Dict, List
import re
import os
import warnings

# Fix PyTorch 2.6 weights_only issue with Bark models
import torch
if hasattr(torch.serialization, 'add_safe_globals'):
    # Register numpy types as safe for Bark model loading
    try:
        import numpy.core.multiarray
        torch.serialization.add_safe_globals([numpy.core.multiarray.scalar])
        print("[Vocals] Registered numpy types for PyTorch safe loading")
    except Exception as e:
        print(f"[Vocals] Warning: Could not register safe globals: {e}")

# Try to import Bark
try:
    from bark import SAMPLE_RATE as BARK_SAMPLE_RATE, generate_audio, preload_models
    BARK_AVAILABLE = True
    print("[Vocals] Bark TTS loaded successfully")
except ImportError:
    BARK_AVAILABLE = False
    print("[Vocals] Warning: Bark not available. Install with: pip install git+https://github.com/suno-ai/bark.git")


def parse_lyrics_with_timing(lyrics: str) -> List[Dict[str, any]]:
    """
    Parse lyrics with timing information.
    Format: (Section – start_time – end_time)
    Lyrics text
    
    Returns list of segments with {type, start, end, text}
    """
    segments = []
    lines = lyrics.strip().split('\n')
    
    current_segment = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Match timing header: (Section – 0:00 – 0:06)
        timing_match = re.match(r'\(([^–]+)–\s*(\d+:\d+)\s*–\s*(\d+:\d+)\)', line)
        if timing_match:
            section_type = timing_match.group(1).strip()
            start_str = timing_match.group(2)
            end_str = timing_match.group(3)
            
            # Convert time to seconds
            start_parts = start_str.split(':')
            start_sec = int(start_parts[0]) * 60 + int(start_parts[1])
            
            end_parts = end_str.split(':')
            end_sec = int(end_parts[0]) * 60 + int(end_parts[1])
            
            if current_segment:
                segments.append(current_segment)
            
            current_segment = {
                'type': section_type,
                'start': start_sec,
                'end': end_sec,
                'duration': end_sec - start_sec,
                'text': ''
            }
        else:
            # Add to current segment text
            if current_segment:
                if current_segment['text']:
                    current_segment['text'] += '\n'
                current_segment['text'] += line
    
    if current_segment:
        segments.append(current_segment)
    
    return segments


def generate_vocals_placeholder(
    lyrics: str,
    duration: int,
    sample_rate: int = 32000,
    vocal_style: str = "spoken"
) -> Dict[str, any]:
    """
    Generate vocal audio from lyrics using Bark TTS.
    
    Uses Bark (https://github.com/suno-ai/bark) for realistic TTS.
    Falls back to placeholder if Bark not available.
    
    Args:
        lyrics: Full lyrics text with optional timing
        duration: Target duration in seconds
        sample_rate: Audio sample rate (will resample from Bark's 24kHz)
        vocal_style: "spoken", "sung", "rap"
    
    Returns:
        Dict with 'waveform', 'sample_rate', 'segments'
    """
    segments = parse_lyrics_with_timing(lyrics)
    
    if not BARK_AVAILABLE:
        # Fallback to silence placeholder
        print("[Vocals] Using placeholder (Bark not available)")
        waveform = np.zeros(duration * sample_rate, dtype=np.float32)
        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'segments': segments,
            'vocal_style': vocal_style,
            'note': 'Placeholder: Install Bark for actual vocals'
        }
    
    # Generate vocals with Bark
    print(f"[Vocals] Generating with Bark (style: {vocal_style})")
    try:
        # Preload models on first use
        if not hasattr(generate_vocals_placeholder, '_models_loaded'):
            print("[Vocals] Loading Bark models (first run takes ~30s)...")
            
            # Fix PyTorch 2.6 weights_only loading issue
            # Bark's models use numpy types that need to be explicitly allowed
            import torch
            original_load = torch.load
            
            def patched_load(*args, **kwargs):
                """Patch torch.load to use weights_only=False for Bark models"""
                kwargs['weights_only'] = False
                return original_load(*args, **kwargs)
            
            # Temporarily patch torch.load
            torch.load = patched_load
            try:
                preload_models()
                print("[Vocals] Bark models loaded!")
            finally:
                # Restore original torch.load
                torch.load = original_load
            
            generate_vocals_placeholder._models_loaded = True
        
        # Create full waveform at Bark's native sample rate
        bark_waveform = np.zeros(int(duration * BARK_SAMPLE_RATE), dtype=np.float32)
        
        # Select voice based on style
        voice_presets = {
            'spoken': 'v2/en_speaker_6',  # Clear male voice
            'sung': 'v2/en_speaker_9',    # Musical voice
            'rap': 'v2/en_speaker_3'      # Rhythmic voice
        }
        voice = voice_presets.get(vocal_style, 'v2/en_speaker_6')
        
        # Generate each segment
        for i, segment in enumerate(segments):
            text = segment['text'].strip()
            if not text:
                continue
            
            print(f"[Vocals] Generating {segment['type']}: \"{text[:40]}...\"")
            
            # Generate audio for this segment
            try:
                # Patch torch.load for Bark's weights_only issue
                import torch
                original_load = torch.load
                torch.load = lambda *args, **kwargs: original_load(*args, **{**kwargs, 'weights_only': False})
                
                try:
                    audio_array = generate_audio(text, history_prompt=voice)
                finally:
                    torch.load = original_load
                
                # Place in timeline
                start_samples = int(segment['start'] * BARK_SAMPLE_RATE)
                segment_len = len(audio_array)
                end_samples = min(start_samples + segment_len, len(bark_waveform))
                
                # Mix into waveform
                bark_waveform[start_samples:end_samples] = audio_array[:end_samples - start_samples]
                
                print(f"[Vocals]   ✓ Generated {len(audio_array)/BARK_SAMPLE_RATE:.1f}s at {segment['start']}s")
            except Exception as e:
                print(f"[Vocals]   ✗ Error generating segment: {e}")
                continue
        
        # Resample to target sample rate if needed
        if BARK_SAMPLE_RATE != sample_rate:
            print(f"[Vocals] Resampling from {BARK_SAMPLE_RATE}Hz to {sample_rate}Hz")
            waveform = resample_audio(bark_waveform, BARK_SAMPLE_RATE, sample_rate)
        else:
            waveform = bark_waveform
        
        # Ensure correct length
        target_samples = duration * sample_rate
        if len(waveform) < target_samples:
            waveform = np.pad(waveform, (0, target_samples - len(waveform)))
        elif len(waveform) > target_samples:
            waveform = waveform[:target_samples]
        
        return {
            'waveform': waveform.astype(np.float32),
            'sample_rate': sample_rate,
            'segments': segments,
            'vocal_style': vocal_style,
            'note': f'Generated with Bark TTS (voice: {voice})'
        }
    
    except Exception as e:
        print(f"[Vocals] Error during Bark synthesis: {e}")
        # Fallback to silence
        waveform = np.zeros(duration * sample_rate, dtype=np.float32)
        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'segments': segments,
            'vocal_style': vocal_style,
            'note': f'Error: {str(e)}'
        }


def resample_audio(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """
    Simple linear resampling for audio.
    For production, consider using librosa or scipy.signal.resample.
    """
    if orig_sr == target_sr:
        return audio
    
    # Calculate new length
    duration = len(audio) / orig_sr
    new_length = int(duration * target_sr)
    
    # Simple linear interpolation
    indices = np.linspace(0, len(audio) - 1, new_length)
    resampled = np.interp(indices, np.arange(len(audio)), audio)
    
    return resampled.astype(np.float32)


def mix_vocals_with_music(
    music_waveform: np.ndarray,
    vocal_waveform: np.ndarray,
    music_volume: float = 0.7,
    vocal_volume: float = 1.0
) -> np.ndarray:
    """
    Mix vocal track with instrumental music.
    
    Args:
        music_waveform: Background music audio
        vocal_waveform: Vocal audio
        music_volume: Music volume multiplier (0-1)
        vocal_volume: Vocal volume multiplier (0-1)
    
    Returns:
        Mixed audio waveform
    """
    # Ensure same length
    target_len = max(len(music_waveform), len(vocal_waveform))
    
    if len(music_waveform) < target_len:
        music_waveform = np.pad(
            music_waveform,
            (0, target_len - len(music_waveform)),
            mode='constant'
        )
    
    if len(vocal_waveform) < target_len:
        vocal_waveform = np.pad(
            vocal_waveform,
            (0, target_len - len(vocal_waveform)),
            mode='constant'
        )
    
    # Mix with volume control
    mixed = (music_waveform * music_volume) + (vocal_waveform * vocal_volume)
    
    # Normalize to prevent clipping
    max_val = np.abs(mixed).max()
    if max_val > 1.0:
        mixed = mixed / max_val
    
    return mixed.astype(np.float32)


# Integration helpers for your existing pipeline
def should_add_vocals(genre: str, engine: str) -> bool:
    """Check if vocals should be added for this genre/engine combo."""
    vocal_genres = {'pop', 'rock', 'country', 'blues', 'rap', 'r&b'}
    return genre.lower() in vocal_genres and engine != 'ollama'


def get_default_lyrics(genre: str, duration: int) -> str:
    """Generate placeholder lyrics if none provided."""
    bpm = 120
    bars = int((duration * bpm) / 60 / 4)
    
    templates = {
        'blues': "(Verse 1 – 0:00 – 0:{:02d})\nWalking down that lonesome road,\nCarrying my heavy load.",
        'rock': "(Verse 1 – 0:00 – 0:{:02d})\nTurn it up and let it ring,\nFeel the power, hear it sing.",
        'country': "(Verse 1 – 0:00 – 0:{:02d})\nOut here where the wild wind blows,\nThat's where my heart truly goes.",
    }
    
    template = templates.get(genre.lower(), templates['rock'])
    return template.format(min(duration, 59))
