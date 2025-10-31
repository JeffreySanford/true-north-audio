import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface MusicGenResult {
  waveform: string;
  sample_rate: number;
  vocals?: string;
  audio_url?: string;
}

@Injectable({ providedIn: 'root' })
export class MusicGenService {
  private http = inject(HttpClient);

  private readonly BASE_URL = 'http://localhost:3000/api';

  generateMusic(
      genre: string,
      duration: number,
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
        seed,
        idea,
        vocal_artist,
        tempo,
        variation,
        songSections
      });
  }
}
