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
  // Multi-section song structure
  songSections: Array<{ type: string; duration: number; transition?: string }> = [
    { type: 'verse', duration: 16, transition: 'none' },
    { type: 'chorus', duration: 16, transition: 'none' }
  ];

  addSection() {
    this.songSections.push({ type: 'verse', duration: 8, transition: 'none' });
  }

  removeSection(i: number) {
    if (this.songSections.length > 1) {
      this.songSections.splice(i, 1);
    }
  }
  playMp3() {
    if (this.result?.audio_url) {
      const audioElem = document.getElementById('musicgen-audio') as HTMLAudioElement;
      if (audioElem) {
        audioElem.src = this.result.audio_url;
        audioElem.load();
        audioElem.play();
      }
    }
  }

  playWav() {
    if (this.result?.waveform && this.result?.sample_rate) {
      const audioElem = document.getElementById('musicgen-audio') as HTMLAudioElement;
      if (audioElem) {
        const wavBlob = this.audioPlayer.base64ToWavBlob(this.result.waveform, this.result.sample_rate);
        audioElem.src = URL.createObjectURL(wavBlob);
        audioElem.load();
        audioElem.play();
      }
    }
  }

  downloadWav() {
    if (this.result?.waveform && this.result?.sample_rate) {
      const wavBlob = this.audioPlayer.base64ToWavBlob(this.result.waveform, this.result.sample_rate);
      const url = URL.createObjectURL(wavBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'musicgen.wav';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  }
  audioUrlNotFound = false;
  directSource?: AudioBufferSourceNode;

  title = 'True North Audio';
  subtitle = 'Create vibrant music and video assets';

  genre = 'ambient';
  duration = 10;
  seed?: number;
  tempo = 120;
  idea?: string;
  vocal_artist = 'none';
  variation = 'original';
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
        this.idea,
        this.vocal_artist,
        this.tempo,
        this.variation,
        this.songSections // Pass sections to service
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
        // Check if audio_url file exists
        this.audioUrlNotFound = false;
        if (response && response.audio_url) {
          fetch(response.audio_url)
            .then(res => {
              if (!res.ok) {
                this.audioUrlNotFound = true;
              }
            })
            .catch(() => {
              this.audioUrlNotFound = true;
            });
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

    playDirect() {
      if (this.result?.waveform && this.result?.sample_rate) {
        const floatArray = this.audioPlayer.decodeBase64ToFloat32Array(this.result.waveform);
        if (!this.audioPlayer.audioCtx) {
          this.audioPlayer.audioCtx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
        }
        const buffer = this.audioPlayer.audioCtx.createBuffer(1, floatArray.length, this.result.sample_rate);
        buffer.getChannelData(0).set(floatArray);
        this.directSource = this.audioPlayer.audioCtx.createBufferSource();
        this.directSource.buffer = buffer;
        this.directSource.connect(this.audioPlayer.audioCtx.destination);
        this.directSource.start();
      }
    }

    stopDirect() {
      if (this.directSource) {
        this.directSource.stop();
        this.directSource.disconnect();
        this.directSource = undefined;
      }
    }
}
