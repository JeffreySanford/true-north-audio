#!/bin/bash

# Kill all True North Audio services
echo "🛑 Stopping all True North Audio services..."

# Kill Node.js processes
echo "Stopping Node.js processes..."
taskkill //F //IM node.exe 2>/dev/null || echo "No node processes found"

# Kill Python processes
echo "Stopping Python processes..."
taskkill //F //IM python.exe 2>/dev/null || echo "No Python processes found"

# Kill MongoDB Memory Server processes  
echo "Stopping MongoDB Memory Server..."
taskkill //F //IM mongod.exe 2>/dev/null || echo "No MongoDB Memory Server processes found"

# Kill orphaned Git Bash shells (except current)
echo "Stopping orphaned bash shells..."
CURRENT_BASH_WINPID=""
if [ -f /proc/self/winpid ]; then
	CURRENT_BASH_WINPID=$(cat /proc/self/winpid 2>/dev/null)
fi
if [ -n "$CURRENT_BASH_WINPID" ]; then
	taskkill //F //FI "IMAGENAME eq bash.exe" //FI "PID ne $CURRENT_BASH_WINPID" 2>/dev/null || echo "No extra bash shells found"
else
	taskkill //F //IM bash.exe 2>/dev/null || echo "No bash shells found"
fi

# Stop Nx daemon
echo "Stopping Nx daemon..."
npx nx daemon --stop 2>/dev/null || echo "Nx daemon not running"

sleep 2

# Verify all ports are free
echo ""
bash scripts/check-ports.sh
