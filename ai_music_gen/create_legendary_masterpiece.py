#!/usr/bin/env python3
"""
LEGENDARY MASTERPIECE - Professional-quality AI blues with advanced production
"""
import os
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import signal
import mido
import warnings
warnings.filterwarnings('ignore')

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "backend" / \
    "src" / "assets" / "generated"
# MIDI file with JAMES BROWN FUNK arrangement!
MIDI_FILE = "liberty_blues_JAMES_BROWN_FUNK.mid"

# Song structure
STRUCTURE = {
    "intro": 0, "verse_1": 16, "chorus_1": 28, "verse_2": 40,
    "chorus_2": 52, "bridge": 64, "guitar_solo": 76,
    "final_chorus": 88, "outro": 100
}

VOCAL_MAPPING = {
    "verse_1": "vocal_verse_1.wav", "chorus_1": "vocal_chorus_1.wav",
    "verse_2": "vocal_verse_2.wav", "chorus_2": "vocal_chorus_2.wav",
    "bridge": "vocal_bridge.wav", "final_chorus": "vocal_final_chorus.wav",
    "outro": "vocal_outro.wav"
}

BPM = 108  # James Brown funk tempo!
BEATS_PER_BAR = 4
SAMPLE_RATE = 24000
MS_PER_BEAT = (60 / BPM) * 1000


def bars_to_samples(bars):
    """Convert bar number to sample position"""
    ms = bars * BEATS_PER_BAR * MS_PER_BEAT
    return int((ms / 1000) * SAMPLE_RATE)

# ==================== AUDIO EFFECTS ====================


def create_reverb_ir(length_samples, decay=0.4):
    """Create impulse response for reverb"""
    t = np.arange(length_samples) / SAMPLE_RATE
    # Exponential decay with random noise
    ir = np.random.randn(length_samples) * np.exp(-decay * t * 10)
    # Add early reflections
    for i in range(5):
        delay = int(np.random.uniform(0.01, 0.05) * SAMPLE_RATE)
        if delay < length_samples:
            ir[delay] += np.random.uniform(0.3, 0.7)
    return ir / np.max(np.abs(ir))


def apply_reverb(audio, wet_level=0.25, room_size=0.6):
    """Add realistic reverb"""
    ir_length = int(room_size * SAMPLE_RATE)
    ir = create_reverb_ir(ir_length)

    if len(audio.shape) == 2:
        # Stereo
        left_wet = signal.fftconvolve(audio[:, 0], ir, mode='same')
        right_wet = signal.fftconvolve(audio[:, 1], ir, mode='same')
        wet = np.column_stack([left_wet, right_wet])
    else:
        # Mono
        wet = signal.fftconvolve(audio, ir, mode='same')

    return audio * (1 - wet_level) + wet * wet_level


def apply_delay(audio, delay_time=0.375, feedback=0.4, wet_level=0.2):
    """Add tape-style delay (3/16 note delay at 88 BPM)"""
    delay_samples = int(delay_time * SAMPLE_RATE)

    if len(audio.shape) == 2:
        output = np.copy(audio)
        for channel in range(2):
            delayed = np.zeros_like(audio[:, channel])
            for i in range(3):  # 3 repeats
                start = delay_samples * (i + 1)
                gain = feedback ** (i + 1)
                if start < len(delayed):
                    delayed[start:] += audio[:len(delayed) -
                                             start, channel] * gain
            output[:, channel] += delayed * wet_level
    else:
        output = audio.copy()
        delayed = np.zeros_like(audio)
        for i in range(3):
            start = delay_samples * (i + 1)
            gain = feedback ** (i + 1)
            if start < len(delayed):
                delayed[start:] += audio[:len(delayed) - start] * gain
        output += delayed * wet_level

    return output


