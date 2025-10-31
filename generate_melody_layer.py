#!/usr/bin/env python3
"""Layer 2: Melodic elements - bells, music box, eerie tones."""

import numpy as np
from scipy.io import wavfile

def bell(t, freq, harmonics=[1, 2, 3, 4.2, 5.8]):
    """Generate a church bell sound with inharmonic partials."""
    sound = np.zeros_like(t)
    for i, h in enumerate(harmonics):
        amp = 1.0 / (i + 1)
        sound += amp * np.sin(2 * np.pi * freq * h * t)
    return sound

def generate_melody_layer(duration=12, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)

    # Church bells - five tolls throughout
    bell_times = [0.5, 3.0, 5.5, 8.0, 10.5]
    bell_freq = 220  # Low A
    for bell_time in bell_times:
        start = int(bell_time * sample_rate)
        dur = int(3.0 * sample_rate)
        if start + dur < len(audio):
            bell_t = np.linspace(0, 3.0, dur)
            bell_sound = bell(bell_t, bell_freq)
            bell_env = np.exp(-bell_t * 1.2)  # Long decay
            audio[start:start + dur] += bell_sound * bell_env * 0.25

    # Eerie music box melody (dissonant minor scale)
    # Play a creepy descending pattern
    notes = [
        (1.5, 523.25),   # C5
        (2.5, 493.88),   # B4
        (4.0, 440.00),   # A4
        (5.0, 415.30),   # G#4 (dissonant)
        (6.5, 392.00),   # G4
        (8.5, 329.63),   # E4
        (10.0, 293.66),  # D4
    ]

    for note_time, freq in notes:
        start = int(note_time * sample_rate)
        dur = int(0.8 * sample_rate)
        if start + dur < len(audio):
            note_t = np.linspace(0, 0.8, dur)
            # Music box has metallic quality - add harmonics
            note_sound = (
                0.5 * np.sin(2 * np.pi * freq * note_t) +
                0.3 * np.sin(2 * np.pi * freq * 2 * note_t) +
                0.2 * np.sin(2 * np.pi * freq * 3 * note_t)
            )
            # Sharp attack, slow decay
            note_env = np.exp(-note_t * 3)
            audio[start:start + dur] += note_sound * note_env * 0.15

    # Ghostly theremin swells
    theremin_times = [(4.0, 5.5), (9.0, 10.5)]
    for start_time, end_time in theremin_times:
        start = int(start_time * sample_rate)
        dur = int((end_time - start_time) * sample_rate)
        if start + dur < len(audio):
            theremin_t = np.linspace(0, end_time - start_time, dur)
            # Frequency sweeps up then down
            sweep_progress = theremin_t / (end_time - start_time)
            freq_sweep = 300 + 200 * np.sin(np.pi * sweep_progress)
            theremin_sound = 0.18 * np.sin(2 * np.pi * freq_sweep * theremin_t)
            # Swell envelope
            theremin_env = np.sin(np.pi * sweep_progress)
            audio[start:start + dur] += theremin_sound * theremin_env

    return audio

if __name__ == "__main__":
    audio = generate_melody_layer()
    wavfile.write('melody_layer.wav', 44100, (audio / np.max(np.abs(audio)) * 0.8 * 32767).astype(np.int16))
    print("✓ Melody layer created")
