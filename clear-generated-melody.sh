#!/bin/bash
# Remove all generated melody files from backend and frontend
set -e

rm -f backend/src/assets/generated/*.mp3
rm -f backend/src/assets/generated/*.wav
rm -f frontend/public/audio/generated/*.mp3
rm -f frontend/public/audio/generated/*.wav