def apply_eq_band(audio, freq, gain_db, q=1.0):
    """Apply parametric EQ at specific frequency"""
    # nyq = SAMPLE_RATE / 2  # Unused variable removed
    w0 = 2 * np.pi * freq / SAMPLE_RATE
    alpha = np.sin(w0) / (2 * q)
    A = 10 ** (gain_db / 40)

    # Peaking filter coefficients
    b0 = 1 + alpha * A
    b1 = -2 * np.cos(w0)
    b2 = 1 - alpha * A
    a0 = 1 + alpha / A
    a1 = -2 * np.cos(w0)
    a2 = 1 - alpha / A

    b = np.array([b0, b1, b2]) / a0
    a = np.array([a0, a1, a2]) / a0

    if len(audio.shape) == 2:
        return np.column_stack([
            signal.filtfilt(b, a, audio[:, 0]),
            signal.filtfilt(b, a, audio[:, 1])
        ])
    else:
        return signal.filtfilt(b, a, audio)


def master_eq(audio):
    """Apply mastering EQ curve"""
    # Bass boost (80 Hz)
    audio = apply_eq_band(audio, 80, 2.0, q=0.7)
    # Low-mid clarity (250 Hz cut)
    audio = apply_eq_band(audio, 250, -1.5, q=1.5)
    # Presence boost (3 kHz)
    audio = apply_eq_band(audio, 3000, 3.0, q=1.2)
    # Air (12 kHz)
    audio = apply_eq_band(audio, 12000, 2.0, q=0.7)
    return audio


def multiband_compress(audio):
    """3-band compression for professional sound - optimized"""
    print("      Processing low band (20-200 Hz)...")
    # Split into 3 bands: low (20-200), mid (200-2k), high (2k-20k)
    sos_low = signal.butter(
        2, 200, 'lowpass', fs=SAMPLE_RATE, output='sos')  # Reduced order
    sos_high = signal.butter(2, 2000, 'highpass', fs=SAMPLE_RATE, output='sos')
    sos_mid = signal.butter(
        2, [200, 2000], 'bandpass', fs=SAMPLE_RATE, output='sos')

    if len(audio.shape) == 2:
        low_left = signal.sosfiltfilt(sos_low, audio[:, 0])
        low_right = signal.sosfiltfilt(sos_low, audio[:, 1])
        low = np.column_stack([low_left, low_right])

        print("      Processing mid band (200-2k Hz)...")
        mid_left = signal.sosfiltfilt(sos_mid, audio[:, 0])
        mid_right = signal.sosfiltfilt(sos_mid, audio[:, 1])
        mid = np.column_stack([mid_left, mid_right])

        print("      Processing high band (2k-20k Hz)...")
        high_left = signal.sosfiltfilt(sos_high, audio[:, 0])
        high_right = signal.sosfiltfilt(sos_high, audio[:, 1])
        high = np.column_stack([high_left, high_right])
    else:
        low = signal.sosfiltfilt(sos_low, audio)
        mid = signal.sosfiltfilt(sos_mid, audio)
        high = signal.sosfiltfilt(sos_high, audio)

    # Compress each band differently
    print("      Compressing bands...")
    low = compress_audio(low, threshold=0.6, ratio=3.0)
    mid = compress_audio(mid, threshold=0.5, ratio=4.0)
    high = compress_audio(high, threshold=0.4, ratio=2.0)

    return low + mid + high


def compress_audio(
        audio,
        threshold=0.5,
        ratio=4.0,
        attack=0.005,
        release=0.05):
    """Dynamic range compression"""
    attack_samples = int(attack * SAMPLE_RATE)
    release_samples = int(release * SAMPLE_RATE)

    if len(audio.shape) == 2:
        compressed = np.zeros_like(audio)
        for ch in range(2):
            compressed[:, ch] = _compress_channel(
                audio[:, ch], threshold, ratio, attack_samples, release_samples
            )
        return compressed
    else:
        return _compress_channel(
            audio,
            threshold,
            ratio,
            attack_samples,
            release_samples)


