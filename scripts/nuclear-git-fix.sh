#!/bin/bash
# Nuclear option: Reset to origin/master and recommit all changes

echo "⚠️  GIT REPOSITORY REPAIR - NUCLEAR OPTION"
echo "=========================================="
echo ""
echo "This will:"
echo "1. Backup your current code to a temp branch"
echo "2. Reset master to origin/master (last clean state)"
echo "3. Re-apply all your changes in one clean commit"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

cd "$(dirname "$0")/.."

# Create backup branch
echo "📦 Creating backup branch..."
git branch backup-before-reset-$(date +%Y%m%d-%H%M%S) 2>/dev/null || true

# Show what we're about to lose
echo ""
echo "🔍 Commits that will be re-applied:"
git log --oneline origin/master..HEAD

# Save all current changes (including untracked)
echo ""
echo "💾 Saving all current files..."
git add -A
git stash push -m "Pre-reset backup $(date +%Y%m%d-%H%M%S)"

# Reset to clean origin state
echo ""
echo "🔄 Resetting to origin/master..."
git reset --hard origin/master

# Restore files
echo ""
echo "📂 Restoring your changes..."
git stash pop || true

# Remove generated files
echo ""
echo "🗑️  Removing generated files..."
rm -f backend/src/assets/generated/*.mp3 2>/dev/null || true
rm -f backend/src/assets/generated/*.wav 2>/dev/null || true
rm -f ai-music-gen/backend/src/assets/generated/*.mp3 2>/dev/null || true
rm -f ai-music-gen/backend/src/assets/generated/*.wav 2>/dev/null || true
rm -f test_bark_output.wav 2>/dev/null || true

# Stage everything except generated files
echo ""
echo "📝 Staging code changes..."
git add -A

echo ""
echo "✅ Ready to commit!"
echo ""
echo "Next steps:"
echo "1. Review changes: git status"
echo "2. Commit: git commit -m 'feat: Add Bark TTS vocal synthesis integration'"
echo "3. Push: git push origin master"
