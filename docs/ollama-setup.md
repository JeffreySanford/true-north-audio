# Ollama Setup Guide

## Overview

Ollama is an optional AI service used by True North Audio for music generation. The application will work without it, but music generation features will be limited.

## Current Status

When you see errors like:
```
Error: connect ECONNREFUSED ::1:11434
Error: connect ECONNREFUSED 127.0.0.1:11434
```

This means **Ollama is not running** (or not installed). This is okay for development - the application will continue to work, but music generation via Ollama will not be available.

## Installation

### Windows
```bash
winget install Ollama.Ollama
```

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Starting Ollama

After installation, start the Ollama service:

```bash
ollama serve
```

This will start Ollama on `http://localhost:11434`

## Verifying Ollama is Running

```bash
# Check if Ollama is responding
curl http://localhost:11434/api/tags

# Or check version
ollama --version
```

## Using Ollama with True North Audio

1. **Start Ollama** (in a separate terminal):
   ```bash
   ollama serve
   ```

2. **Pull required models** (optional, will download on first use):
   ```bash
   ollama pull llama3.2
   ```

3. **Start your application**:
   ```bash
   pnpm serve:all
   ```

## Troubleshooting

### Service Won't Start
- **Windows**: Check if another service is using port 11434
  ```bash
  netstat -ano | findstr :11434
  ```
- **macOS/Linux**: 
  ```bash
  lsof -i :11434
  ```

### Connection Refused Errors
- Verify Ollama is running: `ollama --version`
- Start the service: `ollama serve`
- Check firewall settings aren't blocking port 11434

### Application Works Without Ollama
The backend now gracefully handles Ollama being unavailable. You'll see user-friendly error messages instead of crashes when trying to generate music without Ollama running.

## Architecture Notes

- **Backend Service**: `backend/src/audio-asset/musicgen.service.ts` - Handles Ollama communication with error fallback
- **Ollama API Proxy**: Can be started with `pnpm serve:ollama` (port 11434)
- **Python Integration**: `ai-music-gen/engines/ollama.py` - Direct Ollama API integration

## Optional vs Required

| Feature | Requires Ollama |
|---------|----------------|
| Basic app functionality | ❌ No |
| Music generation with MusicGen | ❌ No |
| Music generation with Ollama | ✅ Yes |
| Backend API endpoints | ❌ No |
| Frontend UI | ❌ No |

## Developer Mode

For development without Ollama:
1. The preflight checks will warn but not fail
2. Backend will start successfully  
3. Music generation requests will return descriptive error messages
4. All other features work normally

## Production Deployment

For production:
1. Install and start Ollama as a system service
2. Configure appropriate models
3. Set up health checks for the Ollama service
4. Monitor Ollama logs for performance issues

## Related Documentation

- [Ollama Engine Documentation](./ollama-engine.md)
- [AI Integration Guide](./ai-integration.md)
- [Backend MusicGen Service](./backend-musicgen.md)
