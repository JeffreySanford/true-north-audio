# Machine Setup Checklist - Quick Reference

## 🚀 Quick Start (30 Minutes)

Perfect for experienced developers who know the stack.

### 1. Prerequisites (10 min)
```powershell
# Install with Chocolatey (run as Administrator)
choco install git nodejs-lts python311 -y
npm install -g pnpm
```

### 2. Clone & Install (10 min)
```bash
git clone https://github.com/JeffreySanford/true-north-audio.git
cd true-north-audio
git checkout vocal-integration
pnpm install
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. GPU Setup (5 min)
```bash
# Install CUDA-enabled PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install audiocraft
```

### 4. Configure & Run (5 min)
```bash
# Copy .env.example to .env and add API keys (optional)
copy .env.example .env
# Start everything
pnpm dev
```

**Open**: http://localhost:4200

---

## 🔧 Detailed Setup (2-3 Hours)

For first-time setup or troubleshooting.

### Phase 1: System Prerequisites

#### Windows Prerequisites
- [ ] **Visual Studio Build Tools** (required for Python packages)
  ```powershell
  # Run as Administrator
  Invoke-WebRequest -Uri https://aka.ms/vs/17/release/vs_BuildTools.exe -OutFile vs_BuildTools.exe
  .\vs_BuildTools.exe --quiet --wait --norestart --nocache `
    --add Microsoft.VisualStudio.Workload.VCTools `
    --add Microsoft.VisualStudio.Component.Windows10SDK.20348 `
    --includeRecommended
  ```
  **Time**: 15-30 minutes

- [ ] **NVIDIA CUDA Toolkit** (for GPU acceleration)
  - Download: https://developer.nvidia.com/cuda-downloads
  - Version: 11.8 (GTX 1080, RTX 3060) or 12.1 (RTX 4070+)
  - Install with default settings
  - **Time**: 10-15 minutes
  - Verify: `nvcc --version`

- [ ] **Update NVIDIA Drivers**
  - Download: https://www.nvidia.com/download/index.aspx
  - Choose: Studio (stable) or Game Ready (latest)
  - **Time**: 10-15 minutes
  - Verify: `nvidia-smi`

#### Development Tools
- [ ] **Git**
  ```powershell
  choco install git
  ```
  Verify: `git --version`

- [ ] **Node.js 18+ LTS**
  ```powershell
  choco install nodejs-lts
  ```
  Verify: `node --version` (should be 18.x+)

- [ ] **pnpm**
  ```powershell
  npm install -g pnpm
  ```
  Verify: `pnpm --version`

- [ ] **Python 3.11**
  ```powershell
  choco install python311
  ```
  Verify: `python --version` (should be 3.11.x)
  
  ⚠️ **Note**: Python 3.13 may have compatibility issues, use 3.11

#### Optional Tools
- [ ] **MongoDB** (local database)
  ```powershell
  choco install mongodb
  ```
  Or use MongoDB Atlas (cloud)

- [ ] **VS Code**
  ```powershell
  choco install vscode
  ```

### Phase 2: Project Setup

#### Clone Repository
```bash
# HTTPS
git clone https://github.com/JeffreySanford/true-north-audio.git

# SSH (if configured)
git clone git@github.com:JeffreySanford/true-north-audio.git

cd true-north-audio
git checkout vocal-integration
```

#### Install Node.js Dependencies
```bash
pnpm install
```

**Expected time**: 2-5 minutes  
**Expected size**: ~500MB in node_modules

**Troubleshooting**:
- If EPERM errors: Close all editors, run as Administrator
- If network errors: Check proxy settings or use VPN
- If peer dependency warnings: Safe to ignore (Nx handles them)

#### Setup Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (CMD)
.venv\Scripts\activate.bat

# Activate (Git Bash)
source .venv/Scripts/activate

# Upgrade pip and tools
python -m pip install --upgrade pip setuptools wheel
```

#### Install Python Dependencies
```bash
# Core dependencies
pip install -r requirements.txt
```

**Expected time**: 3-5 minutes  
**Expected size**: ~1GB in .venv

#### Install PyTorch with CUDA
```bash
# For GTX 1080, RTX 3060 (CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For RTX 4070+ (CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Expected time**: 2-3 minutes  
**Expected size**: ~2GB

**Verify GPU Detection**:
```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not found')"
```

**Expected output**:
```
CUDA Available: True
GPU: NVIDIA GeForce GTX 1080  # or your GPU model
```

#### Install AudioCraft (MusicGen)
```bash
pip install audiocraft
```

**Expected time**: 1-2 minutes

### Phase 3: Configuration

#### Create Environment File
```bash
# Copy template
copy .env.example .env

# Edit with your favorite editor
notepad .env  # or code .env (VS Code)
```

