#!/bin/bash
# Fix git push issues by excluding large generated files

set -e

cd "$(dirname "$0")"

echo "🔧 Fixing Git Repository Issues"
echo "================================"
echo ""

# Check if we have uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  You have uncommitted changes. Stashing them..."
    git stash
    STASHED=1
else
    STASHED=0
fi

# Update .gitignore to exclude generated files
echo ""
echo "📝 Updating .gitignore to exclude generated files..."

cat >> .gitignore << 'EOF'

# Generated audio files (large binaries, don't commit)
*.mp3
*.wav
backend/src/assets/generated/
ai-music-gen/backend/src/assets/generated/
test_bark_output.wav

# Bark model cache (huge files)
*.pt
.cache/
EOF

echo "✅ .gitignore updated"

# Remove any tracked generated files
echo ""
echo "🗑️  Removing large generated files from git tracking..."
git rm --cached backend/src/assets/generated/*.mp3 2>/dev/null || true
git rm --cached backend/src/assets/generated/*.wav 2>/dev/null || true
git rm --cached ai-music-gen/backend/src/assets/generated/*.mp3 2>/dev/null || true
git rm --cached ai-music-gen/backend/src/assets/generated/*.wav 2>/dev/null || true

# Restore stashed changes if any
if [ $STASHED -eq 1 ]; then
    echo ""
    echo "📦 Restoring your changes..."
    git stash pop
fi

echo ""
echo "✅ Repository cleaned!"
echo ""
echo "Next steps:"
echo "1. Commit the .gitignore changes:"
echo "   git add .gitignore"
echo "   git commit -m 'chore: exclude generated audio files from git'"
echo ""
echo "2. Try pushing again:"
echo "   git push origin master"
echo ""
echo "If push still fails, the corrupt object needs deeper fixing:"
echo "   git push origin master --force-with-lease"
