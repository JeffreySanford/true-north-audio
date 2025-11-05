#!/usr/bin/env python3
"""
Suno AI API Integration for True North Audio
High-quality commercial music generation
"""
import os
import requests
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

SUNO_API_KEY = os.environ.get('SUNO_API_KEY')
SUNO_API_URL = "https://api.suno.ai/v1"
SUNO_AVAILABLE = SUNO_API_KEY is not None


def _ensure_api_key():
    """Check if Suno API key is configured"""
    if not SUNO_AVAILABLE:
        print("[Suno] WARNING: SUNO_API_KEY environment variable not set")
        print("[Suno] Get your API key from: https://suno.ai/api")
        print("[Suno] Set it with: export SUNO_API_KEY='your_key_here'")
        return False
    return True


def generate_music(
    prompt: str,
    duration: int = 30,
    make_instrumental: bool = False,
    wait_audio: bool = True,
    timeout: int = 300
) -> Optional[Dict[str, Any]]:
    """
    Generate music using Suno AI
    
    Args:
        prompt: Text description of the music to generate
        duration: Duration in seconds (15, 30, 60, 120)
        make_instrumental: Generate instrumental only (no vocals)
        wait_audio: Wait for generation to complete
        timeout: Maximum seconds to wait for completion
        
    Returns:
        Dict with audio_url, metadata, or None if failed
    """
    if not _ensure_api_key():
        return None
    
    print(f"[Suno] Generating music: {prompt[:50]}...")
    
    # Create generation request
    headers = {
        "Authorization": f"Bearer {SUNO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "make_instrumental": make_instrumental,
        "wait_audio": wait_audio
    }
    
    try:
        # Submit generation request
        response = requests.post(
            f"{SUNO_API_URL}/generate",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        if not wait_audio:
            return result
        
        # Poll for completion
        generation_id = result.get('id')
        if not generation_id:
            print(f"[Suno] Error: No generation ID returned")
            return None
        
        print(f"[Suno] Generation ID: {generation_id}")
        print(f"[Suno] Waiting for completion (max {timeout}s)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            status_response = requests.get(
                f"{SUNO_API_URL}/generate/{generation_id}",
                headers=headers,
                timeout=30
            )
            status_response.raise_for_status()
            status = status_response.json()
            
            state = status.get('status', 'unknown')
            print(f"[Suno] Status: {state}")
            
            if state == 'complete':
                audio_url = status.get('audio_url')
                if audio_url:
                    print(f"[Suno] Generation complete! URL: {audio_url}")
                    return {
                        'audio_url': audio_url,
                        'duration': status.get('duration', duration),
                        'metadata': status.get('metadata', {}),
                        'generation_id': generation_id,
                        'engine': 'suno'
                    }
                else:
                    print(f"[Suno] Warning: No audio URL in completed result")
                    return None
            
            elif state == 'failed':
                error = status.get('error', 'Unknown error')
                print(f"[Suno] Generation failed: {error}")
                return None
            
            # Still processing, wait and retry
            time.sleep(5)
        
        # Timeout
        print(f"[Suno] Timeout after {timeout}s")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"[Suno] API request failed: {e}")
        return None
    except Exception as e:
        print(f"[Suno] Unexpected error: {e}")
        return None


def download_audio(audio_url: str, output_path: str) -> bool:
    """
    Download generated audio file
    
    Args:
        audio_url: URL of the generated audio
        output_path: Local path to save the file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"[Suno] Downloading audio to {output_path}")
        response = requests.get(audio_url, stream=True, timeout=60)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"[Suno] Download complete")
        return True
        
    except Exception as e:
        print(f"[Suno] Download failed: {e}")
        return False


def get_credits() -> Optional[Dict[str, Any]]:
    """
    Check remaining API credits
    
    Returns:
        Dict with credit info or None if failed
    """
    if not _ensure_api_key():
        return None
    
    try:
        headers = {"Authorization": f"Bearer {SUNO_API_KEY}"}
        response = requests.get(
            f"{SUNO_API_URL}/credits",
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[Suno] Failed to get credits: {e}")
        return None


# Test function
if __name__ == "__main__":
    print("Testing Suno AI integration...")
    
    if not SUNO_AVAILABLE:
        print("ERROR: SUNO_API_KEY not set")
        print("Please set it in .env file or environment")
        exit(1)
    
    # Check credits
    credits = get_credits()
    if credits:
        print(f"Credits: {credits}")
    
    # Test generation
    result = generate_music(
        prompt="Upbeat acoustic folk song with guitar and harmonica, happy and energetic",
        duration=15,
        make_instrumental=True,
        wait_audio=True
    )
    
    if result:
        print(f"SUCCESS: {result}")
    else:
        print("FAILED: No result returned")
