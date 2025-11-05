def generate_riffusion_sample(genre, duration, seed=None, idea=None, vocal_artist=None, tempo=None, variation=None, songSections=None):
    """
    Generate music with vocals using Riffusion (Stable Diffusion for audio)
    
    Riffusion converts text prompts into spectrograms, then to audio with vocals.
    Much more natural-sounding than Bark TTS for singing.
    
    Requires: pip install riffusion torch diffusers
    """
    try:
        import numpy as np
        from riffusion.spectrogram_params import SpectrogramParams
        from riffusion.spectrogram_image_converter import SpectrogramImageConverter
        from riffusion.riffusion_pipeline import RiffusionPipeline
        import torch
        
        print("[Riffusion] Loading Riffusion model...")
        
        # Load Riffusion pipeline
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipeline = RiffusionPipeline.load_checkpoint(
            checkpoint="riffusion/riffusion-model-v1",
            device=device,
            dtype=torch.float16 if device == "cuda" else torch.float32
        )
        
        print(f"[Riffusion] Using device: {device}")
        
        # Build prompt for music with vocals
        vocal_prompt = ""
        if vocal_artist:
            vocal_prompt = f"with {vocal_artist} style vocals"
        elif variation == "vocal":
            vocal_prompt = "with soulful male vocals singing blues"
        
        prompt = f"{genre} music {vocal_prompt}, {idea or 'emotional and expressive'}"
        if tempo:
            prompt += f", {tempo} BPM"
        
        print(f"[Riffusion] Prompt: {prompt}")
        print(f"[Riffusion] Generating {duration}s audio...")
        
        # Generate spectrogram
        params = SpectrogramParams()
        converter = SpectrogramImageConverter(params=params)
        
        # Generate in chunks (Riffusion works best with ~5-6 second clips)
        chunk_duration = 5.0
        num_chunks = int(np.ceil(duration / chunk_duration))
        
        all_audio = []
        
        for i in range(num_chunks):
            print(f"[Riffusion] Generating chunk {i+1}/{num_chunks}")
            
            # Generate spectrogram image
            result = pipeline(
                prompt=prompt,
                negative_prompt="low quality, distorted, quiet, silent",
                num_inference_steps=50,
                guidance_scale=7.0,
                seed=seed + i if seed else None
            )
            
            # Convert spectrogram to audio
            audio = converter.audio_from_spectrogram_image(
                result.images[0],
                apply_filters=True
            )
            
            all_audio.append(audio)
        
        # Concatenate chunks
        waveform = np.concatenate(all_audio)
        
        # Trim to exact duration
        target_samples = int(duration * params.sample_rate)
        if len(waveform) > target_samples:
            waveform = waveform[:target_samples]
        elif len(waveform) < target_samples:
            waveform = np.pad(waveform, (0, target_samples - len(waveform)))
        
        print(f"[Riffusion] Generated {duration}s with vocals")
        
        return {
            'waveform': waveform.astype(np.float32),
            'sample_rate': params.sample_rate,
            'vocals': f'Riffusion-generated vocals ({prompt})',
            'audio_url': f'/audio/generated/riffusion_{genre}_{seed or "random"}.mp3'
        }
        
    except ImportError as e:
        print(f"[Riffusion] Not available: {e}")
        print("[Riffusion] Install with: pip install riffusion diffusers torch")
        
        # Fallback to placeholder
        import numpy as np
        sample_rate = 22050
        waveform = np.random.uniform(-1, 1, sample_rate * duration).astype(np.float32)
        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'vocals': 'Riffusion not installed (placeholder)',
            'audio_url': '/audio/generated/riffusion_sample.mp3'
        }
    
    except Exception as e:
        print(f"[Riffusion] Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback
        import numpy as np
        sample_rate = 22050
        waveform = np.random.uniform(-1, 1, sample_rate * duration).astype(np.float32)
        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'vocals': f'Riffusion error: {str(e)}',
            'audio_url': '/audio/generated/riffusion_error.mp3'
        }
