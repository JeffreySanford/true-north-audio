# Backend AI Music Generation Integration

## Purpose
Integrates the Python AI music generation library with the NestJS backend, exposing a REST endpoint for music creation.

## Architecture
- **Python FastAPI** (`libs/musicgen/api.py`): `/generate-music` endpoint generates music waveform.
- **NestJS Service** (`MusicGenService`): Calls FastAPI endpoint via HTTP.
- **NestJS Controller** (`MusicGenController`): Exposes `/musicgen/generate` POST endpoint for frontend/API clients.
- **AppModule**: Wires up controller, service, and HttpModule.

## Endpoint
- `POST /musicgen/generate`
  - **Body:** `{ genre: string, duration: number, seed?: number }`
  - **Response:** `{ waveform: string (base64), sample_rate: number }`

## Example Request
```json
POST /musicgen/generate
{
  "genre": "ambient",
  "duration": 10,
  "seed": 42
}
```

## Testing
- Unit tests for controller/service verify endpoint wiring and output.
- Run: `nx test backend --testFile=src/audio-asset/musicgen.controller.spec.ts`

## Next Steps
- Connect frontend UI to this endpoint
- Expand Python music generation features
- Add integration/E2E tests
