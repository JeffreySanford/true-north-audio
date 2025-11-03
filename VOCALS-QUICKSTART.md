# Vocal Synthesis - Quick Reference

## ✅ What's Done

Your music generation system now supports **lyrics and vocals**:

- **✅ Lyrics parsing** - Extracts timing from `(Verse 1 – 0:00 – 0:15)` format
- **✅ API integration** - `/api/musicgen/generate` accepts `lyrics` and `vocal_style`
- **✅ Waveform mixing** - Combines vocals with instrumental tracks
- **✅ Python code** - Clean, no linting errors
- **✅ Test suite** - `test_vocals.py` demonstrates usage

## 🔔 Important: Vocals are Currently Silent

The vocal synthesis is a **placeholder** that returns silent audio. To get actual singing/speech:

### Install a TTS Library

**Option 1: Bark (Best for singing)**
```bash
pip install bark-tts
```

**Option 2: Coqui TTS (Best for speech)**
```bash
pip install TTS
```

Then update `ai-music-gen/engines/vocals.py` line 61-85 to replace the placeholder with real synthesis.

## Quick Usage Examples

### Via API (curl)

```bash
curl -X POST http://localhost:8000/api/musicgen/generate \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "blues",
    "duration": 120,
    "tempo": 90,
    "lyrics": "(Verse 1 – 0:00 – 0:15)\nLost my job in the summer of '\''09,\nFactory closed, said they'\''d be just fine.",
    "vocal_style": "spoken",
    "vocal_artist": "AI_Male_1"
  }'
```

### Via Python

```python
from musicgen.core import generate_music

result = generate_music(
    genre='blues',
    duration=120,
    tempo=90,
    lyrics="""
(Verse 1 – 0:00 – 0:15)
Your lyrics here

(Chorus – 0:15 – 0:35)
More lyrics...
""",
    vocal_style='spoken',
    seed=42
)

print(f"Generated: {result['audio_url']}")
print(f"Segments: {len(result.get('vocal_segments', []))}")
```

### Test Your Lyrics

```bash
# Run the test suite
python ai-music-gen/test_vocals.py
```

## Lyrics Format

```
(Section Name – start_time – end_time)
Lyrics text on one or more lines

(Next Section – start_time – end_time)
More lyrics...
```

**Example:**
```
(Verse 1 – 0:00 – 0:15)
Lost my job in the summer of '09,
Factory closed, said they'd be just fine.

(Chorus – 0:15 – 0:35)
It's the Liberty Vote Blues, can't shake it away,
Promises made but they never stay.
```

## API Changes

### New Request Fields

```typescript
{
  // Existing fields...
  genre: string,
  duration: number,
  tempo: number,
  
  // NEW FIELDS:
  lyrics?: string,        // Structured lyrics with timing
  vocal_style?: string,   // "spoken", "sung", "rap"
}
```

### New Response Fields

```typescript
{
  // Existing fields...
  waveform: string,
  sample_rate: number,
  audio_url: string,
  
  // NEW/ENHANCED FIELDS:
  vocals: {
    description: string,
    segments: Array<{
      type: string,      // "Verse 1", "Chorus", etc.
      start: number,     // Start time in seconds
      end: number,       // End time in seconds
      duration: number,  // Duration in seconds
      text: string       // Lyrics text
    }>,
    style: string,       // "spoken", "sung", "rap"
    has_lyrics: boolean
  },
  vocal_segments: Array<...>  // Same as vocals.segments
}
```

## File Changes Summary

### New Files
- `ai-music-gen/engines/vocals.py` - Vocal synthesis engine (placeholder)
- `ai-music-gen/test_vocals.py` - Test suite with your Liberty Vote Blues lyrics
- `docs/vocals-integration.md` - Complete integration guide

### Modified Files
- `ai-music-gen/musicgen/core.py` - Added `lyrics` and `vocal_style` params
- `ai-music-gen/musicgen/api.py` - API accepts lyrics/vocal_style
- Both files: Clean, no errors

## Next Steps

### 1. Test the Integration (Silent Vocals)

```bash
# Start services
./scripts/serve-all.sh

# In another terminal, test vocals
python ai-music-gen/test_vocals.py
```

### 2. Add Real Vocals

Install Bark:
```bash
pip install bark-tts
```

Update `ai-music-gen/engines/vocals.py`:
```python
from bark import generate_audio, preload_models

def generate_vocals_placeholder(...):  # Rename to generate_vocals_bark
    preload_models()
    
    segments = parse_lyrics_with_timing(lyrics)
    waveform = np.zeros(duration * sample_rate)
    
    for seg in segments:
        # Generate audio for this segment
        audio = generate_audio(seg['text'])
        
        # Insert at correct time
        start_idx = int(seg['start'] * sample_rate)
        end_idx = min(start_idx + len(audio), len(waveform))
        waveform[start_idx:end_idx] = audio[:end_idx - start_idx]
    
    return {'waveform': waveform, ...}
```

### 3. Frontend Integration

Add lyrics textarea to `frontend/src/app/components/music-generator/`:

```typescript
export class MusicGeneratorComponent {
  lyrics = '';
  vocalStyle: 'spoken' | 'sung' | 'rap' = 'spoken';

  generateMusic() {
    const request = {
      ...this.currentRequest,
      lyrics: this.lyrics,
      vocal_style: this.vocalStyle
    };
    // ... submit to API
  }
}
```

## Resources

- **Full Guide**: See `docs/vocals-integration.md`
- **Bark TTS**: https://github.com/suno-ai/bark
- **Coqui TTS**: https://github.com/coqui-ai/TTS
- **Test Suite**: `ai-music-gen/test_vocals.py`

## Troubleshooting

**Vocals are silent:**
- Expected! Install Bark or TTS library for real audio.

**"Vocal engine not available":**
- Check that `ai-music-gen/engines/vocals.py` exists
- Verify imports work: `python -c "import engines.vocals"`

**Segments not parsed:**
- Format must be: `(Section – 0:00 – 0:15)` with space-dash-space
- Use proper time format: `M:SS` or `MM:SS`

**API doesn't accept lyrics:**
- Restart FastAPI: `pkill -f "python -m musicgen.api" && python -m musicgen.api`
- Check logs: `tail -f /tmp/fastapi.log`
