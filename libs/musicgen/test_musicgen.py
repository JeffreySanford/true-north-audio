import numpy as np
from musicgen import generate_music

def test_generate_music_shape():
    waveform = generate_music(genre='ambient', duration=2, seed=42)
    assert isinstance(waveform, np.ndarray)
    assert waveform.shape[0] == 22050 * 2

def test_generate_music_different_genres():
    ambient = generate_music(genre='ambient', duration=1, seed=1)
    rock = generate_music(genre='rock', duration=1, seed=1)
    assert not np.allclose(ambient, rock)
