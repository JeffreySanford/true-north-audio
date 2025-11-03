# True North Audio - Improvement Roadmap

## Current State
✅ Project structure with Nx monorepo
✅ Angular frontend + NestJS backend
✅ Python AI music generation module
✅ Dependencies tracked and auto-installed
✅ Hardware detection (i9 24-core, 63GB RAM)

## 🎯 Priority Improvements

### 1. **AI Music Generation (HIGH PRIORITY)**

#### Current Issue
- Generating random noise/static instead of real music
- AudioCraft not fully integrated

#### Solution
```bash
# Install AudioCraft properly
pip install git+https://github.com/facebookresearch/audiocraft

# OR use lighter alternative:
pip install music21  # For MIDI-based generation
```

#### Code Improvements Needed
- ✅ Hardware detection implemented
- ⚠️ Need real MusicGen model loading
- ⚠️ Need proper audio synthesis
- ⚠️ Need vocals with Bark TTS integration

**Implementation Steps:**
1. Create fallback system (MIDI → MusicGen → Professional)
2. Add model caching to avoid re-downloading
3. Implement chunk-based generation for long songs
4. Add progress bars for model loading

---

### 2. **Lyrics & Vocal Generation**

#### Current
- Lyrics defined but not synthesized
- No actual vocal generation

#### Improvements
**Option A: Bark TTS (Open Source)**
```python
from bark import SAMPLE_RATE, generate_audio
from bark.generation import preload_models

# Generate vocals for each segment
audio = generate_audio(text, history_prompt="v2/en_speaker_9")
```

**Option B: Alternative TTS**
- Coqui TTS (faster, less realistic)
- Microsoft Azure TTS (cloud, costs money)
- ElevenLabs API (highest quality, expensive)

**Recommended:** Start with Bark for blues style vocals

---

### 3. **Multi-Instrument Orchestration**

#### Current
Single waveform generation

#### Improvements
```python
# Generate separate stems
guitar_lead = generate_instrument("blues guitar lead", duration=160)
bass_line = generate_instrument("walking bass", duration=160)
drums = generate_instrument("shuffle drums", duration=160)
organ = generate_instrument("hammond b3", duration=160)

# Mix with proper levels
mixed = mix_stems({
    'guitar_lead': (guitar_lead, 0.8),
    'bass': (bass_line, 0.6),
    'drums': (drums, 0.7),
    'organ': (organ, 0.5)
})
```

