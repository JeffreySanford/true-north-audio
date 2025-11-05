import numpy as np
from ai_music_gen.musicgen import generate_music


def test_generate_music_shape():
    waveform = generate_music(genre='ambient', duration=2, seed=42)
    assert isinstance(waveform, np.ndarray)
    assert waveform.shape[0] == 32000 * 2


def test_generate_music_different_genres():
    ambient = generate_music(genre='ambient', duration=1, seed=1)
    rock = generate_music(genre='rock', duration=1, seed=1)
    assert not np.allclose(ambient, rock)
import base64
import hashlib
import os
from pathlib import Path

import importlib
import sys
import types

import numpy as np
import pytest
from fastapi.testclient import TestClient

from musicgen.core import generate_music


GENERATED_DIR = Path(os.getcwd()) / "backend" / "src" / "assets" / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


GENRE_CASES = [
    (
        "ambient",
        11,
        "686a743705c4393604b75d5f57b91088d7e1e334a3c359603a7129b89642d8ef",
        "2e13c75f6ac4dc6736db43db48d931252046cfb049b86370ba32df6ca362c8ad",
        12_536,
    ),
    (
        "rock",
        22,
        "619c2ccef236f6cfe9150e29c1d2f226ac3ce9d7ef3d46bd4b7ec94ccca8d3d3",
        "c478433e4e28c6fe5de42de5250bae26b265247be4f8961aa9f8a24c84055432",
        12_536,
    ),
    (
        "jazz",
        33,
        "65033cfd7b0587449b5c16dbd1e5dd98bc486839028c720ae8e496f8f831f6f9",
        "60c30f116e77f42f715bcaa5adb37c3185a79052049b2bc33b988a32c369762d",
        12_536,
    ),
    (
        "electronic",
        44,
        "62e950f8e35e84bf966d9b521ed1cb01b325140a3f32b6b702f5c75edea7c329",
        "82246c61237760d6866c5bf42ad819f42e27f58c1e2f72245d62af0cde3d4e68",
        12_536,
    ),
    (
        "hiphop",
        55,
        "1678f32e720098793ec98b6af3524275adf57390d20b40f0aa247465b57fce55",
        "f1151f5d2e4be4e940a1954cfbeaf51363b569dbbb977285faa87ce36674cb16",
        12_536,
    ),
    (
        "classical",
        66,
        "2738b69a16892182646b4e1472a834cb1237da23c766e1bbc8c5b9d7da4a434d",
        "36a3a5fe47901b63edb98ef106b3eade37579dc8da98bf6ae60c74845213265d",
        12_536,
    ),
    (
        "pop",
        77,
        "9246e354fe6d25daa00dda6ba30f8773093e8e862a8fdf9e149a988ef81f01a4",
        "6cb9e397110bb0afa61dda6e34e8733a02b53d0105713fcb6889fa75dcf1122b",
        12_536,
    ),
    (
        "folk",
        88,
        "b2ec6e5661117f08507886e3ae9d224d1d5ff569ce68c15f3218857169bf7174",
        "1a745dba400ad0eedadd4974c29b06d1be474cf2c7aae103c21c748fdb71c52a",
        12_536,
    ),
    (
        "blues",
        99,
        "36fa2aa0106f39fd82426b6fee8f976ae183fac65a7619a5f29a184d38d397e5",
        "b73a7bddc3390b380f2178578d02595598da574b4055187d9607ad3eec412444",
        12_536,
    ),
    (
        "metal",
        111,
        "c45ff74e7f1d1932f4682361d5d02bb3a742e462ff00fabdee5542b740200f15",
        "7d11489ea956e168175467837a77e0e756456ce34259d323d4176d6e24fc8389",
        12_536,
    ),
]


import base64
import hashlib
import os
from pathlib import Path



import importlib
import sys
import types

import numpy as np
import pytest
from fastapi.testclient import TestClient