#### Required Environment Variables
```env
# ===================================
# REQUIRED (for basic functionality)
# ===================================
NODE_ENV=development
PORT=3000
MONGODB_URI=mongodb://localhost:27017/true-north-audio

# ===================================
# OPTIONAL (Cloud API Keys)
# ===================================
# Suno (50 songs/day free): https://suno.com/
SUNO_API_KEY=

# Udio (3 songs/day free): https://udio.com/
UDIO_API_KEY=

# ElevenLabs (10k chars/month free): https://elevenlabs.io/
ELEVENLABS_API_KEY=

# ===================================
# LOCAL MUSICGEN CONFIGURATION
# ===================================
# Model: small (1.5GB), medium (6GB), large (15GB)
MUSICGEN_MODEL=small

# Device: cuda (GPU) or cpu
MUSICGEN_DEVICE=cuda
```

#### Get API Keys (Optional)

**Suno** (Free Tier: 50 songs/day):
1. Visit: https://suno.com/
2. Sign up for free account
3. Go to: Settings → API
4. Copy API key to .env

**Udio** (Free Tier: 3 songs/day):
1. Visit: https://udio.com/
2. Sign up for free account
3. Go to: Account → API Keys
4. Copy API key to .env

**ElevenLabs** (Free Tier: 10k chars/month):
1. Visit: https://elevenlabs.io/
2. Sign up for free account
3. Go to: Profile → API Keys
4. Copy API key to .env

### Phase 4: Verification

#### Lint All Projects
```bash
pnpm nx run-many --target=lint --all
```

**Expected**: All projects pass (no errors)

#### Run All Tests
```bash
pnpm nx run-many --target=test --all
```

**Expected**: All test suites pass

#### Build All Projects
```bash
pnpm nx run-many --target=build --all
```

**Expected**: Clean builds with no errors

#### Test Python Engines
```bash
# Test GPU detection
python -c "import torch; assert torch.cuda.is_available(), 'GPU not detected'; print('✓ GPU:', torch.cuda.get_device_name(0))"

# Test MusicGen info
python -c "from ai_music_gen.engines.musicgen_local import get_model_info; import json; print(json.dumps(get_model_info(), indent=2))"

# Test imports
python -c "import audiocraft; import torch; import elevenlabs; import requests; print('✓ All imports successful')"
```

### Phase 5: First Run

#### Start Development Services
```bash
# Start all services (recommended)
pnpm dev

# Or start individually:
# Terminal 1: pnpm nx serve backend
# Terminal 2: cd ai-music-gen && python musicgen/api.py
# Terminal 3: cd ai-music-gen && python musicgen/olamma_api.py
# Terminal 4: pnpm nx serve frontend --proxy-config=src/proxy.conf.json
```

**Expected startup time**: 10-30 seconds

#### Verify Services
- [ ] **Backend**: http://localhost:3000/api
  - Should show: "Cannot GET /api" (normal, needs endpoint path)
  
- [ ] **Python API**: http://localhost:8000/docs
  - Should show: FastAPI Swagger UI
  
- [ ] **Ollama Proxy**: http://localhost:11434
  - Should show: Ollama API info
  
- [ ] **Frontend**: http://localhost:4200
  - Should show: True North Audio UI

#### Test Music Generation

**Test 1: Local MusicGen** (requires model download on first run):
1. Open: http://localhost:4200
2. Select engine: "MusicGen Local"
3. Enter prompt: "Upbeat acoustic guitar melody"
4. Duration: 10 seconds (for quick test)
5. Click "Generate"
6. **First generation will download model (~1.5GB, 5-10 min)**
7. Watch GPU usage: `nvidia-smi -l 1` in separate terminal

**Expected**: 
- Model download progress (first time only)
- GPU usage visible in nvidia-smi
- Audio file generated in ~10-30 seconds
- Audio plays in browser

**Test 2: Cloud Engine** (requires API key):
1. Select engine: "Suno" or "Udio"
2. Enter same prompt
3. Click "Generate"

**Expected**:
- Faster generation (30-60 seconds)
- Higher quality audio
- No model download needed

### Phase 6: Performance Tuning

#### Monitor GPU Usage
```powershell
# Real-time monitoring
nvidia-smi -l 1

# Detailed memory
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv -l 1
```

**During generation, expect**:
- GPU Utilization: 80-100%
- Memory Usage: 2-4GB (small), 6-8GB (medium), 14-16GB (large)
- Temperature: 60-80°C (normal)

#### Optimize Model Selection

**8GB VRAM (GTX 1080, RTX 3060)**:
```env
MUSICGEN_MODEL=small  # Best choice
```

**12GB VRAM (RTX 3080, RTX 3080 Ti)**:
```env
MUSICGEN_MODEL=medium  # Better quality
```

**24GB VRAM (RTX 4090, A6000)**:
```env
MUSICGEN_MODEL=large  # Best quality
```

#### Benchmark Performance

Run generation test:
```bash
bash scripts/generate-liberty-vote-blues.sh
```

Record times:
- Model load time: _____ seconds
- Generation time (120s song): _____ seconds
- Total time: _____ seconds

