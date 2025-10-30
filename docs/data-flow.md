# Data Flow & RxJS Streams

## Backend
- All CRUD operations use RxJS hot observables (Subjects)
- Services emit data streams for controllers to consume
- Controllers return observables directly to clients

## Frontend
- Angular uses RxJS Observables for all async data
- Feature modules subscribe to backend streams
- UI updates reactively to data changes

## Integration
- REST endpoints return observable streams
- WebSocket endpoints can be added for real-time features
