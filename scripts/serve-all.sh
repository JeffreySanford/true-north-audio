#!/bin/bash
set -e  # Exit on error

# Get absolute workspace root
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Parse arguments
VERBOSE=0
if [ "$1" = "--verbose" ] || [ "$1" = "-v" ]; then
    VERBOSE=1
fi

# Log files
BACKEND_LOG="/tmp/backend.log"
FRONTEND_LOG="/tmp/frontend.log"
FASTAPI_LOG="/tmp/fastapi.log"
OLLAMA_LOG="/tmp/ollama.log"

# Track PIDs for cleanup
BACKEND_PID=""
FRONTEND_PID=""
FASTAPI_PID=""
OLLAMA_PID=""

# Verbose output function
verbose_log() {
    if [ $VERBOSE -eq 1 ]; then
        echo "  [DEBUG] $1"
    fi
}

# Status reporting
print_stage() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

print_success() {
    echo "  ✅ $1"
}

print_error() {
    echo "  ❌ $1"
}

print_info() {
    echo "  ℹ️  $1"
}

print_waiting() {
    echo "  ⏳ $1"
}

# Cleanup function
cleanup() {
    echo ""
    print_stage "��� SHUTTING DOWN SERVICES"
    
    if [ -n "$FRONTEND_PID" ]; then
        echo "  Stopping Frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null && print_success "Frontend stopped" || print_info "Already stopped"
    fi
    
    if [ -n "$OLLAMA_PID" ]; then
        echo "  Stopping Ollama Proxy (PID: $OLLAMA_PID)..."
        kill $OLLAMA_PID 2>/dev/null && print_success "Ollama Proxy stopped" || print_info "Already stopped"
    fi
    
    if [ -n "$FASTAPI_PID" ]; then
        echo "  Stopping FastAPI (PID: $FASTAPI_PID)..."
        kill $FASTAPI_PID 2>/dev/null && print_success "FastAPI stopped" || print_info "Already stopped"
    fi
    
    if [ -n "$BACKEND_PID" ]; then
        echo "  Stopping Backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null && print_success "Backend stopped" || print_info "Already stopped"
    fi
    
    echo ""
    print_success "All services stopped"
    echo ""
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

clear
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║         ��� TRUE NORTH AUDIO - STARTING ALL SERVICES           ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

if [ $VERBOSE -eq 1 ]; then
    echo "  ��� VERBOSE MODE ENABLED"
    echo ""
fi

START_TIME=$(date +%s)

# ============================================================================
# STAGE 1: CLEANUP
# ============================================================================
print_stage "��� STAGE 1: CLEANUP EXISTING PROCESSES"

verbose_log "Killing node processes..."
taskkill //F //IM node.exe 2>&1 | grep -v "ERROR" >/dev/null && print_success "Node processes stopped" || print_info "No node processes running"

verbose_log "Killing python processes..."
taskkill //F //IM python.exe 2>&1 | grep -v "ERROR" >/dev/null && print_success "Python processes stopped" || print_info "No Python processes running"

verbose_log "Checking ports 3000, 4200, 8000, 11434..."
for port in 3000 4200 8000 11434; do
    PID=$(netstat -ano | grep ":$port.*LISTENING" | awk '{print $5}' | head -1)
    if [ -n "$PID" ]; then
        verbose_log "Killing process on port $port (PID: $PID)"
        taskkill //F //PID $PID 2>&1 | grep -v "ERROR" >/dev/null
    fi
done

verbose_log "Resetting Nx cache..."
npx nx reset > /dev/null 2>&1
print_success "Cleanup complete"

# ============================================================================
# STAGE 2: BUILD BACKEND
# ============================================================================
print_stage "��� STAGE 2: BUILD BACKEND"

verbose_log "Running: npx nx run @true-north-audio/backend:build --skip-nx-cache"

npx nx run @true-north-audio/backend:build --skip-nx-cache
BUILD_EXIT=$?

if [ $BUILD_EXIT -eq 0 ]; then
    print_success "Backend build complete"
else
    print_error "Backend build failed"
    exit 1
fi

# ============================================================================
# STAGE 3: START BACKEND
# ============================================================================
print_stage "��� STAGE 3: START BACKEND (Port 3000)"

print_info "Backend will use in-memory MongoDB (mongodb-memory-server)"
print_info "First run may download MongoDB binaries (~200MB, 1-2 min)"
echo ""

verbose_log "Log file: $BACKEND_LOG"
verbose_log "Command: NODE_ENV=development node backend/dist/main.js"

# Start backend in background
NODE_ENV=development node backend/dist/main.js > $BACKEND_LOG 2>&1 &
BACKEND_PID=$!

verbose_log "Backend PID: $BACKEND_PID"
print_info "Backend process started (PID: $BACKEND_PID)"

# Wait for backend to be ready
print_waiting "Waiting for backend to respond (max 120s)..."
WAIT_TIME=0
MAX_WAIT=120
BACKEND_READY=0

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    # Check if process still exists
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "Backend process died unexpectedly"
        echo ""
        echo "Last 30 lines of backend log:"
        tail -30 $BACKEND_LOG | sed 's/^/    /'
        exit 1
    fi
    
    # Check if backend is responding
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api 2>/dev/null || echo "000")
    if echo "$HTTP_CODE" | grep -Eq '^(2|3)[0-9]{2}$'; then
        print_success "Backend ready after ${WAIT_TIME}s (HTTP $HTTP_CODE)"
        BACKEND_READY=1
        break
    fi
    
    # Show progress every 5 seconds
    if [ $((WAIT_TIME % 5)) -eq 0 ] && [ $WAIT_TIME -gt 0 ]; then
        if [ $VERBOSE -eq 1 ]; then
            echo "  [$WAIT_TIME s] Still waiting... (HTTP: $HTTP_CODE)"
            echo "  Recent log output:"
            tail -3 $BACKEND_LOG 2>/dev/null | sed 's/^/    /' || echo "    (no output yet)"
        else
            echo -n "."
        fi
    fi
    
    sleep 1
    WAIT_TIME=$((WAIT_TIME + 1))
