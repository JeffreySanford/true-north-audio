import { Component, inject } from '@angular/core';
import { MusicGenService, MusicGenResult } from './musicgen.service';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.html',
  styleUrls: ['./main-page.scss'],
  animations: [],
})
export class MainPageComponent {
  title = 'True North Audio';
  subtitle = 'Create vibrant music and video assets';

  genre = 'ambient';
  duration = 10;
  seed?: number;
  loading = false;
  result?: MusicGenResult;
  error?: string;

  private musicGen = inject(MusicGenService);

  generateMusic() {
    this.loading = true;
    this.error = undefined;
    this.result = undefined;
    this.musicGen.generateMusic(this.genre, this.duration, this.seed).subscribe({
      next: (res: MusicGenResult) => {
        this.result = res;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to generate music.';
        this.loading = false;
      },
    });
  }
}
