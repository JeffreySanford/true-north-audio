# Bark TTS Installation Complete! 🎉

## ✅ What's Installed

- **Bark TTS** - Realistic vocal synthesis
- **Transformers** - Hugging Face models
- **All dependencies** - Ready to generate vocals

## Quick Test

### Option 1: Simple Bark Test (Recommended First)

Test Bark directly with a short sample:

```bash
cd ai-music-gen
python test_bark_quick.py
```

**What happens:**
1. Downloads Bark models on first run (~1GB, 1-2 minutes)
2. Generates a 6-second vocal sample
3. Saves `test_bark_output.wav`
4. Shows audio variance to confirm it's not silent

**Expected output:**
```
[Vocals] Loading Bark models (first run takes ~30s)...
[Vocals] Bark models loaded!
[Vocals] Generating Verse 1: "Hello, this is a test..."
✅ Generation complete!
   Variance: 0.045123 (has audio!)
💾 Saved to: test_bark_output.wav
```

### Option 2: Full Song Test

Test with your "Liberty Vote Blues" lyrics:

```bash
cd ai-music-gen
python test_vocals.py
```

**Note:** This generates a full 2-minute song with vocals. Takes 5-10 minutes.

## Generated Files

After running tests, you'll have:

```
ai-music-gen/
  test_bark_output.wav       ← Simple Bark test (6 seconds)
  
backend/src/assets/generated/
  blues_AI_Male_1_42.wav     ← Full song from test_vocals.py
  blues_AI_Male_1_42.mp3     ← Converted to MP3 (if ffmpeg installed)
```

## Play the Audio

**Windows:**
```bash
# Using ffplay (if you have ffmpeg)
ffplay test_bark_output.wav

# Or use default player
start test_bark_output.wav
```

**Git Bash:**
```bash
cmd //c start test_bark_output.wav
```

## Integration Status

✅ **Bark installed and working**
✅ **Vocals module updated to use Bark**
✅ **API endpoints accept lyrics**
✅ **Music generation mixes vocals + instrumental**

## What Happens Now

When you call the API with lyrics:

```bash
curl -X POST http://localhost:8000/api/musicgen/generate \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "blues",
    "duration": 30,
    "tempo": 90,
    "lyrics": "(Verse 1 – 0:00 – 0:10)\nLost my job in the summer of '\''09",
    "vocal_style": "spoken"
  }'
```

**Bark will:**
1. Parse your lyrics with timing
2. Generate realistic vocals for each section
3. Mix vocals with instrumental at correct timestamps
4. Return combined audio

## Performance Notes

**First Generation:**
- Model download: ~1GB, 1-2 minutes
- Model loading: ~30 seconds
- Vocal generation: ~10-20 seconds per verse

**Subsequent Generations:**
- Models cached, no download
- Loading: instant (models stay in memory)
- Generation: ~10-20 seconds per verse

## Voice Options

You can change the voice style:

```python
result = generate_music(
    lyrics="...",
    vocal_style='spoken',  # Clear speech
    # OR
    vocal_style='sung',    # Musical singing
    # OR
    vocal_style='rap'      # Rhythmic delivery
)
```

Each style uses a different Bark voice preset:
- `spoken` → `v2/en_speaker_6` (clear male voice)
- `sung` → `v2/en_speaker_9` (musical voice)
- `rap` → `v2/en_speaker_3` (rhythmic voice)

## Troubleshooting

**"Out of memory" error:**
- Bark needs ~4GB RAM
- Try shorter lyrics (30-60 seconds instead of 2 minutes)
- Close other programs

**Models downloading slowly:**
- First run downloads from Hugging Face
- Patience! Models are ~1GB
- Future runs use cached models

**Vocals sound robotic:**
- Normal for Bark (it's good but not perfect)
- Try different voice presets
- Adjust text with punctuation for better intonation

**Generation takes too long:**
- Each 10-second segment takes ~10-20 seconds
- 2-minute song = 12 segments = ~2-4 minutes total
- Consider shorter test lyrics first

## Next Steps

1. **Test Basic Bark:**
   ```bash
   python test_bark_quick.py
   ```

2. **Test Full Song:**
   ```bash
   python test_vocals.py
   ```

3. **Use in Your App:**
   - Start services: `./scripts/serve-all.sh`
   - Use frontend to generate with lyrics
   - Or call API directly

4. **Experiment:**
   - Try different vocal_style options
   - Adjust lyrics timing
   - Mix different genres with vocals

## Resources

- **Bark Repo**: https://github.com/suno-ai/bark
- **Bark Demo**: https://huggingface.co/spaces/suno/bark
- **Voice Presets**: See Bark repo for all available voices
- **Your Docs**: `docs/vocals-integration.md`
