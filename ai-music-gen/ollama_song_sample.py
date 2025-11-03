from musicgen.engines.ollama import generate_ollama_sample

# Example: Generate a modern hiphop version of "The Best Is Yet To Come" by Dean Martin
if __name__ == "__main__":
    genre = "hiphop"
    duration = 180  # Full song, 3 minutes
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
    print("Ollama Song Sample Result:")
    print(f"Sample Rate: {result['sample_rate']}")
    print(f"Waveform (first 32): {result['waveform'][:32]}")
    print(f"Vocals: {result['vocals']}")
    print(f"Audio URL: {result['audio_url']}")
