# Features


## Music Generation
- Support for many genres and vocal features
- Local AI model integration (Ollama, etc.)
- Audio asset management
- Long-form and multi-section song generation (verse, chorus, bridge, etc.)

## Video (Planned)
- Video asset management and processing
- UI for video upload/preview

## User Management
- Role-based access control (RBAC)
- User CRUD operations

## Data Streaming

# Features

## Music Generation

- Liberty Blues as the default sample for all genres
- Dramatically expanded genre support (11+ genres)
- 25+ instruments (guitar, bass, organ, drums, harmonica, sax, piano, horns, strings, percussion, etc.)
- AI-generated vocals with emotion markers
- Professional mixing/mastering effects

## API Endpoints

- `/api/genres` - List all genres (GET)
- `/api/genres/:name` - Get genre details (GET)
- `/api/genres/toggle-instrument` - Enable/disable instruments per genre (POST)
- `/api/instruments` - List all instruments (GET)

## Frontend UI

- Genre selector (dropdown, swipe left/right for mobile)
- Instrument toggles (switches per genre)
- Mobile-first responsive layout
- Liberty Blues as default sample (always available)
- Multiple views: main, genre detail, instrument detail

## Data Model

- MongoDB schemas for genres, instruments, tracks, generation history
- DTOs for genre/instrument selection and toggling
- All genres/instruments seeded at API startup

## Supported Genres

- Chicago Blues
- James Brown Funk
- Massive Blues Orchestra
- Memphis Soul
- Motown
- Delta Blues
- Jazz Blues
- Texas Blues
- New Orleans Funk
- British Blues Rock

## Instrument List

- lead_guitar
- rhythm_guitar
- organ
- piano
- bass
- harmonica
- sax_tenor
- sax_bari
- trumpet
- trumpet_1
- trumpet_2
- drums
- trombone
- conga_bongo
- electric_piano
- synth_pad
- brass_section
- percussion
- tambourine
- strings
- vibraphone
- slide_guitar
- acoustic_guitar
- drums_minimal
- jazz_guitar
- drums_jazz
- sax_alto
- tuba

## Example Workflow

- User selects genre (e.g. James Brown Funk)
- Toggles instruments (e.g. enable horns, disable harmonica)
- Generates music using Liberty Blues sample
- API stores genre/instrument selection in MongoDB
- Frontend displays results with swipe navigation and mobile-first views