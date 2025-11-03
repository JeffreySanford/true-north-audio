#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ElevenLabs TTS Engine for True North Audio
Provides natural-sounding voice synthesis with emotion
"""
import os
import requests
import numpy as np
from typing import Optional, Dict, Any
import warnings

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required if env vars set manually

# Check if ElevenLabs API key is available
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
ELEVENLABS_AVAILABLE = ELEVENLABS_API_KEY is not None

# ElevenLabs API configuration
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_SAMPLE_RATE = 44100  # High-quality audio

# Voice presets for different styles
VOICE_PRESETS = {
    'male_deep': 'pNInz6obpgDQGcFmaJgB',      # Adam - Deep, authoritative
    'male_warm': '21m00Tcm4TlvDq8ikWAM',      # Josh - Warm, conversational
    'male_smooth': 'VR6AewLTigWG4xSOukaG',    # Arnold - Smooth, professional
    'female_warm': 'EXAVITQu4vr4xnSDxMaL',    # Bella - Warm female
    'female_strong': 'MF3mGyEYCl7XYWbV9V6O',  # Elli - Strong female
    'storyteller': 'TxGEqnHWrfWFTfGW9XjX',    # Josh (custom for storytelling)
    'blues_narrator': 'pNInz6obpgDQGcFmaJgB', # Deep voice for blues narration
}

def _ensure_api_key():
    """Check if API key is configured"""
    if not ELEVENLABS_AVAILABLE:
        print("[ElevenLabs] WARNING: ELEVENLABS_API_KEY environment variable not set")
        print("[ElevenLabs] Get your API key from: https://elevenlabs.io/app/settings/api-keys")
        print("[ElevenLabs] Set it with: export ELEVENLABS_API_KEY='your_key_here'")
        return False
    return True

def get_voices() -> Dict[str, Any]:
    """Get available voices from ElevenLabs API"""
    if not _ensure_api_key():
        return {'available': False, 'voices': []}
    
    try:
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY
        }
        response = requests.get(f"{ELEVENLABS_API_URL}/voices", headers=headers)
        response.raise_for_status()
        
        voices_data = response.json()
        return {
            'available': True,
            'voices': voices_data.get('voices', []),
            'presets': VOICE_PRESETS
        }
    except Exception as e:
        print(f"[ElevenLabs] Error fetching voices: {e}")
        return {'available': False, 'error': str(e)}

def generate_speech(
    text: str,
    voice_id: Optional[str] = None,
    vocal_style: str = 'blues_narrator',
    stability: float = 0.5,
    similarity_boost: float = 0.75,
    style: float = 0.5,
    use_speaker_boost: bool = True
) -> Optional[bytes]:
    """
    Generate speech audio using ElevenLabs API
    
    Args:
        text: Text to convert to speech
        voice_id: Specific voice ID (overrides vocal_style)
        vocal_style: Preset voice style from VOICE_PRESETS
        stability: Voice stability (0-1, higher = more consistent)
        similarity_boost: Clarity vs similarity (0-1)
        style: Style exaggeration (0-1)
        use_speaker_boost: Enhance speaker characteristics
    
    Returns:
        Audio bytes (MP3 format) or None if failed
    """
    if not _ensure_api_key():
        return None
    
    # Select voice
    if voice_id is None:
        voice_id = VOICE_PRESETS.get(vocal_style, VOICE_PRESETS['blues_narrator'])
    
    print(f"[ElevenLabs] Generating speech with voice: {voice_id}")
    print(f"[ElevenLabs] Text length: {len(text)} characters")
    
    try:
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",  # Best for English
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": use_speaker_boost
            }
        }
        
        response = requests.post(
            f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        audio_bytes = response.content
        print(f"[ElevenLabs] Generated {len(audio_bytes)} bytes of audio")
        
        return audio_bytes
        
    except requests.exceptions.HTTPError as e:
        print(f"[ElevenLabs] HTTP Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"[ElevenLabs] Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"[ElevenLabs] Error generating speech: {e}")
        return None

def generate_vocals_elevenlabs(
    lyrics: str,
    duration: int,
    sample_rate: int = 32000,
    vocal_style: str = 'blues_narrator',
    voice_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate vocals using ElevenLabs TTS
    
    Args:
        lyrics: Full lyrics text
        duration: Target duration (not strictly enforced)
        sample_rate: Output sample rate
        vocal_style: Voice style preset
        voice_id: Specific voice ID (optional)
    
    Returns:
        Dict with waveform, sample_rate, and metadata
    """
    if not _ensure_api_key():
        # Return silence if API key not configured
        print("[ElevenLabs] API key not configured, returning silence")
        waveform = np.zeros(duration * sample_rate, dtype=np.float32)
        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'vocal_style': vocal_style,
            'note': 'ElevenLabs API key not configured. Set ELEVENLABS_API_KEY environment variable.'
        }
    
    # Generate speech
    audio_bytes = generate_speech(
        text=lyrics,
        voice_id=voice_id,
        vocal_style=vocal_style,
        stability=0.6,      # Slightly more consistent for music
        similarity_boost=0.8,  # Clear pronunciation
        style=0.7,          # More expressive
        use_speaker_boost=True
    )
    
    if audio_bytes is None:
        # Fallback to silence
        waveform = np.zeros(duration * sample_rate, dtype=np.float32)
        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'vocal_style': vocal_style,
            'note': 'ElevenLabs generation failed'
        }
    
    # Save the MP3 file temporarily and convert to waveform
    import tempfile
    import subprocess
    
    try:
        # Save MP3
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as mp3_file:
            mp3_file.write(audio_bytes)
            mp3_path = mp3_file.name
        
        # Convert to WAV using ffmpeg
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav_file:
            wav_path = wav_file.name
        
        subprocess.run([
            'ffmpeg', '-i', mp3_path,
            '-ar', str(sample_rate),
            '-ac', '1',  # Mono
            '-f', 'wav',
            wav_path,
            '-y'
        ], check=True, capture_output=True)
        
        # Load WAV as numpy array
        import scipy.io.wavfile as wavfile
        sr, waveform = wavfile.read(wav_path)
        
        # Convert to float32 and normalize
        if waveform.dtype == np.int16:
            waveform = waveform.astype(np.float32) / 32768.0
        elif waveform.dtype == np.int32:
            waveform = waveform.astype(np.float32) / 2147483648.0
        
        # Clean up temp files
        os.unlink(mp3_path)
        os.unlink(wav_path)
        
        print(f"[ElevenLabs] Generated {len(waveform)/sample_rate:.1f}s of audio")
        
        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'vocal_style': vocal_style,
            'voice_id': voice_id or VOICE_PRESETS.get(vocal_style),
            'note': 'Generated with ElevenLabs TTS'
        }
        
    except Exception as e:
        print(f"[ElevenLabs] Error converting audio: {e}")
        waveform = np.zeros(duration * sample_rate, dtype=np.float32)
        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'vocal_style': vocal_style,
            'note': f'Error: {str(e)}'
        }

# Test function
if __name__ == "__main__":
    print("ElevenLabs TTS Engine Test")
    print("=" * 50)
    
    if not ELEVENLABS_AVAILABLE:
        print("X ElevenLabs API key not configured")
        print("Set ELEVENLABS_API_KEY environment variable")
    else:
        print("OK ElevenLabs API key found")
        
        # Test voice listing
        voices = get_voices()
        if voices['available']:
            print(f"\nOK Found {len(voices['voices'])} voices")
            print("\nAvailable presets:")
            for name, voice_id in VOICE_PRESETS.items():
                print(f"  - {name}: {voice_id}")
        
        # Test generation
        print("\n Testing speech generation...")
        test_text = "This is a test of the ElevenLabs text to speech system."
        audio = generate_speech(test_text, vocal_style='blues_narrator')
        if audio:
            print(f"OK Generated {len(audio)} bytes of audio")
        else:
            print("X Generation failed")
