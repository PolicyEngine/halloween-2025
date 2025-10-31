#!/usr/bin/env python3
"""Layer 1: PURE LOW-END POWER - Nothing above 250Hz."""

import numpy as np
from scipy.io import wavfile

def generate_bass_layer(duration=12, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)

    # ===== SUB-BASS SECTION (20-60Hz) - ABSOLUTE MAXIMUM POWER =====
    # Use EVEN HIGHER amplitudes - 12 sine waves
    sub_freqs = [20, 23, 26, 29, 32, 35, 38, 42, 46, 50, 54, 58]
    for i, freq in enumerate(sub_freqs):
        amp = 1.1 - (i * 0.04)  # EXTRA loud, slower falloff
        audio += amp * np.sin(2 * np.pi * freq * t)

    # Stronger modulation
    sub_mod = 0.9 + 0.1 * np.sin(2 * np.pi * 0.11 * t)
    audio *= sub_mod

    # ===== BASS SECTION (60-250Hz) - ABSOLUTE MAXIMUM =====
    # Add MORE frequencies and HIGHER amplitudes
    bass_freqs = [60, 65, 70, 75, 80, 85, 92, 100, 108, 118, 128, 140, 152, 165, 180, 195, 212, 230, 248]
    bass_layer = np.zeros_like(t)
    for i, freq in enumerate(bass_freqs):
        amp = 1.15 - (i * 0.03)  # Even higher, even slower falloff
        bass_layer += amp * np.sin(2 * np.pi * freq * t)

    # Stronger modulation
    bass_mod = 0.88 + 0.12 * np.sin(2 * np.pi * 0.15 * t)
    audio += bass_layer * bass_mod

    # ===== THUNDER RUMBLES - Full low-end spectrum =====
    # Add more rumbles, especially in middle section for pacing
    for rumble_time in [2.0, 4.8, 6.2, 7.6, 9.5, 11.0]:
        start = int(rumble_time * sample_rate)
        dur = int(1.8 * sample_rate)
        if start + dur < len(audio):
            rumble_t = np.linspace(0, 1.8, dur)

            # Massive rumble with BOTH sub-bass and bass
            rumble = np.zeros_like(rumble_t)

            # Sub-bass components
            for freq in [25, 30, 35, 40, 45, 50, 55]:
                rumble += 0.6 * np.sin(2 * np.pi * freq * rumble_t)

            # Bass components
            for freq in [70, 90, 110, 130, 150, 180, 220]:
                rumble += 0.55 * np.sin(2 * np.pi * freq * rumble_t)

            # Heavy noise for texture
            rumble += 0.25 * np.random.randn(len(rumble_t))

            # Envelope
            env = np.exp(-((rumble_t - 0.7) ** 2) / 0.5)
            audio[start:start + dur] += rumble * env * 0.8

    return audio

if __name__ == "__main__":
    audio = generate_bass_layer()
    # Don't normalize down - keep it LOUD
    wavfile.write('bass_layer.wav', 44100, (audio / np.max(np.abs(audio)) * 0.95 * 32767).astype(np.int16))
    print("✓ Bass layer created - PURE LOW-END POWER")
