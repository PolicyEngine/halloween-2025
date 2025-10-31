#!/usr/bin/env python3
"""Layer 4: Atmospheric pads, ghostly choir, eerie ambience."""

import numpy as np
from scipy.io import wavfile

def generate_atmosphere_layer(duration=12, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)

    # === GHOSTLY CHOIR (dissonant sustained chords) ===
    # Three chord progressions throughout
    chord_times = [(0.5, 4.0), (5.0, 8.5), (9.0, 12.0)]
    chords = [
        [220, 261.63, 329.63, 415.30],  # Am add G# (very dissonant)
        [196, 246.94, 311.13, 369.99],  # G minor add F#
        [174.61, 220, 277.18, 329.63],  # F minor add E
    ]

    for (start_time, end_time), chord in zip(chord_times, chords):
        start = int(start_time * sample_rate)
        dur = int((end_time - start_time) * sample_rate)
        if start + dur < len(audio):
            chord_t = np.linspace(0, end_time - start_time, dur)
            chord_sound = np.zeros_like(chord_t)

            for freq in chord:
                # Each voice with slight vibrato
                vibrato = freq * (1 + 0.02 * np.sin(2 * np.pi * 5 * chord_t))
                voice = 0.08 * np.sin(2 * np.pi * vibrato * chord_t)
                chord_sound += voice

            # ADSR envelope for choir
            attack_len = int(0.4 * len(chord_t))
            release_len = int(0.5 * len(chord_t))
            env = np.ones_like(chord_t)
            env[:attack_len] = np.linspace(0, 1, attack_len) ** 1.5
            env[-release_len:] = np.linspace(1, 0, release_len) ** 2

            audio[start:start + dur] += chord_sound * env

    # === AMBIENT PAD (dark sustained tone) ===
    pad_freq = 110  # Low A
    pad = (
        0.12 * np.sin(2 * np.pi * pad_freq * t) +
        0.10 * np.sin(2 * np.pi * pad_freq * 1.5 * t) +
        0.08 * np.sin(2 * np.pi * pad_freq * 2.01 * t)  # Slight detune
    )
    # Slow modulation
    pad_mod = 0.6 + 0.4 * np.sin(2 * np.pi * 0.18 * t)
    audio += pad * pad_mod

    # === ETHEREAL HIGH SHIMMER ===
    shimmer_freq = 1800 + 300 * np.sin(2 * np.pi * 0.4 * t)
    shimmer = 0.06 * np.sin(2 * np.pi * shimmer_freq * t)
    shimmer *= (0.5 + 0.5 * np.sin(2 * np.pi * 0.3 * t))
    audio += shimmer

    return audio

if __name__ == "__main__":
    audio = generate_atmosphere_layer()
    wavfile.write('atmosphere_layer.wav', 44100, (audio / np.max(np.abs(audio)) * 0.85 * 32767).astype(np.int16))
    print("✓ Atmosphere/choir layer created")
