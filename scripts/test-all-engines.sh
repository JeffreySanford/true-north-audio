#!/bin/bash
#
# Automated Test Runner for All AI Music Generation Engines
#
# This script runs comprehensive tests on Suno, Udio, and MusicGen engines,
# generates reports, and validates integration with the backend API.
#
# Usage:
#   bash scripts/test-all-engines.sh [options]
#
# Options:
#   --fast        Skip slow generation tests
#   --engine      Test specific engine only (suno|udio|musicgen)
#   --no-api      Skip backend API integration tests
#   --report      Generate HTML report
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
FAST_MODE=false
SPECIFIC_ENGINE=""
SKIP_API=false
GENERATE_REPORT=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --fast)
            FAST_MODE=true
            shift
            ;;
        --engine)
            SPECIFIC_ENGINE="$2"
            shift 2
            ;;
        --no-api)
            SKIP_API=true
            shift
            ;;
        --report)
            GENERATE_REPORT=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  AI Music Generation Engine Test Suite${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if Python virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠  Virtual environment not activated${NC}"
    echo -e "${YELLOW}   Activating .venv...${NC}"
    if [[ -f ".venv/Scripts/activate" ]]; then
        source .venv/Scripts/activate
    elif [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
    else
        echo -e "${RED}✗ Virtual environment not found${NC}"
        echo -e "${RED}  Run: python -m venv .venv${NC}"
        exit 1
    fi
fi

# Verify Python modules are installed
echo -e "${BLUE}Checking dependencies...${NC}"
python -c "import audiocraft, torch, requests" 2>/dev/null || {
    echo -e "${RED}✗ Missing Python dependencies${NC}"
    echo -e "${RED}  Run: pip install -r requirements.txt${NC}"
    exit 1
}
echo -e "${GREEN}✓ All dependencies installed${NC}"

# Check GPU availability
echo -e "${BLUE}Checking GPU...${NC}"
python -c "import torch; print('✓ GPU Available:' if torch.cuda.is_available() else '⚠ CPU Only:'); print('  ' + (torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'No GPU detected'))"

echo ""

# Create test results directory
RESULTS_DIR="test-results"
mkdir -p "$RESULTS_DIR"

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
RESULTS_FILE="$RESULTS_DIR/engine-tests-$TIMESTAMP.json"

# Build test command
TEST_CMD="python tests/test_all_engines.py"

if [[ "$FAST_MODE" == "true" ]]; then
    TEST_CMD="$TEST_CMD --fast"
    echo -e "${YELLOW}⚡ Fast mode: Skipping slow generation tests${NC}"
fi

if [[ -n "$SPECIFIC_ENGINE" ]]; then
    TEST_CMD="$TEST_CMD --engine $SPECIFIC_ENGINE"
    echo -e "${BLUE}🎯 Testing specific engine: $SPECIFIC_ENGINE${NC}"
fi

TEST_CMD="$TEST_CMD --output $RESULTS_FILE --verbose"

echo ""
echo -e "${BLUE}Running engine tests...${NC}"
echo -e "${BLUE}Command: $TEST_CMD${NC}"
echo ""

# Run tests
if $TEST_CMD; then
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  ✓ All Tests Passed${NC}"
    echo -e "${GREEN}================================================${NC}"
    TEST_EXIT_CODE=0
else
    echo ""
    echo -e "${RED}================================================${NC}"
    echo -e "${RED}  ✗ Some Tests Failed${NC}"
    echo -e "${RED}================================================${NC}"
    TEST_EXIT_CODE=1
fi

echo ""
echo -e "${BLUE}Results saved to: $RESULTS_FILE${NC}"

# Run API integration tests if not skipped
if [[ "$SKIP_API" == "false" ]]; then
    echo ""
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  Backend API Integration Tests${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    
    # Check if backend is running
    if curl -s http://localhost:3000/api >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is running${NC}"
        
        # Run API tests
        echo -e "${BLUE}Running API integration tests...${NC}"
        
        # Test health endpoint
        echo -n "  Testing health endpoint... "
        if curl -s http://localhost:3000/api/health >/dev/null 2>&1; then
            echo -e "${GREEN}✓${NC}"
        else
            echo -e "${YELLOW}⚠ (endpoint may not exist)${NC}"
        fi
        
        # Test music generation endpoint structure
        echo -n "  Testing generation endpoint... "
        RESPONSE=$(curl -s -X POST http://localhost:3000/api/audio-asset/generate \
            -H "Content-Type: application/json" \
            -d '{
                "engine": "musicgen",
                "prompt": "test",
                "duration": 10
            }' 2>/dev/null || echo "error")
        
        if [[ "$RESPONSE" != "error" ]]; then
            echo -e "${GREEN}✓ Endpoint responds${NC}"
        else
            echo -e "${YELLOW}⚠ Endpoint not responding${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Backend not running (skipping API tests)${NC}"
        echo -e "${YELLOW}  Start with: pnpm dev${NC}"
    fi
fi

# Generate HTML report if requested
if [[ "$GENERATE_REPORT" == "true" ]]; then
    echo ""
    echo -e "${BLUE}Generating HTML report...${NC}"
    
    REPORT_FILE="$RESULTS_DIR/engine-tests-$TIMESTAMP.html"
    
    python -c "
import json
import sys
from datetime import datetime

with open('$RESULTS_FILE', 'r') as f:
    results = json.load(f)

html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Engine Test Results - ''' + results['timestamp'] + '''</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .summary { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .engine { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .pass { color: #4CAF50; font-weight: bold; }
        .fail { color: #f44336; font-weight: bold; }
        .test { margin: 10px 0; padding: 10px; background: #f9f9f9; border-left: 3px solid #ddd; }
        .test.passed { border-color: #4CAF50; }
        .test.failed { border-color: #f44336; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }
        th { background: #2196F3; color: white; }
    </style>
</head>
<body>
    <h1>🎵 AI Music Generation Engine Test Results</h1>
    
    <div class='summary'>
        <h2>Summary</h2>
        <p><strong>Timestamp:</strong> ''' + results['timestamp'] + '''</p>
        <p><strong>Fast Mode:</strong> ''' + str(results['fast_mode']) + '''</p>
'''

total_tests = sum(e.get('total_tests', 0) for e in results['engines'].values())
total_passed = sum(e.get('passed', 0) for e in results['engines'].values())
total_failed = sum(e.get('failed', 0) for e in results['engines'].values())

html += '''
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total Tests</td><td>''' + str(total_tests) + '''</td></tr>
            <tr><td>Passed</td><td class='pass'>''' + str(total_passed) + '''</td></tr>
            <tr><td>Failed</td><td class='fail'>''' + str(total_failed) + '''</td></tr>
            <tr><td>Success Rate</td><td>''' + f'{(total_passed/total_tests*100):.1f}%' if total_tests > 0 else 'N/A' + '''</td></tr>
        </table>
    </div>
'''

for engine_name, engine_data in results['engines'].items():
    html += '''
    <div class='engine'>
        <h2>''' + engine_name.upper() + ''' Engine</h2>
        <p><strong>Tests:</strong> ''' + str(engine_data.get('total_tests', 0)) + '''</p>
        <p><strong>Passed:</strong> <span class='pass'>''' + str(engine_data.get('passed', 0)) + '''</span></p>
        <p><strong>Failed:</strong> <span class='fail'>''' + str(engine_data.get('failed', 0)) + '''</span></p>
        <p><strong>Success Rate:</strong> ''' + f\"{engine_data.get('success_rate', 0):.1f}%\" + '''</p>
        <p><strong>Time:</strong> ''' + f\"{engine_data.get('total_time', 0):.2f}s\" + '''</p>
        
        <h3>Test Results</h3>
    '''
    
    for test in engine_data.get('results', []):
        status_class = 'passed' if test['passed'] else 'failed'
        status_icon = '✓' if test['passed'] else '✗'
        
        html += f'''
        <div class='test {status_class}'>
            <strong>{status_icon} {test['name']}</strong> ({test['duration']:.2f}s)
        '''
        
        if test['error']:
            html += f\"<br><span style='color: #f44336;'>Error: {test['error']}</span>\"
        
        if test.get('details'):
            html += \"<br><small>Details: \" + str(test['details']) + \"</small>\"
        
        html += '</div>'
    
    html += '</div>'

html += '''
</body>
</html>
'''

with open('$REPORT_FILE', 'w') as f:
    f.write(html)

print('Report generated: $REPORT_FILE')
"
    
    echo -e "${GREEN}✓ HTML report generated: $REPORT_FILE${NC}"
fi

# Print summary
echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

python -c "
import json
with open('$RESULTS_FILE', 'r') as f:
    results = json.load(f)
    
for engine, data in results['engines'].items():
    status = '✓' if data.get('failed', 0) == 0 else '✗'
    print(f'{engine.upper():10} {status} {data.get(\"passed\", 0)}/{data.get(\"total_tests\", 0)} passed ({data.get(\"success_rate\", 0):.1f}%)')
"

echo ""

# Exit with test exit code
exit $TEST_EXIT_CODE
