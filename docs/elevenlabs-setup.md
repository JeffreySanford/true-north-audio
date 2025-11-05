# ElevenLabs TTS Setup Guide

## What is ElevenLabs?
The best text-to-speech AI available. Creates natural, emotional voices that sound almost human.

## Pricing
- **Free tier**: 10,000 characters/month (~5-10 songs)
- **Starter**: $5/month - 30,000 characters
- **Creator**: $11/month - 100,000 characters

Get started: https://elevenlabs.io/

## Setup Instructions

### 1. Get Your API Key
1. Go to https://elevenlabs.io/
2. Sign up for a free account
3. Navigate to Settings → API Keys
4. Click "Generate API Key"
5. Copy your API key

### 2. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:ELEVENLABS_API_KEY = "your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set ELEVENLABS_API_KEY=your_api_key_here
```

**Linux/Mac (Bash):**
```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

**Permanent (add to your shell profile):**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export ELEVENLABS_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Install Python Package
```bash
pip install elevenlabs requests scipy
```

### 4. Test the Integration
```bash
python ai-music-gen/engines/elevenlabs.py
```

You should see:
```
✅ ElevenLabs API key found
✅ Found X voices
```

## Usage

### Via API Request
```bash
curl -X POST http://localhost:3000/api/musicgen/generate \
  -H "Content-Type: application/json" \
  -d '{
    "genre": "blues",
    "duration": 120,
    "tempo": 90,
    "idea": "Liberty Vote Blues",
    "vocal_engine": "elevenlabs",
    "vocal_style": "blues_narrator",
    "lyrics": "Your lyrics here..."
  }'
```

### Available Voice Styles
- `male_deep` - Deep, authoritative (Adam)
- `male_warm` - Warm, conversational (Josh)
- `male_smooth` - Smooth, professional (Arnold)
- `female_warm` - Warm female (Bella)
- `female_strong` - Strong female (Elli)
- `blues_narrator` - Deep voice for blues narration (default)

## Important Notes

### What ElevenLabs CAN Do:
✅ Natural-sounding speech
✅ Emotional narration
✅ Expressive reading of lyrics
✅ Voice cloning (with samples)

### What ElevenLabs CANNOT Do Well:
❌ Traditional singing (musical notes)
❌ Complex melodies
❌ Harmonies

### Best Use Cases:
- Spoken word over music
- Blues/rap narration style
- Audiobook-style delivery with music
- Voice acting for songs

## Alternative: For Real Singing
If you need traditional singing vocals, consider:
- **Suno AI** ($10/month) - Best AI singing
- **Udio** ($10/month) - Professional AI vocals
- Both available at their websites (can't be self-hosted)

## Troubleshooting

**"API key not found"**
- Make sure environment variable is set
- Restart your terminal/IDE after setting it
- Check spelling: `ELEVENLABS_API_KEY`

**"HTTP 401 Unauthorized"**
- Invalid API key
- Check your key at https://elevenlabs.io/app/settings/api-keys

**"HTTP 429 Too Many Requests"**
- You've exceeded your monthly character limit
- Upgrade your plan or wait for next month
- Free tier: 10,000 chars/month

**"Generation takes too long"**
- Normal for first request (models load)
- Subsequent requests are faster
- ~2-5 seconds per paragraph

## Cost Calculator

**Free Tier** (10,000 characters/month):
- Average 2-minute song lyrics: ~1,500 characters
- Approximately 6-7 songs/month free

**Starter** ($5/month, 30,000 characters):
- Approximately 20 songs/month

**Creator** ($11/month, 100,000 characters):
- Approximately 65 songs/month

## Support
- ElevenLabs Docs: https://elevenlabs.io/docs
- API Reference: https://elevenlabs.io/docs/api-reference
- Discord: https://discord.gg/elevenlabs
