# Installing FFmpeg Development Libraries on Windows for Python `av`

The Python `av` package requires FFmpeg development libraries (not just ffmpeg.exe) to build and run correctly. These libraries provide the necessary headers and `.lib` files for compiling C extensions.

## Steps to Install FFmpeg Development Libraries

### 1. Download FFmpeg Development Build

#### Automated Step: Install FFmpeg binaries (runtime only)
You can use Chocolatey, Winget, or Scoop to install the FFmpeg runtime binaries automatically:

```powershell
choco install ffmpeg
# or
winget install ffmpeg
# or
scoop install ffmpeg
```

**Note:** These commands install only the runtime binaries (`ffmpeg.exe`, `ffprobe.exe`, etc.), NOT the development libraries required for Python `av`.

#### Manual Step: Download FFmpeg Development Libraries
- Go to the official FFmpeg site: https://ffmpeg.org/download.html
- Under "Windows" select a link to a development build (e.g., [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/)).
- Download the **"dev"** or **"shared"** build, which includes headers and `.lib` files (not just binaries).

### 2. Extract and Locate Libraries
- Extract the downloaded archive to a folder, e.g., `C:\ffmpeg-dev`.
- Inside, locate the `include` (headers) and `lib` (library files, e.g., `avformat.lib`, `avcodec.lib`, etc.).

### 3. Add FFmpeg to Environment Variables
- Add the `bin` folder to your `PATH` (for runtime DLLs).
- Add the `lib` folder to your `LIB` or `LIBPATH` environment variable.
- Add the `include` folder to your `INCLUDE` environment variable.

#### Example (PowerShell):
```powershell
$env:PATH += ";C:\ffmpeg-dev\bin"
$env:LIB += ";C:\ffmpeg-dev\lib"
$env:LIBPATH += ";C:\ffmpeg-dev\lib"
$env:INCLUDE += ";C:\ffmpeg-dev\include"
```

### 4. Verify Installation
- Open a new terminal and run:
  ```bash
  echo %LIB%
  echo %INCLUDE%
  ffmpeg -version
  ```
- Ensure the paths are set and ffmpeg runs.

### 5. Reinstall Python `av`
- In your project directory, run:
  ```bash
  pip install --force-reinstall av==11.0.0
  ```
- If successful, the build will find the required `.lib` files and complete.

## Troubleshooting
- If you see `LINK : fatal error LNK1181: cannot open input file 'avformat.lib'`, double-check your `LIB` and `INCLUDE` paths.
- Make sure you are using a compatible version of Visual Studio Build Tools (recommended: 2022 or later).
- If you have multiple Python environments, ensure you are installing into the correct one.

## References
- [FFmpeg Official Downloads](https://ffmpeg.org/download.html)
- [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
- [Python av Documentation](https://github.com/PyAV-Org/PyAV)

---
**Note:** These steps are required only for Windows users building the `av` package from source. On Linux/macOS, system package managers usually provide the necessary development libraries.
