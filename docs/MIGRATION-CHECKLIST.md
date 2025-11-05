# Migration Checklist - Moving to High-Performance Machine

## Pre-Migration Checklist (Current Machine)

### ✅ Phase 1: Backup Critical Data

- [ ] **Export environment configuration**
  ```bash
  copy .env .env.backup
  copy .env.example .env.template
  ```

- [ ] **Backup Python environment**
  ```bash
  # List all installed packages
  .\.venv\Scripts\Activate.ps1
  pip freeze > requirements-migration.txt
  python --version > python-version.txt
  ```

- [ ] **Backup Node.js environment**
  ```bash
  pnpm list --depth 0 > package-snapshot.txt
  node --version > node-version.txt
  pnpm --version > pnpm-version.txt
  ```

- [ ] **Export database data** (if applicable)
  ```bash
  # MongoDB export (if using)
  mongodump --db true-north-audio --out ./backup/mongodb
  ```

- [ ] **Backup generated assets**
  ```bash
  # Copy all generated music/audio files
  xcopy /E /I backend\static\audio backup\audio
  xcopy /E /I backend\static\generated backup\generated
  ```

- [ ] **Backup AI models** (optional - saves 1-20GB download)
  ```bash
  # Copy HuggingFace cache (if MusicGen models downloaded)
  xcopy /E /I %USERPROFILE%\.cache\huggingface backup\huggingface
  xcopy /E /I %USERPROFILE%\.cache\torch backup\torch
  ```

- [ ] **Document custom configurations**
  - [ ] Note any custom proxy settings
  - [ ] Note any custom build configurations
  - [ ] Note any firewall/antivirus exceptions
  - [ ] Screenshot VS Code extensions list

- [ ] **Export API keys and credentials**
  - [ ] Suno API key
  - [ ] Udio API key
  - [ ] ElevenLabs API key
  - [ ] Any OAuth tokens or session data

- [ ] **Commit and push all code changes**
  ```bash
  git status
  git add .
  git commit -m "Pre-migration snapshot - $(date)"
  git push origin vocal-integration
  ```

### ✅ Phase 2: Verify Backup Integrity

- [ ] **Test environment file**
  ```bash
  # Verify .env.backup is readable
  type .env.backup
  ```

- [ ] **Verify package lists**
  ```bash
  # Check both files were created
  dir requirements-migration.txt
  dir package-snapshot.txt
  ```

- [ ] **Verify backup size**
  ```powershell
  # Check total backup size
  (Get-ChildItem -Path backup -Recurse | Measure-Object -Property Length -Sum).Sum / 1GB
  ```

- [ ] **Copy backups to external drive/cloud**
  - [ ] Copy `backup/` folder to external drive
  - [ ] Or upload to cloud storage (Google Drive, Dropbox, OneDrive)
  - [ ] Verify upload completed successfully

### ✅ Phase 3: Documentation

- [ ] **Document current working state**
  - [ ] Note which features are working
  - [ ] Note any known issues or workarounds
  - [ ] List current branch and last commit hash
  - [ ] Screenshot working application

- [ ] **Create transfer notes**
  ```bash
  # Create notes file
  echo "Migration Date: $(date)" > MIGRATION-NOTES.txt
  echo "Current Branch: $(git branch --show-current)" >> MIGRATION-NOTES.txt
  echo "Last Commit: $(git log -1 --oneline)" >> MIGRATION-NOTES.txt
  echo "Node Version: $(node --version)" >> MIGRATION-NOTES.txt
  echo "Python Version: $(python --version)" >> MIGRATION-NOTES.txt
  ```

---

## New Machine Setup Checklist

### ✅ Phase 1: System Prerequisites

