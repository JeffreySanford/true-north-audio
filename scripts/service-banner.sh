#!/bin/bash

# Service Readiness Banner
# Displays service status with timing after startup

START_TIME=$(date +%s)

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  🎵 TRUE NORTH AUDIO - SERVICE STATUS"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Wait a moment for services to fully start
sleep 3

# Function to check service and measure response time
check_service() {
    local port=$1
    local name=$2
    local endpoint=$3
    
    local start=$(date +%s%3N)
    if curl -s -o /dev/null -m 2 -w "%{http_code}" http://localhost:${port}${endpoint} > /tmp/status_${port}.txt 2>/dev/null; then
        local end=$(date +%s%3N)
        local elapsed=$((end - start))
        local status=$(cat /tmp/status_${port}.txt)
        
        if [ "$status" = "200" ] || [ "$status" = "000" ] && curl -s http://localhost:${port}${endpoint} >/dev/null 2>&1; then
            echo "  ✅ ${name} (${port})"
            echo "     http://localhost:${port}${endpoint}"
            echo "     Response time: ${elapsed}ms"
        else
            echo "  ⚠️  ${name} (${port}) - Status: ${status}"
        fi
    else
        echo "  ❌ ${name} (${port}) - Not responding"
    fi
    echo ""
}

# Check all services
check_service 3000 "Backend API" "/api"
check_service 4200 "Frontend" "/"
check_service 8000 "FastAPI (MusicGen)" "/docs"
check_service 11434 "Ollama Proxy" "/api/version"

END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))

echo "════════════════════════════════════════════════════════════════"
echo "  Total startup time: ${TOTAL_TIME}s"
echo "  Press Ctrl+C to stop all services"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Cleanup temp files
rm -f /tmp/status_*.txt
