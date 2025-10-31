#!/bin/bash
# Sync all generated .mp3 files from backend to frontend for serving
set -e

SRC="backend/src/assets/generated"
DEST="frontend/public/audio/generated"

mkdir -p "$DEST"
cp "$SRC"/*.mp3 "$DEST"/