def _compress_channel(
        audio,
        threshold,
        ratio,
        attack_samples,
        release_samples):
    """Compress single channel"""
    gain_reduction = np.ones_like(audio)
    envelope = 0.0

    for i in range(len(audio)):
        # Envelope follower
        if abs(audio[i]) > envelope:
            envelope += (abs(audio[i]) - envelope) / attack_samples
        else:
            envelope -= envelope / release_samples

        # Apply compression
        if envelope > threshold:
            gain_reduction[i] = threshold + (envelope - threshold) / ratio
            gain_reduction[i] /= envelope

    return audio * gain_reduction


def create_vocal_harmony(vocal, semitones):
    """Pitch shift vocal for harmony"""
    # Simple resampling-based pitch shift
    factor = 2 ** (semitones / 12)

    if len(vocal.shape) == 2:
        harmony = np.zeros_like(vocal)
        for ch in range(2):
            # Create indices and padded source
            source = vocal[:, ch]
            padded_length = int(len(source) * factor) + len(source)
            padded = np.pad(
                source, (0, padded_length - len(source)), mode='edge')

            # Create indices for resampling
            indices = np.arange(len(source)) * factor
            indices = np.clip(indices, 0, len(padded) - 1)

            # Resample
            harmony[:, ch] = np.interp(
                indices,
                np.arange(len(padded)),
                padded
            )
    else:
        padded_length = int(len(vocal) * factor) + len(vocal)
        padded = np.pad(vocal, (0, padded_length - len(vocal)), mode='edge')
        indices = np.arange(len(vocal)) * factor
        indices = np.clip(indices, 0, len(padded) - 1)
        harmony = np.interp(
            indices,
            np.arange(len(padded)),
            padded
        )
    return harmony * 0.4  # Quieter than lead


def apply_wah_effect(audio, center_freq=800, depth=600):
    """Wah-wah effect for guitar solo"""
    modulation = np.sin(2 * np.pi * 1.5 * np.arange(len(audio)) / SAMPLE_RATE)
    freq_modulation = center_freq + depth * modulation

    output = np.copy(audio)
    chunk_size = 512

    for i in range(0, len(audio) - chunk_size, chunk_size):
        freq = freq_modulation[i]
        chunk = audio[i:i +
                      chunk_size] if len(audio.shape) == 1 else audio[i:i +
                                                                      chunk_size, :]
        filtered = apply_eq_band(chunk, freq, 12.0, q=5.0)
        if len(audio.shape) == 2:
            output[i:i + chunk_size, :] = filtered
        else:
            output[i:i + chunk_size] = filtered

    return output


def create_fade(length_samples, fade_type='in'):
    """Create fade curve"""
    t = np.linspace(0, 1, length_samples)
    if fade_type == 'in':
        # Exponential fade in
        return t ** 2
    else:
        # Logarithmic fade out
        return (1 - t) ** 1.5

# ==================== MIDI SYNTHESIS ====================


