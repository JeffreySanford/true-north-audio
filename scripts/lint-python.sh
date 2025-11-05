#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║              🐍 PYTHON LINTING - TRUE NORTH AUDIO             ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

ERRORS=0

# Check if flake8 is installed
if ! python -m flake8 --version &> /dev/null; then
    echo "⚠️  flake8 not found, installing..."
    python -m pip install flake8 --quiet
fi

# Lint ai-music-gen
echo "📁 Linting ai-music-gen/..."
if python -m flake8 ai-music-gen/ --count --select=E9,F63,F7,F82 --show-source --statistics; then
    echo "  ✅ No critical errors"
else
    echo "  ❌ Critical errors found"
    ERRORS=$((ERRORS + 1))
fi

# Full lint report
echo ""
echo "📊 Full lint report..."
python -m flake8 ai-music-gen/ --count --statistics

# Lint libs/musicgen
echo ""
echo "📁 Linting libs/musicgen/..."
if [ -d "libs/musicgen" ]; then
    if python -m flake8 libs/musicgen/ --count --select=E9,F63,F7,F82 --show-source --statistics; then
        echo "  ✅ No critical errors"
    else
        echo "  ❌ Critical errors found"
        ERRORS=$((ERRORS + 1))
    fi
    
    echo ""
    echo "📊 Full lint report..."
    python -m flake8 libs/musicgen/ --count --statistics
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                 ✅ PYTHON LINTING PASSED                       ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                 ❌ PYTHON LINTING FAILED                       ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "  To fix automatically, run: pnpm lint:python:fix"
    exit 1
fi
