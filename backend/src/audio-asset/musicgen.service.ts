import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Observable, map, tap, catchError, of } from 'rxjs';
import { OlammaLog } from '../models/olamma-log.model';
import { WorkspaceLogger } from '../app/workspace-logger';
export interface MusicGenResult {
  waveform: string;
  sample_rate: number;
  vocals?: string;
  audio_url?: string;
  error?: string;
}

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
  private logger: WorkspaceLogger;
  constructor(
    private readonly http: HttpService,
    @InjectModel('OlammaLog') private readonly olammaLogModel: Model<OlammaLog>
  ) {
    this.logger = new WorkspaceLogger();
  }

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
    engine: string,
    model?: string,
    seed?: number,
    idea?: string,
    vocal_artist?: string,
    tempo?: number,
    variation?: string,
    songSections?: Array<{ type: string; duration: number; transition?: string }>
  ): Observable<MusicGenResult> {
    // Call Olamma in-memory FastAPI
    return this.http
      .post<{ waveform: string; sample_rate: number; vocals?: string; audio_url?: string; error?: string }>(
        'http://localhost:11434/musicgen',
        {
          genre,
          duration,
          engine,
          model,
          seed,
          idea,
          vocal_artist,
          tempo,
          variation,
          songSections
        }
      )
      .pipe(
        map((response) => response.data),
        tap(async (result) => {
          // Log to MongoDB
          await this.olammaLogModel.create({
            prompt: `Genre: ${genre}, Duration: ${duration}, Engine: ${engine}, Model: ${model}, Seed: ${seed}, Idea: ${idea}, VocalArtist: ${vocal_artist}, Tempo: ${tempo}, Variation: ${variation}, SongSections: ${JSON.stringify(songSections)}`,
            audioUrl: result.audio_url || '',
            createdAt: new Date(),
          });
          // Log to workspace log file
          this.logger.info(
            `MusicGen: genre=${genre}, duration=${duration}, engine=${engine}, model=${model}, seed=${seed}, idea=${idea}, vocal_artist=${vocal_artist}, tempo=${tempo}, variation=${variation}, songSections=${JSON.stringify(songSections)}, audioUrl=${result.audio_url}, error=${result.error}`
          );
        }),
        catchError((error) => {
          const errorMessage = error.code === 'ECONNREFUSED' 
            ? 'Ollama service is not running. Please start Ollama with: ollama serve'
            : `Music generation failed: ${error.message}`;
          
          this.logger.error(`MusicGen Error: ${errorMessage}`, error.stack);
          
          // Return a user-friendly error response instead of throwing
          return of({
            waveform: '',
            sample_rate: 0,
            error: errorMessage
          } as MusicGenResult);
        })
      );
  }
}
