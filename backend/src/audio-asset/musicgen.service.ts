import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Observable, map, tap } from 'rxjs';
import { OlammaLog } from '../models/olamma-log.model';
import { WorkspaceLogger } from '../app/workspace-logger';
export interface MusicGenResult {
  waveform: string;
  sample_rate: number;
  vocals?: string;
  audio_url?: string;
  error?: string;
  engine?: 'audiocraft' | 'bark' | 'midi';  // Which engine was used
  generation_time?: number;  // Time taken in seconds
  model_info?: string;  // Model details
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
    @InjectModel('OlammaLog') private readonly olammaLogModel: Model<OlammaLog>,
    @InjectModel('AudioAsset') private readonly audioAssetModel: Model<any>
  ) {
    this.logger = new WorkspaceLogger();
  }

  /**
   * Check which AI engines are available on the Python backend.
   * @returns Observable with availability status for each engine
   */
  checkAvailableEngines(): Observable<{ 
    audiocraft: boolean; 
    bark: boolean; 
    midi: boolean;
    recommended: 'audiocraft' | 'bark' | 'auto';
  }> {
    return this.http
      .get<{ audiocraft: boolean; bark: boolean; midi: boolean; recommended: 'audiocraft' | 'bark' | 'auto' }>(
        'http://localhost:11434/musicgen/engines'
      )
      .pipe(
        map((response) => response.data)
      );
  }

  /**
   * Request music generation from the Python FastAPI service.
   * Endpoint: POST http://localhost:11434/musicgen
   * @param genre Music genre (e.g., 'ambient', 'rock')
   * @param duration Duration in seconds
   * @param seed Optional random seed for reproducibility
   * @param idea Optional idea/prompt for generation
   * @param vocal_artist Optional vocal artist style
   * @param tempo Optional tempo in BPM
   * @param variation Optional variation type
   * @param songSections Optional song structure sections
   * @param engine AI engine to use: 'audiocraft', 'bark', or 'auto'
   * @returns Observable<MusicGenResult>
   *
   * Example:
   *   service.generateMusic('ambient', 10, 42, undefined, undefined, 120, 'original', [], 'auto').subscribe(result => ...)
   */
  generateMusic(
    genre: string,
    duration: number,
    seed?: number,
    idea?: string,
    vocal_artist?: string,
    tempo?: number,
    variation?: string,
    songSections?: Array<{ type: string; duration: number; transition?: string }>,
    engine: 'audiocraft' | 'bark' | 'auto' = 'auto'
  ): Observable<MusicGenResult> {
    // Call Olamma in-memory FastAPI
    return this.http
      .post<MusicGenResult>(
        'http://localhost:11434/musicgen',
        {
          genre,
          duration,
          seed,
          idea,
          vocal_artist,
          tempo,
          variation,
          songSections,
          engine
        }
      )
      .pipe(
        map((response) => response.data),
        tap(async (result) => {
          // Log to MongoDB
          await this.olammaLogModel.create({
            prompt: `Genre: ${genre}, Duration: ${duration}, Seed: ${seed}, Idea: ${idea}, VocalArtist: ${vocal_artist}, Tempo: ${tempo}, Variation: ${variation}, SongSections: ${JSON.stringify(songSections)}, Engine: ${engine}`,
            audioUrl: result.audio_url || '',
            createdAt: new Date(),
          });
          // Save generated song to AudioAsset collection
          if (result.audio_url) {
            await this.audioAssetModel.create({
              title: idea || `${genre} song`,
              genre: genre, // You may need to resolve genre ObjectId
              filePath: result.audio_url,
              vocalFeatures: [], // Extend as needed
            });
          }
          // Log to workspace log file
          this.logger.info(
            `MusicGen: genre=${genre}, duration=${duration}, seed=${seed}, idea=${idea}, vocal_artist=${vocal_artist}, tempo=${tempo}, variation=${variation}, songSections=${JSON.stringify(songSections)}, engine=${engine}, usedEngine=${result.engine}, audioUrl=${result.audio_url}, generationTime=${result.generation_time}s, error=${result.error}`
          );
        })
      );
  }
}
