// ...existing code...
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AudioPlayerService {
  public audioCtx: AudioContext | null = null;

  playWaveformBase64(base64: string, sampleRate: number) {
    const floatArray = this.decodeBase64ToFloat32Array(base64);
    this.playFloat32Array(floatArray, sampleRate);
  }

  base64ToWavBlob(base64: string, sampleRate: number): Blob {
    const floatArray = this.decodeBase64ToFloat32Array(base64);
    const wavBuffer = this.encodeWav(floatArray, sampleRate);
    return new Blob([wavBuffer], { type: 'audio/wav' });
  }

  private encodeWav(floatArray: Float32Array, sampleRate: number): ArrayBuffer {
    const numSamples = floatArray.length;
    const buffer = new ArrayBuffer(44 + numSamples * 2);
    const view = new DataView(buffer);
    // RIFF header
    this.writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + numSamples * 2, true);
    this.writeString(view, 8, 'WAVE');
    // fmt chunk
    this.writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true); // PCM chunk size
    view.setUint16(20, 1, true); // PCM format
    view.setUint16(22, 1, true); // Mono
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true); // Byte rate
    view.setUint16(32, 2, true); // Block align
    view.setUint16(34, 16, true); // Bits per sample
    // data chunk
    this.writeString(view, 36, 'data');
    view.setUint32(40, numSamples * 2, true);
    // PCM samples
    let offset = 44;
    for (let i = 0; i < numSamples; i++, offset += 2) {
      const s = Math.max(-1, Math.min(1, floatArray[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
    return buffer;
  }

  private writeString(view: DataView, offset: number, str: string) {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  }

  public decodeBase64ToFloat32Array(base64: string): Float32Array {
    const binary = atob(base64);
    const len = binary.length / 4;
    const floatArray = new Float32Array(len);
    for (let i = 0; i < len; i++) {
      const bytes = [
        binary.charCodeAt(i * 4),
        binary.charCodeAt(i * 4 + 1),
        binary.charCodeAt(i * 4 + 2),
        binary.charCodeAt(i * 4 + 3),
      ];
      const view = new DataView(new Uint8Array(bytes).buffer);
      floatArray[i] = view.getFloat32(0, true);
    }
    return floatArray;
  }

  private playFloat32Array(floatArray: Float32Array, sampleRate: number) {
    if (!this.audioCtx) {
      this.audioCtx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
    }
    const buffer = this.audioCtx.createBuffer(1, floatArray.length, sampleRate);
    buffer.getChannelData(0).set(floatArray);
    const source = this.audioCtx.createBufferSource();
    source.buffer = buffer;
    source.connect(this.audioCtx.destination);
    source.start();
  }
}