from musicgen.core import generate_music


GENERATED_DIR = Path(os.getcwd()) / "backend" / "src" / "assets" / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


GENRE_CASES = [
    (
        "ambient",
        11,
        "686a743705c4393604b75d5f57b91088d7e1e334a3c359603a7129b89642d8ef",
        "2e13c75f6ac4dc6736db43db48d931252046cfb049b86370ba32df6ca362c8ad",
        12_536,
    ),
    (
        "rock",
        22,
        "619c2ccef236f6cfe9150e29c1d2f226ac3ce9d7ef3d46bd4b7ec94ccca8d3d3",
        "c478433e4e28c6fe5de42de5250bae26b265247be4f8961aa9f8a24c84055432",
        12_536,


    ),
    (

        "jazz",
        33,
        "65033cfd7b0587449b5c16dbd1e5dd98bc486839028c720ae8e496f8f831f6f9",
        "60c30f116e77f42f715bcaa5adb37c3185a79052049b2bc33b988a32c369762d",
        12_536,
    ),
    (
        "electronic",
        44,

        "62e950f8e35e84bf966d9b521ed1cb01b325140a3f32b6b702f5c75edea7c329",
        "82246c61237760d6866c5bf42ad819f42e27f58c1e2f72245d62af0cde3d4e68",

        12_536,
    ),
    (
        "hiphop",


        55,
        "1678f32e720098793ec98b6af3524275adf57390d20b40f0aa247465b57fce55",
        "f1151f5d2e4be4e940a1954cfbeaf51363b569dbbb977285faa87ce36674cb16",
        12_536,
    ),
    (
        "classical",
        66,
        "2738b69a16892182646b4e1472a834cb1237da23c766e1bbc8c5b9d7da4a434d",
        "36a3a5fe47901b63edb98ef106b3eade37579dc8da98bf6ae60c74845213265d",
        12_536,
    ),
    (
        "pop",
        77,
        "9246e354fe6d25daa00dda6ba30f8773093e8e862a8fdf9e149a988ef81f01a4",
        "6cb9e397110bb0afa61dda6e34e8733a02b53d0105713fcb6889fa75dcf1122b",
        12_536,
    ),
    (
        "folk",
        88,
        "b2ec6e5661117f08507886e3ae9d224d1d5ff569ce68c15f3218857169bf7174",
        "1a745dba400ad0eedadd4974c29b06d1be474cf2c7aae103c21c748fdb71c52a",
        12_536,


    ),
    (
        "blues",
        99,

        "36fa2aa0106f39fd82426b6fee8f976ae183fac65a7619a5f29a184d38d397e5",
        "b73a7bddc3390b380f2178578d02595598da574b4055187d9607ad3eec412444",
        12_536,
    ),
    (

        "metal",
        111,

        "c45ff74e7f1d1932f4682361d5d02bb3a742e462ff00fabdee5542b740200f15",
        "7d11489ea956e168175467837a77e0e756456ce34259d323d4176d6e24fc8389",
        12_536,
    ),
]


def _expected_audio_paths(genre: str, seed: int) -> tuple[Path, Path, str]:
    mp3_name = f"{genre}_AI_Male_1_{seed}.mp3"
    wav_name = f"{genre}_AI_Male_1_{seed}.wav"

    return GENERATED_DIR / mp3_name, GENERATED_DIR / wav_name, mp3_name


