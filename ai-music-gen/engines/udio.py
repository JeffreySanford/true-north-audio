"""
Udio AI API Integration Module

This module provides integration with Udio.com's AI music generation API.
Handles authentication, music generation, polling, and audio file download.

API Endpoints:
- POST /api/generate - Create generation task
- GET /api/feed - Check generation status
- GET /api/download - Download generated audio

Environment Variables Required:
- UDIO_API_KEY: API authentication key from udio.com

Usage:
    from engines.udio import generate_music, get_credits
    
    # Generate music
    result = generate_music(
        prompt="Upbeat americana song about voting and freedom",
        duration=120,
        lyrics="Verse 1: Walking to the polls...",
        vocal_style="country male",
        genre="americana"
    )
    
    if result.get("success"):
        audio_url = result["audio_url"]
        audio_data = download_audio(audio_url)
        
    # Check credits
    credits = get_credits()
"""

import os
import time
import json
import logging
from typing import Dict, Any, Optional, List
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Udio API configuration
UDIO_API_BASE_URL = "https://api.udio.com/v1"
UDIO_API_TIMEOUT = 300  # 5 minutes max wait for generation
UDIO_POLL_INTERVAL = 5  # Check status every 5 seconds


def _ensure_api_key() -> str:
    """
    Retrieve and validate Udio API key from environment.
    
    Returns:
        str: API key
        
    Raises:
        ValueError: If UDIO_API_KEY not found in environment
    """
    api_key = os.getenv("UDIO_API_KEY")
    if not api_key:
        raise ValueError(
            "UDIO_API_KEY not found in environment. "
            "Please add it to your .env file:\n"
            "UDIO_API_KEY=your_api_key_here"
        )
    return api_key


