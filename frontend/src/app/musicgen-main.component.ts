import { Component, OnInit } from '@angular/core';
import { inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface Genre {
  name: string;
  instruments: string[];
  description?: string;
  bpm?: number;
  timeSignature?: string;
  groove?: string;
  mandatoryInstruments?: string[];
  scriptTemplate?: string;
}

@Component({
  selector: 'app-musicgen-main',
  templateUrl: './musicgen-main.component.html',
  styleUrls: ['./musicgen-main.component.scss'],
  standalone: false
})
export class MusicGenMainComponent implements OnInit {
  genres: Genre[] = [];
  selectedGenre: Genre | null = null;
  instruments: string[] = [];
  activeInstruments: string[] = [];

  private http = inject(HttpClient);

  ngOnInit() {
    this.http.get<Genre[]>('/api/genres').subscribe(genres => {
      this.genres = genres;
      this.selectedGenre = genres[0]; // Liberty Blues default
      this.activeInstruments = genres[0]?.instruments || [];
    });
    this.http.get<string[]>('/api/instruments').subscribe(insts => this.instruments = insts);
  }

  onGenreChange(genre: Genre): void {
    this.selectedGenre = genre;
    this.activeInstruments = genre.instruments;
  }

  toggleInstrument(inst: string): void {
    const enabled = !this.activeInstruments.includes(inst);
    this.http.post<{ instruments: string[] }>(
      '/api/genres/toggle-instrument',
      {
        genreName: this.selectedGenre ? this.selectedGenre.name : '',
        instrument: inst,
        enabled: enabled
      }
    ).subscribe((res: { instruments: string[] }) => {
      this.activeInstruments = res.instruments;
    });
  }
}
