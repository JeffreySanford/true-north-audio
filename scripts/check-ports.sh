#!/bin/bash

# Port checking utility for True North Audio
# Usage: bash check-ports.sh

echo "=== TRUE NORTH AUDIO PORT STATUS ==="
echo ""

# Function to check a single port (Windows-compatible)
check_port() {
    local port=$1
    local name=$2
    
    # Use netstat for Windows Git Bash compatibility
    if netstat -ano 2>/dev/null | grep -q ":${port}.*LISTENING"; then
        echo "⚠️  Port ${port} (${name}): ACTIVE"
        return 1
    else
        echo "✅ Port ${port} (${name}): FREE"
        return 0
    fi
}

# Check all required ports
ALL_FREE=0

check_port 3000 "Backend" || ALL_FREE=1
check_port 4200 "Frontend" || ALL_FREE=1
check_port 8000 "FastAPI" || ALL_FREE=1
# Ollama (11434) is allowed to be active; do not set ALL_FREE=1 for it
check_port 11434 "Ollama"

# Check for MongoDB Memory Server processes
MONGO_PROCESSES=$(ps aux 2>/dev/null | grep -i mongod | grep -v grep | wc -l)
if [ "$MONGO_PROCESSES" -gt 0 ]; then
    echo "ℹ️  MongoDB Memory Server processes: $MONGO_PROCESSES (OK for testing)"
else
    echo "✅ MongoDB Memory Server: Not running"
fi

echo ""

if [ $ALL_FREE -eq 0 ]; then
    echo "✅ All ports are free and ready!"
    exit 0
else
    echo "⚠️  Some ports are in use. Run 'pnpm kill:all' to free them."
    exit 1
fi