def synthesize_instrument(note_events, total_samples, instrument_type):
    """Synthesize specific instrument with improved sound"""
    audio_left = np.zeros(total_samples, dtype=np.float32)
    audio_right = np.zeros(total_samples, dtype=np.float32)

    for event in note_events:
        if 'end' not in event or event['end'] <= event['start']:
            continue

        start = event['start']
        end = min(event['end'], total_samples)
        if end <= start or start >= total_samples:
            continue

        duration = (end - start) / SAMPLE_RATE
        t = np.linspace(0, duration, end - start)
        freq = 440 * (2 ** ((event['note'] - 69) / 12))
        velocity_factor = event['velocity'] / 127

        if instrument_type == 'lead_guitar':
            # Heavy distortion with vibrato
            vibrato = 1 + 0.015 * np.sin(2 * np.pi * 5 * t)
            fundamental = np.sin(2 * np.pi * freq * vibrato * t)
            wave = np.tanh(fundamental * 4) * 0.6  # Heavy distortion
            wave += np.sin(2 * np.pi * freq * 2 * vibrato * t) * 0.2
            wave += np.sin(2 * np.pi * freq * 3 * vibrato * t) * 0.1
            pan = 0.65  # Slightly right

        elif instrument_type == 'rhythm_guitar':
            # Rhythm guitar - cleaner, chordal
            wave = np.sin(2 * np.pi * freq * t) * 0.6
            wave += np.sin(2 * np.pi * freq * 2 * t) * 0.2
            wave = np.tanh(wave * 1.2) * 0.5  # Light distortion
            pan = 0.35  # Slightly left

        elif instrument_type == 'piano':
            # Piano with hammer attack
            wave = np.sin(2 * np.pi * freq * t) * 0.7
            wave += np.sin(2 * np.pi * freq * 2 * t) * 0.2
            wave += np.sin(2 * np.pi * freq * 3 * t) * 0.1
            wave = wave * 0.5
            pan = 0.6  # Slightly right

        elif instrument_type == 'harmonica':
            # Harmonica - reedy, bright
            wave = (np.sin(2 * np.pi * freq * t) * 0.6 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.3 +
                    np.sin(2 * np.pi * freq * 5 * t) * 0.2)
            wave = wave * 0.4
            pan = 0.55  # Slightly right

        elif instrument_type == 'sax_tenor':
            # Tenor Saxophone - rich, warm
            wave = (np.sin(2 * np.pi * freq * t) * 0.7 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.4 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.3 +
                    np.sin(2 * np.pi * freq * 4 * t) * 0.2)
            wave = np.tanh(wave * 1.3) * 0.5
            pan = 0.45  # Slightly left

        elif instrument_type == 'sax_bari':
            # Baritone Sax - deep, powerful
            wave = (np.sin(2 * np.pi * freq * t) * 0.8 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.5 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.3)
            wave = np.tanh(wave * 1.5) * 0.6
            pan = 0.35  # Left

        elif instrument_type == 'trumpet':
            # Trumpet - bright, cutting
            wave = (np.sin(2 * np.pi * freq * t) * 0.6 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.5 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.4 +
                    np.sin(2 * np.pi * freq * 4 * t) * 0.3 +
                    np.sin(2 * np.pi * freq * 5 * t) * 0.2)
            wave = np.tanh(wave * 1.4) * 0.55
            pan = 0.65  # Right

        elif instrument_type == 'trumpet_1':
            # High trumpet - very bright
            wave = (np.sin(2 * np.pi * freq * t) * 0.6 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.5 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.4 +
                    np.sin(2 * np.pi * freq * 4 * t) * 0.35 +
                    np.sin(2 * np.pi * freq * 5 * t) * 0.25)
            wave = np.tanh(wave * 1.5) * 0.6
            pan = 0.7  # Right

        elif instrument_type == 'trumpet_2':
            # Mid trumpet
            wave = (np.sin(2 * np.pi * freq * t) * 0.65 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.45 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.35 +
                    np.sin(2 * np.pi * freq * 4 * t) * 0.25)
            wave = np.tanh(wave * 1.3) * 0.55
            pan = 0.6  # Slightly right

        elif instrument_type == 'trombone':
            # Trombone - smooth, mid-range
            wave = (np.sin(2 * np.pi * freq * t) * 0.75 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.4 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.25)
            wave = np.tanh(wave * 1.2) * 0.5
            pan = 0.55  # Slightly right

        elif instrument_type == 'brass_section':
            # Full brass section - massive sound
            wave = (np.sin(2 * np.pi * freq * t) * 0.8 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.6 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.4 +
                    np.sin(2 * np.pi * freq * 4 * t) * 0.3)
            wave = np.tanh(wave * 1.6) * 0.7
            pan = 0.5  # Center for big hits

        elif instrument_type == 'electric_piano':
            # Rhodes-style electric piano
            wave = (np.sin(2 * np.pi * freq * t) * 0.6 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.3 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.15)
            # Add FM-like bell tone
            mod = np.sin(2 * np.pi * freq * 4.1 * t)
            wave = np.sin(2 * np.pi * freq * t + mod * 0.5) * 0.5
            pan = 0.4  # Slightly left

        elif instrument_type == 'synth_pad':
            # Warm pad with slow attack
            attack = min(duration * 0.3, 0.5)  # Slow attack
            attack_samples = int(attack * SAMPLE_RATE)
            envelope = np.ones(len(t))
            if len(envelope) > attack_samples:
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

            wave = (np.sin(2 * np.pi * freq * t) * 0.5 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.3 +
                    np.sin(2 * np.pi * freq * 1.5 * t) * 0.2)  # Detuned
            wave = wave * envelope * 0.3
            pan = 0.5  # Center

        elif instrument_type == 'conga_bongo':
            # Latin percussion
            if event['note'] in [64, 65]:  # Congas
                wave = np.sin(2 * np.pi * 200 * t * np.exp(-10 * t)) * 0.7
                wave += np.random.randn(len(t)) * 0.2 * np.exp(-15 * t)
                pan = 0.6 if event['note'] == 64 else 0.4
            else:  # Bongos
                wave = np.sin(2 * np.pi * 300 * t * np.exp(-12 * t)) * 0.6
                wave += np.random.randn(len(t)) * 0.2 * np.exp(-18 * t)
                pan = 0.55

        elif instrument_type == 'percussion':
            # Shaker and tambourine
            wave = np.random.randn(len(t)) * 0.3 * np.exp(-8 * t)
            # High-pass filter for bright sound
            sos = signal.butter(4, 4000, 'highpass',
                                fs=SAMPLE_RATE, output='sos')
            wave = signal.sosfilt(sos, wave)
            pan = 0.5 + np.random.uniform(-0.2, 0.2)

        elif instrument_type == 'sax':  # Legacy support
            wave = (np.sin(2 * np.pi * freq * t) * 0.7 +
                    np.sin(2 * np.pi * freq * 2 * t) * 0.4 +
                    np.sin(2 * np.pi * freq * 3 * t) * 0.3 +
                    np.sin(2 * np.pi * freq * 4 * t) * 0.2)
            wave = np.tanh(wave * 1.3) * 0.5
            pan = 0.45

        elif instrument_type == 'bass':
            # Fat bass with sub harmonic
            wave = np.sin(2 * np.pi * freq * t) * 0.7
            wave += np.sin(2 * np.pi * freq * 0.5 * t) * 0.3  # Sub octave
            wave = np.tanh(wave * 1.8) * 0.8
            pan = 0.5  # Center

        elif instrument_type == 'organ':
            # Hammond drawbar simulation with Leslie
            leslie_rate = 6.0  # Hz
            leslie_depth = 0.3
            leslie_mod = 1 + leslie_depth * np.sin(2 * np.pi * leslie_rate * t)

            # Drawbar harmonics: 16' 8' 4' 2'
            wave = (np.sin(2 * np.pi * freq * 0.5 * t) * 0.4 +  # 16'
                    np.sin(2 * np.pi * freq * t) * 0.8 +          # 8'
                    np.sin(2 * np.pi * freq * 2 * t) * 0.4 +      # 4'
                    np.sin(2 * np.pi * freq * 4 * t) * 0.2)       # 2'
            wave = wave * leslie_mod * 0.4
            pan = 0.35  # Slightly left

        elif instrument_type == 'drums':
            # Improved drum synthesis
            if event['note'] in [36, 35]:  # Kick
                wave = np.sin(2 * np.pi * 60 * t * np.exp(-8 * t)) * 0.9
                wave += np.random.randn(len(t)) * 0.1 * np.exp(-15 * t)
            elif event['note'] in [38, 40]:  # Snare
                wave = np.random.randn(len(t)) * 0.7 * np.exp(-12 * t)
                wave += np.sin(2 * np.pi * 200 * t) * 0.3 * np.exp(-10 * t)
            elif event['note'] in [42, 44, 46]:  # Hi-hat
                wave = np.random.randn(len(t)) * 0.4 * np.exp(-20 * t)
                sos = signal.butter(4, 6000, 'highpass',
                                    fs=SAMPLE_RATE, output='sos')
                wave = signal.sosfilt(sos, wave)
            else:  # Other percussion
                wave = np.random.randn(len(t)) * 0.5 * np.exp(-10 * t)
            pan = 0.5 + np.random.uniform(-0.3, 0.3)

        else:
            wave = np.sin(2 * np.pi * freq * t) * 0.5
            pan = 0.5

        # Enhanced ADSR envelope
        attack = int(0.008 * SAMPLE_RATE)
        decay = int(0.04 * SAMPLE_RATE)
        sustain_level = 0.7
        release = int(0.12 * SAMPLE_RATE)

        envelope = np.ones(len(wave))
        if len(wave) > attack:
            envelope[:attack] = np.linspace(0, 1, attack) ** 0.5
        if len(wave) > attack + decay:
            envelope[attack:attack +
                     decay] = np.linspace(1, sustain_level, decay)
        if len(wave) > release:
            envelope[-release:] = np.linspace(sustain_level, 0, release) ** 0.5

        wave = wave * envelope * velocity_factor

        # Stereo placement
        left_gain = np.sqrt(1 - pan)
        right_gain = np.sqrt(pan)

        audio_left[start:end] += wave * left_gain
        audio_right[start:end] += wave * right_gain

    return np.column_stack([audio_left, audio_right])