def generate_music(
    prompt: str,
    duration: int = 30,
    lyrics: Optional[str] = None,
    vocal_style: Optional[str] = None,
    genre: Optional[str] = None,
    mood: Optional[str] = None,
    tempo: Optional[int] = None,
    instrumental: bool = False,
    tags: Optional[List[str]] = None,
    custom_model: Optional[str] = None,
    seed: Optional[int] = None,
    num_generations: int = 1
) -> Dict[str, Any]:
    """
    Generate music using Udio AI API.
    
    Args:
        prompt: Text description of the music to generate
        duration: Length in seconds (10-240, default 30)
        lyrics: Optional lyrics text (will be sung if provided)
        vocal_style: Style of vocals (e.g., "country male", "blues female")
        genre: Music genre (e.g., "americana", "blues", "rock")
        mood: Emotional tone (e.g., "uplifting", "melancholic")
        tempo: BPM (40-240)
        instrumental: If True, no vocals even if lyrics provided
        tags: List of style tags to influence generation
        custom_model: Use specific Udio model version
        seed: Random seed for reproducibility
        num_generations: Number of variations to create (1-5)
        
    Returns:
        Dict containing:
            - success: bool
            - generation_id: str (if successful)
            - audio_url: str (if successful)
            - audio_urls: List[str] (if num_generations > 1)
            - metadata: Dict with generation details
            - error: str (if failed)
            
    Raises:
        requests.RequestException: Network/API errors
        ValueError: Invalid parameters
    """
    api_key = _ensure_api_key()
    
    # Validate parameters
    if duration < 10 or duration > 240:
        raise ValueError("Duration must be between 10 and 240 seconds")
    
    if tempo and (tempo < 40 or tempo > 240):
        raise ValueError("Tempo must be between 40 and 240 BPM")
        
    if num_generations < 1 or num_generations > 5:
        raise ValueError("num_generations must be between 1 and 5")
    
    # Build request payload
    payload = {
        "prompt": prompt,
        "duration": duration,
        "num_generations": num_generations
    }
    
    # Add optional parameters
    if lyrics and not instrumental:
        payload["lyrics"] = lyrics
        
    if vocal_style and not instrumental:
        payload["vocal_style"] = vocal_style
        
    if instrumental:
        payload["instrumental"] = True
        
    if genre:
        payload["genre"] = genre
        
    if mood:
        payload["mood"] = mood
        
    if tempo:
        payload["tempo"] = tempo
        
    if tags:
        payload["tags"] = tags
        
    if custom_model:
        payload["model"] = custom_model
        
    if seed is not None:
        payload["seed"] = seed
    
    # Headers with authentication
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "TrueNorthAudio/1.0"
    }
    
    logger.info(f"Submitting Udio generation request: {prompt[:50]}...")
    
    try:
        # Submit generation request
        response = requests.post(
            f"{UDIO_API_BASE_URL}/generate",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        generation_id = result.get("generation_id")
        if not generation_id:
            return {
                "success": False,
                "error": "No generation_id returned from Udio API"
            }
        
        logger.info(f"Generation started: {generation_id}")
        
        # Poll for completion
        audio_urls = _poll_for_completion(generation_id, headers)
        
        if not audio_urls:
            return {
                "success": False,
                "error": "Generation completed but no audio URLs returned"
            }
        
        # Return result
        result_data = {
            "success": True,
            "generation_id": generation_id,
            "metadata": {
                "prompt": prompt,
                "duration": duration,
                "genre": genre,
                "mood": mood,
                "tempo": tempo,
                "has_lyrics": bool(lyrics),
                "vocal_style": vocal_style,
                "instrumental": instrumental,
                "num_generations": num_generations
            }
        }
        
        # Add audio URLs (single or multiple)
        if num_generations == 1:
            result_data["audio_url"] = audio_urls[0]
        else:
            result_data["audio_urls"] = audio_urls
            result_data["audio_url"] = audio_urls[0]  # First one as primary
        
        logger.info(f"Generation completed: {generation_id}")
        return result_data
        
    except requests.RequestException as e:
        logger.error(f"Udio API request failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"Unexpected error in generate_music: {e}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def _poll_for_completion(
    generation_id: str,
    headers: Dict[str, str]
) -> Optional[List[str]]:
    """
    Poll Udio API for generation completion.
    
    Args:
        generation_id: ID of the generation to check
        headers: HTTP headers with authentication
        
    Returns:
        List of audio URLs if successful, None if timeout or error
    """
    start_time = time.time()
    
    while time.time() - start_time < UDIO_API_TIMEOUT:
        try:
            # Check generation status
            response = requests.get(
                f"{UDIO_API_BASE_URL}/feed",
                headers=headers,
                params={"generation_id": generation_id},
                timeout=10
            )
            response.raise_for_status()
            status_data = response.json()
            
            status = status_data.get("status")
            
            if status == "completed":
                # Extract audio URLs
                songs = status_data.get("songs", [])
                audio_urls = [song.get("audio_url") for song in songs if song.get("audio_url")]
                
                if audio_urls:
                    logger.info(f"Generation {generation_id} completed with {len(audio_urls)} tracks")
                    return audio_urls
                else:
                    logger.error(f"Generation completed but no audio URLs found")
                    return None
                    
            elif status == "failed":
                error_msg = status_data.get("error", "Unknown error")
                logger.error(f"Generation {generation_id} failed: {error_msg}")
                return None
                
            elif status in ["pending", "processing"]:
                logger.debug(f"Generation {generation_id} still {status}...")
                time.sleep(UDIO_POLL_INTERVAL)
                
            else:
                logger.warning(f"Unknown status: {status}")
                time.sleep(UDIO_POLL_INTERVAL)
                
        except requests.RequestException as e:
            logger.warning(f"Error polling status: {e}")
            time.sleep(UDIO_POLL_INTERVAL)
    
    logger.error(f"Generation {generation_id} timed out after {UDIO_API_TIMEOUT}s")
    return None


def download_audio(audio_url: str) -> Optional[bytes]:
    """
    Download generated audio file from Udio CDN.
    
    Args:
        audio_url: Direct URL to audio file
        
    Returns:
        Audio file bytes if successful, None if error
    """
    try:
        logger.info(f"Downloading audio from Udio CDN...")
        response = requests.get(audio_url, timeout=30)
        response.raise_for_status()
        
        audio_data = response.content
        logger.info(f"Downloaded {len(audio_data)} bytes")
        return audio_data
        
    except requests.RequestException as e:
        logger.error(f"Failed to download audio: {e}")
        return None


def get_credits() -> Dict[str, Any]:
    """
    Check remaining Udio API credits.
    
    Returns:
        Dict containing:
            - success: bool
            - credits_remaining: int
            - credits_total: int
            - reset_date: str (ISO format)
            - error: str (if failed)
    """
    api_key = _ensure_api_key()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "TrueNorthAudio/1.0"
    }
    
    try:
        response = requests.get(
            f"{UDIO_API_BASE_URL}/account/credits",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        return {
            "success": True,
            "credits_remaining": data.get("remaining", 0),
            "credits_total": data.get("total", 0),
            "reset_date": data.get("reset_date")
        }
        
    except requests.RequestException as e:
        logger.error(f"Failed to fetch credits: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def test_udio_api():
    """
    Test Udio API integration with a simple generation.
    Run this to verify your API key and configuration.
    """
    print("=" * 60)
    print("Udio API Integration Test")
    print("=" * 60)
    
    # Check API key
    try:
        api_key = _ensure_api_key()
        print(f"✓ API Key found: {api_key[:8]}...{api_key[-4:]}")
    except ValueError as e:
        print(f"✗ {e}")
        return
    
    # Check credits
    print("\nChecking credits...")
    credits = get_credits()
    if credits.get("success"):
        print(f"✓ Credits: {credits['credits_remaining']}/{credits['credits_total']}")
    else:
        print(f"✗ Credits check failed: {credits.get('error')}")
        return
    
    # Test generation
    print("\nGenerating test track (30s Americana snippet)...")
    result = generate_music(
        prompt="Upbeat americana song with acoustic guitar and heartfelt male vocals",
        duration=30,
        genre="americana",
        mood="uplifting",
        tempo=88,
        lyrics="This is a test of Udio integration\nMaking music with AI generation",
        vocal_style="country male",
        num_generations=1
    )
    
    if result.get("success"):
        print(f"✓ Generation successful!")
        print(f"  Generation ID: {result['generation_id']}")
        print(f"  Audio URL: {result['audio_url'][:50]}...")
        
        # Try downloading
        print("\nDownloading audio...")
        audio_data = download_audio(result['audio_url'])
        if audio_data:
            print(f"✓ Downloaded {len(audio_data)} bytes")
            print("\n" + "=" * 60)
            print("Udio API Integration Test: PASSED")
            print("=" * 60)
        else:
            print("✗ Download failed")
    else:
        print(f"✗ Generation failed: {result.get('error')}")


if __name__ == "__main__":
    # Run test when executed directly
    test_udio_api()
