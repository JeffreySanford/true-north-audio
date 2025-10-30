import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { Observable, map } from 'rxjs';

/**
 * Service for integrating with the Python AI music generation API.
 * Provides methods to request music generation from the FastAPI backend.
 *
 * Usage:
 *   Inject MusicGenService and call generateMusic with desired parameters.
 *   Returns an Observable with the generated waveform and sample rate.
 */
@Injectable()
export class MusicGenService {
  constructor(private readonly http: HttpService) {}

  /**
   * Request music generation from the Python FastAPI service.
   * Endpoint: POST http://localhost:8000/api/musicgen/generate
   * @param genre Music genre (e.g., 'ambient', 'rock')
   * @param duration Duration in seconds
   * @param seed Optional random seed for reproducibility
   * @returns Observable<{ waveform: string; sample_rate: number }>
   *
   * Example:
   *   service.generateMusic('ambient', 10, 42).subscribe(result => ...)
   */
  generateMusic(
    genre: string,
    duration: number,
    seed?: number
  ): Observable<{ waveform: string; sample_rate: number }> {
    return this.http
      .post('http://localhost:8000/api/musicgen/generate', {
        genre,
        duration,
        seed,
      })
      .pipe(map((response: { data: { waveform: string; sample_rate: number } }) => response.data));
  }
}