def synthesize_midi_pro(midi_file, total_samples):
    """Synthesize MIDI with professional instrument modeling"""
    print("🎹 Synthesizing MIDI with professional instrument models...")

    # Use full path if relative path given
    if not os.path.isabs(midi_file):
        midi_file = OUTPUT_DIR / midi_file

    mid = mido.MidiFile(midi_file)
    tempo = 60_000_000 // BPM

    # Collect note events per instrument - JAMES BROWN FUNK STYLE!
    instruments = {
        0: {'events': [], 'name': 'rhythm_guitar'},  # Chicken scratch
        1: {'events': [], 'name': 'lead_guitar'},    # Funky licks
        2: {'events': [], 'name': 'bass'},           # Syncopated funk
        3: {'events': [], 'name': 'organ'},          # Stabs
        4: {'events': [], 'name': 'trumpet_1'},      # High brass
        5: {'events': [], 'name': 'trumpet_2'},      # Mid brass
        6: {'events': [], 'name': 'sax_tenor'},      # Lead horn
        7: {'events': [], 'name': 'sax_bari'},       # Low horn
        8: {'events': [], 'name': 'trombone'},       # Mid horn
        9: {'events': [], 'name': 'drums'},          # Funk groove
        10: {'events': [], 'name': 'percussion'},    # Congas, cowbell
        11: {'events': [], 'name': 'piano'}          # Stabs
    }

    for track in mid.tracks:
        time_s = 0
        active_notes = {}

        for msg in track:
            if msg.time > 0:
                time_s += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)

            if msg.type == 'note_on' and msg.velocity > 0:
                key = (msg.channel, msg.note)
                active_notes[key] = {
                    'start': int(time_s * SAMPLE_RATE),
                    'channel': msg.channel,
                    'note': msg.note,
                    'velocity': msg.velocity
                }
            elif msg.type in ['note_off', 'note_on']:
                key = (msg.channel, msg.note)
                if key in active_notes:
                    event = active_notes[key]
                    event['end'] = int(time_s * SAMPLE_RATE)
                    if msg.channel in instruments:
                        instruments[msg.channel]['events'].append(event)
                    del active_notes[key]

    # Synthesize each instrument separately
    tracks = {}
    for channel, inst_data in instruments.items():
        print(f"   🎵 {inst_data['name']}: {len(inst_data['events'])} notes")
        tracks[inst_data['name']] = synthesize_instrument(
            inst_data['events'], total_samples, inst_data['name']
        )

    # Mix instruments - JAMES BROWN FUNK STYLE!
    backing = np.zeros((total_samples, 2), dtype=np.float32)

    # Foundation - Bass and drums LOUD (funk is all about the pocket!)
    backing += tracks['bass'] * 1.2         # Fat funk bass
    backing += tracks['drums'] * 1.0        # Heavy drums

    # Rhythm - Chicken scratch guitar is KEY
    backing += tracks['rhythm_guitar'] * 0.9  # Prominent chicken scratch

    # Lead guitar - funky licks
    backing += tracks['lead_guitar'] * 0.75

    # Horns - tight and punchy
    backing += tracks['trumpet_1'] * 0.8
    backing += tracks['trumpet_2'] * 0.75
    backing += tracks['sax_tenor'] * 0.8
    backing += tracks['sax_bari'] * 0.7
    backing += tracks['trombone'] * 0.7

    # Keys - short stabs
    backing += tracks['organ'] * 0.6
    backing += tracks['piano'] * 0.6

    # Percussion - cowbell and congas
    backing += tracks['percussion'] * 0.5

    # Apply effects to guitar solo section
    solo_start = bars_to_samples(STRUCTURE['guitar_solo'])
    solo_end = bars_to_samples(STRUCTURE['final_chorus'])
    print(f"   🎸 Enhancing guitar solo section...")
    solo_section = backing[solo_start:solo_end].copy()
    solo_section = apply_wah_effect(solo_section) * 1.3  # Boost + wah
    backing[solo_start:solo_end] = solo_section

    # Normalize
    max_val = np.abs(backing).max()
    if max_val > 0:
        backing = backing / max_val * 0.65

    print(f"   ✅ Synthesized {total_samples/SAMPLE_RATE:.1f}s backing track")
    return backing

