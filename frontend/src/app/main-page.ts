import { Component, inject } from '@angular/core';
import { MusicGenService, MusicGenResult } from './musicgen.service';
import { AudioPlayerService } from './audio-player.service';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.html',
  styleUrls: ['./main-page.scss'],
  animations: [],
  standalone: false
})
export class MainPageComponent {
  title = 'True North Audio';
  subtitle = 'Create vibrant music and video assets';

  genre = 'ambient';
  duration = 10;
  seed?: number;
  tempo = 120;
  idea?: string;
  loading = false;
  result?: MusicGenResult;
  error?: string;

  private musicGen = inject(MusicGenService);
  private audioPlayer = inject(AudioPlayerService);

  generateMusic() {
    this.loading = true;
    this.error = undefined;
    this.result = undefined;
    this.musicGen.generateMusic(
      this.genre,
      this.duration,
      this.seed,
      this.idea
    ).subscribe({
      next: (response) => {
        this.result = response;
        // Set audio player src
        if (response && response.waveform) {
          const audioElem = document.getElementById('musicgen-audio') as HTMLAudioElement;
          if (audioElem) {
            const wavBlob = this.audioPlayer.base64ToWavBlob(response.waveform, response.sample_rate);
            audioElem.src = URL.createObjectURL(wavBlob);
            audioElem.load();
            audioElem.play();
          }
        }
        // Set vocals transcription
        const vocalsElem = document.getElementById('vocals-output');
        if (vocalsElem && response && response.vocals) {
          vocalsElem.textContent = response.vocals;
        }
        this.loading = false;
      },
      error: (err) => {
        this.error = err?.message || 'Failed to generate music.';
        this.loading = false;
      }
    });
  }
}
