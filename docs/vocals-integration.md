# Vocal Synthesis Integration Guide

## Overview

The music generation system now supports **vocals and lyrics**! You can generate songs with spoken or sung vocals that sync with your instrumental tracks.

## Current Status

**✅ Implemented:**
- Lyrics parsing with timing information (verse, chorus, bridge markers)
- Waveform mixing (vocals + instrumental)
- API endpoints accept lyrics
- Vocal style selection (spoken, sung, rap)
- Segment extraction from structured lyrics

**🔄 Placeholder (needs real TTS):**
- Currently returns silence for vocals
- You need to install a TTS/vocal synthesis library for actual audio

## Quick Start

### 1. Using the API

```bash
curl -X POST http://localhost:8000/api/musicgen/generate \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "blues",
    "duration": 120,
    "tempo": 90,
    "lyrics": "(Verse 1 – 0:00 – 0:15)\nLost my job in the summer of '\''09...",
    "vocal_style": "spoken",
    "vocal_artist": "AI_Male_1"
  }'
```

### 2. Using Python

```python
from musicgen.core import generate_music

lyrics = """
(Verse 1 – 0:00 – 0:15)
Lost my job in the summer of '09,
Factory closed, said they'd be just fine.

(Chorus – 0:15 – 0:35)
It's the Liberty Vote Blues, can't shake it away,
Promises made but they never stay.
"""

result = generate_music(
    genre='blues',
    duration=120,
    tempo=90,
    lyrics=lyrics,
    vocal_style='spoken',
    seed=42
)

print(f"Generated: {result['audio_url']}")
print(f"Segments: {len(result['vocal_segments'])}")
```

### 3. Run the Test Suite

```bash
# From workspace root
python ai-music-gen/test_vocals.py
```

## Lyrics Format

Use this format for timed lyrics:

```
(Section Type – start_time – end_time)
Your lyrics text here
Multiple lines supported

(Next Section – start_time – end_time)
More lyrics...
```

**Example:**
```
(Verse 1 – 0:00 – 0:15)
First verse lyrics
Over multiple lines

(Chorus – 0:15 – 0:35)
Chorus lyrics here

(Verse 2 – 0:35 – 0:50)
Second verse

(Bridge – 0:50 – 1:05)
Bridge section

(Outro – 1:05 – 1:20)
Ending
```

**Supported Section Types:**
- Verse 1, Verse 2, Verse 3, etc.
- Chorus
- Bridge
- Intro
- Outro
- Pre-Chorus
- Post-Chorus

## API Reference

### POST /api/musicgen/generate

**New Parameters:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `lyrics` | string | null | Structured lyrics with timing |
| `vocal_style` | string | "spoken" | Vocal delivery: "spoken", "sung", "rap" |

**Response includes:**

```json
{
  "waveform": "base64...",
  "sample_rate": 32000,
  "audio_url": "/audio/generated/blues_AI_Male_1_42.mp3",
  "vocals": {
    "description": "Melodic lead...",
    "segments": [
      {
        "type": "Verse 1",
        "start": 0,
        "end": 15,
        "duration": 15,
        "text": "Lost my job in the summer of '09..."
      }
    ],
    "style": "spoken",
    "has_lyrics": true
  }
}
```

## Adding Real Vocal Synthesis

Currently, the vocal track is **silent placeholder audio**. To add actual vocals:

### Option 1: Bark (Recommended for Singing)

Bark is the best open-source model for realistic singing and speech.

```bash
pip install bark-tts
```

**Update `ai-music-gen/engines/vocals.py`:**

```python
from bark import SAMPLE_RATE, generate_audio, preload_models

# One-time setup
preload_models()

def generate_vocals_with_bark(lyrics: str, duration: int, sample_rate: int):
    segments = parse_lyrics_with_timing(lyrics)
    full_waveform = np.zeros(duration * sample_rate)
    
    for segment in segments:
        text = segment['text']
        start_samples = int(segment['start'] * sample_rate)
        
        # Generate audio for this segment
        audio = generate_audio(text, history_prompt='v2/en_speaker_6')
        
        # Place in timeline
        end_samples = min(start_samples + len(audio), len(full_waveform))
        full_waveform[start_samples:end_samples] = audio[:end_samples - start_samples]
    
    return full_waveform
```

