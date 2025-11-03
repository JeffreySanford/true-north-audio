# True North Audio - Setup Guide

## Prerequisites

### Required Software
- **Node.js** 18.x or higher
- **Python** 3.9 or higher (3.10+ recommended)
- **pnpm** (for Node package management)
- **Git** (for AudioCraft installation)

### Hardware Recommendations
- **CPU**: Multi-core processor (i7/i9 or equivalent)
- **RAM**: 16GB minimum, 32GB+ recommended
- **GPU**: NVIDIA GPU with CUDA support (optional but highly recommended for AI music generation)
- **Storage**: 20GB+ free space (AI models are large)

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/JeffreySanford/true-north-audio.git
cd true-north-audio
```

### 2. Install Node Dependencies
```bash
pnpm install
```
This will automatically install Python dependencies via the `postinstall` hook.

### 3. Verify Python Dependencies
If automatic installation failed, manually install:
```bash
# Install all Python dependencies
python -m pip install -r requirements.txt

# Or use the npm script
pnpm install:python
```

### 4. Install AI Music Generation Models (Optional but Recommended)
For professional AI music generation:
```bash
# AudioCraft (Meta's MusicGen)
python -m pip install git+https://github.com/facebookresearch/audiocraft

# Bark TTS for vocals
python -m pip install suno-bark
```

## Python Requirements

### Core Requirements (`requirements.txt`)
All Python dependencies are tracked in two files:
- **Root `requirements.txt`**: Consolidated dependencies for the entire project
- **`ai-music-gen/requirements.txt`**: AI music generation specific dependencies

### Key Dependencies
- **torch** - PyTorch for AI models
- **audiocraft** - Meta's MusicGen for professional music generation
- **suno-bark** - Bark TTS for AI vocals
- **librosa** - Audio analysis and processing
- **soundfile** - High-quality audio I/O
- **scipy** - Signal processing for effects
- **fastapi** - REST API for music generation
- **pydub** - Audio manipulation

## NPM Integration

### Automatic Installation
When you run `pnpm install`, the `postinstall` script automatically installs Python dependencies:

```json
"postinstall": "python -m pip install -r requirements.txt || echo 'Python dependencies install failed. Run manually: pip install -r requirements.txt'"
```

### Manual Installation Scripts
```bash
# Install Python dependencies
pnpm install:python

# Install with dev dependencies
pnpm install:python:dev
```

### Available NPM Scripts
```bash
# Development
pnpm serve:all          # Start all services (backend, frontend, APIs)
pnpm serve:backend      # Start backend only
pnpm serve:frontend     # Start frontend only
pnpm serve:fastapi      # Start Python FastAPI server
pnpm serve:ollama       # Start Ollama API server

# Build
pnpm build:all          # Build all projects
pnpm build:backend      # Build backend
pnpm build:frontend     # Build frontend

# Testing
pnpm test:all           # Run all tests
pnpm test:python        # Run Python tests

# Linting
pnpm lint:all           # Lint all code
pnpm lint:python        # Lint Python code
pnpm lint:python:fix    # Auto-fix Python linting issues

# Utilities
pnpm sync:audio         # Sync generated audio files
pnpm clear:melody       # Clear generated melodies
pnpm clean:all          # Full workspace cleanup
```

## AI Music Generation

### Generate Liberty Vote Blues
```bash
cd ai-music-gen
python generate_liberty_blues.py
```

This will:
1. Detect your hardware (CPU cores, RAM, GPU)
2. Load Meta's MusicGen model
3. Generate a professional 2:40 blues song
4. Save as both WAV (studio quality) and MP3

### Hardware Optimization
- **GPU**: Automatically detected and used if CUDA is available
- **CPU**: Utilizes all available cores for parallel processing
- **Performance**: 
  - With GPU: 3-5 minutes
  - CPU only: 15-25 minutes (24 cores)

## Troubleshooting

### Python Modules Not Found
```bash
# Verify Python installation
python --version

# Reinstall dependencies
pnpm install:python

# Or manually
pip install -r requirements.txt
```

### AudioCraft Installation Fails
AudioCraft requires Git:
```bash
# Install directly from GitHub
pip install git+https://github.com/facebookresearch/audiocraft

# Alternative: Install dependencies first
pip install torch torchaudio transformers
pip install git+https://github.com/facebookresearch/audiocraft
```

### CUDA/GPU Not Detected
1. Verify NVIDIA drivers are installed
2. Check CUDA toolkit version:
   ```bash
   nvidia-smi
   ```
3. Install CUDA-enabled PyTorch:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

### Memory Issues
If you encounter OOM (Out of Memory) errors:
- Reduce duration in generation scripts
- Close other applications
- Consider generating in shorter chunks
- Use CPU instead of GPU for smaller models

## Development Workflow

### Adding New Python Dependencies
1. Add to `requirements.txt`
2. Install: `pnpm install:python`
3. Commit both `requirements.txt` and any lock files

### Project Structure
```
true-north-audio/
├── ai-music-gen/              # Python AI music generation
│   ├── generate_liberty_blues.py
│   ├── musicgen/              # MusicGen core
│   └── requirements.txt       # AI-specific deps
├── backend/                   # NestJS backend
├── frontend/                  # Angular frontend
├── requirements.txt           # Consolidated Python deps
└── package.json              # Node/npm configuration
```

## Next Steps

1. Run the example: `cd ai-music-gen && python generate_liberty_blues.py`
2. Explore the generated audio in `backend/src/assets/generated/`
3. Customize the lyrics or prompts in `generate_liberty_blues.py`
4. Start the full stack: `pnpm serve:all`

## Support

For issues:
- Check this setup guide
- Review error messages carefully
- Ensure all prerequisites are installed
- Verify Python and Node versions match requirements
