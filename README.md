
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
- Optimized for local use on i7/i9 CPUs, NVIDIA GPUs
- Easy migration to cloud (DigitalOcean, Docker, etc.)



## Getting Started
1. Install dependencies: `pnpm install`
2. Install Angular Material (required for frontend UI):
  - At workspace root: `pnpm add -w @angular/material @angular/cdk`
  - If you see EPERM or permission errors, close all editors/servers, ensure write access, and retry. You may need to run as administrator.
3. Run all lint/build/test/serve tasks via Nx or pnpm scripts (see below). Never use underlying tooling directly.
4. Run backend: `nx serve backend` (must be running before frontend for proxy)
5. Run frontend: `nx serve frontend --proxy-config=src/proxy.conf.json`
6. To generate longer songs, set the duration slider up to 180 seconds in the UI. For multi-section songs, see planned features below.


## Nx Scripts & Workflow
Run tasks for individual projects or all at once. All scripts are guaranteed to only operate on source files (never build artifacts):
- Lint: `pnpm lint:backend`, `pnpm lint:frontend`, `pnpm lint:all`
- Build: `pnpm build:backend`, `pnpm build:frontend`, `pnpm build:all`
- Serve: `pnpm serve:backend`, `pnpm serve:frontend`, `pnpm serve:all` (includes proxy config)
- Test: `pnpm test:backend`, `pnpm test:frontend`, `pnpm test:all`




## Frontend Notes
- All Angular Material components used in the UI must be imported in `AppModule` (see `src/app/app-module.ts`).
- `FormsModule` is required for `ngModel` support.
- The main page uses a vibrant, animated Material Design 3 layout, with:
  - `mat-card`, `mat-form-field`, `mat-select`, `mat-slider`, `mat-expansion-panel`, `mat-chip-list`, and more
  - Advanced options for music generation (genre, duration up to 180s, seed, variation, tempo)
  - Future extensibility for video, remix, vocal/instrumental, multi-section songs, and more
  - All UI fits between header and footer, with responsive and stylish design
- If you see errors about unknown Material elements or `ngModel`, check your module imports and that Material/CDK are installed.



## Documentation
- All endpoints must be documented in `API_ENDPOINTS.md`.
- See `/docs` for detailed guides on architecture, features, and usage.
- All new features and endpoints (including multi-section song generation) must be documented and tested before merging.

## Planned Features
- Multi-section song generation (verse, chorus, bridge, etc.)
- Song arrangement and transitions
- Lyrics and vocal synthesis (future)
- Video asset management

