# Installing C++ Build Tools for AudioCraft

AudioCraft requires C++ compilation for the `blis` package (via spacy). Here's how to fix it:

## Option 1: Install Microsoft Visual C++ Build Tools (Recommended)

1. **Download Build Tools**:
   - Visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Or direct download: https://aka.ms/vs/17/release/vs_BuildTools.exe

2. **Install with Desktop Development with C++**:
   - Run `vs_BuildTools.exe`
   - Select "Desktop development with C++"
   - Make sure these are checked:
     - MSVC v143 - VS 2022 C++ x64/x86 build tools
     - Windows 10/11 SDK
     - C++ CMake tools for Windows
   - Size: ~7GB
   - Install time: ~20-30 minutes

3. **Restart your terminal** after installation

4. **Retry AudioCraft installation**:
   ```bash
   pip install git+https://github.com/facebookresearch/audiocraft
   ```

## Option 2: Use Pre-built Wheels (Faster)

Try installing spacy with pre-built wheels first, which might allow AudioCraft to install:

```bash
# Install spacy with pre-built wheels
pip install spacy==3.7.6 --only-binary :all:

# Then try AudioCraft
pip install git+https://github.com/facebookresearch/audiocraft
```

## Option 3: Use Alternative Python Version

Python 3.11 or 3.10 may have better pre-built wheel support:

```bash
# Download Python 3.11 from python.org
# Then create virtual environment:
python3.11 -m venv .venv-py311
.venv-py311\Scripts\activate
pip install -r requirements.txt
pip install git+https://github.com/facebookresearch/audiocraft
```

## Option 4: Skip AudioCraft - Use Bark TTS Instead

**You already have this working!** Use the Bark TTS version:

```bash
cd /c/repos/true-north-audio/ai-music-gen
C:/Python313/python.exe generate_liberty_blues_bark.py
```

This uses:
- ✅ Bark TTS for vocals (already installed)
- ✅ MIDI for instrumentals (no dependencies)
- ✅ No C++ compilation needed

## Current Status

Your system has:
- ✅ Python 3.13.3
- ✅ Bark TTS (suno-bark 0.1.5)
- ✅ Core audio libraries (torch, scipy, numpy, mido)
- ❌ AudioCraft (blocked by blis compilation)

The error you're seeing is:
```
[COMMAND] C:\Program Files\LLVM\bin\clang.exe -c ...
error: [WinError 2] The system cannot find the file specified
```

This means pip is trying to use clang (from LLVM) but the build setup is incorrect for Windows.

## Recommended Next Steps

1. **Quick win**: Use `generate_liberty_blues_bark.py` (works now!)
2. **If you want AudioCraft**: Install VS Build Tools (Option 1)
3. **Alternative**: Try Python 3.11 with better wheel support (Option 3)
