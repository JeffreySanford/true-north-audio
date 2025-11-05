# Testing Guide - AI Music Generation Engines

## Overview

This project includes comprehensive automated testing for all three AI music generation engines:
- **Suno AI** (Cloud)
- **Udio AI** (Cloud)
- **MusicGen Local** (Local GPU/CPU)

Tests cover:
- Module imports and dependencies
- API key validation and configuration
- Credits/quota checking
- Music generation with various parameters
- Audio quality validation
- Performance benchmarking
- Error handling and edge cases

## Quick Start

### Run All Tests (Fast Mode)
```bash
# Skip slow generation tests
bash scripts/test-all-engines.sh --fast
```

### Test All Engines (Full Suite)
```bash
# Run complete test suite (includes generation tests)
bash scripts/test-all-engines.sh
```

### Test Specific Engine
```bash
# Test only MusicGen
bash scripts/test-all-engines.sh --engine musicgen

# Test only Suno
bash scripts/test-all-engines.sh --engine suno

# Test only Udio
bash scripts/test-all-engines.sh --engine udio
```

### Generate HTML Report
```bash
# Run tests and create HTML report
bash scripts/test-all-engines.sh --report
```

## Test Categories

### 1. Import Tests
Verifies that engine modules import correctly with all dependencies.

**What's Tested**:
- Module imports succeed
- All required functions available
- No import errors or missing dependencies

**Example**:
```python
from engines.suno import generate_music, get_credits
from engines.udio import generate_music, get_credits
from engines.musicgen_local import generate_music, get_model_info
```

### 2. Configuration Tests
Validates environment configuration and hardware detection.

**What's Tested**:
- Environment variables loaded correctly
- API keys present (if configured)
- GPU detected (for MusicGen)
- Device selection working (CUDA vs CPU)

**Example Output**:
```
Device: cuda
GPU: NVIDIA GeForce GTX 1080 (8.0GB)
```

### 3. API Key Validation
Tests authentication and API key handling.

**What's Tested**:
- API key retrieval from environment
- Key validation
- Graceful handling of missing keys
- Error messages appropriate

**Note**: Tests pass even without API keys configured (non-fatal for testing).

### 4. Credits/Quota Tests
Checks credit balance and usage limits for cloud engines.

**What's Tested**:
- Credit retrieval API calls
- Quota limits returned correctly
- Daily/monthly limits accessible
- Error handling for API failures

**Example Output**:
```json
{
  "success": true,
  "credits_remaining": 45,
  "credits_total": 50,
  "reset_date": "2025-11-06T00:00:00Z"
}
```

### 5. Short Generation Tests
Quick 10-second generation to verify basic functionality.

**What's Tested**:
- Generation request succeeds
- Audio returned in expected format
- Metadata correct (duration, sample rate)
- Generation completes within timeout
- GPU utilized (for MusicGen)

**Parameters**:
- Duration: 10 seconds (fast test)
- Prompt: "Simple acoustic guitar test"
- Model: small (for MusicGen)

**Expected Time**:
- Suno/Udio: 30-60 seconds
- MusicGen (GPU): 10-30 seconds
- MusicGen (CPU): 2-5 minutes

### 6. Parameter Variation Tests
Tests different generation parameters and configurations.

**What's Tested**:
- Different prompts
- Various durations (10s, 30s, 60s)
- Temperature variations
- CFG guidance values
- Genre specifications
- Vocal styles
- Instrumental mode

**Example Variations**:
```python
# High temperature (more creative)
generate_music(prompt="...", temperature=1.5)

# High guidance (closer to prompt)
generate_music(prompt="...", cfg_coef=5.0)

# Different genres
generate_music(prompt="...", genre="americana")
generate_music(prompt="...", genre="blues")
```

### 7. Error Handling Tests
Validates graceful error handling and edge cases.

**What's Tested**:
- Invalid parameters rejected
- Network failures handled
- Timeout handling
- Out-of-memory errors caught
- API rate limits respected
- Missing API keys handled gracefully

**Edge Cases**:
- Duration = 0 or negative
- Empty prompt
- Invalid engine name
- Corrupt audio data
- Insufficient VRAM

## Running Tests Manually

### Python Test Script
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run all engines
python tests/test_all_engines.py

# Run specific engine
python tests/test_all_engines.py --engine musicgen

# Verbose output
python tests/test_all_engines.py --verbose

# Fast mode (skip generation)
python tests/test_all_engines.py --fast

# Save results to file
python tests/test_all_engines.py --output test-results/results.json
```

### Bash Test Script
```bash
# Full test suite
bash scripts/test-all-engines.sh

# Fast mode
bash scripts/test-all-engines.sh --fast

# Specific engine
bash scripts/test-all-engines.sh --engine musicgen

# With HTML report
bash scripts/test-all-engines.sh --report

# Skip API integration tests
bash scripts/test-all-engines.sh --no-api

# Combine options
bash scripts/test-all-engines.sh --fast --engine musicgen --report
```

## Test Results

### Console Output
```
==================================================
Testing MUSICGEN Engine
==================================================
[MusicGen] Starting test suite for MusicGen
[MusicGen] ✓ PASS - Import Module (0.15s)
[MusicGen] ✓ PASS - Hardware Configuration (0.03s)
[MusicGen] ✓ PASS - Short Generation (10s) (12.45s)
[MusicGen] ✓ PASS - Parameter Variations (5.67s)

