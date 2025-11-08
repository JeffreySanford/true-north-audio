# PowerShell script to set up FFmpeg development environment for Python av
# Usage: Run in a PowerShell window after extracting FFmpeg to C:\ffmpeg-dev

$ffmpegDevPath = "C:\FFMPEG"

# Add FFmpeg bin to PATH
$env:PATH += ";$ffmpegDevPath\bin"
# Add FFmpeg lib to LIB and LIBPATH
$env:LIB += ";$ffmpegDevPath\lib"
$env:LIBPATH += ";$ffmpegDevPath\lib"
# Add FFmpeg include to INCLUDE
$env:INCLUDE += ";$ffmpegDevPath\include"

Write-Host "FFmpeg dev environment variables set for this session."
Write-Host "PATH: $env:PATH"
Write-Host "LIB: $env:LIB"
Write-Host "INCLUDE: $env:INCLUDE"

# Verify ffmpeg is available
ffmpeg -version

# Reinstall Python av
Write-Host "Reinstalling Python av..."
pip install --force-reinstall av==11.0.0

Write-Host "If you see no errors above, FFmpeg dev setup is complete!"
