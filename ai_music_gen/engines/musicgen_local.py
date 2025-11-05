"""
Meta MusicGen Local Integration Module

This module provides local AI music generation using Meta's MusicGen model.
Runs on local hardware (CPU or CUDA GPU) for privacy-focused use cases.

Models Available:
- musicgen-small: 300M params, ~1.5GB, fastest (recommended for GTX 1080)
- musicgen-medium: 1.5B params, ~6GB, balanced
- musicgen-large: 3.3B params, ~15GB, highest quality (requires 24GB+ VRAM)
- musicgen-melody: Can condition on melody input

Environment:
- Requires: audiocraft, torch
- Optional: CUDA-enabled PyTorch for GPU acceleration
- Hardware: 8GB+ RAM (CPU), 4GB+ VRAM (GPU)

Usage:
    from engines.musicgen_local import generate_music, get_model_info
    
    # Generate music
    result = generate_music(
        prompt="Upbeat americana song with acoustic guitar",
        duration=30,
        model="small",  # or "medium", "large", "melody"
        use_sampling=True,
        top_k=250,
        top_p=0.0,
        temperature=1.0,
        cfg_coef=3.0
    )
    
    if result.get("success"):
        audio_array = result["audio"]  # numpy array
        sample_rate = result["sample_rate"]  # 32000 Hz
        
    # Check model info
    info = get_model_info()
"""

import os
import logging
from typing import Dict, Any, Optional, List
import numpy as np
import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

logger = logging.getLogger(__name__)

# Global model cache (lazy-loaded)
_model_cache = {}
_device = None


def _get_device() -> torch.device:
    """
    Determine optimal device (CUDA GPU or CPU).
    
    Returns:
        torch.device: CUDA if available, otherwise CPU
    """
    global _device
    if _device is None:
        if torch.cuda.is_available():
            _device = torch.device("cuda")
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            logger.info(f"Using GPU: {gpu_name} ({gpu_memory:.1f}GB)")
        else:
            _device = torch.device("cpu")
            logger.warning("CUDA not available, using CPU (slower)")
    return _device


def _load_model(model_size: str = "small") -> MusicGen:
    """
    Load MusicGen model (with caching).
    
    Args:
        model_size: Model size ("small", "medium", "large", "melody")
        
    Returns:
        MusicGen model instance
        
    Raises:
        ValueError: Invalid model size
        RuntimeError: Model loading failed
    """
    valid_sizes = ["small", "medium", "large", "melody"]
    if model_size not in valid_sizes:
        raise ValueError(f"model_size must be one of {valid_sizes}, got: {model_size}")
    
    # Check cache
    if model_size in _model_cache:
        logger.debug(f"Using cached MusicGen-{model_size}")
        return _model_cache[model_size]
    
    # Load model
    try:
        logger.info(f"Loading MusicGen-{model_size} (first load may download ~{_get_model_size(model_size)}GB)...")
        device = _get_device()
        
        model = MusicGen.get_pretrained(f"facebook/musicgen-{model_size}")
        model.to(device)
        
        _model_cache[model_size] = model
        logger.info(f"MusicGen-{model_size} loaded successfully on {device}")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load MusicGen-{model_size}: {e}")
        raise RuntimeError(f"Model loading failed: {e}")


def _get_model_size(model: str) -> float:
    """Get approximate model download size in GB."""
    sizes = {
        "small": 1.5,
        "medium": 6.0,
        "large": 15.0,
        "melody": 1.5
    }
    return sizes.get(model, 1.5)


