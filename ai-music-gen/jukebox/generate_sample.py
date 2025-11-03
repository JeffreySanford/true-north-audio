
import torch
import numpy as np
import os
import sys
from scipy.io.wavfile import write

# Add the real Jukebox source directory to sys.path
jukebox_src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ai-music-gen/ai-music-gen/jukebox/jukebox'))
jukebox_parent_path = os.path.abspath(os.path.join(jukebox_src_path, '..'))
for p in [jukebox_src_path, jukebox_parent_path]:
    if p not in sys.path:
        sys.path.insert(0, p)
from make_models import make_vqvae, make_prior
from hparams import Hyperparams, setup_hparams

def main():
    # Set up paths
    checkpoint_path = os.path.join(os.path.dirname(__file__), "jukebox", "checkpoints", "vqvae.pth.tar")
    prior_path = os.path.join(os.path.dirname(__file__), "jukebox", "checkpoints", "prior_level_2.pth.tar")
    output_path = os.path.join(os.path.dirname(__file__), "sample.wav")

    # Load hyperparameters
    hps = setup_hparams("vqvae", {})

    # Load models
    vqvae = make_vqvae(hps, checkpoint_path)
    prior = make_prior(hps, prior_path)

    # Generate random latent codes
    codes = torch.randint(0, vqvae.n_codes, (1, hps.n_ctx), dtype=torch.long)

    # Decode to waveform
    waveform = vqvae.decode(codes)
    waveform = waveform.cpu().numpy().squeeze()

    # Normalize and save
    waveform = np.int16(waveform / np.max(np.abs(waveform)) * 32767)
    write(output_path, hps.sr, waveform)

    print(f"Sample saved to {output_path}")

if __name__ == "__main__":
    main()
# Generate sample (this is a minimal example, see Jukebox repo for full lyrics/music prompt usage)
print("Generating sample...")
zs = [None, None, None]
labels = None
sample = prior.sample(n_samples=1, labels=labels, zs=zs, sampling_temperature=0.98)

print("Sample generated. Saving...")
vqvae.decode(sample, "sample_output.wav")
print("Saved to sample_output.wav")
