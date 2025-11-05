#!/bin/bash
# Simple progress monitor - checks for new MP3 files

ASSETS_DIR="backend/src/assets/generated"
START_TIME=$(date +%s)

echo "🎤 Vocal Generation Monitor"
echo "================================"
echo "Started: $(date '+%H:%M:%S')"
echo "Watching: $ASSETS_DIR"
echo ""
echo "Expected: 15-20 minutes for full vocal generation"
echo "   - Bark model load: ~30s"
echo "   - Each vocal segment: ~2-3 min"
echo "   - Total segments: 7"
echo ""
echo "Checking for new files every 30 seconds..."
echo "================================"
echo ""

LAST_FILE=""
ITERATION=0

while true; do
    ITERATION=$((ITERATION + 1))
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    MINUTES=$((ELAPSED / 60))
    SECONDS=$((ELAPSED % 60))
    
    # Find most recent MP3 file
    LATEST_FILE=$(ls -t "$ASSETS_DIR"/*.mp3 2>/dev/null | head -1)
    
    if [ -n "$LATEST_FILE" ] && [ "$LATEST_FILE" != "$LAST_FILE" ]; then
        SIZE=$(ls -lh "$LATEST_FILE" | awk '{print $5}')
        FILENAME=$(basename "$LATEST_FILE")
        echo "[+$(printf '%02d:%02d' $MINUTES $SECONDS)] New file detected: $FILENAME ($SIZE)"
        LAST_FILE="$LATEST_FILE"
        
        # Check if file contains "vocal" in name
        if [[ "$FILENAME" == *"vocal"* ]] || [[ "$FILENAME" == *"blues"* ]]; then
            echo "   ✓ This appears to be our Liberty Blues with vocals!"
        fi
    fi
    
    # Show periodic status
    if [ $((ITERATION % 2)) -eq 0 ]; then
        echo "[+$(printf '%02d:%02d' $MINUTES $SECONDS)] Still generating... (check $(($MINUTES + 1)))"
    fi
    
    # Check if we've been running too long
    if [ $ELAPSED -gt 1800 ]; then  # 30 minutes
        echo ""
        echo "⚠️  Generation taking longer than expected (>30 min)"
        echo "   Check backend logs for issues"
        break
    fi
    
    sleep 30
done
