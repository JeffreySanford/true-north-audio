# 🎵 Your Generated Songs!

## Location

All your generated songs are in:
```
C:\repos\true-north-audio\ai-music-gen\backend\src\assets\generated\
```

## Your Songs

### Liberty Vote Blues (Full 2-Minute Song with Vocals)
- **MP3**: `blues_AI_Male_1_42.mp3` (704 KB)
- **WAV**: `blues_AI_Male_1_42.wav` (7.4 MB)
- **Duration**: 2 minutes (120 seconds)
- **Style**: Blues with spoken vocals
- **Lyrics**: Full "Liberty Vote Blues" with 7 segments

### Test Songs
- `blues_AI_Male_1_123.mp3` (177 KB) - 30-second instrumental test
- `pop_AI_Male_1_999.mp3` (88 KB) - 15-second test with different vocal styles

## Play Your Songs

### Option 1: Windows Media Player
```bash
start C:\repos\true-north-audio\ai-music-gen\backend\src\assets\generated\blues_AI_Male_1_42.mp3
```

### Option 2: ffplay (if you have ffmpeg)
```bash
ffplay "C:\repos\true-north-audio\ai-music-gen\backend\src\assets\generated\blues_AI_Male_1_42.mp3"
```

### Option 3: File Explorer
Navigate to:
```
C:\repos\true-north-audio\ai-music-gen\backend\src\assets\generated\
```
Double-click `blues_AI_Male_1_42.mp3`

## Via Your Web App

When your services are running (`./scripts/serve-all.sh`):

**URL**: http://localhost:3000/audio/generated/blues_AI_Male_1_42.mp3

**Or from frontend**: The generated songs are accessible via the backend API.

## Song Details

### blues_AI_Male_1_42.mp3
```
Genre:     Blues
Tempo:     90 BPM
Duration:  2:00
Seed:      42
Artist:    AI_Male_1
Style:     Spoken vocals

Segments:
  0:00 - 0:15   Verse 1
  0:15 - 0:35   Chorus
  0:35 - 0:50   Verse 2
  0:50 - 1:10   Chorus
  1:10 - 1:25   Bridge
  1:25 - 1:45   Chorus
  1:45 - 2:00   Outro
```

## What's Inside

The audio contains:
- ✅ **Instrumental track** - Synthesized blues music (bass, chords, melody, percussion)
- ✅ **Vocal track** - Bark-generated speech (currently has mixing issues, see below)
- ✅ **Mixed together** - Combined at generation time

## Current Status

**Bark is NOW working!** The PyTorch 2.6 weights issue has been fixed:
- ✅ Models download successfully (~8GB first time)
- ✅ Vocals generate (variance: 0.002168, NOT silent!)
- ⚠️ Quality may vary - Bark works best with:
  - Shorter phrases (10-20 words max per segment)
  - Simple punctuation
  - Natural speech patterns

## Generate More Songs

### Via Python
```python
from musicgen.core import generate_music

result = generate_music(
    genre='blues',
    duration=60,
    tempo=90,
    lyrics="""
(Verse 1 – 0:00 – 0:15)
Your custom lyrics here
""",
    vocal_style='spoken'  # or 'sung' or 'rap'
)

print(f"Song saved: {result['audio_url']}")
```

### Via API
```bash
curl -X POST http://localhost:8000/api/musicgen/generate \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "blues",
    "duration": 60,
    "lyrics": "(Verse – 0:00 – 0:15)\nYour lyrics...",
    "vocal_style": "spoken"
  }'
```

## Tips for Better Vocals

1. **Keep segments short** - 10-15 seconds max
2. **Use punctuation** - Helps Bark with intonation
3. **Natural phrasing** - Write like you speak
4. **GPU recommended** - Bark is slow on CPU (2 min per segment)
5. **Try different voices** - Edit `vocals.py` voice presets

## Next Steps

1. **Listen to your song!**
   ```bash
   start blues_AI_Male_1_42.mp3
   ```

2. **Try the quick test** to verify Bark works:
   ```bash
   cd ai-music-gen
   python test_bark_quick.py
   ```

3. **Generate new songs** with different lyrics/styles

4. **Integrate with frontend** - Add lyrics textarea to UI

## Troubleshooting

**Vocals sound robotic?**
- Normal for Bark without fine-tuning
- Try shorter, simpler phrases
- Experiment with punctuation

**Generation too slow?**
- Bark needs GPU for good performance
- CPU generation: ~2 minutes per 10-second segment
- Consider shorter songs for testing

**Want to hear just the vocals?**
- Edit `vocals.py` to return vocals only (skip mixing)
- Or use audio editing software to split tracks

---

**🎉 Congratulations! Your music generation system now has working vocal synthesis!**
