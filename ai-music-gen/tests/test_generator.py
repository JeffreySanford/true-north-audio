from ai_music_gen.generator import generate_melody

def test_generate_melody():
    path = generate_melody(length=4)
    assert path.endswith('.mid')
