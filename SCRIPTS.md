# Package Scripts Reference

## Quick Start
- `pnpm start` - Start all services (full preflight + serve)
- `pnpm dev` - Run `serve-dev.sh` (build backend once, start backend + frontend)

## Development
- `pnpm dev` - Recommended development workflow (calls `serve-dev.sh`)
- `pnpm serve:all` - Start all services with preflight checks
- `pnpm serve:backend` - Start NestJS backend only
- `pnpm serve:frontend` - Start Angular frontend only
- `pnpm serve:fastapi` - Start Python FastAPI service
- `pnpm serve:ollama` - Start Ollama API service

## Build & Test
- `pnpm build` - Build backend + frontend
- `pnpm test` - Run unit tests
- `pnpm test:e2e` - Run end-to-end tests
- `pnpm test:watch` - Run tests in watch mode

## Code Quality
- `pnpm lint` - Lint all TypeScript projects
- `pnpm lint:all` - Lint TypeScript + Python
- `pnpm lint:fix` - Auto-fix linting issues

## Health Checks
- `pnpm preflight` - Full validation (requirements + lint + build + test)
- `pnpm health` - Check system requirements + service status
- `pnpm check:requirements` - Verify Python, pip, ollama installed

## Maintenance
- `pnpm clean` - Clean Nx cache and build artifacts
- `pnpm clean:all` - Deep clean + reinstall dependencies
- `pnpm reset` - Clean all + reopen VS Code
- `pnpm clear:melody` - Remove generated audio files

## Python-Specific
- `pnpm lint:python` - Lint Python code with flake8
- `pnpm test:python` - Run pytest tests
- `pnpm build:python` - Python build placeholder