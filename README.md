# True North Audio: Nx Monorepo Music Maker


## Overview
True North Audio is a local-first, AI-powered music and video asset creator, built as a robust Nx monorepo. It is optimized for modern hardware (i7/i9 CPUs, NVIDIA GPUs), but is cloud-ready for future deployment. The architecture and workflow are designed for maintainability, extensibility, and strict code quality.



### Key Features
- **Frontend:** Angular (Material Design 3), non-standalone components, RxJS data streams, vibrant UI, clear status indicators
- **Backend:** NestJS, MongoDB (Mongoose ODM), WebSocket streaming, RBAC user management, static file serving for generated assets
- **Audio/AI:** Local model integration (Ollama, etc.), scalable genre/vocal feature support, advanced creative controls, support for long-form and multi-section song generation (verse, chorus, bridge, etc.)
- **Song Structure:** Multi-section song requests (planned), with support for arranging verses, choruses, and transitions.
- **Video:** Planned for future releases (video asset management, remix, etc.)
- **User Management:** Role-based access control (RBAC), extensible for future OAuth/cloud auth
- **Nx Workspace:** Modular, strict boundaries, shared libraries for DTOs/types, robust lint/build/test workflow


## Project Structure
- `/frontend` - Angular UI (Material Design 3, RxJS, vibrant/animated UI)
- `/backend` - NestJS API server (MongoDB, static file serving, AI integration)
- `/frontend-e2e` - Playwright E2E tests for frontend
- `/backend-e2e` - Jest E2E tests for backend
- `/packages` - (future) Shared libraries for DTOs/types, audio/video logic, data-access, UI components


## Coding Standards & Workflow
- **Nx First:** All build, lint, test, serve, and e2e tasks must be run via Nx (`nx run`, `nx run-many`, `nx affected`). Never use underlying tooling directly.
- **Strict Linting:** ESLint, Prettier, and Angular style guides are strictly enforced. Lint targets are configured to *never* lint build artifacts (dist, build, out, test-output, etc.). Only source files are linted.
- **TypeScript:** Strict mode enabled. No implicit any, no unused variables, no inferrable type annotations.
- **Angular:** Non-standalone components (`standalone: false`). All Material components must be imported in `AppModule`. Use RxJS and WebSockets for data flow; avoid Promises for app data.
- **Backend:** NestJS, MongoDB (Mongoose ODM), in-memory MongoDB for dev/test. Static file serving for generated assets. All endpoints must be documented and tested.
- **Frontend:** Vibrant, animated Material Design 3 UI. Connection status indicator in footer (red/yellow/green/black). Abstracted header/footer. Clear browser console logging for all initialization stages.
- **Documentation:** All endpoints and features must be documented (`API_ENDPOINTS.md`, `/docs`).
- **Hardware:** Optimized for local-first (i7/i9 CPUs, NVIDIA GPUs), but cloud-ready (DigitalOcean, Docker, etc.).


## Hardware & Deployment

### Current Development Configuration (November 2025)
This project is optimized for high-performance local AI music generation:
- **CPU**: 16+ cores (Intel i9/AMD Ryzen 9 recommended)
- **RAM**: 32GB+ (64GB recommended for large models)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (GTX 1080, RTX 3060, RTX 4070+)
- **Storage**: SSD with 50GB+ free space for models and generated assets

### Supported Deployment Options
- **Local Development**: Full-featured with GPU acceleration (recommended)
- **Cloud Hybrid**: Cloud APIs (Suno/Udio) + local processing
- **Cloud Deployment**: DigitalOcean, Docker, Kubernetes (future)

### AI Music Generation Engines
1. **Suno AI** (Cloud): Professional quality, 50 songs/day free tier
2. **Udio AI** (Cloud): Professional quality, 3 songs/day free tier  
3. **Meta MusicGen** (Local): 100% private, unlimited generations, requires GPU

See [docs/hardware-requirements.md](docs/hardware-requirements.md) for detailed specifications and [docs/ai-integration.md](docs/ai-integration.md) for engine configuration.



## Getting Started

1. Install dependencies: `pnpm install`
2. **Windows Only:** Install Visual Studio Build Tools for Python package compilation (required for AI/musicgen):
   - Run `bash setup-windows-build-tools.sh` from the workspace root, or manually download and run the installer:
     - `curl -LO https://aka.ms/vs/17/release/vs_BuildTools.exe`
     - `./vs_BuildTools.exe --quiet --wait --norestart --nocache --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.Windows10SDK.20348 --includeRecommended`
   - This step is required for building scientific Python packages (NumPy, Audiocraft, etc.) on Windows.
3. Install Angular Material (required for frontend UI):
   - At workspace root: `pnpm add -w @angular/material @angular/cdk`
   - If you see EPERM or permission errors, close all editors/servers, ensure write access, and retry. You may need to run as administrator.
