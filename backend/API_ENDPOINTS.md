# Backend API Endpoints

## AppController
- `GET /api` — Returns API status message

## MusicGenController
- `POST /api/musicgen/generate` — Generate music (body: `{ genre, duration, seed? }`)

## AudioAssetController
- `POST /api/audio-assets` — Create audio asset
- `GET /api/audio-assets` — List all audio assets
- `GET /api/audio-assets/:id` — Get audio asset by ID
- `PUT /api/audio-assets/:id` — Update audio asset by ID
- `DELETE /api/audio-assets/:id` — Delete audio asset by ID

## UserController
- `POST /api/users` — Create user
- `GET /api/users` — List all users
- `GET /api/users/:id` — Get user by ID
- `PUT /api/users/:id` — Update user by ID
- `DELETE /api/users/:id` — Delete user by ID

## VideoAssetController
- `POST /api/video-assets` — Create video asset
- `GET /api/video-assets` — List all video assets
- `GET /api/video-assets/:id` — Get video asset by ID
- `PUT /api/video-assets/:id` — Update video asset by ID
- `DELETE /api/video-assets/:id` — Delete video asset by ID

## VocalFeatureController
- `POST /api/vocal-features` — Create vocal feature
- `GET /api/vocal-features` — List all vocal features
- `GET /api/vocal-features/:id` — Get vocal feature by ID
- `PUT /api/vocal-features/:id` — Update vocal feature by ID
- `DELETE /api/vocal-features/:id` — Delete vocal feature by ID

---

**Note:** All endpoints expect and return JSON. See controller files for DTO details.