# ==================== MAIN MIXING ====================


def load_vocal(filepath):
    """Load vocal WAV file"""
    rate, data = wavfile.read(str(filepath))
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    if len(data.shape) == 1:
        data = np.column_stack([data, data])
    return data


def create_masterpiece():
    """Create the legendary masterpiece with all enhancements"""
    print("=" * 70)
    print("  🔥 LEGENDARY MASTERPIECE - PROFESSIONAL PRODUCTION 🔥")
    print("=" * 70)
    print()

    total_bars = 108
    total_samples = bars_to_samples(total_bars)
    duration_s = total_samples / SAMPLE_RATE

    print(
        f"📊 Duration: {total_bars} bars = {duration_s:.1f}s ({duration_s/60:.1f} min)")
    print(f"   Sample rate: {SAMPLE_RATE} Hz, BPM: {BPM}")
    print()

    # Synthesize backing track with pro instruments
    backing = synthesize_midi_pro(MIDI_FILE, total_samples)

    print()
    print("🎤 Processing vocals with effects...")
    vocal_track = np.zeros((total_samples, 2), dtype=np.float32)

    for section, vocal_file in VOCAL_MAPPING.items():
        vocal_path = OUTPUT_DIR / vocal_file
        if not vocal_path.exists():
            continue

        vocal_data = load_vocal(vocal_path)
        start_pos = bars_to_samples(STRUCTURE[section])

        # Add vocal harmonies to choruses
        if 'chorus' in section:
            print(f"   🎵 {section}: Adding harmonies...")
            harmony_3rd = create_vocal_harmony(vocal_data, 4)  # Major 3rd
            harmony_5th = create_vocal_harmony(vocal_data, 7)  # Perfect 5th
            vocal_data = vocal_data + harmony_3rd * 0.5 + harmony_5th * 0.3
        else:
            print(f"   ✅ {section}")

        # Apply reverb and delay
        vocal_data = apply_reverb(vocal_data, wet_level=0.3, room_size=0.5)
        vocal_data = apply_delay(vocal_data, delay_time=0.375, wet_level=0.15)

        # Place in track
        end_pos = start_pos + len(vocal_data)
        if end_pos > total_samples:
            vocal_data = vocal_data[:total_samples - start_pos]
            end_pos = total_samples

        vocal_track[start_pos:end_pos] = vocal_data

    print()
    print("🎚️  Mixing and mastering...")

    # Dynamic volume automation
    automation = np.ones(total_samples)
    # Intro build
    intro_end = bars_to_samples(STRUCTURE['verse_1'])
    automation[:intro_end] = np.linspace(0.7, 1.0, intro_end)
    # Solo boost
    solo_start = bars_to_samples(STRUCTURE['guitar_solo'])
    solo_end = bars_to_samples(STRUCTURE['final_chorus'])
    automation[solo_start:solo_end] *= 1.15
    # Final chorus climax
    climax_start = bars_to_samples(STRUCTURE['final_chorus'])
    climax_end = bars_to_samples(STRUCTURE['outro'])
    automation[climax_start:climax_end] *= 1.2
    # Outro fade
    outro_start = bars_to_samples(STRUCTURE['outro'])
    fade_out = create_fade(total_samples - outro_start, 'out')
    automation[outro_start:] *= fade_out

    automation_stereo = np.column_stack([automation, automation])

    # Mix with automation
    mixed = (vocal_track * 2.0 + backing * 0.8) * automation_stereo

    # Multiband compression
    print("   🎛️  Multiband compression...")
    mixed = multiband_compress(mixed)

    # Master EQ
    print("   🎚️  Mastering EQ...")
    mixed = master_eq(mixed)

    # Final limiting
    mixed = compress_audio(mixed, threshold=0.65, ratio=6.0)

    # Normalize to -1dB
    max_val = np.abs(mixed).max()
    if max_val > 0:
        mixed = mixed / max_val * 0.89

    print("   ✅ Mastering complete!")
    print()

    # Save main version - JAMES BROWN FUNK!
    output_file = OUTPUT_DIR / "LIBERTY_BLUES_JB_FUNK.wav"
    print(f"💾 Saving: {output_file}")
    wavfile.write(str(output_file), SAMPLE_RATE,
                  (mixed * 32767).astype(np.int16))

    # Save alternative versions
    print()
    print("🎵 Creating alternative versions...")

    # Instrumental only
    inst_file = OUTPUT_DIR / "LEGENDARY_MASTERPIECE_instrumental.wav"
    inst_mix = backing * automation_stereo * 1.2
    inst_mix = master_eq(multiband_compress(inst_mix))
    wavfile.write(str(inst_file), SAMPLE_RATE,
                  (inst_mix * 32767).astype(np.int16))
    print(f"   🎸 Instrumental: {inst_file}")

    # Vocals only
    vox_file = OUTPUT_DIR / "LEGENDARY_MASTERPIECE_vocals.wav"
    vox_mix = vocal_track * 1.5
    wavfile.write(str(vox_file), SAMPLE_RATE,
                  (vox_mix * 32767).astype(np.int16))
    print(f"   🎤 Vocals: {vox_file}")

    print()
    print("=" * 70)
    print("🎉 MASTERPIECE COMPLETE!")
    print("=" * 70)
    print()
    print(f"🎵 Main: {output_file}")
    print(
        f"📊 Duration: {duration_s:.1f}s, Size: {output_file.stat().st_size/1024/1024:.1f}MB")
    print()
    print("✨ ENHANCEMENTS APPLIED:")
    print("   ✅ Reverb and delay on vocals")
    print("   ✅ Vocal harmonies on choruses (3rd + 5th)")
    print("   ✅ Enhanced guitar distortion + Leslie organ")
    print("   ✅ Wah-wah effect on guitar solo")
    print("   ✅ Dynamic volume automation")
    print("   ✅ Multiband compression (3 bands)")
    print("   ✅ Professional mastering EQ")
    print("   ✅ Fade-in intro / Fade-out outro")
    print("   ✅ Instrumental + vocal versions")
    print()
    print("🚀 Generated 100% by AI on your RTX 3080!")
    print()

    return output_file


if __name__ == "__main__":
    try:
        output = create_masterpiece()
        print(f"🔊 Playing masterpiece...")
        os.system(
            f'powershell -c "(New-Object Media.SoundPlayer \"{output}\").PlaySync()"')
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
