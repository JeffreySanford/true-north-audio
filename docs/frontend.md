# Frontend Documentation

## Purpose
Vibrant, expressive UI for music and video creation using Angular and Material Design 3.

## Principles
- Material Design 3: expressive colors, clear UI/UX, smooth animations
- Rigid coding standards: SCSS for styles, HTML in separate files, strict separation of concerns
- All styles in SCSS, no inline styles
- Animations for feedback and engagement

## Structure
- Main entry: `MainPageComponent` (`app-main-page`)
- Feature modules/components for asset management (planned)
- Angular Material components for UI elements

## API Integration
- Connects to backend `/musicgen/generate` for AI music generation
- Uses typed Angular services for HTTP requests

## Example Usage
```typescript
// Trigger music generation from frontend
musicGenService.generateMusic('ambient', 10, 42).subscribe(result => {
	// Handle waveform and sample rate
});
```

## Roadmap
- Add asset management UI (list, create, edit, view)
- Integrate music generation controls
- Expand animation and feedback