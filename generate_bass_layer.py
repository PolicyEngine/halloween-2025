#!/usr/bin/env python3
"""Layer 1: Deep bass, drones, and rumbles."""

import numpy as np
from scipy.io import wavfile

def generate_bass_layer(duration=12, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)

    # Sub-bass drone (40-55Hz range - you feel this)
    bass1 = 0.25 * np.sin(2 * np.pi * 42 * t)
    bass2 = 0.20 * np.sin(2 * np.pi * 54 * t)
    bass3 = 0.15 * np.sin(2 * np.pi * 48 * t)
    # Slow modulation for "breathing"
    mod = 0.7 + 0.3 * np.sin(2 * np.pi * 0.12 * t)
    audio += (bass1 + bass2 + bass3) * mod

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
