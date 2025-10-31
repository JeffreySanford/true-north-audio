import { Controller, Post, Body } from '@nestjs/common';
import { MusicGenService, MusicGenResult } from './musicgen.service';
import { Observable } from 'rxjs';


/**
 * DTO for music generation request.
 * @property genre Music genre (e.g., 'ambient', 'rock')
 * @property duration Duration in seconds
 * @property seed Optional random seed for reproducibility
 */
export class GenerateMusicDto {
  genre!: string;
  duration!: number;
  seed?: number;
  idea?: string;
  vocal_artist?: string;
  tempo?: number;
  variation?: string;
  songSections?: Array<{ type: string; duration: number; transition?: string }>;
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
   * POST /musicgen/generate
   * Triggers music generation with provided parameters.
   * @param dto GenerateMusicDto
   * @returns Observable with waveform and sample rate
   *
   * Example:
   *   POST /musicgen/generate { genre: 'ambient', duration: 10, seed: 42 }
   */
  @Post('generate')
  generate(@Body() dto: GenerateMusicDto): Observable<MusicGenResult> {
    return this.musicGenService.generateMusic(
      dto.genre,
      dto.duration,
      dto.seed,
      dto.idea,
      dto.vocal_artist,
      dto.tempo,
      dto.variation,
      dto.songSections
    );
  }
}
