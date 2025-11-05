# Setup Guide for High-Performance Machine

## Hardware Configuration
This guide assumes you're setting up True North Audio on a high-performance workstation with:
- **CPU**: 16+ cores
- **RAM**: 32GB+
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **Storage**: 50GB+ free space on SSD

## Prerequisites

### 1. System Requirements (Windows)

**Install Visual Studio Build Tools** (required for Python packages):
```powershell
# Download installer
Invoke-WebRequest -Uri https://aka.ms/vs/17/release/vs_BuildTools.exe -OutFile vs_BuildTools.exe

# Install (run as Administrator)
.\vs_BuildTools.exe --quiet --wait --norestart --nocache `
  --add Microsoft.VisualStudio.Workload.VCTools `
  --add Microsoft.VisualStudio.Component.Windows10SDK.20348 `
  --includeRecommended
```

**Install NVIDIA CUDA Toolkit** (for GPU acceleration):
1. Download from: https://developer.nvidia.com/cuda-downloads
2. Choose: Windows → x86_64 → 11.8 or 12.1
3. Install with default settings
4. Verify: `nvcc --version`

**Update NVIDIA Drivers**:
- Download latest Game Ready or Studio drivers from: https://www.nvidia.com/download/index.aspx
- Recommended: Studio drivers for stability

### 2. Node.js & Package Manager

**Install Node.js 18+**:
```powershell
# Using Chocolatey
choco install nodejs-lts

# Or download from: https://nodejs.org/
```

**Install pnpm**:
```powershell
npm install -g pnpm
```

### 3. Python Environment

**Install Python 3.10-3.11** (3.13 may have compatibility issues):
```powershell
# Using Chocolatey
choco install python311

# Verify
python --version  # Should show 3.11.x
```

## Project Setup

### 1. Clone Repository
```bash
git clone https://github.com/JeffreySanford/true-north-audio.git
cd true-north-audio
git checkout vocal-integration  # Current development branch
```

### 2. Install Node Dependencies
```bash
# Install all workspace dependencies
pnpm install
```

### 3. Setup Python Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.venv\Scripts\activate.bat

# Activate (Git Bash/WSL)
source .venv/Scripts/activate
```

### 4. Install Python Dependencies

**Core Dependencies**:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Install PyTorch with CUDA** (for GPU acceleration):
```bash
# For CUDA 11.8 (most compatible with GTX 1080, RTX 3060)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1 (RTX 4000 series)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Verify CUDA Installation**:
```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not found')"
```

Expected output:
```
CUDA Available: True
GPU: NVIDIA GeForce GTX 1080  # or your GPU model
```

**Install AI Music Generation Libraries**:
```bash
# Meta's AudioCraft (for local MusicGen)
pip install audiocraft

# Additional AI libraries
pip install elevenlabs python-dotenv requests
```

### 5. Environment Configuration

Create `.env` file in project root:
```env
# ===================================
# Cloud API Keys (Optional)
# ===================================
# Get free tier at: https://suno.com/
SUNO_API_KEY=

# Get free tier at: https://udio.com/
UDIO_API_KEY=

# Get free tier at: https://elevenlabs.io/
ELEVENLABS_API_KEY=

# ===================================
# Local MusicGen Configuration
# ===================================
# Model size: small (1.5GB), medium (6GB), large (15GB)
MUSICGEN_MODEL=small

# Device: cuda (GPU) or cpu
MUSICGEN_DEVICE=cuda

# Cache directory for downloaded models
MUSICGEN_CACHE_DIR=~/.cache/musicgen

# ===================================
# MongoDB Configuration
# ===================================
MONGODB_URI=mongodb://localhost:27017/true-north-audio

# ===================================
# Backend Configuration
# ===================================
NODE_ENV=development
PORT=3000
```

### 6. Verify Installation

**Test Backend**:
```bash
pnpm nx run backend:lint
pnpm nx run backend:test
```

**Test Frontend**:
```bash
pnpm nx run frontend:lint
pnpm nx run frontend:test
```

**Test Python AI Modules**:
```bash
# Test MusicGen (will download ~1.5GB model on first run)
python -c "from ai-music-gen.engines.musicgen_local import test_musicgen; test_musicgen()"

