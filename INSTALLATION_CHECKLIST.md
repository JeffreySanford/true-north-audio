# Visual Studio Build Tools Installation Checklist

## ⏳ Step 1: Download (In Progress)
- [ ] Download `vs_BuildTools.exe` from https://aka.ms/vs/17/release/vs_BuildTools.exe
- [ ] File size: ~1-2 MB (installer), will download ~7GB during installation

## 🔧 Step 2: Run Installer

1. **Locate** the downloaded `vs_BuildTools.exe` (usually in Downloads folder)
2. **Run** the installer (double-click)
3. **Allow** administrator permissions when prompted

## ✅ Step 3: Select Components

When the Visual Studio Installer opens:

### Required: Check "Desktop development with C++"
This is the main workload - CHECK THIS BOX!

### On the right side panel, make sure these are checked:
- [x] **MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)**
- [x] **Windows 11 SDK (10.0.22621.0)** or **Windows 10 SDK**
- [x] **C++ CMake tools for Windows**
- [x] **C++ ATL for latest v143 build tools (x86 & x64)** (optional but recommended)

### Installation Details:
- **Download size**: ~7GB
- **Installation time**: 20-30 minutes (depending on internet speed)
- **Disk space required**: ~7GB

## 📥 Step 4: Install

1. Click **"Install"** button (bottom right)
2. Wait for download and installation to complete
3. Do NOT close the installer until it says "Installation succeeded"

## 🔄 Step 5: Restart Terminal

**IMPORTANT**: Close ALL terminal windows and reopen them after installation completes.

The new PATH variables won't be available in existing terminals!

## ✅ Step 6: Verify Installation

Open a NEW terminal and run:

```bash
# Check if Visual Studio tools are available
where cl

# Expected output: C:\Program Files\Microsoft Visual Studio\...\cl.exe
```

If `cl.exe` is not found, you may need to run:
```bash
"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
```

## 🎸 Step 7: Install AudioCraft

Once Build Tools are installed and verified:

```bash
cd /c/repos/true-north-audio
pip install git+https://github.com/facebookresearch/audiocraft
```

This time, the `blis` compilation should succeed!

## ✅ Step 8: Verify AudioCraft

```bash
python -c "import audiocraft; print('✅ AudioCraft installed successfully!')"
```

## 🎵 Step 9: Test Music Generation

```bash
cd /c/repos/true-north-audio/ai-music-gen
python generate_liberty_blues.py
```

## 🚀 Step 10: Restart Frontend/Backend

If they're running:
```bash
# Stop them (Ctrl+C) and restart
cd /c/repos/true-north-audio/backend
npm start

# In another terminal
cd /c/repos/true-north-audio/frontend
npm start
```

The UI will automatically detect AudioCraft and enable the option!

---

## ⏰ Current Progress

- [x] Download initiated
- [ ] Installer running
- [ ] Components selected
- [ ] Installation in progress
- [ ] Installation complete
- [ ] Terminal restarted
- [ ] cl.exe verified
- [ ] AudioCraft installed
- [ ] AudioCraft verified
- [ ] Testing complete

---

## 💡 Tips

- **Coffee time**: The installation takes 20-30 minutes - perfect for a break!
- **Keep installer open**: Don't close it until it says complete
- **Restart terminal**: This is critical - new PATH won't work in old terminals
- **Check disk space**: Make sure you have at least 10GB free

## 🆘 Troubleshooting

### Issue: "cl.exe not found" after installation
**Solution**: Run the vcvars64.bat script or restart your computer

### Issue: AudioCraft still fails to compile
**Solution**: Make sure you restarted the terminal and run `where cl` to verify

### Issue: Installation failed
**Solution**: Check you have admin rights and ~7GB free disk space

---

## 📞 Next Steps After Installation

Once AudioCraft is installed, the True North Audio UI will show:

```
🎸 AudioCraft (MusicGen)
Full AI music generation with instruments and melody
✓ Available
```

You'll be able to generate professional AI music with full instrumental arrangements!
