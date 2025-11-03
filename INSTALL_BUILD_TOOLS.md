# Installing Microsoft Visual C++ Build Tools

## Quick Start

### Step 1: Download Build Tools
Download from: https://aka.ms/vs/17/release/vs_BuildTools.exe
Or visit: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Step 2: Install with Required Components

1. Run `vs_BuildTools.exe`
2. Select "Desktop development with C++"
3. Make sure these are checked in the right panel:
   - ✅ MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)
   - ✅ Windows 11 SDK (10.0.22621.0) or Windows 10 SDK
   - ✅ C++ CMake tools for Windows
   - ✅ C++ ATL for latest build tools

4. Click Install (requires ~7GB disk space)
5. Wait ~20-30 minutes for installation

### Step 3: Verify Installation

Open a NEW terminal (important - restart your terminal) and run:

```bash
# Check if cl.exe (MSVC compiler) is available
where cl

# If not found, you may need to run Developer Command Prompt or:
"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
```

### Step 4: Install AudioCraft

Once Build Tools are installed and you've restarted your terminal:

```bash
cd /c/repos/true-north-audio
pip install git+https://github.com/facebookresearch/audiocraft
```

This time it should successfully compile blis and complete the installation!

### Step 5: Verify AudioCraft Installation

```bash
python -c "import audiocraft; print('AudioCraft installed successfully!')"
```

## Alternative: One-Line PowerShell Installation

Open PowerShell as Administrator and run:

```powershell
# Download and install Build Tools silently
Invoke-WebRequest -Uri "https://aka.ms/vs/17/release/vs_BuildTools.exe" -OutFile "$env:TEMP\vs_BuildTools.exe"
Start-Process -FilePath "$env:TEMP\vs_BuildTools.exe" -ArgumentList "--quiet", "--wait", "--norestart", "--nocache", "--add", "Microsoft.VisualStudio.Workload.VCTools", "--includeRecommended" -Wait
```

**Note**: This will take ~20-30 minutes and requires ~7GB of disk space.

## What This Fixes

The Build Tools provide:
- `cl.exe` - Microsoft C/C++ Compiler
- `link.exe` - Microsoft Linker
- Windows SDK headers and libraries
- CMake and build infrastructure

This allows Python packages like `blis` (required by `spacy` 3.7.6) to compile C++ extensions on Windows.

## After Installation

You'll have access to both:
- 🎸 **AudioCraft/MusicGen** - Full AI music generation with instruments
- 🎤 **Bark TTS** - AI vocals and speech synthesis

The updated UI will let you choose which engine to use!
