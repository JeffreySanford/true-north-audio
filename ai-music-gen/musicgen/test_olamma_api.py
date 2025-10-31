"""
Olamma in-memory server test for musicgen API.
"""
import requests


def test_olamma_status():
    resp = requests.get("http://localhost:11434/olamma/status")
    assert resp.status_code == 200
    assert resp.json()["status"] in ["running", "not running"]


def test_musicgen_proxy():
    # This test assumes Olamma is running and a compatible model is loaded
    payload = {
        "prompt": "A vibrant jazz melody",
        "seed": 42,
        "tempo": 120
    }
    resp = requests.post("http://localhost:11434/musicgen", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "audio_url" in data or "error" in data
