from ai_music_gen import generate_melody, check_resources

if __name__ == "__main__":
    check_resources()
    generate_melody(length=8, tempo=120)
