def generate_ollama_sample(genre, idea, model='llama3.2'):
    import numpy as np
    import requests

    # Build prompt for Ollama
    prompt = f"Generate creative lyrics for a {genre} song with the idea: {idea}. Make it fun and engaging. Structure it with verses, chorus, and bridge."

    # Try to call Ollama API
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            vocals = data.get('response', 'Ollama vocals (generated)').strip()
        else:
            vocals = 'Ollama vocals (API error)'
    except Exception as e:
        print(f"Ollama not available: {e}. Using stub.")
        vocals = 'Ollama vocals (stub)'

    return {
        'vocals': vocals
    }
