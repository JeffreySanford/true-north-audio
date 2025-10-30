import numpy as np

def generate_music(genre: str = 'ambient', duration: int = 10, seed: int = None) -> np.ndarray:
    """
    Generate a basic AI music track (placeholder).
    Args:
        genre (str): Music genre (e.g., 'ambient', 'pop', 'rock').
        duration (int): Duration in seconds.
        seed (int): Random seed for reproducibility.
    Returns:
        np.ndarray: Generated audio waveform (dummy sine wave).
    """
    if seed is not None:
        np.random.seed(seed)
    sr = 22050  # Sample rate
    t = np.linspace(0, duration, int(sr * duration))
    freq = 440 if genre == 'rock' else 220
    waveform = 0.5 * np.sin(2 * np.pi * freq * t)
    # Add random noise for demo
    waveform += 0.05 * np.random.randn(len(t))
    return waveform
