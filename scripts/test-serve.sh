#!/bin/bash

echo "Testing backend startup and detection..."

# Start backend
echo "Starting backend..."
NODE_ENV=development node backend/dist/main.js > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait and check
echo "Waiting for 'Application is running on' message..."
WAIT=0
MAX_WAIT=15

while [ $WAIT -lt $MAX_WAIT ]; do
    if grep -q "Application is running on" /tmp/backend.log 2>/dev/null; then
        echo "✅ Found message after ${WAIT}s!"
        echo "Last 5 lines of log:"
        tail -5 /tmp/backend.log
        kill $BACKEND_PID 2>/dev/null
        exit 0
    fi
    echo "  Waiting... ${WAIT}s"
    sleep 1
    WAIT=$((WAIT + 1))
done

echo "❌ Timeout after ${MAX_WAIT}s"
echo "Last 10 lines of log:"
tail -10 /tmp/backend.log
kill $BACKEND_PID 2>/dev/null
exit 1
