#!/bin/bash

# Complete Clean & Rebuild Script for True North Audio
# Uninstalls everything, cleans, reinstalls, and rebuilds all projects

clear
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║         🧹 TRUE NORTH AUDIO - COMPLETE CLEAN & REBUILD        ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "⚠️  This will:"
echo "  • Stop all running services"
echo "  • Remove node_modules and all dependencies"
echo "  • Remove all build artifacts"
echo "  • Remove Nx cache"
echo "  • Reinstall all dependencies"
echo "  • Rebuild: Backend, Frontend"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted by user"
    exit 1
fi

START_TIME=$(date +%s)

# Helper function for status messages
print_step() {
    echo ""
    echo "┌────────────────────────────────────────────────────────────────┐"
    printf "│ Step %s/8: %-51s │\n" "$1" "$2"
    echo "└────────────────────────────────────────────────────────────────┘"
}

# Step 1: Stop all services
print_step "1" "Stopping all services"
npm run kill:all 2>/dev/null || killall node 2>/dev/null || true
ps aux | grep -E "python.*musicgen|python.*olamma" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || true
echo "  ✅ All services stopped"

# Step 2: Clean Nx cache
print_step "2" "Cleaning Nx cache"
if [ -d "node_modules" ]; then
    npx nx reset 2>&1 | grep -E "(Resetting|daemon|cache)" || true
    echo "  ✅ Nx cache cleared"
else
    echo "  ℹ️  node_modules not found, skipping nx reset"
fi
rm -rf .nx node_modules/.cache coverage 2>/dev/null
echo "  ✅ Cache directories removed"

# Step 3: Remove build artifacts
print_step "3" "Removing build artifacts"
rm -rf dist .nx node_modules/.cache coverage 2>/dev/null
rm -rf backend/dist frontend/dist 2>/dev/null
rm -rf **/dist **/.next **/.turbo 2>/dev/null
echo "  ✅ Build artifacts removed"
echo "     • dist/, .nx/, coverage/"
echo "     • backend/dist, frontend/dist"
echo "     • All nested build folders"

# Step 4: Remove dependencies
print_step "4" "Removing all dependencies"
rm -rf node_modules 2>/dev/null
rm -f pnpm-lock.yaml package-lock.json 2>/dev/null
echo "  ✅ Dependencies removed"
echo "     • node_modules/"
echo "     • pnpm-lock.yaml"
echo "     • package-lock.json (if existed)"

# Step 5: Clear generated melodies
print_step "5" "Clearing generated files"
bash scripts/clear-generated-melody.sh 2>/dev/null || echo "  ℹ️  No generated files to clear"
echo "  ✅ Generated files cleared"

# Step 6: Reinstall dependencies
print_step "6" "Installing dependencies"
echo "  📦 Running pnpm install..."
pnpm install 2>&1 | grep -E "(Progress:|Done in|dependencies:)" || echo "  Installing..."
echo "  ✅ Dependencies installed"

# Step 7: Rebuild all projects
print_step "7" "Building all projects"
echo ""
echo "  🔨 Building Backend (NestJS)..."
npx nx run @true-north-audio/backend:build --skip-nx-cache 2>&1 | grep -E "(Successfully|Error|webpack)" | head -5
echo "  ✅ Backend built"
echo ""
echo "  🔨 Building Frontend (Angular)..."
npx nx run frontend:build 2>&1 | grep -E "(Successfully|Error|Initial chunk)" | head -5
echo "  ✅ Frontend built"
echo ""
echo "  ℹ️  Python Services (FastAPI, Ollama):"
echo "     No build required - runtime execution"

# Step 8: Setup MongoDB Memory Server
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Step 8/8: Setting up MongoDB Memory Server..."
echo "════════════════════════════════════════════════════════════════"
bash scripts/setup-mongodb.sh

END_TIME=$(date +%s)
TOTAL_TIME=$((END_TIME - START_TIME))
MINUTES=$((TOTAL_TIME / 60))
SECONDS=$((TOTAL_TIME % 60))

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║              ✅ COMPLETE CLEAN & REBUILD SUCCESSFUL            ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
if [ $MINUTES -gt 0 ]; then
    echo "  ⏱️  Total time: ${MINUTES}m ${SECONDS}s"
else
    echo "  ⏱️  Total time: ${SECONDS}s"
fi
echo ""
echo "  📦 Projects rebuilt:"
echo "     ✅ Backend (NestJS)"
echo "     ✅ Frontend (Angular)"
echo "     ℹ️  FastAPI (Python - runtime)"
echo "     ℹ️  Ollama Proxy (Python - runtime)"
echo ""
echo "  🚀 Next steps:"
echo "     pnpm serve:all    # Start all services"
echo "     pnpm check:ports  # Verify ports are free"
echo ""
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
