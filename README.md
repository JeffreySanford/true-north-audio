# TrueNorthAudio

<a alt="Nx logo" href="https://nx.dev" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/nrwl/nx/master/images/nx-logo.png" width="45"></a>

✨ Your new, shiny [Nx workspace](https://nx.dev) is almost ready ✨.

[Learn more about this workspace setup and its capabilities](https://nx.dev/nx-api/js?utm_source=nx_project&amp;utm_medium=readme&amp;utm_campaign=nx_projects) or run `npx nx graph` to visually explore what was created. Now, let's get you up to speed!

## Finish your CI setup

[Click here to finish setting up your workspace!](https://cloud.nx.app/connect/tkKlDHfUO7)


## Generate a library

```sh
npx nx g @nx/js:lib packages/pkg1 --publishable --importPath=@my-org/pkg1
```

## Run tasks

To build the library use:

```sh
npx nx build pkg1
```

To run any task with Nx use:

```sh
npx nx <target> <project-name>
```

These targets are either [inferred automatically](https://nx.dev/concepts/inferred-tasks?utm_source=nx_project&utm_medium=readme&utm_campaign=nx_projects) or defined in the `project.json` or `package.json` files.

[More about running tasks in the docs &raquo;](https://nx.dev/features/run-tasks?utm_source=nx_project&utm_medium=readme&utm_campaign=nx_projects)

## Versioning and releasing

To version and release the library use


# True North Audio: Nx Monorepo Music Maker

## Overview
This repository is an Nx monorepo for a local-first, AI-powered music maker application. It is designed to run independently on modern hardware (i7/i9 CPUs, NVIDIA GPUs) and is extensible for future cloud deployment (e.g., DigitalOcean).

### Key Features
- **Frontend:** Angular (Material Design 3), non-standalone components, RxJS data streams
- **Backend:** NestJS, MongoDB (Mongoose ODM), WebSocket streaming, RBAC user management
- **Audio/AI:** Local model integration (Ollama, etc.), scalable genre/vocal feature support
- **Video:** Initial planning for video asset management and processing
- **User Management:** Role-based access control (RBAC), no OAuth yet
- **Nx Workspace:** Modular structure, shared libraries for DTOs/types, strict coding standards

## Project Structure
- `/apps/frontend` - Angular UI
- `/apps/backend` - NestJS API server
- `/libs/shared` - Shared types, DTOs
- `/libs/audio` - Audio logic
- `/libs/video` - Video logic (planned)
- `/libs/data-access` - Data models/services
- `/libs/ui` - Angular UI components
- `/apps/frontend-e2e` - Frontend E2E tests
- `/apps/backend-e2e` - Backend E2E tests

## Coding Standards & Requirements
- Always use Nx CLI for all build, lint, test, serve, and e2e tasks (never use underlying tooling directly)
- Use non-standalone Angular components (standalone: false)
- All Angular Material components must be imported in AppModule
- Use RxJS data streams and WebSockets for frontend-backend communication; avoid Promises for app data
- Strict TypeScript: no implicit any, no unused variables, no inferrable type annotations
- Strict linting: ESLint, Prettier, and Angular style guides enforced
- Modular Nx workspace: shared libraries for DTOs/types, clear separation of apps/libs
- Backend: NestJS, MongoDB (Mongoose ODM), in-memory MongoDB for dev/test (mongodb-memory-server)
- Frontend: Angular Material Design 3, vibrant UI, clear browser console logging for all initialization stages
- Connection status indicator in footer (red/yellow/green/black)
- Abstracted header and footer components (declared in AppModule)
- All endpoints documented in backend/API_ENDPOINTS.md
- Hardware: optimized for local-first (i7/i9 CPUs, NVIDIA GPUs), cloud-ready
- All new features and endpoints must be documented and tested

## Hardware & Deployment
- Optimized for local use on i7/i9 CPUs, NVIDIA GPUs
- Easy migration to cloud (DigitalOcean, Docker)

## Getting Started
1. Install dependencies: `pnpm install`
2. Install Angular Material (required for frontend UI):
	- At workspace root: `pnpm add -w @angular/material @angular/cdk`
	- If you see EPERM or permission errors, close all editors/servers, ensure write access, and retry. You may need to run as administrator.
3. Run frontend: `nx serve frontend`
4. Run backend: `nx serve backend`

## Nx Scripts
You can run tasks for individual projects or all at once:
- Lint: `pnpm lint:backend`, `pnpm lint:frontend`, `pnpm lint:all`
- Build: `pnpm build:backend`, `pnpm build:frontend`, `pnpm build:all`
- Serve: `pnpm serve:backend`, `pnpm serve:frontend`, `pnpm serve:all`
- Test: `pnpm test:backend`, `pnpm test:frontend`, `pnpm test:all`


## Frontend Notes
- All Angular Material components used in the UI must be imported in `AppModule` (see `src/app/app-module.ts`).
- `FormsModule` is required for `ngModel` support.
- The main page uses a vibrant, animated Material Design 3 layout, with:
	- `mat-card`, `mat-form-field`, `mat-select`, `mat-slider`, `mat-expansion-panel`, `mat-chip-list`, and more
	- Advanced options for music generation (genre, duration, seed, variation, tempo)
	- Future extensibility for video, remix, vocal/instrumental, and more
	- All UI fits between header and footer, with responsive and stylish design
- If you see errors about unknown Material elements or `ngModel`, check your module imports and that Material/CDK are installed.

## Documentation
See `/docs` for detailed guides on architecture, features, and usage.