**Tools:**
- **pydub** for mixing (already installed ✅)
- **pedalboard** (Spotify's audio effects)
- **pyrubberband** for time-stretching

---

### 4. **Professional Audio Processing**

#### Current
- Basic compression, reverb, EQ implemented
- All simulated, not actually applied

#### Improvements
**Real Audio Effects:**
```python
from pedalboard import Pedalboard, Compressor, Reverb, Gain
from pedalboard.io import AudioFile

board = Pedalboard([
    Compressor(threshold_db=-16, ratio=4),
    Reverb(room_size=0.25, wet_level=0.2),
    Gain(gain_db=0.5)
])

# Apply to audio
effected = board(audio, sample_rate)
```

**Install:**
```bash
pip install pedalboard
```

---

### 5. **Blues-Specific Enhancements**

#### Musical Improvements
1. **12-Bar Blues Progression**
   ```python
   progression = [
       ("I", 4), ("IV", 2), ("I", 2),
       ("V", 1), ("IV", 1), ("I", 2)
   ]
   ```

2. **Blues Scale (E minor pentatonic)**
   ```python
   blues_scale = [0, 3, 5, 6, 7, 10, 12]  # Semitones from root
   ```

3. **Shuffle Rhythm (swing)**
   ```python
   swing_ratio = 2.0  # Triplet feel
   ```

4. **Guitar Techniques**
   - String bends (pitch automation)
   - Vibrato (LFO on pitch)
   - Slide guitar (portamento)

---

### 6. **Performance Optimization**

#### Current
- GPU detection implemented ✅
- Multi-core support ready ✅
- Not actually using them yet ⚠️

#### Improvements

**GPU Acceleration:**
```python
# Move models to GPU
model = model.to('cuda')

# Use mixed precision
with torch.cuda.amp.autocast():
    audio = model.generate(prompt)
```

**Parallel Generation:**
```python
from multiprocessing import Pool

def generate_section(section):
    return model.generate(section['prompt'])

with Pool(24) as pool:  # Use all 24 cores
    sections = pool.map(generate_section, song_sections)
```

**Caching:**
```python
import hashlib
import pickle

def cached_generate(prompt):
    cache_key = hashlib.md5(prompt.encode()).hexdigest()
    cache_file = f".cache/{cache_key}.pkl"
    
    if os.path.exists(cache_file):
        return pickle.load(open(cache_file, 'rb'))
    
    result = model.generate(prompt)
    pickle.dump(result, open(cache_file, 'wb'))
    return result
```

---

### 7. **Better Project Integration**

#### Frontend Integration
```typescript
// frontend/src/app/services/music-generation.service.ts
export class MusicGenerationService {
  generateSong(config: SongConfig): Observable<GenerationProgress> {
    return this.http.post('/api/musicgen/generate', config)
      .pipe(
        map(response => ({
          progress: response.progress,
          audioUrl: response.audioUrl,
          status: response.status
        }))
      );
  }
}
```

#### Backend Endpoint
```typescript
// backend/src/music-gen/music-gen.controller.ts
@Post('generate')
async generateMusic(@Body() config: GenerateMusicDto) {
  return this.pythonService.callMusicGen(config);
}
```

---

### 8. **Quality of Life Improvements**

#### Better CLI Output
```python
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
) as progress:
    task = progress.add_task("Generating music...", total=100)
    # ... generation code
    progress.update(task, advance=10)
```

#### Configuration File
```yaml
# config/music-generation.yaml
defaults:
  genre: blues
  tempo: 88
  duration: 160
  sample_rate: 48000
  
instruments:
  lead_guitar:
    volume: 0.8
    effects: [reverb, compression]
  bass:
    volume: 0.6
  drums:
    volume: 0.7
```

---

### 9. **Testing & Quality Assurance**

#### Add Tests
```python
# tests/test_music_generation.py
def test_generate_blues():
    result = generate_music(genre='blues', duration=10)
    assert result['status'] == 'success'
    assert len(result['waveform']) > 0
    assert result['sample_rate'] == 48000
```

#### Audio Quality Metrics
```python
def analyze_audio_quality(waveform):
    return {
        'peak_db': calculate_peak(waveform),
        'rms_db': calculate_rms(waveform),
        'dynamic_range': calculate_dynamic_range(waveform),
        'spectral_centroid': calculate_spectral_features(waveform)
    }
```

---

### 10. **Documentation & Examples**

#### Create Examples
```
examples/
├── simple_melody.py          # Basic MIDI generation
├── blues_with_vocals.py      # Liberty Blues
├── multi_track_song.py       # Full orchestration
└── realtime_generation.py    # Streaming audio
```

#### API Documentation
```bash
# Generate docs
cd ai-music-gen
python -m pydoc -w musicgen.core
```

---

## 🚀 Quick Wins (Do These First)

### 1. Fix AudioCraft Installation
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in virtual environment
pip install -r requirements.txt
pip install git+https://github.com/facebookresearch/audiocraft
```

### 2. Add Simple MIDI Fallback
Update `generate_liberty_blues.py` to generate MIDI first, then upgrade to AI later:
```python
# If AudioCraft not available, fall back to MIDI
try:
    from audiocraft.models import MusicGen
    USE_AI = True
except ImportError:
    USE_AI = False
    print("AudioCraft not available, using MIDI generation")
```

### 3. Add Progress Bars
```bash
pip install tqdm rich
```

### 4. Enable GPU if Available
The code is ready, just needs models loaded properly.

### 5. Add Audio Player
```python
from pydub import AudioSegment
from pydub.playback import play

audio = AudioSegment.from_mp3("output.mp3")
play(audio)
```

---

## 📊 Success Metrics

### Current
- ⚠️ Generates static/noise
- ⚠️ No vocals
- ⚠️ No real instruments
- ⏱️ Fast (0.3 seconds - too fast, fake)

### Target
- ✅ Professional blues music
- ✅ Synthesized vocals with lyrics
- ✅ Multiple instruments (guitar, bass, drums, organ)
- ⏱️ 3-5 minutes generation time (with GPU)
- 🎵 -14 LUFS professional loudness
- 📊 48kHz/24-bit studio quality

---

## 💡 Next Steps

1. **Immediate** (Today):
   - Fix AudioCraft installation in virtual environment
   - Add MIDI fallback for testing
   - Test with 10-second samples

2. **Short-term** (This Week):
   - Integrate real MusicGen model
   - Add progress indicators
   - Implement caching

3. **Medium-term** (This Month):
   - Add Bark TTS vocals
   - Multi-track generation
   - Professional audio processing

4. **Long-term** (Future):
   - Real-time generation
   - Web interface integration
   - Collaborative features

---

## 🔧 Development Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Development
python generate_liberty_blues.py --duration 10  # Quick test
python generate_liberty_blues.py --gpu          # Use GPU
python generate_liberty_blues.py --cache        # Use caching

# Testing
pytest tests/
python -m pytest --cov=ai_music_gen

# Linting
flake8 ai-music-gen/
black ai-music-gen/

# Full workflow
npm run test:all
npm run build:all
npm run serve:all
```

---

## 📚 Resources

- [AudioCraft Docs](https://github.com/facebookresearch/audiocraft)
- [Bark TTS](https://github.com/suno-ai/bark)
- [MusicGen Paper](https://arxiv.org/abs/2306.05284)
- [Blues Music Theory](https://www.thejazzpianosite.com/jazz-piano-lessons/jazz-blues/)

---

**Want to tackle any of these improvements? Let me know which area to focus on first!** 🎸🎵
