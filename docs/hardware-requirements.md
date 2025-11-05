# Hardware Requirements & Configuration

## Current System Configuration (November 2025)

This project is being developed on a high-performance workstation optimized for AI music generation.

### Specifications
- **CPU**: High-core count processor (16+ cores recommended)
- **RAM**: 32GB+ (64GB recommended for large models)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (e.g., GTX 1080, RTX 3060, RTX 4070)
- **Storage**: SSD with 50GB+ free space for models and generated assets
- **OS**: Windows 10/11 with WSL2, or Linux (Ubuntu 20.04+)

## AI Music Generation Engines

The project supports three music generation engines with different hardware requirements:

### 1. Cloud-Based Engines (Suno, Udio)
**Hardware Requirements**: Minimal (runs in cloud)
- **CPU**: Any modern CPU
- **RAM**: 4GB+
- **Network**: Stable internet connection
- **Storage**: Minimal (only stores downloaded results)

**Pros**:
- Professional-quality output (⭐⭐⭐⭐⭐)
- Fast generation (30-60 seconds)
- No local GPU required
- Always uses latest models

**Cons**:
- Requires API credits (free tier available)
- Data sent to cloud (privacy concerns)
- Requires internet connection
- Limited free tier (10-50 songs/day)

### 2. Local MusicGen (Meta AudioCraft)
**Hardware Requirements**: Moderate to High
- **CPU**: 8+ cores (for CPU-only mode)
- **RAM**: 16GB minimum, 32GB+ recommended
- **GPU**: NVIDIA GPU with CUDA support
  - **Minimum**: GTX 1060 (6GB VRAM) - musicgen-small
  - **Recommended**: GTX 1080 (8GB VRAM) - musicgen-small/medium
  - **High-end**: RTX 3090/4090 (24GB VRAM) - musicgen-large
- **Storage**: 2-20GB for models

**Model Sizes**:
| Model | Parameters | VRAM | Download Size | Quality | Speed (GPU) |
|-------|-----------|------|---------------|---------|-------------|
| **musicgen-small** | 300M | 2GB | 1.5GB | ⭐⭐⭐ | Fast (10-30s) |
| **musicgen-medium** | 1.5B | 6GB | 6GB | ⭐⭐⭐⭐ | Medium (30-60s) |
| **musicgen-large** | 3.3B | 16GB | 15GB | ⭐⭐⭐⭐⭐ | Slow (60-180s) |
| **musicgen-melody** | 300M | 2GB | 1.5GB | ⭐⭐⭐ | Fast (10-30s) |

**Pros**:
- 100% local (complete privacy)
- Unlimited generations (no API costs)
- Full control over model parameters
- Works offline

**Cons**:
- Requires significant hardware
- Lower quality than cloud services
- First run downloads large models
- Slower generation times

## GPU Configuration

### CUDA Setup for NVIDIA GPUs

To utilize your NVIDIA GPU for faster local generation:

1. **Check Current PyTorch Installation**:
```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available())"
```

2. **Install CUDA-enabled PyTorch** (if CPU-only):
```bash
# For CUDA 11.8 (most compatible)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1 (newer GPUs)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

3. **Verify GPU Detection**:
```bash
python -c "import torch; print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not found')"
```

### Expected Performance

**MusicGen-Small on Different Hardware**:
| Hardware | 30s Song | 120s Song | Model Load |
|----------|----------|-----------|------------|
| CPU (16-core) | ~2-5 min | ~10-20 min | ~10s |
| GTX 1080 (8GB) | ~15-30s | ~60-120s | ~5s |
| RTX 3090 (24GB) | ~10-20s | ~40-80s | ~3s |
| RTX 4090 (24GB) | ~8-15s | ~30-60s | ~2s |

## Minimum vs Recommended Configurations

### Minimum (Cloud-Only)
- **CPU**: Dual-core Intel/AMD
- **RAM**: 8GB
- **GPU**: Not required
- **Network**: Broadband internet
- **Use Case**: Testing, free tier usage, occasional generation

### Recommended (Hybrid)
- **CPU**: 8+ cores Intel i7/Ryzen 7
- **RAM**: 32GB
- **GPU**: NVIDIA RTX 3060 (12GB VRAM) or better
- **Storage**: 512GB SSD
- **Use Case**: Active development, privacy tier + cloud tier

### High-Performance (Local-First)
- **CPU**: 16+ cores Intel i9/Ryzen 9/Threadripper
- **RAM**: 64GB+
- **GPU**: NVIDIA RTX 4090 (24GB VRAM) or A6000
- **Storage**: 1TB+ NVMe SSD
- **Use Case**: Production workloads, large-scale generation, professional use

## Model Storage Locations

Models are cached in the following locations:
- **HuggingFace Cache**: `~/.cache/huggingface/` or `C:\Users\<username>\.cache\huggingface\`
- **AudioCraft Models**: `~/.cache/torch/hub/`
- **Suno/Udio**: No local models (cloud-based)

To clear model cache and free space:
```bash
# Linux/Mac
rm -rf ~/.cache/huggingface/
rm -rf ~/.cache/torch/

# Windows (PowerShell)
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\huggingface\
Remove-Item -Recurse -Force $env:USERPROFILE\.cache\torch\
```

## Network Requirements

### Cloud Engines (Suno, Udio)
- **Bandwidth**: 5 Mbps+ for smooth operation
- **Latency**: <200ms for API calls
- **Data Usage**: ~10-20MB per generation (depends on song length)

### Local MusicGen
- **Initial Setup**: 1.5-15GB download (one-time, per model)
- **Runtime**: No network required after model download

## Development Environment Setup

### Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install audiocraft torch torchaudio elevenlabs python-dotenv requests
```

### Environment Variables
Create `.env` file in project root:
```env
# Cloud API Keys (optional, for cloud engines)
SUNO_API_KEY=your_suno_api_key_here
UDIO_API_KEY=your_udio_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# Model Configuration (for local MusicGen)
MUSICGEN_MODEL=small  # or medium, large, melody
MUSICGEN_DEVICE=cuda  # or cpu
MUSICGEN_CACHE_DIR=~/.cache/musicgen
```

## Monitoring & Optimization

### GPU Monitoring
```bash
# Watch GPU usage in real-time
nvidia-smi -l 1

# Check memory usage
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

### CPU Monitoring
```bash
# Windows (PowerShell)
Get-Counter '\Processor(_Total)\% Processor Time'

# Linux
htop
```

### Memory Optimization
- **Close unused applications** before generation
- **Use musicgen-small** for GTX 1080 (8GB VRAM)
- **Enable mixed precision** (automatic in AudioCraft)
- **Reduce batch size** if OOM errors occur

## Troubleshooting

### "CUDA out of memory"
- Use smaller model (small instead of medium/large)
- Reduce song duration
- Close other GPU applications
- Restart Python kernel to clear cache

### "Model download failed"
- Check internet connection
- Verify HuggingFace is accessible
- Manually download from: https://huggingface.co/facebook/musicgen-small
- Place in cache directory

### "Generation too slow on CPU"
- Install CUDA-enabled PyTorch
- Verify GPU detection
- Update NVIDIA drivers
- Use cloud engines for faster results

## Future Hardware Considerations

As AI models evolve, hardware requirements may increase. Plan for:
- **GPU VRAM**: 16GB+ becoming standard for high-quality models
- **System RAM**: 64GB+ for running multiple models simultaneously
- **Storage**: NVMe SSDs for faster model loading
- **Network**: High-speed internet for cloud hybrid workflows