done

if [ $BACKEND_READY -eq 0 ]; then
    print_error "Backend failed to start within ${MAX_WAIT}s"
    echo ""
    echo "Last 50 lines of backend log:"
    tail -50 $BACKEND_LOG | sed 's/^/    /'
    exit 1
fi

# ============================================================================
# STAGE 4: START FASTAPI
# ============================================================================
print_stage "��� STAGE 4: START FASTAPI (Port 8000)"

verbose_log "Log file: $FASTAPI_LOG"
verbose_log "Command: python -m musicgen.api"

PYTHONPATH="$WORKSPACE_ROOT/ai-music-gen" python -m musicgen.api > "$FASTAPI_LOG" 2>&1 &
FASTAPI_PID=$!

verbose_log "FastAPI PID: $FASTAPI_PID"
print_info "FastAPI process started (PID: $FASTAPI_PID)"

print_waiting "Waiting for FastAPI to respond (max 30s)..."
WAIT_TIME=0
MAX_WAIT=30
FASTAPI_READY=0

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if ! kill -0 $FASTAPI_PID 2>/dev/null; then
        print_error "FastAPI process died unexpectedly"
        echo ""
        echo "Last 30 lines of FastAPI log:"
        tail -30 $FASTAPI_LOG | sed 's/^/    /'
        exit 1
    fi
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs 2>/dev/null || echo "000")
    if echo "$HTTP_CODE" | grep -Eq '^(2|3)[0-9]{2}$'; then
        print_success "FastAPI ready after ${WAIT_TIME}s (HTTP $HTTP_CODE)"
        FASTAPI_READY=1
        break
    fi
    
    if [ $((WAIT_TIME % 3)) -eq 0 ] && [ $WAIT_TIME -gt 0 ]; then
        [ $VERBOSE -eq 1 ] && echo "  [$WAIT_TIME s] Checking... (HTTP: $HTTP_CODE)" || echo -n "."
    fi
    
    sleep 1
    WAIT_TIME=$((WAIT_TIME + 1))
done

if [ $FASTAPI_READY -eq 0 ]; then
    print_error "FastAPI failed to start within ${MAX_WAIT}s"
    echo ""
    echo "Last 30 lines of FastAPI log:"
    tail -30 $FASTAPI_LOG | sed 's/^/    /'
    exit 1
fi

# ============================================================================
# STAGE 5: START OLLAMA PROXY
# ============================================================================
print_stage "��� STAGE 5: START OLLAMA PROXY (Port 11434)"

verbose_log "Log file: $OLLAMA_LOG"
verbose_log "Command: python -c 'from libs.musicgen.olamma_api import app; import uvicorn; uvicorn.run(app, host=\"0.0.0.0\", port=11434)'"

PYTHONPATH="$WORKSPACE_ROOT" python -c "from libs.musicgen.olamma_api import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=11434)" > "$OLLAMA_LOG" 2>&1 &
OLLAMA_PID=$!

verbose_log "Ollama Proxy PID: $OLLAMA_PID"
print_info "Ollama Proxy process started (PID: $OLLAMA_PID)"