**Expected performance** (musicgen-small):
| Hardware | Load | Generate (120s) | Total |
|----------|------|-----------------|-------|
| CPU (16-core) | 10s | 600-1200s | ~10-20 min |
| GTX 1080 | 5s | 60-120s | ~1-2 min |
| RTX 4090 | 2s | 30-60s | ~30-60s |

---

## 📋 Pre-Flight Checklist

Before starting development, ensure:

### System
- [x] NVIDIA drivers updated
- [x] CUDA toolkit installed
- [x] Visual Studio Build Tools installed
- [x] GPU detected: `nvidia-smi` works

### Tools
- [x] Git installed and configured
- [x] Node.js 18+ installed
- [x] pnpm installed globally
- [x] Python 3.11 installed

### Project
- [x] Repository cloned
- [x] On correct branch: `vocal-integration`
- [x] Node modules installed: `node_modules/` exists
- [x] Python venv created: `.venv/` exists
- [x] Python dependencies installed
- [x] PyTorch with CUDA installed
- [x] AudioCraft installed

### Configuration
- [x] `.env` file created
- [x] Required variables set (NODE_ENV, PORT, MONGODB_URI)
- [x] Optional API keys configured (if using cloud engines)
- [x] MUSICGEN_DEVICE=cuda (if using GPU)

### Verification
- [x] All lints pass
- [x] All tests pass
- [x] All builds succeed
- [x] GPU detected by PyTorch
- [x] Services start without errors
- [x] Frontend loads at localhost:4200
- [x] Can generate music

---

## 🔥 Common Issues & Solutions

### Issue: CUDA Not Available

**Symptom**: `torch.cuda.is_available()` returns `False`

**Solutions**:
1. Check drivers: `nvidia-smi`
2. Check CUDA: `nvcc --version`
3. Reinstall PyTorch:
   ```bash
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
4. Restart terminal/IDE

### Issue: Import Errors

**Symptom**: `ModuleNotFoundError`

**Solutions**:
1. Activate venv: `.\.venv\Scripts\Activate.ps1`
2. Verify installation: `pip list | grep <package>`
3. Reinstall: `pip install -r requirements.txt`

### Issue: Port Already in Use

**Symptom**: `EADDRINUSE: address already in use :::3000`

**Solutions**:
1. Kill processes: `bash scripts/kill-all.sh`
2. Or manually: `netstat -ano | findstr :3000`, then `taskkill /PID <PID> /F`

### Issue: Out of Memory

**Symptom**: "CUDA out of memory"

**Solutions**:
1. Use smaller model: `MUSICGEN_MODEL=small`
2. Reduce duration (try 30s instead of 120s)
3. Close other GPU apps
4. Restart Python to clear cache

### Issue: Slow Generation

**Symptom**: Generation takes 10+ minutes

**Solutions**:
1. Verify GPU is being used: `nvidia-smi` should show activity
2. Check device setting: `MUSICGEN_DEVICE=cuda` in .env
3. Close other GPU applications
4. Use smaller model for faster results

---

## ✅ Success Criteria

Setup is complete when:

- [x] `pnpm dev` starts all services without errors
- [x] Frontend loads at http://localhost:4200
- [x] Backend API responds at http://localhost:3000/api
- [x] Python API docs visible at http://localhost:8000/docs
- [x] GPU detected: `nvidia-smi` shows your GPU
- [x] PyTorch detects GPU: `torch.cuda.is_available() == True`
- [x] Can generate 10s test song with MusicGen
- [x] GPU shows activity during generation (nvidia-smi)
- [x] Generated audio plays in browser
- [x] No console errors during normal operation

---

## 📞 Support Resources

- **Documentation**: `/docs` folder in repository
- **Hardware Guide**: [docs/hardware-requirements.md](./hardware-requirements.md)
- **AI Integration**: [docs/ai-integration.md](./ai-integration.md)
- **Migration Guide**: [docs/MIGRATION-CHECKLIST.md](./MIGRATION-CHECKLIST.md)
- **Setup Guide**: [docs/setup-guide-high-performance.md](./setup-guide-high-performance.md)

---

## ⏱️ Time Estimates

**First-Time Setup**:
- Prerequisites: 30-60 min (includes CUDA, drivers, Build Tools)
- Project Setup: 15-30 min (clone, install dependencies)
- Configuration: 10-15 min (create .env, get API keys)
- Verification: 10-15 min (run tests, start services)
- First Generation: 10-15 min (model download on first run)
- **Total**: 1.5 - 2.5 hours

**Experienced User** (prerequisites already installed):
- Clone and install: 10 min
- Configure: 5 min
- Verify and start: 5 min
- **Total**: 20-30 minutes

**Model Pre-Download** (optional, saves time later):
- musicgen-small: 5-10 min (~1.5GB)
- musicgen-medium: 10-15 min (~6GB)
- musicgen-large: 20-30 min (~15GB)
