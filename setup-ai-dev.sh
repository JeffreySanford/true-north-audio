#!/bin/bash
# AI Development Environment Setup
# For True North Audio - Desktop (i9 + RTX 3080)

set -e  # Exit on error

echo "🚀 True North Audio - AI Development Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check current state
echo "📊 Checking current system state..."
echo ""

echo "CPU Info:"
wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors 2>&1 || echo "⚠️  WMIC not available"
echo ""

echo "GPU Info:"
powershell -Command "Get-WmiObject Win32_VideoController | Where-Object {$_.Name -like '*NVIDIA*'} | Select-Object Name, AdapterRAM | Format-List" 2>&1 || echo "⚠️  PowerShell query failed"
echo ""

echo "Current PyTorch:"
python -c "import torch; print(f'Version: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')" 2>&1 || echo "⚠️  PyTorch not installed"
echo ""

# Step 2: VS Code Extensions
echo "📦 Step 1/4: Installing VS Code Extensions..."
echo ""

echo "Installing Continue.dev..."
code --install-extension continue.continue 2>&1 || echo "⚠️  Failed to install Continue.dev"

echo "Checking GitHub Copilot..."
if code --list-extensions | grep -q "github.copilot"; then
    echo "✅ GitHub Copilot already installed"
else
    echo "⚠️  GitHub Copilot not found (optional)"
fi
echo ""

# Step 3: Ollama
echo "🤖 Step 2/4: Ollama Installation"
echo ""
echo "Please install Ollama manually:"
echo "  1. Download from: https://ollama.com/download/windows"
echo "  2. Or run: winget install Ollama.Ollama"
echo ""
read -p "Press Enter when Ollama is installed and running..."
echo ""

# Verify Ollama
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found!"
    
    echo "📥 Downloading AI models (this takes 5-10 minutes)..."
    echo ""
    
    # Pull models
    echo "Pulling deepseek-coder:6.7b (optimized for RTX 3080 4GB VRAM)..."
    ollama pull deepseek-coder:6.7b || echo "⚠️  Failed to pull deepseek-coder"
    
    echo "Pulling codellama:7b (alternative model)..."
    ollama pull codellama:7b || echo "⚠️  Failed to pull codellama"
    
    echo "Pulling nomic-embed-text (for code search)..."
    ollama pull nomic-embed-text || echo "⚠️  Failed to pull nomic-embed-text"
    
    echo ""
    echo "✅ Models downloaded!"
    ollama list
else
    echo "❌ Ollama not found. Please install it and re-run this script."
    exit 1
fi
echo ""

# Step 4: CUDA + PyTorch
echo "🔥 Step 3/4: GPU Acceleration (PyTorch + CUDA)"
echo ""
echo "Current PyTorch status:"
python -c "import torch; print(f'Version: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}')"
echo ""

read -p "Do you want to install CUDA-enabled PyTorch? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 Installing PyTorch with CUDA support..."
    
    # Uninstall CPU version
    pip uninstall -y torch torchvision torchaudio 2>&1 || true
    
    # Install GPU version
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    
    echo ""
    echo "✅ PyTorch installation complete!"
    echo "Verifying CUDA support..."
    python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
    echo ""
    
    if python -c "import torch; exit(0 if torch.cuda.is_available() else 1)" 2>/dev/null; then
        echo "✅ GPU acceleration ENABLED! 🎉"
    else
        echo "⚠️  CUDA not available. You may need to install CUDA Toolkit:"
        echo "    Download from: https://developer.nvidia.com/cuda-downloads"
        echo "    Or run: winget install NVIDIA.CUDA"
    fi
else
    echo "⏭️  Skipping PyTorch GPU installation"
fi
echo ""

# Step 5: Configure Continue.dev
echo "⚙️  Step 4/4: Configuring Continue.dev..."
echo ""

CONTINUE_CONFIG="$HOME/.continue/config.json"
CONTINUE_DIR="$HOME/.continue"

mkdir -p "$CONTINUE_DIR"

cat > "$CONTINUE_CONFIG" << 'EOF'
{
  "models": [
    {
      "title": "DeepSeek Coder 6.7B (GPU)",
      "provider": "ollama",
      "model": "deepseek-coder:6.7b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "CodeLlama 7B (GPU)",
      "provider": "ollama",
      "model": "codellama:7b",
      "apiBase": "http://localhost:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "DeepSeek Coder",
    "provider": "ollama",
    "model": "deepseek-coder:6.7b",
    "apiBase": "http://localhost:11434"
  },
  "embeddingsProvider": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "apiBase": "http://localhost:11434"
  },
  "allowAnonymousTelemetry": false,
  "disableIndexing": false
}
EOF

echo "✅ Continue.dev configured at: $CONTINUE_CONFIG"
echo ""

# Summary
echo "=========================================="
echo "🎉 Setup Complete!"
echo "=========================================="
echo ""
echo "✅ Installed Components:"
echo "  - Continue.dev VS Code extension"
echo "  - Ollama local AI runtime"
echo "  - AI models: deepseek-coder, codellama, nomic-embed-text"
echo "  - PyTorch with GPU support (if selected)"
echo ""
echo "📊 Your Hardware:"
echo "  - CPU: i9-12900K (16 cores, 24 threads)"
echo "  - GPU: RTX 3080 (4GB VRAM)"
echo "  - RAM: 63.7GB"
echo ""
echo "🚀 Next Steps:"
echo "  1. Restart VS Code"
echo "  2. Open a code file"
echo "  3. Press Ctrl+I to use Continue.dev chat"
echo "  4. Start typing to get AI autocomplete"
echo "  5. Check GPU usage: nvidia-smi -l 1"
echo ""
echo "📚 Documentation:"
echo "  - AI_OPTIMIZATION_GUIDE.md (comprehensive guide)"
echo "  - PROJECT_STATUS.md (project progress)"
echo ""
echo "⚡ Performance Tips:"
echo "  - Use 'deepseek-coder:6.7b' for best quality on RTX 3080"
echo "  - Use 'codellama:7b' for faster responses"
echo "  - Monitor GPU: nvidia-smi -l 1"
echo "  - Check Ollama: ollama list"
echo ""
echo "🔧 Troubleshooting:"
echo "  - If AI is slow: Check 'nvidia-smi' shows GPU usage"
echo "  - If Ollama fails: Restart Ollama service"
echo "  - If VS Code doesn't see models: Check Continue.dev settings"
echo ""
echo "Happy coding! 🎸🎵"
