#!/usr/bin/env python3
"""Master script: Mix all layers and combine with video."""

import numpy as np
from scipy.io import wavfile
from pathlib import Path
import subprocess

# Generate all layers
print("Generating soundtrack layers...")
subprocess.run(['python3', 'generate_bass_layer.py'], check=True)
subprocess.run(['python3', 'generate_melody_layer.py'], check=True)
subprocess.run(['python3', 'generate_atmosphere_layer.py'], check=True)
subprocess.run(['python3', 'generate_effects_layer.py'], check=True)

print("\nMixing layers...")

# Load all layers
sr1, bass = wavfile.read('bass_layer.wav')
sr2, melody = wavfile.read('melody_layer.wav')
sr3, atmosphere = wavfile.read('atmosphere_layer.wav')
sr4, effects = wavfile.read('effects_layer.wav')

# Convert to float
bass = bass.astype(np.float32) / 32767
melody = melody.astype(np.float32) / 32767
atmosphere = atmosphere.astype(np.float32) / 32767
effects = effects.astype(np.float32) / 32767

# Mix with careful levels (4 layers now!)
mixed = (
    0.40 * bass +           # Strong bass presence
    0.30 * melody +         # Melodic elements
    0.35 * atmosphere +     # Atmospheric layer
    0.45 * effects          # Sound effects (most prominent)
)

# Master compression/limiting to prevent clipping
mixed = mixed / np.max(np.abs(mixed)) * 0.88

# Apply master fade for looping
fade_samples = int(2.0 * sr1)
fade_in = (np.linspace(0, 1, fade_samples)) ** 2
fade_out = (np.linspace(1, 0, fade_samples)) ** 2
mixed[:fade_samples] *= fade_in
mixed[-fade_samples:] *= fade_out

# Save mixed soundtrack
mixed_int16 = (mixed * 32767).astype(np.int16)
wavfile.write('spooky-soundtrack-final.wav', sr1, mixed_int16)

size_mb = Path('spooky-soundtrack-final.wav').stat().st_size / 1024 / 1024
print(f"✓ Mixed soundtrack: {size_mb:.1f} MB")

# Combine with video
print("\nCombining with video...")
video_input = Path.home() / "Desktop" / "halloween-policyengine-silent-looped.mp4"
video_output = Path.home() / "Desktop" / "halloween-policyengine-final.mp4"

ffmpeg_cmd = [
    'ffmpeg', '-y',
    '-i', str(video_input),
    '-i', 'spooky-soundtrack-final.wav',
    '-c:v', 'copy',
    '-c:a', 'aac',
    '-b:a', '320k',  # High quality audio
    '-shortest',
    str(video_output)
]

result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
if result.returncode == 0:
    size_mb = video_output.stat().st_size / 1024 / 1024
    print(f"✓ Final video: {video_output}")
    print(f"✓ File size: {size_mb:.1f} MB")
    print("\n✓ Opening video...")
    subprocess.run(['open', '-a', 'QuickTime Player', str(video_output)])
    print("\n🎃 Done! Listen with headphones for full spooky effect! 👻")
else:
    print(f"Error: {result.stderr}")

# Cleanup intermediate files
print("\nCleaning up intermediate files...")
for f in ['bass_layer.wav', 'melody_layer.wav', 'atmosphere_layer.wav', 'effects_layer.wav']:
    Path(f).unlink(missing_ok=True)
print("✓ Cleanup complete")
