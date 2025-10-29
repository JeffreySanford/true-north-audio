# Architecture Overview

This document describes the high-level architecture of the True North Audio Nx monorepo.

## Monorepo Structure
- Nx workspace with Angular frontend and NestJS backend
- Shared libraries for DTOs, types, and business logic
- Modular design for easy feature expansion

## Data Flow
- RxJS Observables for frontend async data
- WebSocket streaming for real-time backend communication
- MongoDB for persistent storage

## Extensibility
- Designed for local-first use, with cloud migration in mind
- Easy to add new genres, vocal features, and video capabilities

See other docs for details on each feature.