#!/usr/bin/env python3
"""Layer 1: Deep bass, drones, and rumbles."""

import numpy as np
from scipy.io import wavfile

def generate_bass_layer(duration=12, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)

    # Sub-bass drone (30-55Hz range - you FEEL this)
    # Much more sub-bass content for visceral impact
    bass1 = 0.35 * np.sin(2 * np.pi * 35 * t)  # Even lower
    bass2 = 0.32 * np.sin(2 * np.pi * 42 * t)
    bass3 = 0.28 * np.sin(2 * np.pi * 48 * t)
    bass4 = 0.25 * np.sin(2 * np.pi * 54 * t)
    # Slow modulation for "breathing"
    mod = 0.75 + 0.25 * np.sin(2 * np.pi * 0.12 * t)
    audio += (bass1 + bass2 + bass3 + bass4) * mod

    # Additional deep rumbling layer (25-40 Hz)
    deep_rumble = (
        0.25 * np.sin(2 * np.pi * 28 * t) +
        0.20 * np.sin(2 * np.pi * 32 * t)
    )
    # Slow swell
    rumble_mod = 0.6 + 0.4 * np.sin(2 * np.pi * 0.08 * t)
    audio += deep_rumble * rumble_mod

    # Thunder rumbles (3 throughout)
    for rumble_time in [2.5, 7.0, 10.5]:
        start = int(rumble_time * sample_rate)
        dur = int(1.5 * sample_rate)
        if start + dur < len(audio):
            rumble_t = np.linspace(0, 1.5, dur)
            # Complex low frequency mix
            rumble = (
                0.4 * np.sin(2 * np.pi * 30 * rumble_t) +
                0.3 * np.sin(2 * np.pi * 38 * rumble_t) +
                0.25 * np.sin(2 * np.pi * 45 * rumble_t)
            )
            # Add noise for texture
            rumble += 0.15 * np.random.randn(len(rumble_t))
            # Envelope: builds then fades
            env = np.exp(-((rumble_t - 0.6) ** 2) / 0.4)
            audio[start:start + dur] += rumble * env * 0.6

    return audio

if __name__ == "__main__":
    audio = generate_bass_layer()
    wavfile.write('bass_layer.wav', 44100, (audio / np.max(np.abs(audio)) * 0.8 * 32767).astype(np.int16))
    print("✓ Bass layer created")
