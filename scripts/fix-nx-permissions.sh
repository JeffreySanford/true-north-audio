#!/bin/bash

echo "🔧 Fixing Nx permissions and cache issues..."

# Kill any running Node.js processes
echo "Stopping Node.js processes..."
taskkill /F /IM node.exe 2>/dev/null || echo "No node processes to kill"

# Wait a moment for processes to fully terminate
sleep 2

# Try to stop Nx daemon gracefully
echo "Stopping Nx daemon..."
npx nx daemon --stop 2>/dev/null || echo "Nx daemon not running"

# Remove cache directories that might have permission issues
echo "Cleaning cache directories..."
rm -rf .nx/cache/* 2>/dev/null || echo "Cache already clean"
rm -rf node_modules/.cache 2>/dev/null || echo "Node modules cache already clean"
rm -rf dist 2>/dev/null || echo "Dist already clean"

# Give it a moment
sleep 1

echo "✅ Cleanup complete!"
echo ""
echo "Now you can run:"
echo "  pnpm serve:quick    (skip preflight checks)"
echo "  pnpm serve:all      (with full preflight)"