# Test GPU availability
python -c "from ai-music-gen.engines.musicgen_local import get_model_info; print(get_model_info())"
```

## Running the Application

### Development Mode (Recommended)

**Option 1: Start All Services Together**:
```bash
pnpm dev  # Runs serve-dev.sh
```

This will:
1. Build backend once
2. Start NestJS backend (port 3000)
3. Start FastAPI Python service (port 8000)
4. Start Ollama proxy (port 11434)
5. Start Angular frontend (port 4200) with proxy

**Option 2: Start Services Individually**:

Terminal 1 - Backend:
```bash
pnpm nx serve backend
```

Terminal 2 - Python FastAPI:
```bash
cd ai-music-gen
python musicgen/api.py
```

Terminal 3 - Ollama Proxy:
```bash
cd ai-music-gen
python musicgen/olamma_api.py
```

Terminal 4 - Frontend:
```bash
pnpm nx serve frontend --proxy-config=src/proxy.conf.json
```

### Access the Application
- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:3000/api
- **Python API**: http://localhost:8000
- **Ollama Proxy**: http://localhost:11434

## Performance Optimization

### GPU Memory Optimization

**For 8GB VRAM (GTX 1080, RTX 3060)**:
- Use `MUSICGEN_MODEL=small` (default)
- Close other GPU applications (browsers, games)
- Monitor VRAM: `nvidia-smi -l 1`

**For 12GB+ VRAM (RTX 3080, 4070)**:
- Can use `MUSICGEN_MODEL=medium` for better quality
- Can run multiple generations simultaneously

**For 24GB VRAM (RTX 4090, A6000)**:
- Can use `MUSICGEN_MODEL=large` for best quality
- Can run batch generations

### Model Pre-Download (Optional)

To avoid waiting during first generation:
```bash
python -c "
from audiocraft.models import MusicGen
print('Downloading musicgen-small...')
MusicGen.get_pretrained('facebook/musicgen-small')
print('Download complete!')
"
```

For medium or large models:
```bash
# Medium (~6GB)
python -c "from audiocraft.models import MusicGen; MusicGen.get_pretrained('facebook/musicgen-medium')"

# Large (~15GB)
python -c "from audiocraft.models import MusicGen; MusicGen.get_pretrained('facebook/musicgen-large')"
```

### System Monitoring

**Watch GPU Usage**:
```powershell
# Real-time monitoring
nvidia-smi -l 1

# Detailed memory info
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv -l 1
```

**Watch CPU/RAM**:
```powershell
# PowerShell
Get-Counter '\Processor(_Total)\% Processor Time', '\Memory\Available MBytes' -Continuous

# Or use Task Manager (Ctrl+Shift+Esc)
```

## Troubleshooting

### "CUDA out of memory"
**Solution**: Use smaller model or reduce song duration
```env
MUSICGEN_MODEL=small  # Instead of medium/large
```

### "PyTorch not using GPU"
**Solution**: Reinstall CUDA-enabled PyTorch
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### "Import error: audiocraft"
**Solution**: Install in correct virtual environment
```bash
# Make sure .venv is activated
.\.venv\Scripts\Activate.ps1
pip install audiocraft
```

### "Model download fails"
**Solution**: Check network and HuggingFace access
```bash
# Verify connection
curl https://huggingface.co

# Clear cache and retry
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface\
```

### "Port already in use"
**Solution**: Kill existing processes
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use script
bash scripts/kill-all.sh
```

## Testing Music Generation

### Test Cloud Engines (Free Tier)

**Suno Test** (requires free account):
```bash
python -c "
from ai_music_gen.engines.suno import test_suno_api
test_suno_api()
"
```

**Udio Test** (requires free account):
```bash
python -c "
from ai_music_gen.engines.udio import test_udio_api
test_udio_api()
"
```

### Test Local MusicGen

**Quick Test** (10s generation):
```bash
python -c "
from ai_music_gen.engines.musicgen_local import test_musicgen
test_musicgen()
"
```

**Generate Liberty Vote Blues** (120s):
```bash
bash scripts/generate-liberty-vote-blues.sh
```

## Next Steps

1. **Get API Keys** (optional):
   - Suno: https://suno.com/ (50 songs/day free)
   - Udio: https://udio.com/ (3 songs/day free)
   - ElevenLabs: https://elevenlabs.io/ (10k chars/month free)

2. **Test All Engines**:
   - Generate same song with Suno, Udio, and MusicGen
   - Compare quality, speed, and results
   - Document preferences

3. **Optimize Performance**:
   - Monitor GPU usage during generation
   - Experiment with model sizes
   - Tune generation parameters

4. **Start Development**:
   - See [docs/architecture.md](./docs/architecture.md)
   - See [docs/api-endpoints.md](./docs/api-endpoints.md)
   - See [docs/ai-integration.md](./docs/ai-integration.md)

## Backup and Migration

### Save Models (avoid re-downloading)
```bash
# Backup HuggingFace cache
xcopy /E /I %USERPROFILE%\.cache\huggingface D:\Backups\huggingface

# Restore on new machine
xcopy /E /I D:\Backups\huggingface %USERPROFILE%\.cache\huggingface
```

### Export Configuration
```bash
# Save all installed packages
pip freeze > requirements-snapshot.txt
pnpm list --depth 0 > package-snapshot.txt

# Save environment variables
copy .env .env.backup
```

## Support & Resources

- **Documentation**: See `/docs` folder
- **Hardware Guide**: [docs/hardware-requirements.md](./docs/hardware-requirements.md)
- **AI Integration**: [docs/ai-integration.md](./docs/ai-integration.md)
- **API Endpoints**: [docs/api-endpoints.md](./docs/api-endpoints.md)
- **Repository**: https://github.com/JeffreySanford/true-north-audio