def generate_music(
    prompt: str,
    duration: int = 30,
    model: str = "small",
    use_sampling: bool = True,
    top_k: int = 250,
    top_p: float = 0.0,
    temperature: float = 1.0,
    cfg_coef: float = 3.0,
    two_step_cfg: bool = False,
    extend_stride: Optional[int] = None,
    seed: Optional[int] = None,
    melody_path: Optional[str] = None,
    melody_sample_rate: int = 32000
) -> Dict[str, Any]:
    """
    Generate music using local MusicGen model.
    
    Args:
        prompt: Text description of music to generate
        duration: Length in seconds (max ~30s without chunking)
        model: Model size ("small", "medium", "large", "melody")
        use_sampling: Use sampling vs greedy decoding (True = more creative)
        top_k: Top-k sampling parameter (250 = default, higher = more diverse)
        top_p: Top-p (nucleus) sampling (0.0 = disabled)
        temperature: Sampling temperature (1.0 = default, >1 = more random)
        cfg_coef: Classifier-free guidance coefficient (3.0 = default, higher = closer to prompt)
        two_step_cfg: Use two-step classifier-free guidance (experimental)
        extend_stride: For longer generations, overlap size (experimental)
        seed: Random seed for reproducibility
        melody_path: Path to melody audio file (only for "melody" model)
        melody_sample_rate: Sample rate of melody audio
        
    Returns:
        Dict containing:
            - success: bool
            - audio: np.ndarray (shape: [1, channels, samples])
            - sample_rate: int (32000 Hz)
            - duration_actual: float (seconds)
            - metadata: Dict with generation details
            - error: str (if failed)
            
    Raises:
        ValueError: Invalid parameters
        RuntimeError: Generation failed
    """
    try:
        # Validate parameters
        if duration < 1 or duration > 300:
            raise ValueError("Duration must be between 1 and 300 seconds")
        
        if temperature <= 0:
            raise ValueError("Temperature must be positive")
            
        if cfg_coef < 0:
            raise ValueError("cfg_coef must be non-negative")
        
        # Load model
        musicgen = _load_model(model)
        
        # Set generation parameters
        musicgen.set_generation_params(
            duration=duration,
            use_sampling=use_sampling,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            cfg_coef=cfg_coef,
            two_step_cfg=two_step_cfg
        )
        
        if extend_stride is not None:
            musicgen.set_generation_params(extend_stride=extend_stride)
        
        # Set seed for reproducibility
        if seed is not None:
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed(seed)
        
        # Generate audio
        logger.info(f"Generating music: '{prompt[:50]}...' ({duration}s, {model})")
        
        descriptions = [prompt]
        
        # Handle melody conditioning (for musicgen-melody model)
        if model == "melody" and melody_path:
            from audiocraft.data.audio_utils import convert_audio
            import torchaudio
            
            melody_wav, sr = torchaudio.load(melody_path)
            if sr != melody_sample_rate:
                melody_wav = convert_audio(melody_wav, sr, melody_sample_rate, musicgen.sample_rate)
            melody_wav = melody_wav.unsqueeze(0).to(_get_device())
            
            logger.info(f"Conditioning on melody: {melody_path}")
            audio = musicgen.generate_with_chroma(
                descriptions=descriptions,
                melody_wavs=melody_wav,
                melody_sample_rate=melody_sample_rate,
                progress=True
            )
        else:
            audio = musicgen.generate(descriptions, progress=True)
        
        # Convert to numpy
        audio_np = audio.cpu().numpy()
        
        # Calculate actual duration
        duration_actual = audio_np.shape[-1] / musicgen.sample_rate
        
        logger.info(f"Generation completed: {duration_actual:.2f}s @ {musicgen.sample_rate}Hz")
        
        return {
            "success": True,
            "audio": audio_np,
            "sample_rate": musicgen.sample_rate,
            "duration_actual": duration_actual,
            "metadata": {
                "prompt": prompt,
                "model": model,
                "duration_requested": duration,
                "use_sampling": use_sampling,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "cfg_coef": cfg_coef,
                "seed": seed,
                "device": str(_get_device()),
                "has_melody": bool(melody_path)
            }
        }
        
    except Exception as e:
        logger.error(f"MusicGen generation failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def save_audio(
    audio: np.ndarray,
    sample_rate: int,
    output_path: str,
    format: str = "wav",
    strategy: str = "loudness"
) -> bool:
    """
    Save generated audio to file.
    
    Args:
        audio: Audio array from generate_music()
        sample_rate: Sample rate (typically 32000)
        output_path: Output file path (without extension)
        format: Audio format ("wav", "mp3", "flac")
        strategy: Normalization strategy ("loudness", "peak", "clip", "none")
        
    Returns:
        True if saved successfully, False otherwise
    """
    try:
        # Remove extension if provided
        output_path = os.path.splitext(output_path)[0]
        
        # Convert numpy to torch tensor
        audio_tensor = torch.from_numpy(audio).squeeze(0)
        
        # Save using audiocraft utility
        audio_write(
            output_path,
            audio_tensor,
            sample_rate,
            format=format,
            strategy=strategy
        )
        
        logger.info(f"Audio saved: {output_path}.{format}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save audio: {e}")
        return False


