import numpy as np
from musicgen.engines.ollama import generate_ollama_sample

def test_generate_ollama_sample():
    genre = "hiphop"
    duration = 180
    idea = "Modern hiphop version of 'The Best Is Yet To Come' by Dean Martin"
    vocal_artist = "AI_Male_1"
    tempo = 90
    variation = "remix"
    songSections = [
        {"type": "intro", "duration": 16, "transition": "fade"},
        {"type": "verse", "duration": 32, "transition": "drum_fill"},
        {"type": "chorus", "duration": 32, "transition": "cut"},
        {"type": "bridge", "duration": 16, "transition": "fade"},
        {"type": "outro", "duration": 16, "transition": "fade"}
    ]
    result = generate_ollama_sample(
        genre=genre,
        duration=duration,
        idea=idea,
        vocal_artist=vocal_artist,
        tempo=tempo,
        variation=variation,
        songSections=songSections
    )
    assert isinstance(result, dict)
    assert "waveform" in result
    assert isinstance(result["waveform"], np.ndarray)
    assert result["waveform"].shape[0] == result["sample_rate"] * duration
    assert "vocals" in result
    assert "audio_url" in result
    print("Ollama engine test passed.")

if __name__ == "__main__":
    test_generate_ollama_sample()
