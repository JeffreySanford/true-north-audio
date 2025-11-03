def generate_riffusion_sample(genre, duration, seed=None, idea=None, vocal_artist=None, tempo=None, variation=None, songSections=None):
    import numpy as np
    sample_rate = 22050
    waveform = np.random.uniform(-1, 1, sample_rate * duration).astype(np.float32)
    return {
        'waveform': waveform,
        'sample_rate': sample_rate,
        'vocals': 'Riffusion vocals (stub)',
        'audio_url': '/audio/generated/riffusion_sample.mp3'
    }
