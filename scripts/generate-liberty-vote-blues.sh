#!/bin/bash
# Generate Liberty Vote Blues using the API

API_URL="http://localhost:3000/api/musicgen/generate"
CONFIG_FILE="$(dirname "$0")/liberty-vote-blues.json"

echo "=========================================="
echo "  Liberty Vote Blues - Music Generation"
echo "=========================================="
echo ""

# Check if backend is running
if ! curl -s http://localhost:3000/api > /dev/null 2>&1; then
    echo "❌ Backend is not running on port 3000"
    echo "   Please start services with: ./scripts/serve-all.sh"
    exit 1
fi

echo "✅ Backend is running"
echo ""
echo "📝 Configuration: $CONFIG_FILE"
echo "🎵 Generating Liberty Vote Blues..."
echo ""

# Generate the song
RESPONSE=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d @"$CONFIG_FILE")

# Parse response
AUDIO_URL=$(echo "$RESPONSE" | grep -o '"audio_url":"[^"]*"' | cut -d'"' -f4)
ERROR=$(echo "$RESPONSE" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)

if [ -n "$ERROR" ] && [ "$ERROR" != "null" ]; then
    echo "❌ Generation failed:"
    echo "   $ERROR"
    exit 1
fi

if [ -z "$AUDIO_URL" ] || [ "$AUDIO_URL" = "null" ]; then
    echo "❌ No audio URL returned"
    echo "   Response: $RESPONSE"
    exit 1
fi

echo "✅ Generation complete!"
echo ""
echo "🎵 Audio URL: $AUDIO_URL"
echo "🌐 Full URL: http://localhost:3000$AUDIO_URL"
echo ""

# Try to play the song
FULL_URL="http://localhost:3000$AUDIO_URL"
echo "🎧 Opening in browser..."
start "$FULL_URL" 2>/dev/null || open "$FULL_URL" 2>/dev/null || xdg-open "$FULL_URL" 2>/dev/null

echo ""
echo "✨ Done!"
