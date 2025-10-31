from musicgen.core import generate_melody


def test_generate_melody():
    result = generate_melody(length=4)
    audio_url = result.get('audio_url', '')
    assert audio_url.endswith('.mp3')
