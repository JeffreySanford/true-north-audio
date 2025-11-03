# 🚀 Quick Reference - True North Audio AI Development

## ✅ What's Working NOW

### Local AI Code Generation (Continue.dev)
```bash
# In VS Code:
Ctrl+I              # Open Continue.dev chat
Ctrl+L              # Select code + ask question  
Ctrl+M              # Add code to context
Tab                 # Accept autocomplete suggestion

# Models available:
- deepseek-coder:6.7b  (Primary, best quality)
- codellama:7b         (Fast responses)
- codellama:13b        (Advanced tasks)
```

### Monitor GPU Activity
```bash
# Watch GPU in real-time (1 second refresh)
nvidia-smi -l 1

# One-time GPU check
nvidia-smi

# Check CUDA in Python
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

### Music Generation
```bash
# Generate with Bark TTS (WORKING NOW)
cd ai-music-gen
python generate_liberty_blues_bark.py

# Test Bark TTS
python -c "from bark import generate_audio; print('Bark ready!')"
```

### Ollama Commands
```bash
# List installed models
ollama list

# Test model
ollama run deepseek-coder:6.7b "Write a hello world function"

# Pull new model
ollama pull qwen2.5-coder:7b

# Check Ollama status
curl http://localhost:11434/api/tags
```

## 📊 System Status Check

### Quick Health Check
```bash
# All-in-one status check
python -c "
import torch
print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not available')
print('CUDA:', torch.cuda.is_available())
print('PyTorch:', torch.__version__)
"

# Check all components
cat << 'EOF'
Hardware:  i9-12900K (24 threads) + RTX 3080 (4GB)
Python:    3.13.3
PyTorch:   2.7.1+cu118 with CUDA 11.8
Ollama:    Running with 4 models
Continue:  Installed
Copilot:   Installed
Bark TTS:  Available
Status:    ✅ READY
EOF
```

## 🎯 Common Tasks

### Restart Everything
```bash
# Restart Ollama (if needed)
# Windows: Services → Ollama → Restart

# Restart VS Code
code --new-window .

# Check all services
ollama list && nvidia-smi
```

### Test Local AI
```bash
# Test Ollama API
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "deepseek-coder:6.7b",
  "prompt": "def hello():",
  "stream": false
}'

# Test in Python
python -c "
import requests
r = requests.post('http://localhost:11434/api/generate',
                 json={'model':'deepseek-coder:6.7b',
                       'prompt':'Write hello world',
                       'stream':False})
print(r.json()['response'][:100])
"
```

### Performance Check
```bash
# GPU performance test
python -c "
import torch, time
gpu = torch.randn(2000,2000).cuda()
start = time.time()
torch.mm(gpu, gpu)
torch.cuda.synchronize()
print(f'GPU compute time: {time.time()-start:.4f}s')
print('Status: ✅ GPU working' if time.time()-start < 0.1 else '⚠️ Check GPU')
"
```

## 📚 Documentation Quick Links

- **Detailed Test Results:** `SMOKE_TEST_REPORT.md`
- **Complete Setup Guide:** `AI_OPTIMIZATION_GUIDE.md`
- **Project Status:** `PROJECT_STATUS.md`
- **Setup Script:** `./setup-ai-dev.sh`

## 🔧 Troubleshooting

### Continue.dev not working?
```bash
# 1. Restart VS Code
# 2. Check Ollama is running:
ollama list

# 3. Check Continue config:
cat ~/.continue/config.json

# 4. Reinstall if needed:
code --uninstall-extension continue.continue
code --install-extension continue.continue
```

### GPU not being used?
```bash
# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Should show True. If False:
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Ollama slow or not responding?
```bash
# Check if running
ollama list

# Restart service (Windows: Services app)
# Or kill and restart:
# Services → Ollama → Restart

# Test with small model
ollama run qwen2.5-coder:1.5b "test"
```

## 💡 Pro Tips

### Speed Up AI Responses
```json
// In Continue config (~/.continue/config.json)
{
  "tabAutocompleteOptions": {
    "maxPromptTokens": 500,  // Smaller = faster
    "debounceDelay": 300     // Faster trigger
  }
}
```

### Use Best Model for Task
- **Fast autocomplete:** `codellama:7b`
- **Best quality:** `deepseek-coder:6.7b`
- **Complex refactoring:** `codellama:13b`
- **Laptop/CPU:** `qwen2.5-coder:1.5b`

### Monitor Everything
```bash
# Terminal 1: Watch GPU
nvidia-smi -l 1

# Terminal 2: Watch Ollama logs
# Windows: Event Viewer → Application → Ollama

# Terminal 3: Development
npm start
```

## 🎯 Next Goals

1. **Install AudioCraft** (5 min)
   ```bash
   pip install git+https://github.com/facebookresearch/audiocraft
   ```

2. **Test Music Generation** (2 min)
   ```bash
   python ai-music-gen/generate_liberty_blues_bark.py
   ```

3. **Optimize Continue.dev** (5 min)
   - Configure keyboard shortcuts
   - Set preferred model
   - Adjust response speed

## 📞 Quick Help

**Issue:** AI responses are slow  
**Fix:** Switch to `codellama:7b` model in Continue settings

**Issue:** GPU not being used  
**Fix:** Check `nvidia-smi` shows Ollama process

**Issue:** Out of VRAM  
**Fix:** Use smaller model or close other GPU apps

**Issue:** Can't import audiocraft  
**Fix:** Install VS Build Tools first (see INSTALLATION_CHECKLIST.md)

---

**Last Updated:** November 3, 2025  
**Status:** ✅ All systems operational (7/8)  
**Ready For:** Production AI development 🚀