MusicGen Summary:
  Total: 4
  Passed: 4
  Failed: 0
  Success Rate: 100.0%
  Time: 18.30s
```

### JSON Results
Results saved to `test-results/engine-tests-YYYYMMDD-HHMMSS.json`:

```json
{
  "timestamp": "2025-11-05T14:30:00",
  "fast_mode": false,
  "engines": {
    "musicgen": {
      "engine": "MusicGen",
      "total_tests": 7,
      "passed": 7,
      "failed": 0,
      "success_rate": 100.0,
      "total_time": 45.23,
      "results": [
        {
          "name": "Import Module",
          "passed": true,
          "duration": 0.15,
          "error": null,
          "details": {}
        },
        {
          "name": "Hardware Configuration",
          "passed": true,
          "duration": 0.03,
          "details": {
            "device": "cuda",
            "cuda_available": true,
            "gpu_name": "NVIDIA GeForce GTX 1080",
            "gpu_memory": 8.0
          }
        }
      ]
    }
  }
}
```

### HTML Report
Generated with `--report` flag, includes:
- Visual summary with color-coded results
- Per-engine breakdowns
- Individual test details
- Performance metrics
- Error messages and stack traces

**Open**: `test-results/engine-tests-YYYYMMDD-HHMMSS.html`

## CI/CD Integration

### GitHub Actions
Add to `.github/workflows/test-engines.yml`:

```yaml
name: Test AI Engines

on:
  push:
    branches: [ main, vocal-integration ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
    
    - name: Run tests (fast mode)
      run: |
        source .venv/bin/activate
        bash scripts/test-all-engines.sh --fast --no-api
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: test-results/
```

### Local Pre-Commit Hook
Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run fast tests before commit
echo "Running engine tests..."
bash scripts/test-all-engines.sh --fast

if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Make executable: `chmod +x .git/hooks/pre-commit`

## Troubleshooting Test Failures

### Import Errors
**Symptom**: `ModuleNotFoundError: No module named 'engines'`

**Solution**:
```bash
# Verify virtual environment activated
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### GPU Not Detected
**Symptom**: Tests pass but show "CPU Only"

**Solution**:
```bash
# Verify CUDA
nvidia-smi
nvcc --version

# Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### API Key Errors
**Symptom**: Tests fail with "API key not found"

**Solution**:
- Tests should pass even without API keys (graceful handling)
- If you want to test cloud engines, add keys to `.env`:
  ```env
  SUNO_API_KEY=your_key_here
  UDIO_API_KEY=your_key_here
  ```

### Timeout Errors
**Symptom**: Generation tests timeout

**Solution**:
- Use `--fast` mode to skip generation tests
- Increase timeout in test script
- Check network connection (for cloud engines)
- Verify GPU is being used (for MusicGen)

### Out of Memory
**Symptom**: "CUDA out of memory" during tests

**Solution**:
```bash
# Use smaller model
export MUSICGEN_MODEL=small

# Or skip generation tests
bash scripts/test-all-engines.sh --fast
```

## Performance Benchmarks

### Expected Test Times

**Fast Mode** (skips generation):
- All engines: ~5-10 seconds
- Per engine: ~2-3 seconds

**Full Suite** (with generation):
| Engine | Import | Config | Credits | Generate (10s) | Total |
|--------|--------|--------|---------|----------------|-------|
| Suno | <1s | <1s | 2-3s | 30-60s | ~35-65s |
| Udio | <1s | <1s | 2-3s | 30-60s | ~35-65s |
| MusicGen (GPU) | <1s | <1s | N/A | 10-30s | ~15-35s |
| MusicGen (CPU) | <1s | <1s | N/A | 120-300s | ~2-5min |

**First Run** (downloads models):
- MusicGen small: +5-10 minutes (1.5GB download)
- MusicGen medium: +10-15 minutes (6GB download)
- MusicGen large: +20-30 minutes (15GB download)

## Best Practices

### Development Workflow
1. **Before starting work**: Run `bash scripts/test-all-engines.sh --fast`
2. **After changes**: Run full test suite
3. **Before commit**: Run fast tests
4. **Before PR**: Run full suite with report

### Continuous Testing
```bash
# Watch mode (re-run on changes)
while true; do
    bash scripts/test-all-engines.sh --fast
    sleep 30
done
```

### Scheduled Testing
Add to crontab:
```bash
# Run full tests daily at 2 AM
0 2 * * * cd /path/to/true-north-audio && bash scripts/test-all-engines.sh --report
```

## Adding New Tests

### Extend Existing Suite
Edit `tests/test_all_engines.py`:

```python
class MusicGenTestSuite(EngineTestSuite):
    def test_my_new_feature(self):
        """Test description"""
        result = TestResult("My New Test")
        start = time.time()
        try:
            # Your test code here
            result.passed = True
        except Exception as e:
            result.error = str(e)
        finally:
            result.duration = time.time() - start
            self.add_result(result)
```

### Create New Test File
For specialized tests:

```python
# tests/test_performance.py
import pytest
from engines.musicgen_local import generate_music

def test_generation_speed():
    """Benchmark generation speed"""
    result = generate_music("test", duration=10, model="small")
    assert result["success"]
    assert result["duration_actual"] < 30  # Should be fast
```

Run with: `pytest tests/test_performance.py`

## Support

For issues with testing:
1. Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
2. Review test logs in `test-results/`
3. Run with `--verbose` for detailed output
4. Check GPU status: `nvidia-smi`
5. Verify dependencies: `pip list`
