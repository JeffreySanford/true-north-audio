# API Endpoints

This document lists all backend API endpoints for True North Audio. All endpoints must be documented here and tested before merging.

---

## Music Generation


### POST `/api/musicgen/generate`
- **Description:** Generate music using AI models with the provided parameters. Supports long durations (up to 180 seconds) and planned support for multi-section songs (verse, chorus, bridge, etc.).
- **Body:**
  - `genre` (string, required): Music genre (e.g., 'ambient', 'rock', 'pop', 'jazz', etc.)
  - `duration` (number, required): Duration in seconds (up to 180s; longer planned)
  - `seed` (number, optional): Random seed for reproducibility
  - `idea` (string, optional): Text prompt or idea for the music
  - `vocal_artist` (string, optional): Vocal artist/model to use
  - `tempo` (number, optional): Tempo in BPM
  - `variation` (string, optional): 'original', 'remix', 'vocal', 'instrumental'
  - `sections` (array, planned): Array of song sections (verse, chorus, bridge, etc.) with durations and prompts
- **Returns:**
  - `waveform` (string, base64): Audio waveform data
  - `sample_rate` (number): Sample rate of the audio
  - `vocals` (string, optional): Transcribed vocals
  - `audio_url` (string, optional): URL to generated audio file (if available)

---

## Genres

### GET `/api/genres`
- **Description:** Get all available music genres.
- **Returns:**
  - Array of genres: `{ name: string, description?: string }[]`

---

## Health & Status

### GET `/api`
- **Description:** Health check endpoint. Returns a simple message if the API is running.
- **Returns:**
  - `{ message: string }`

---

## Static Assets

### GET `/audio/generated/*`
- **Description:** Serve generated audio assets (WAV/MP3/etc.) from the backend static file server.
- **Returns:**
  - Audio file (binary)

---

## Logging

- All music generation requests and results are logged to MongoDB (`OlammaLog`) and to a workspace log file for auditing and debugging.

---

## Notes
- All endpoints are subject to strict linting, testing, and documentation requirements.
- For new endpoints, update this file and add tests before merging.
