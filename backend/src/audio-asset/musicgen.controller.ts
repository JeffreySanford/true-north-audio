import { Controller, Post, Body } from '@nestjs/common';
import { MusicGenService } from './musicgen.service';
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
  generate(@Body() dto: GenerateMusicDto): Observable<{ waveform: string; sample_rate: number }> {
    return this.musicGenService.generateMusic(dto.genre, dto.duration, dto.seed);
  }
}
