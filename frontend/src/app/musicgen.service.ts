import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface MusicGenResult {
  waveform: string;
  sample_rate: number;
}

@Injectable({ providedIn: 'root' })
export class MusicGenService {
  private http = inject(HttpClient);

  generateMusic(genre: string, duration: number, seed?: number): Observable<MusicGenResult> {
    return this.http.post<MusicGenResult>('/api/musicgen/generate', { genre, duration, seed });
  }
}