def get_model_info() -> Dict[str, Any]:
    """
    Get information about available models and hardware.
    
    Returns:
        Dict containing:
            - device: str ("cuda" or "cpu")
            - gpu_name: str (if CUDA available)
            - gpu_memory: float (GB, if CUDA available)
            - loaded_models: List[str] (models in cache)
            - available_models: List[Dict] with size info
    """
    device = _get_device()
    
    info = {
        "device": str(device),
        "loaded_models": list(_model_cache.keys()),
        "available_models": [
            {"name": "small", "params": "300M", "memory": "1.5GB", "speed": "fastest"},
            {"name": "medium", "params": "1.5B", "memory": "6GB", "speed": "medium"},
            {"name": "large", "params": "3.3B", "memory": "15GB", "speed": "slow"},
            {"name": "melody", "params": "300M", "memory": "1.5GB", "speed": "fast", "note": "supports melody conditioning"}
        ]
    }
    
    if device.type == "cuda":
        info["gpu_name"] = torch.cuda.get_device_name(0)
        info["gpu_memory"] = round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 1)
    
    return info


def clear_cache():
    """
    Clear model cache to free memory.
    Useful when switching between model sizes.
    """
    global _model_cache
    for model_name, model in _model_cache.items():
        del model
        logger.info(f"Cleared {model_name} from cache")
    _model_cache.clear()
    
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.info("Cleared CUDA cache")


def test_musicgen():
    """
    Test MusicGen integration with a simple generation.
    Run this to verify model loading and generation.
    """
    print("=" * 60)
    print("MusicGen Local Integration Test")
    print("=" * 60)
    
    # Check device
    device = _get_device()
    print(f"\nDevice: {device}")
    
    if device.type == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
    else:
        print("Note: Running on CPU (slower). Install CUDA PyTorch for GPU acceleration.")
    
    # Model info
    print("\nAvailable Models:")
    info = get_model_info()
    for model in info["available_models"]:
        print(f"  - {model['name']}: {model['params']} params, ~{model['memory']}, {model['speed']}")
    
    # Test generation
    print("\nGenerating 10s test track with musicgen-small...")
    print("(First run will download model, ~1.5GB)")
    
    result = generate_music(
        prompt="Upbeat americana acoustic guitar melody with heartfelt vibe",
        duration=10,
        model="small",
        temperature=1.0,
        cfg_coef=3.0,
        seed=42
    )
    
    if result.get("success"):
        print(f"\n✓ Generation successful!")
        print(f"  Duration: {result['duration_actual']:.2f}s")
        print(f"  Sample Rate: {result['sample_rate']}Hz")
        print(f"  Shape: {result['audio'].shape}")
        print(f"  Device: {result['metadata']['device']}")
        
        # Save test file
        import tempfile
        test_path = os.path.join(tempfile.gettempdir(), "musicgen_test")
        if save_audio(result["audio"], result["sample_rate"], test_path):
            print(f"\n✓ Test audio saved: {test_path}.wav")
            print("\n" + "=" * 60)
            print("MusicGen Integration Test: PASSED")
            print("=" * 60)
        else:
            print("\n✗ Failed to save test audio")
    else:
        print(f"\n✗ Generation failed: {result.get('error')}")


if __name__ == "__main__":
    # Run test when executed directly
    test_musicgen()