4. Run all lint/build/test/serve tasks via Nx or pnpm scripts (see below). Never use underlying tooling directly.
5. Start development services with `pnpm dev` (runs `serve-dev.sh`, which builds the backend once and launches backend + frontend together).
6. If you need fine-grained control, you can still start the backend via `nx serve backend` and the frontend via `nx serve frontend --proxy-config=src/proxy.conf.json`.
7. To generate longer songs, set the duration slider up to 180 seconds in the UI. For multi-section songs, see planned features below.


## Nx Scripts & Workflow
Run tasks for individual projects or all at once. All scripts are guaranteed to only operate on source files (never build artifacts):
- Lint: `pnpm lint:backend`, `pnpm lint:frontend`, `pnpm lint:all`
- Build: `pnpm build:backend`, `pnpm build:frontend`, `pnpm build:all`
- Serve: `pnpm dev` (recommended dev flow), `pnpm serve:backend`, `pnpm serve:frontend`, `pnpm serve:all` (includes proxy config)
- Test: `pnpm test:backend`, `pnpm test:frontend`, `pnpm test:all`




## Frontend Notes
All Angular Material components used in the UI must be imported in `AppModule` (see `src/app/app-module.ts`).
`FormsModule` is required for `ngModel` support.
The main page uses a vibrant, animated Material Design 3 layout, with:
  - `mat-card`, `mat-form-field`, `mat-select`, `mat-slider`, `mat-expansion-panel`, `mat-chip-list`, and more
  - Advanced options for music generation (genre, duration up to 180s, seed, variation, tempo)
  - Future extensibility for video, remix, vocal/instrumental, multi-section songs, and more
  - All UI fits between header and footer, with responsive and stylish design
**Music Generation Backend Selector:**
The UI includes a backend selector component (`MusicgenSelectorComponent`) that allows users to choose between supported music generation backends (e.g., MusicGen, Jukebox). This Angular Material component is located in `src/app/musicgen-selector.component.ts` with corresponding HTML, SCSS, and spec files. Ensure `AppModule` imports all required Angular Material modules and `FormsModule` for proper functionality. The selector is fully integrated into the workspace lint/build/test scripts.
If you see errors about unknown Material elements or `ngModel`, check your module imports and that Material/CDK are installed.



## Documentation

### Core Documentation
- **[README.md](README.md)** - This file, project overview and quick start
- **[API_ENDPOINTS.md](API_ENDPOINTS.md)** - Complete API endpoint reference

### Setup & Migration
- **[MACHINE-SETUP-CHECKLIST.md](docs/MACHINE-SETUP-CHECKLIST.md)** - Quick and detailed setup guides
- **[MIGRATION-CHECKLIST.md](docs/MIGRATION-CHECKLIST.md)** - Moving to new hardware
- **[setup-guide-high-performance.md](docs/setup-guide-high-performance.md)** - High-performance machine setup

### Architecture & Design
- **[architecture.md](docs/architecture.md)** - System architecture overview
- **[frontend-architecture.md](docs/frontend-architecture.md)** - Angular frontend design
- **[backend.md](docs/backend.md)** - NestJS backend architecture
- **[data-models.md](docs/data-models.md)** - Database schemas and models
- **[data-flow.md](docs/data-flow.md)** - Data flow and communication

### AI Integration
- **[ai-integration.md](docs/ai-integration.md)** - Multi-engine AI architecture (Suno, Udio, MusicGen)
- **[hardware-requirements.md](docs/hardware-requirements.md)** - Hardware specs and GPU configuration
- **[ollama-engine.md](docs/ollama-engine.md)** - Ollama integration for lyrics generation
- **[ollama-setup.md](docs/ollama-setup.md)** - Ollama installation and configuration

### Testing
- **[TESTING-GUIDE.md](docs/TESTING-GUIDE.md)** - Comprehensive testing guide for all engines
- Run automated tests: `bash scripts/test-all-engines.sh`

### Features & Usage
- **[features.md](docs/features.md)** - Feature list and roadmap
- **[user-management.md](docs/user-management.md)** - RBAC and authentication
- **[video-roadmap.md](docs/video-roadmap.md)** - Video feature planning

### Development Guidelines
All new features and endpoints (including multi-section song generation) must be documented and tested before merging.

## Planned Features
- Multi-section song generation (verse, chorus, bridge, etc.)
- Song arrangement and transitions
- Lyrics and vocal synthesis (future)
- Video asset management


## Example: Generate a Full Song with Ollama

To generate a modern hiphop version of a 1940's classic (e.g., "The Best Is Yet To Come" by Dean Martin) using the Ollama engine, run:

```bash
python ai-music-gen/ollama_song_sample.py
```

This will create a full-length song sample (3 minutes, multi-section) using the Ollama engine. You can customize the genre, idea, vocal artist, tempo, and song structure in the script.

Ollama is the default engine in the UI and backend, designed for exclusive local AI music generation. Extend the engine logic in `musicgen/engines/ollama.py` to connect to your own models or APIs.