- [ ] **Install Visual Studio Build Tools**
  ```powershell
  # Download and run installer
  Invoke-WebRequest -Uri https://aka.ms/vs/17/release/vs_BuildTools.exe -OutFile vs_BuildTools.exe
  .\vs_BuildTools.exe --quiet --wait --norestart --nocache `
    --add Microsoft.VisualStudio.Workload.VCTools `
    --add Microsoft.VisualStudio.Component.Windows10SDK.20348 `
    --includeRecommended
  ```

- [ ] **Update NVIDIA GPU drivers**
  - [ ] Visit: https://www.nvidia.com/download/index.aspx
  - [ ] Download latest Studio or Game Ready drivers
  - [ ] Install and restart

- [ ] **Install NVIDIA CUDA Toolkit 11.8 or 12.1**
  - [ ] Visit: https://developer.nvidia.com/cuda-downloads
  - [ ] Choose: Windows → x86_64 → 11.8 or 12.1
  - [ ] Install with default settings
  - [ ] Verify: `nvcc --version`

- [ ] **Install Git**
  ```powershell
  choco install git
  # Or download from: https://git-scm.com/
  ```

- [ ] **Install Node.js 18+ LTS**
  ```powershell
  choco install nodejs-lts
  # Verify
  node --version  # Should be 18.x or higher
  ```

- [ ] **Install pnpm**
  ```powershell
  npm install -g pnpm
  pnpm --version
  ```

- [ ] **Install Python 3.11**
  ```powershell
  choco install python311
  # Verify
  python --version  # Should be 3.11.x
  ```

- [ ] **Install MongoDB (if needed)**
  ```powershell
  choco install mongodb
  # Or use MongoDB Atlas (cloud)
  ```

### ✅ Phase 2: Clone and Setup Project

- [ ] **Clone repository**
  ```bash
  git clone https://github.com/JeffreySanford/true-north-audio.git
  cd true-north-audio
  git checkout vocal-integration
  ```

- [ ] **Restore environment file**
  ```bash
  # Copy from backup
  copy Z:\backup\.env.backup .env
  # Or recreate manually
  copy .env.example .env
  # Edit with your API keys
  ```

- [ ] **Install Node.js dependencies**
  ```bash
  pnpm install
  ```

- [ ] **Create Python virtual environment**
  ```bash
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

- [ ] **Upgrade pip and core tools**
  ```bash
  python -m pip install --upgrade pip setuptools wheel
  ```

- [ ] **Install Python dependencies**
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Install PyTorch with CUDA**
  ```bash
  # For CUDA 11.8 (GTX 1080, RTX 3060)
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  
  # For CUDA 12.1 (RTX 4070+)
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
  ```

- [ ] **Install audiocraft**
  ```bash
  pip install audiocraft
  ```

- [ ] **Verify CUDA installation**
  ```bash
  python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not detected')"
  ```

### ✅ Phase 3: Restore Cached Models (Optional)

- [ ] **Restore HuggingFace cache** (saves ~1-20GB download)
  ```bash
  # If you backed up models from old machine
  xcopy /E /I Z:\backup\huggingface %USERPROFILE%\.cache\huggingface
  xcopy /E /I Z:\backup\torch %USERPROFILE%\.cache\torch
  ```

- [ ] **Or download models fresh** (first generation will download automatically)
  ```bash
  # Pre-download musicgen-small (optional)
  python -c "from audiocraft.models import MusicGen; print('Downloading...'); MusicGen.get_pretrained('facebook/musicgen-small'); print('Done!')"
  ```

### ✅ Phase 4: Verification

- [ ] **Lint all projects**
  ```bash
  pnpm nx run-many --target=lint --all
  ```

- [ ] **Run all tests**
  ```bash
  pnpm nx run-many --target=test --all
  ```

- [ ] **Build all projects**
  ```bash
  pnpm nx run-many --target=build --all
  ```

- [ ] **Test Python engines**
  ```bash
  # Test MusicGen
  python -c "from ai_music_gen.engines.musicgen_local import get_model_info; import json; print(json.dumps(get_model_info(), indent=2))"
  
  # Test GPU detection
  python -c "import torch; assert torch.cuda.is_available(), 'CUDA not available!'; print('✓ GPU detected:', torch.cuda.get_device_name(0))"
  ```

### ✅ Phase 5: Start Application

- [ ] **Start development services**
  ```bash
  pnpm dev
  ```

- [ ] **Verify services are running**
  - [ ] Backend: http://localhost:3000/api
  - [ ] Python API: http://localhost:8000/docs
  - [ ] Ollama Proxy: http://localhost:11434
  - [ ] Frontend: http://localhost:4200

- [ ] **Test music generation**
  - [ ] Generate test song with local MusicGen
  - [ ] Verify GPU utilization (nvidia-smi)
  - [ ] Check audio output quality

### ✅ Phase 6: Performance Tuning

- [ ] **Monitor GPU usage during generation**
  ```powershell
  # In separate terminal
  nvidia-smi -l 1
  ```

- [ ] **Benchmark generation times**
  - [ ] 30s song generation time: _____ seconds
  - [ ] 120s song generation time: _____ seconds
  - [ ] GPU memory usage: _____ MB / _____ MB total

- [ ] **Optimize model selection**
  - [ ] If 8GB VRAM: Use `MUSICGEN_MODEL=small`
  - [ ] If 12GB+ VRAM: Consider `MUSICGEN_MODEL=medium`
  - [ ] If 24GB VRAM: Can use `MUSICGEN_MODEL=large`

- [ ] **Configure environment for optimal performance**
  ```env
  # In .env file
  MUSICGEN_MODEL=small  # or medium/large based on VRAM
  MUSICGEN_DEVICE=cuda  # Ensure GPU is used
  ```

