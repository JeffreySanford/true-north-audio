#!/bin/bash

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║              🧪 PYTHON TESTING - TRUE NORTH AUDIO             ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if pytest is installed
if ! python -m pytest --version &> /dev/null; then
    echo "⚠️  pytest not found, installing..."
    python -m pip install pytest pytest-asyncio --quiet
fi

# Set Python path
export PYTHONPATH=.:ai-music-gen:libs

echo "📦 Running Python tests..."
echo ""
echo "  Test paths:"
echo "    • ai-music-gen/tests/"
echo "    • ai-music-gen/musicgen/"
echo "    • libs/musicgen/"
echo ""

# Run tests with coverage
if python -m pytest -v --tb=short --color=yes; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                 ✅ ALL PYTHON TESTS PASSED                     ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                 ❌ PYTHON TESTS FAILED                         ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 1
fi
