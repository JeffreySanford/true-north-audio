import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface MusicGenResult {
  waveform: string;
  sample_rate: number;
  vocals?: string;
  audio_url?: string;
  engine?: 'audiocraft' | 'bark' | 'midi';  // Which engine was used
  generation_time?: number;  // Time taken in seconds
  model_info?: string;  // Model details
}

export type AIEngine = 'audiocraft' | 'bark' | 'auto';

@Injectable({ providedIn: 'root' })
export class MusicGenService {
  private http = inject(HttpClient);

  private readonly BASE_URL = 'http://localhost:3000/api';

  /**
   * Generate music using the selected AI engine
   * @param engine - 'audiocraft' (MusicGen), 'bark' (vocals + MIDI), or 'auto' (best available)
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
    return this.http.post<MusicGenResult>(`${this.BASE_URL}/musicgen/generate`, {
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
    });
  }

  /**
   * Check which AI engines are available on the backend
   */
  checkAvailableEngines(): Observable<{ 
    audiocraft: boolean; 
    bark: boolean;
    midi: boolean;
    recommended: AIEngine;
  }> {
    return this.http.get<{ 
      audiocraft: boolean; 
      bark: boolean; 
      midi: boolean;
      recommended: AIEngine;
    }>(`${this.BASE_URL}/musicgen/engines`);
  }
}