print_waiting "Waiting for Ollama Proxy to respond (max 20s)..."
WAIT_TIME=0
MAX_WAIT=20
OLLAMA_READY=0

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if ! kill -0 $OLLAMA_PID 2>/dev/null; then
        print_error "Ollama Proxy process died unexpectedly"
        echo ""
        echo "Last 30 lines of Ollama log:"
        tail -30 $OLLAMA_LOG | sed 's/^/    /'
        exit 1
    fi
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/olamma/status 2>/dev/null || echo "000")
    if echo "$HTTP_CODE" | grep -Eq '^(2|3)[0-9]{2}$'; then
        print_success "Ollama Proxy ready after ${WAIT_TIME}s (HTTP $HTTP_CODE)"
        OLLAMA_READY=1
        break
    fi
    
    if [ $((WAIT_TIME % 3)) -eq 0 ] && [ $WAIT_TIME -gt 0 ]; then
        [ $VERBOSE -eq 1 ] && echo "  [$WAIT_TIME s] Checking... (HTTP: $HTTP_CODE)" || echo -n "."
    fi
    
    sleep 1
    WAIT_TIME=$((WAIT_TIME + 1))
done

if [ $OLLAMA_READY -eq 0 ]; then
    print_error "Ollama Proxy failed to start within ${MAX_WAIT}s"
    echo ""
    echo "Last 30 lines of Ollama log:"
    tail -30 $OLLAMA_LOG | sed 's/^/    /'
    exit 1
fi

# ============================================================================
# STAGE 6: START FRONTEND
# ============================================================================
print_stage "��� STAGE 6: START FRONTEND (Port 4200)"

verbose_log "Log file: $FRONTEND_LOG"
verbose_log "Command: ./node_modules/.bin/nx serve frontend --host=0.0.0.0 --port=4200"

NX_DAEMON=false ./node_modules/.bin/nx serve frontend --host=0.0.0.0 --port=4200 > $FRONTEND_LOG 2>&1 &
FRONTEND_PID=$!

verbose_log "Frontend PID: $FRONTEND_PID"
print_info "Frontend process started (PID: $FRONTEND_PID)"

print_waiting "Waiting for frontend to respond (max 120s)..."
print_info "Angular dev server can take 30-60s to compile on first run"
WAIT_TIME=0
MAX_WAIT=120
FRONTEND_READY=0

while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        print_error "Frontend process died unexpectedly"
        echo ""
        echo "Last 50 lines of frontend log:"
        tail -50 $FRONTEND_LOG | sed 's/^/    /'
        exit 1
    fi
    
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:4200/ 2>/dev/null || echo "000")
    if echo "$HTTP_CODE" | grep -Eq '^(2|3)[0-9]{2}$'; then
        print_success "Frontend ready after ${WAIT_TIME}s (HTTP $HTTP_CODE)"
        FRONTEND_READY=1
        break
    fi
    
    if [ $((WAIT_TIME % 10)) -eq 0 ] && [ $WAIT_TIME -gt 0 ]; then
        if [ $VERBOSE -eq 1 ]; then
            echo "  [$WAIT_TIME s] Still compiling... (HTTP: $HTTP_CODE)"
            echo "  Recent log output:"
            tail -3 $FRONTEND_LOG 2>/dev/null | sed 's/^/    /' || echo "    (no output yet)"
        else
            echo -n "."
        fi
    fi
    
    sleep 1
    WAIT_TIME=$((WAIT_TIME + 1))
done

if [ $FRONTEND_READY -eq 0 ]; then
    print_error "Frontend failed to start within ${MAX_WAIT}s"
    echo ""
    echo "Last 80 lines of frontend log:"
    tail -80 $FRONTEND_LOG | sed 's/^/    /'
    exit 1
fi

# ============================================================================
# FINAL STATUS
# ============================================================================
END_TIME=$(date +%s)
STARTUP_TIME=$((END_TIME - START_TIME))

echo ""
print_stage "��� ALL SERVICES RUNNING"
echo ""
printf "  ⏱️  Total startup time: %dm %ds\n" $((STARTUP_TIME/60)) $((STARTUP_TIME%60))
echo ""
echo "  ��� Process IDs:"
echo "     Backend:      $BACKEND_PID"
echo "     FastAPI:      $FASTAPI_PID"
echo "     Ollama Proxy: $OLLAMA_PID"
echo "     Frontend:     $FRONTEND_PID"
echo ""
echo "  ��� Live Endpoints:"
echo "     Frontend:     http://localhost:4200/"
echo "     Backend API:  http://localhost:3000/api"
echo "     FastAPI:      http://localhost:8000/docs"
echo "     Ollama Proxy: http://localhost:11434/olamma/status"
echo ""
echo "  ��� Log Files:"
echo "     Backend:      tail -f $BACKEND_LOG"
echo "     FastAPI:      tail -f $FASTAPI_LOG"
echo "     Ollama:       tail -f $OLLAMA_LOG"
echo "     Frontend:     tail -f $FRONTEND_LOG"
echo ""
echo "  ��� Quick Health Checks:"
echo "     curl --fail http://localhost:3000/api"
echo "     curl --fail http://localhost:4200/"
echo "     curl --fail http://localhost:11434/olamma/status"
echo ""
echo "  ⌨️  Press Ctrl+C to stop all services"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Keep script running and wait for all processes
wait $BACKEND_PID $FASTAPI_PID $OLLAMA_PID $FRONTEND_PID
