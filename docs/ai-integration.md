# AI Integration

## Multi-Engine Architecture (November 2025)

True North Audio now supports **three AI music generation engines** with intelligent routing:

### 1. Cloud Engines (Professional Quality)
- **Suno AI**: Industry-leading quality, vocal support, 50 songs/day free tier
- **Udio AI**: Professional quality, advanced editing, 3 songs/day free tier
- **Pros**: ⭐⭐⭐⭐⭐ quality, fast generation (30-60s), no local GPU needed
- **Cons**: Requires internet, API credits, data sent to cloud

### 2. Local MusicGen (Privacy-First)
- **Meta AudioCraft**: 100% local generation, unlimited use, complete privacy
- **Models**: Small (1.5GB), Medium (6GB), Large (15GB)
- **Pros**: Offline, unlimited, no API costs, full privacy
- **Cons**: Requires GPU (8GB+ VRAM recommended), slower, lower quality than cloud

## Engine Selection Strategy

**Default Routing** (implemented in `api.py`):
- **Quality Tier**: Use Suno/Udio for most users (professional results)
- **Privacy Tier**: Use local MusicGen for sensitive projects (medical, legal, confidential)
- **Fallback**: If cloud APIs unavailable, use local MusicGen

## Local Model Support
- **Ollama**: Text generation for lyrics and prompts (NOT music generation)
- **MusicGen**: Local AI music generation (Meta's open-source model)
- **GPU Acceleration**: CUDA support for NVIDIA GPUs (8GB+ VRAM)
- **CPU Fallback**: Runs on CPU if no GPU (slower, 5-10x)

## Hardware Requirements

See [hardware-requirements.md](./hardware-requirements.md) for detailed specifications.

**Minimum for Local MusicGen**:
- CPU: 8+ cores
- RAM: 16GB+
- GPU: NVIDIA GTX 1060 (6GB VRAM) or better
- Storage: 2-20GB for models

**Recommended Configuration**:
- CPU: 16+ cores (i9/Ryzen 9)
- RAM: 32GB+
- GPU: NVIDIA RTX 3060 (12GB VRAM) or GTX 1080 (8GB)
- Storage: 50GB+ SSD

## Audio Generation

### Frontend Backend Selector
- The frontend provides a backend selector for music creation
- Choose between: **Suno**, **Udio**, **MusicGen Local**
- Implemented as Angular Material component
- Fully tested and linted

### Generation Parameters
All engines support:
- Prompt/description (text)
- Duration (10-240 seconds)
- Genre, mood, tempo
- Lyrics (optional)
- Vocal style (optional)
- Instrumental mode

### API Endpoints

**Generate Music** (Multi-Engine):
```typescript
POST /api/audio-asset/generate
{
  "engine": "suno" | "udio" | "musicgen",
  "prompt": "Upbeat americana song with acoustic guitar",
  "duration": 120,
  "genre": "americana",
  "lyrics": "Optional lyrics...",
  "vocal_style": "country male",
  "tempo": 88
}
```

**Check Credits** (Cloud Engines):
```typescript
GET /api/audio-asset/credits/:engine
// Returns remaining credits for Suno/Udio
```

## Implementation Files

**Engine Modules**:
- `ai-music-gen/engines/suno.py` - Suno AI integration (206 lines)
- `ai-music-gen/engines/udio.py` - Udio AI integration (421 lines)
- `ai-music-gen/engines/musicgen_local.py` - Local MusicGen (396 lines)
- `ai-music-gen/engines/ollama.py` - Ollama text generation

**API Layer**:
- `backend/src/audio-asset/musicgen.controller.ts` - NestJS endpoints
- `backend/src/audio-asset/musicgen.service.ts` - Service layer with engine routing
- `ai-music-gen/musicgen/olamma_api.py` - FastAPI proxy to engines

## Environment Configuration

Create `.env` file with API keys:
```env
# Cloud Engines (optional, free tiers available)
SUNO_API_KEY=your_suno_key_here
UDIO_API_KEY=your_udio_key_here

# Voice Generation (optional)
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# Local MusicGen Configuration
MUSICGEN_MODEL=small  # or medium, large, melody
MUSICGEN_DEVICE=cuda  # or cpu
```

## Testing Engines

Each engine includes a test function:

```bash
# Test Suno API
python -c "from engines.suno import test_suno_api; test_suno_api()"

# Test Udio API
python -c "from engines.udio import test_udio_api; test_udio_api()"

# Test Local MusicGen
python -c "from engines.musicgen_local import test_musicgen; test_musicgen()"
```

## Free Tier Limits

**Suno Free**:
- 50 credits/day (~10 songs)
- Non-commercial use only
- Access to older models

**Udio Free**:
- 10 credits/day + 100/month
- Max 3 full-length songs/day
- No credit card required

**MusicGen Local**:
- ♾️ Unlimited (uses your hardware)
- Commercial use allowed (you own it)
- Requires one-time model download

## Extensibility
- Add new engines by creating `engines/<engine_name>.py`
- Implement standard interface: `generate_music()`, `download_audio()`, `get_credits()`
- Update routing logic in `api.py` to include new engine
- All engines support same parameter set for consistency