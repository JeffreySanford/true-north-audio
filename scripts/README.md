# Scripts Directory

This directory contains utility scripts for managing the True North Audio application.

## Available Scripts

### Port Management

**`check-ports.sh`**
- Checks if required ports (3000, 4200, 8000, 11434) are free or in use
- Usage: `bash scripts/check-ports.sh` or `npm run check:ports`
- Exit code 0 if all ports are free, 1 if any are in use

**`kill-all.sh`**
- Stops all True North Audio services (Node.js, Python, Nx daemon)
- Automatically runs port check after cleanup
- Usage: `bash scripts/kill-all.sh` or `npm run kill:all`

# True North Audio - Scripts Documentation

Comprehensive collection of automation scripts for development, testing, deployment, and monitoring.

## 📁 Script Overview

### 🚀 Service Management

#### `serve-all.sh`
Starts all four True North Audio services with comprehensive logging and status tracking.

**Services:**
- Backend (NestJS) - Port 3000
- Frontend (Angular) - Port 4200
- FastAPI (Python) - Port 8000
- Ollama Proxy (Python) - Port 11434

**Usage:**
```bash
npm run serve:all    # With port checking
npm run serve:quick  # Skip port check
```

**Features:**
- ✅ Automatic port conflict detection
- ✅ Process ID tracking
- ✅ Service health monitoring
- ✅ Graceful shutdown on Ctrl+C
- ✅ Logs saved to `/tmp/{service}.log`

---

#### `monitor.sh` 🆕
**Comprehensive real-time service monitor with interactive dashboard**

**Tracks:**
- 📦 Install processes
- 🔍 Lint operations
- 🧪 Test executions
- 🔨 Build processes
- ▶️ Serve status
- 🧹 Clean operations

**Usage:**
```bash
npm run monitor
```

**Features:**
- 🎨 Color-coded status indicators
- 📊 Real-time activity logs
- 💻 Process tracking (Node.js, Python, npm/pnpm)
- ⌨️ Interactive commands:
  - `r` - Force refresh
  - `q` - Quit monitor
  - `l` - View detailed logs
  - `s` - Start all services
- 🔄 Auto-refresh every 2 seconds
- 🚦 Status indicators:
  - 🟢 Running - Service active and healthy
  - 🔴 Error - Service encountered error
  - 🟡 Active - Service working
  - 🔨 Building - Build in progress
  - 🧪 Testing - Tests running
  - 📦 Installing - Dependencies installing
  - ⚫ Stopped - Service not running

**`serve-all.sh`**
- Starts all services: Backend (3000), Frontend (4200), FastAPI (8000), Ollama proxy (11434)
- Handles process cleanup and service orchestration
- Usage: `bash scripts/serve-all.sh` or `npm run serve:quick`

**`serve-dev.sh`**
- Development mode startup script
- Usage: `bash scripts/serve-dev.sh` or `npm run dev`

### Maintenance

**`fix-nx-permissions.sh`**
- Fixes Nx cache and permission issues
- Stops daemon, cleans cache, and prepares for fresh start
- Usage: `bash scripts/fix-nx-permissions.sh` or `npm run fix:nx`

**`clear-generated-melody.sh`**
- Clears generated melody files from the workspace
- Usage: `bash scripts/clear-generated-melody.sh` or `npm run clear:melody`

## Quick Reference

```bash
# Check if ports are free
npm run check:ports

# Stop all services
npm run kill:all

# Start all services (with preflight checks)
npm run serve:all

# Start all services (skip checks)
npm run serve:quick

# Fix Nx issues
npm run fix:nx

# Clear generated melodies
npm run clear:melody
```

## Port Mappings

| Port  | Service       | Description                    |
|-------|---------------|--------------------------------|
| 3000  | Backend       | NestJS API server             |
| 4200  | Frontend      | Angular development server    |
| 8000  | FastAPI       | Python music generation API   |
| 11434 | Ollama        | Ollama AI proxy service       |

## Workflow

1. **Before starting**: `npm run check:ports` - Verify ports are free
2. **If ports in use**: `npm run kill:all` - Stop all services
3. **Start development**: `npm run serve:quick` - Launch all services
4. **On Nx errors**: `npm run fix:nx` - Fix permission issues

## Notes

- All scripts use bash, ensure Git Bash or WSL is available on Windows
- Scripts automatically handle cross-platform differences where possible
- Check script exit codes for automation/CI integration
