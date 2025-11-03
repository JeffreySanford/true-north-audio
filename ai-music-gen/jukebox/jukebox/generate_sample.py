import sys
import os
import torch

# Add the parent jukebox directory to sys.path


# Add the parent and grandparent directories to sys.path so 'jukebox' and its submodules are importable
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
for p in [parent_dir, grandparent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from jukebox.make_models import make_vqvae, make_prior
    from jukebox.hparams import setup_hparams
except ImportError as e:
    print(f"Error: Could not import Jukebox modules. {e}\nCheck repo structure and sys.path.")
    sys.exit(1)

# Set up model paths
vqvae_path = os.path.join(grandparent_dir, "checkpoints", "vqvae.pth.tar")
prior_path = os.path.join(grandparent_dir, "checkpoints", "prior_level_2.pth.tar")


# Set up hyperparameters using the registry
hps = setup_hparams("vqvae", {})

# Load models
print("Loading VQ-VAE...")
vqvae = make_vqvae(hps, device="cpu")
print("Loading Prior...")
prior = make_prior(hps, vqvae, device="cpu")

# Generate sample (this is a minimal example, see Jukebox repo for full lyrics/music prompt usage)
print("Generating sample...")
zs = [None, None, None]
labels = None
sample = prior.sample(n_samples=1, labels=labels, zs=zs, sampling_temperature=0.98)

print("Sample generated. Saving...")
vqvae.decode(sample, "sample_output.wav")
print("Saved to sample_output.wav")
