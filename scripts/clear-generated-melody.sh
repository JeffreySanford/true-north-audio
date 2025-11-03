#!/bin/bash
# Remove all generated melody files from backend and frontend
set -e

rm -f backend/src/assets/generated/*.mp3
rm -f backend/src/assets/generated/*.wav
rm -f frontend/public/audio/generated/*.mp3
rm -f frontend/public/audio/generated/*.wav

# Add Python 3.13 to PATH for this session (customize path as needed)
export PATH="/c/Python313:/c/Python313/Scripts:$PATH"
echo "Python 3.13 added to PATH for this session."