---

## Post-Migration Checklist

### ✅ Functional Verification

- [ ] **Test all API endpoints**
  - [ ] POST /api/audio-asset/generate (MusicGen)
  - [ ] POST /api/audio-asset/generate (Suno)
  - [ ] POST /api/audio-asset/generate (Udio)
  - [ ] GET /api/audio-asset/credits/:engine
  - [ ] GET /api/audio-asset/list

- [ ] **Test all three engines**
  - [ ] Generate song with Suno (cloud)
  - [ ] Generate song with Udio (cloud)
  - [ ] Generate song with MusicGen (local)
  - [ ] Compare quality and speed

- [ ] **Test frontend features**
  - [ ] Engine selector dropdown
  - [ ] Genre selection
  - [ ] Duration slider (10-240s)
  - [ ] Lyrics input
  - [ ] Vocal style selection
  - [ ] Generate button functionality
  - [ ] Audio playback
  - [ ] Download functionality

### ✅ Performance Verification

- [ ] **Compare performance metrics**
  | Metric | Old Machine | New Machine | Improvement |
  |--------|-------------|-------------|-------------|
  | CPU Cores | _____ | _____ | _____ |
  | RAM | _____ GB | _____ GB | _____ GB |
  | GPU | _____ | _____ | - |
  | VRAM | _____ GB | _____ GB | _____ GB |
  | 30s Song | _____ sec | _____ sec | _____ faster |
  | 120s Song | _____ sec | _____ sec | _____ faster |

- [ ] **Verify GPU acceleration**
  ```bash
  # Should show GPU usage during generation
  nvidia-smi
  ```

### ✅ Documentation Updates

- [ ] **Update MIGRATION-NOTES.txt**
  - [ ] Record migration date
  - [ ] Note any issues encountered
  - [ ] Document performance improvements
  - [ ] List any configuration changes

- [ ] **Update README if needed**
  - [ ] Update hardware specs if significantly different
  - [ ] Update benchmark numbers
  - [ ] Note any new requirements

### ✅ Cleanup

- [ ] **Remove backup files from old machine**
  - [ ] Or archive for disaster recovery

- [ ] **Update documentation**
  - [ ] Mark migration as complete
  - [ ] Archive old machine setup notes

- [ ] **Test disaster recovery**
  - [ ] Verify backups are accessible
  - [ ] Ensure .env file is backed up securely
  - [ ] Confirm API keys still work

---

## Troubleshooting

### Issue: CUDA Not Detected

**Symptoms**: `torch.cuda.is_available()` returns `False`

**Solutions**:
1. Verify NVIDIA drivers installed: `nvidia-smi`
2. Verify CUDA toolkit installed: `nvcc --version`
3. Reinstall PyTorch with CUDA:
   ```bash
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Issue: Out of Memory

**Symptoms**: "CUDA out of memory" error during generation

**Solutions**:
1. Use smaller model: `MUSICGEN_MODEL=small` in .env
2. Reduce song duration
3. Close other GPU applications
4. Restart Python process to clear cache

### Issue: Import Errors

**Symptoms**: `ModuleNotFoundError` or import errors

**Solutions**:
1. Verify virtual environment is activated:
   ```bash
   .\.venv\Scripts\Activate.ps1
   ```
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Check Python version (should be 3.10-3.11)

### Issue: Port Already in Use

**Symptoms**: "EADDRINUSE" or "port already in use"

**Solutions**:
1. Kill existing processes:
   ```bash
   bash scripts/kill-all.sh
   ```
2. Or manually:
   ```powershell
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   ```

---

## Success Criteria

Migration is complete when:

- [x] All services start without errors
- [x] Frontend loads at http://localhost:4200
- [x] Backend API responds at http://localhost:3000/api
- [x] Python API responds at http://localhost:8000
- [x] GPU is detected and utilized (nvidia-smi shows activity)
- [x] All three engines can generate music
- [x] Generated audio plays correctly
- [x] All tests pass (lint, unit, e2e)
- [x] Performance meets or exceeds old machine
- [x] No console errors during normal operation

---

## Timeline Estimate

- **Phase 1-3 (Old Machine)**: 1-2 hours
- **Phase 1-2 (New Machine)**: 2-3 hours
- **Phase 3 (Model Download)**: 1-2 hours (if downloading fresh)
- **Phase 4-6 (Verification)**: 1-2 hours
- **Total**: 5-9 hours (or 2-4 hours if restoring cached models)

---

## Notes

- Keep old machine running until new machine is fully verified
- Test all critical workflows before decommissioning old machine
- Document any hardware-specific issues for future reference
- Consider keeping backups for 30 days after migration