### Option 2: Coqui TTS (Speech)

Better for spoken vocals, podcasts, audiobooks.

```bash
pip install TTS
```

```python
from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

def generate_vocals_with_coqui(text: str):
    return tts.tts(text)
```

### Option 3: Commercial APIs

For production-quality vocals:

**Suno API** (Best for music):
- Realistic singing voices
- Multiple genres and styles
- Costs ~$0.05/song

**ElevenLabs** (Best for speech):
- Ultra-realistic voice cloning
- Low latency
- Costs ~$0.30/1000 characters

**Chirp (Google):**
- Natural speech synthesis
- Integrated with Google Cloud
- Costs ~$16/million characters

## Integration Checklist

- [x] Lyrics parsing with timing
- [x] API accepts `lyrics` and `vocal_style` parameters
- [x] Waveform mixing (vocals + instrumental)
- [x] Vocal segments returned in API response
- [x] Test suite created
- [ ] Install TTS library (Bark or Coqui)
- [ ] Replace `generate_vocals_placeholder()` with real synthesis
- [ ] Add pitch/tempo matching
- [ ] Add voice selection UI in frontend
- [ ] Add lyrics input textarea in frontend

## Frontend Integration

Update `frontend/src/app/components/music-generator/music-generator.component.ts`:

```typescript
export class MusicGeneratorComponent {
  // Add to form
  lyrics: string = '';
  vocalStyle: 'spoken' | 'sung' | 'rap' = 'spoken';

  generateMusic() {
    const request = {
      genre: this.selectedGenre,
      duration: this.duration,
      tempo: this.tempo,
      lyrics: this.lyrics,  // NEW
      vocal_style: this.vocalStyle,  // NEW
      // ... other fields
    };
    
    this.http.post('/api/musicgen/generate', request)
      .subscribe(result => {
        // Display vocal segments
        if (result.vocals?.segments) {
          this.displayLyrics(result.vocals.segments);
        }
      });
  }
}
```

## Testing

```bash
# Test with your Liberty Vote Blues lyrics
python ai-music-gen/test_vocals.py

# Expected output:
# ✓ Generated track: 120 seconds
# ✓ Vocal segments parsed: 8
#   - Verse 1: 0s - 15s
#   - Chorus: 15s - 35s
#   - Verse 2: 35s - 50s
#   ...
```

## Troubleshooting

**"Vocal engine not available" warning:**
- The vocals module couldn't import. Check `ai-music-gen/engines/vocals.py` exists.

**Vocals are silent:**
- This is expected! Install Bark or TTS library to generate real audio.

**Timing is off:**
- Adjust the segment start/end times in your lyrics
- Ensure duration matches the longest segment end time

**Lyrics not parsed:**
- Check format: `(Section – 0:00 – 0:15)` with proper dashes (not hyphens)
- Ensure each section has opening/closing parentheses

## Next Steps

1. **Install Bark** for singing vocals:
   ```bash
   pip install bark-tts
   ```

2. **Update vocals.py** with real TTS (see examples above)

3. **Add frontend UI** for lyrics input:
   - Textarea for lyrics
   - Dropdown for vocal style
   - Preview player with lyrics sync

4. **Enhance mixing**:
   - Add reverb to vocals
   - Adjust EQ for vocal clarity
   - Dynamic ducking (lower music during vocals)

5. **Voice selection**:
   - Let users choose voice characteristics
   - Add pitch shifting for different ranges
   - Support multiple vocalists (duets)

## Resources

- **Bark**: https://github.com/suno-ai/bark
- **Coqui TTS**: https://github.com/coqui-ai/TTS
- **Music timing**: https://en.wikipedia.org/wiki/Song_structure
- **Vocal mixing**: https://www.izotope.com/en/learn/mixing-vocals.html
