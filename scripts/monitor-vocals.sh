#!/bin/bash
# Monitor vocal generation progress with performance metrics

LOG_FILE="/tmp/backend.log"
START_TIME=$(date +%s)

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║         🎤 VOCAL GENERATION PROGRESS MONITOR                  ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Monitoring: $LOG_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Function to calculate elapsed time
elapsed_time() {
    local current=$(date +%s)
    local elapsed=$((current - START_TIME))
    local minutes=$((elapsed / 60))
    local seconds=$((elapsed % 60))
    printf "%02d:%02d" $minutes $seconds
}

# Function to show progress with timestamp
show_progress() {
    local line="$1"
    local timestamp=$(date '+%H:%M:%S')
    local elapsed=$(elapsed_time)
    echo "[$timestamp +${elapsed}] $line"
}

# Count total segments
TOTAL_SEGMENTS=7
echo "📊 Expected Progress:"
echo "   - Total vocal segments: $TOTAL_SEGMENTS (Verse, Chorus, Bridge, Outro)"
echo "   - Bark model load: ~30 seconds"
echo "   - Per segment: ~2-3 minutes"
echo "   - Estimated total: 15-20 minutes"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Track segments completed
SEGMENTS_DONE=0

# Follow the log and show progress
tail -f "$LOG_FILE" 2>/dev/null | while IFS= read -r line; do
    case "$line" in
        *"Loading Bark models"*)
            show_progress "⏳ Loading Bark TTS models (first time setup)..."
            ;;
        *"Bark models loaded"*)
            show_progress "✅ Bark models ready!"
            ;;
        *"Generating Verse"*|*"Generating Chorus"*|*"Generating Bridge"*|*"Generating Outro"*)
            SEGMENTS_DONE=$((SEGMENTS_DONE + 1))
            PERCENT=$((SEGMENTS_DONE * 100 / TOTAL_SEGMENTS))
            show_progress "🎤 Segment $SEGMENTS_DONE/$TOTAL_SEGMENTS ($PERCENT%) - ${line#*Generating }"
            ;;
        *"Generated "*"s at"*)
            show_progress "   ✓ ${line#*Vocals]}"
            ;;
        *"Resampling from"*)
            show_progress "🔄 ${line#*Vocals]}"
            ;;
        *"Error"*)
            show_progress "❌ ERROR: ${line#*Vocals]}"
            ;;
        *"MusicGen] Final duration"*)
            show_progress "✅ ${line#*MusicGen]}"
            ;;
        *"Saving to"*)
            show_progress "💾 ${line#*MusicGen]}"
            ;;
        *"Generation complete"*)
            show_progress "🎉 GENERATION COMPLETE!"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "✅ Total time: $(elapsed_time)"
            echo "✅ Segments completed: $SEGMENTS_DONE/$TOTAL_SEGMENTS"
            break
            ;;
    esac
done

echo ""
echo "Monitor stopped at: $(date '+%Y-%m-%d %H:%M:%S')"