def _assert_valid_song(
    result,
    expected_genre: str,
    duration_seconds: int,
    expected_wave_hash: str,
    expected_mp3_hash: str,
    expected_mp3_size: int,
    mp3_name: str,
) -> None:
    waveform = result['waveform']
    assert isinstance(waveform, np.ndarray)
    assert waveform.shape[0] == 32000 * duration_seconds
    assert np.var(waveform) > 1e-4
    digest = hashlib.sha256(waveform.tobytes()).hexdigest()
    assert digest == expected_wave_hash
    overview = result['overview']
    assert overview['genre'] == expected_genre
    assert overview.get('melody_rest_prob') is not None
    assert result['sample_rate'] == 32000
    audio_url = result['audio_url']
    assert audio_url.endswith(mp3_name)
    mp3_path = GENERATED_DIR / mp3_name
    assert mp3_path.exists()
    mp3_bytes = mp3_path.read_bytes()
    assert len(mp3_bytes) == expected_mp3_size
    mp3_digest = hashlib.sha256(mp3_bytes).hexdigest()
    assert mp3_digest == expected_mp3_hash
    wav_path = mp3_path.with_suffix('.wav')
    assert wav_path.exists()
    assert wav_path.stat().st_size > 10 * 1024


def _load_api_module():
    import musicgen

    if "ai_music_gen" not in sys.modules:
        pkg = types.ModuleType("ai_music_gen")
        pkg.__path__ = []  # mark as namespace package
        sys.modules["ai_music_gen"] = pkg
    pkg = sys.modules["ai_music_gen"]
    sys.modules["ai_music_gen.musicgen"] = musicgen
    setattr(pkg, "musicgen", musicgen)
    if "ai_music_gen.generator" not in sys.modules:
        gen_mod = types.ModuleType("ai_music_gen.generator")

        def _placeholder_generate_song(*args, **kwargs):
            raise RuntimeError("generate_song placeholder invoked")

        gen_mod.generate_song = _placeholder_generate_song
        sys.modules["ai_music_gen.generator"] = gen_mod
        setattr(pkg, "generator", gen_mod)
    return importlib.import_module("ai_music_gen.musicgen.api")


@pytest.mark.parametrize(
    "genre, seed, expected_wave_hash, expected_mp3_hash, expected_mp3_size",
    GENRE_CASES,
)
def test_generate_music_genre_snapshots(
    genre: str,
    seed: int,
    expected_wave_hash: str,
    expected_mp3_hash: str,
    expected_mp3_size: int,
) -> None:
    mp3_path, wav_path, mp3_name = _expected_audio_paths(genre, seed)
    for path in (mp3_path, wav_path):
        if path.exists():
            path.unlink()
    result = generate_music(genre=genre, duration=2, seed=seed)
    _assert_valid_song(
        result,
        genre,
        2,
        expected_wave_hash,
        expected_mp3_hash,
        expected_mp3_size,
        mp3_name,
    )


def test_generate_music_multi_section(monkeypatch, tmp_path) -> None:
    api_module = _load_api_module()
    stub_audio = tmp_path / "multi_section.mp3"
    stub_audio.write_bytes(b"ID3" + b"\x00" * 1024)

    def fake_generate_song(sections, default_tempo=120):
        assert len(sections) == 2
        assert sections[0]['type'] == 'intro'
        assert sections[1]['type'] == 'chorus'
        return str(stub_audio)

    generator_module = sys.modules["ai_music_gen.generator"]
    monkeypatch.setattr(generator_module, "generate_song", fake_generate_song, raising=False)

    client = TestClient(api_module.app)
    payload = {
        "genre": "ambient",
        "duration": 12,
        "engine": "MusicGen (Audiocraft)",
        "songSections": [
            {"type": "intro", "duration": 4, "transition": "none", "tempo": 100},
            {"type": "chorus", "duration": 8, "transition": "fade", "tempo": 120},
        ],
    }

    response = client.post("/api/musicgen/generate", json=payload)
    assert response.status_code == 200
    body = response.json()
    waveform = np.frombuffer(base64.b64decode(body['waveform']), dtype=np.float32)
    expected_samples = 32000 * sum(section['duration'] for section in payload['songSections'])
    assert waveform.shape[0] == expected_samples
    assert abs(np.mean(waveform)) < 0.2
    assert body['audio_url'] == str(stub_audio)
    assert body['sample_rate'] == 32000
