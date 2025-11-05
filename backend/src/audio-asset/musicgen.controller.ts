import { Controller, Post, Body, Get } from '@nestjs/common';
import { MusicGenService, MusicGenResult } from './musicgen.service';
import { Observable } from 'rxjs';


/**
 * DTO for music generation request.
 * @property genre Music genre (e.g., 'ambient', 'rock')
 * @property duration Duration in seconds
 * @property engine Music generation engine (e.g., 'MusicGen', 'Jukebox')
 * @property seed Optional random seed for reproducibility
 * @property engine AI engine to use: 'audiocraft', 'bark', or 'auto'
 */
export class GenerateMusicDto {
  genre!: string;
  duration!: number;
  engine?: string; // Accepts any engine string, e.g., 'audiocraft', 'bark', 'auto', 'MusicGen', etc.
  model?: string;  // Ollama model name, e.g., 'llama3.2'
  seed?: number;
  idea?: string;
  vocal_artist?: string;
  tempo?: number;
  variation?: string;
  songSections?: Array<{ type: string; duration: number; transition?: string }>;
  lyrics?: string;
  vocal_style?: string;
}


/**
 * Controller for AI music generation endpoints.
 * Provides REST API for generating music via Python backend.
 */
@Controller('musicgen')
export class MusicGenController {
  /**
   * Injects MusicGenService for backend integration.
   * @param musicGenService MusicGenService instance
   */
  constructor(private readonly musicGenService: MusicGenService) {}

  /**
   * GET /musicgen/engines
   * Check which AI engines are available on the system.
   * @returns Object with availability status for each engine
   *
   * Example response:
   *   { audiocraft: true, bark: true, midi: true, recommended: 'audiocraft' }
   */
  @Get('engines')
  checkEngines(): Observable<{ 
    audiocraft: boolean; 
    bark: boolean; 
    midi: boolean;
    recommended: 'audiocraft' | 'bark' | 'auto';
  }> {
    return this.musicGenService.checkAvailableEngines();
  }

  /**
   * POST /musicgen/generate
   * Triggers music generation with provided parameters.
   * @param dto GenerateMusicDto
   * @returns Observable with waveform and sample rate
   *
   * Example:
  *   POST /musicgen/generate { genre: 'ambient', duration: 10, engine: 'MusicGen', seed: 42 }
   */
  @Post('generate')
  generate(@Body() dto: GenerateMusicDto): Observable<MusicGenResult> {
    return this.musicGenService.generateMusic(
      dto.genre,
      dto.duration,
      dto.engine ?? 'auto',
      dto.idea,
      dto.vocal_artist,
      dto.tempo,
      dto.variation,
      dto.songSections,
      dto.lyrics,
      dto.vocal_style
    );
  }
}
