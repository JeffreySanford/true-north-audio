import { Component, OnInit, Output, EventEmitter } from '@angular/core';

interface Engine {
  name: string;
  creator: string;
  models?: string[];
}

@Component({
  selector: 'app-musicgen-engine-selector',
  templateUrl: './musicgen-selector.component.html',
  styleUrls: ['./musicgen-selector.component.scss'],
  standalone: false
})
export class MusicgenEngineSelectorComponent implements OnInit {
  engines: Engine[] = [
    { name: 'Ollama', creator: 'Ollama Inc.', models: [] },
    { name: 'MusicGen', creator: 'Meta' },
    { name: 'Jukebox', creator: 'OpenAI' },
    { name: 'Stable Audio', creator: 'Stability AI' },
    { name: 'Riffusion', creator: 'Seth Forsgren & Hayk Martiros' },
    { name: 'OpenAI Jukebox', creator: 'OpenAI' }
  ];
  selectedEngine = this.engines[0];
  selectedModel = '';

  @Output() engineChange = new EventEmitter<{ engine: string; model?: string }>();

  ngOnInit() {
    this.loadOllamaModels();
  }

  loadOllamaModels() {
    // For now, use hardcoded models since the API endpoint isn't working
    const ollamaEngine = this.engines.find(e => e.name === 'Ollama');
    if (ollamaEngine) {
      ollamaEngine.models = ['llama3.2', 'llama3.1', 'codellama'];
      this.selectedModel = 'llama3.2';
      this.emitChange();
    }

    // TODO: Re-enable API call when Ollama service is properly configured
    // this.http.get<{ models: { name: string }[] }>('http://localhost:11434/api/tags').subscribe({
    //   next: (response) => {
    //     const ollamaEngine = this.engines.find(e => e.name === 'Ollama');
    //     if (ollamaEngine) {
    //       ollamaEngine.models = response.models.map(m => m.name);
    //       this.selectedModel = ollamaEngine.models[0] || 'llama3.2';
    //       this.emitChange();
    //     }
    //   },
    //   error: (err) => {
    //     console.error('Failed to load Ollama models', err);
    //     // Fallback
    //     const ollamaEngine = this.engines.find(e => e.name === 'Ollama');
    //     if (ollamaEngine) {
    //       ollamaEngine.models = ['llama3.2'];
    //       this.selectedModel = 'llama3.2';
    //       this.emitChange();
    //     }
    //   }
    // });
  }

  onEngineChange() {
    if (this.selectedEngine.name === 'Ollama') {
      this.selectedModel = this.selectedEngine.models?.[0] || 'llama3.2';
    } else {
      this.selectedModel = '';
    }
    this.emitChange();
  }

  onModelChange() {
    this.emitChange();
  }

  private emitChange() {
    this.engineChange.emit({
      engine: this.selectedEngine.name,
      model: this.selectedModel || undefined
    });
  }
}
