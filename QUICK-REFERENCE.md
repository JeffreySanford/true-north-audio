# Quick Reference Card - Machine Setup & Migration

## 🚀 30-Minute Quick Setup

### Prerequisites
```powershell
# Install with Chocolatey (run as Administrator)
choco install git nodejs-lts python311 -y
npm install -g pnpm
```

### Setup
```bash
# 1. Clone
git clone https://github.com/JeffreySanford/true-north-audio.git
cd true-north-audio
git checkout vocal-integration

# 2. Install Node
pnpm install

# 3. Python environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 4. GPU Support (optional but recommended)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install audiocraft

# 5. Configure
copy .env.example .env
# Edit .env with API keys (optional)

# 6. Run
pnpm dev
# Open: http://localhost:4200
```

---

## 📦 Migration Checklist

### Old Machine (Backup)
```bash
# 1. Environment
copy .env .env.backup
pip freeze > requirements-migration.txt

# 2. Code
git add . && git commit -m "Pre-migration" && git push

# 3. Models (optional, saves 1-20GB download)
xcopy /E /I %USERPROFILE%\.cache\huggingface Z:\backup\huggingface
```

### New Machine (Restore)
```bash
# 1. Clone
git clone <repo> && cd true-north-audio

# 2. Follow 30-minute setup above

# 3. Restore .env
copy Z:\backup\.env.backup .env

# 4. Restore models (optional)
xcopy /E /I Z:\backup\huggingface %USERPROFILE%\.cache\huggingface
```

---

## 🧪 Test Commands

```bash
# Fast tests (5-10 seconds)
bash scripts/test-all-engines.sh --fast

# Full tests with report
bash scripts/test-all-engines.sh --report

# Test specific engine
bash scripts/test-all-engines.sh --engine musicgen

# Manual Python tests
python tests/test_all_engines.py --verbose
```

---

## 🔧 GPU Setup

```bash
# 1. Install CUDA Toolkit
# Download: https://developer.nvidia.com/cuda-downloads
# Choose CUDA 11.8 (most compatible) or 12.1 (newer GPUs)

# 2. Install CUDA PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. Verify
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not found')"

# Expected: CUDA: True, GPU: NVIDIA GeForce <model>
```

---

## ⚙️ Environment Variables (.env)

```env
# REQUIRED
NODE_ENV=development
PORT=3000
MONGODB_URI=mongodb://localhost:27017/true-north-audio

# CLOUD ENGINES (Optional - free tiers available)
SUNO_API_KEY=          # 50 songs/day free
UDIO_API_KEY=          # 3 songs/day free
ELEVENLABS_API_KEY=    # 10k chars/month free

# LOCAL MUSICGEN
MUSICGEN_MODEL=small   # or medium, large
MUSICGEN_DEVICE=cuda   # or cpu
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **CUDA not detected** | `pip uninstall torch && pip install torch --index-url https://download.pytorch.org/whl/cu118` |
| **Port in use** | `bash scripts/kill-all.sh` |
| **Import errors** | `.\.venv\Scripts\Activate.ps1 && pip install -r requirements.txt` |
| **Out of memory** | Set `MUSICGEN_MODEL=small` in .env |
| **Slow generation** | Check GPU usage: `nvidia-smi`, verify `MUSICGEN_DEVICE=cuda` |

---

## 📊 Performance Benchmarks

### MusicGen-Small Generation Times (30s song)
| Hardware | Time |
|----------|------|
| CPU (16-core) | 2-5 min |
| GTX 1080 (8GB) | 15-30s |
| RTX 4090 (24GB) | 8-15s |

---

## 📚 Documentation

| Document | Use Case |
|----------|----------|
| **[MACHINE-SETUP-CHECKLIST.md](docs/MACHINE-SETUP-CHECKLIST.md)** | New machine setup |
| **[MIGRATION-CHECKLIST.md](docs/MIGRATION-CHECKLIST.md)** | Hardware migration |
| **[TESTING-GUIDE.md](docs/TESTING-GUIDE.md)** | Running tests |
| **[hardware-requirements.md](docs/hardware-requirements.md)** | Hardware specs |
| **[ai-integration.md](docs/ai-integration.md)** | AI engines overview |

---

## 🎯 Quick Verification

```bash
# ✓ All should pass
pnpm nx run-many --target=lint --all
pnpm nx run-many --target=test --all
bash scripts/test-all-engines.sh --fast

# ✓ GPU check
nvidia-smi
python -c "import torch; assert torch.cuda.is_available()"

# ✓ Services running
curl http://localhost:3000/api      # Backend
curl http://localhost:8000/docs     # Python API
curl http://localhost:11434         # Ollama
open http://localhost:4200          # Frontend
```

---

## 🔑 Free API Keys

| Service | Free Tier | Signup |
|---------|-----------|--------|
| **Suno** | 50 songs/day | https://suno.com/ |
| **Udio** | 3 songs/day | https://udio.com/ |
| **ElevenLabs** | 10k chars/month | https://elevenlabs.io/ |

---

## 💡 Pro Tips

1. **Use fast tests during development**: `bash scripts/test-all-engines.sh --fast`
2. **Pre-download models**: Run first generation during lunch break
3. **Monitor GPU**: Keep `nvidia-smi -l 1` running in separate terminal
4. **Backup .env**: Never commit, always backup before migration
5. **Use smaller model**: Start with `musicgen-small`, upgrade if needed

---

**Full Documentation**: [docs/README.md](docs/README.md)  
**Support**: Create issue on GitHub repository  
**Version**: 1.0 (November 2025)
