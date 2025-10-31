#!/usr/bin/env python3
"""Layer 3: Sound effects - wind, creaks, footsteps, bats, chains."""

import numpy as np
from scipy.io import wavfile
from scipy import signal

def generate_effects_layer(duration=12, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)

    # === WIND (constant atmospheric) ===
    # Multi-layered wind for richness
    wind = np.zeros_like(t)
    # Low frequency wind
    wind += 0.12 * np.sin(2 * np.pi * 120 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * t))
    # Mid frequency wind
    wind += 0.10 * np.sin(2 * np.pi * 450 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.35 * t))
    # High frequency wind
    wind += 0.08 * np.sin(2 * np.pi * 2000 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.45 * t))
    # Filtered noise for wind texture
    wind_noise = 0.06 * np.random.randn(len(t))
    b, a = signal.butter(3, 0.15)
    wind_noise = signal.filtfilt(b, a, wind_noise)
    wind += wind_noise
    audio += wind

    # === CREAKING WOOD ===
    # Add more creaks in middle section
    creak_times = [1.8, 4.2, 5.5, 6.8, 8.0, 9.5, 10.8]
    for creak_time in creak_times:
        start = int(creak_time * sample_rate)
        dur = int(0.9 * sample_rate)
        if start + dur < len(audio):
            creak_t = np.linspace(0, 0.9, dur)
            # Creaking is frequency sweep with noise
            creak_freq = 180 + 100 * np.sin(2 * np.pi * 2.5 * creak_t)
            creak_sound = 0.18 * np.sin(2 * np.pi * creak_freq * creak_t)
            # Add woody noise texture
            creak_noise = 0.12 * np.random.randn(len(creak_t))
            # Envelope
            creak_env = np.sin(np.pi * creak_t / 0.9) * 0.8
            audio[start:start + dur] += (creak_sound + creak_noise) * creak_env

    # === BAT SWOOSHES ===
    # Add more in middle section for better pacing
    bat_times = [2.0, 3.5, 5.2, 6.5, 7.8, 8.5, 10.2, 11.0]
    for bat_time in bat_times:
        start = int(bat_time * sample_rate)
        dur = int(0.25 * sample_rate)
        if start + dur < len(audio):
            bat_t = np.linspace(0, 0.25, dur)
            # Fast descending sweep
            bat_freq = 4000 - 3500 * (bat_t / 0.25) ** 1.5
            bat_env = np.sin(np.pi * bat_t / 0.25) ** 0.5
            bat_sound = 0.15 * np.sin(2 * np.pi * bat_freq * bat_t)
            # Add flutter effect
            flutter = 1 + 0.3 * np.sin(2 * np.pi * 30 * bat_t)
            audio[start:start + dur] += bat_sound * bat_env * flutter

    # === FOOTSTEPS (building tension) ===
    # Slow footsteps getting closer (louder)
    footstep_times = [0.8, 2.2, 3.6, 5.0, 6.4, 7.8, 9.2]
    for i, step_time in enumerate(footstep_times):
        start = int(step_time * sample_rate)
        dur = int(0.08 * sample_rate)
        if start + dur < len(audio):
            step_t = np.linspace(0, 0.08, dur)
            # Deep thud
            step_sound = 0.25 * np.sin(2 * np.pi * 70 * step_t)
            step_env = np.exp(-step_t * 35)
            # Get progressively louder
            step_vol = 0.6 + 0.4 * (i / len(footstep_times))
            audio[start:start + dur] += step_sound * step_env * step_vol

    # === CHAINS RATTLING ===
    # Add one in middle section
    chain_times = [4.8, 7.2, 10.2]
    for chain_time in chain_times:
        start = int(chain_time * sample_rate)
        dur = int(0.7 * sample_rate)
        if start + dur < len(audio):
            chain_t = np.linspace(0, 0.7, dur)
            chain_sound = np.zeros_like(chain_t)
            # Multiple metallic impacts
            for i in range(12):
                impact_pos = int((i / 12) * len(chain_t))
                impact_dur = int(0.03 * sample_rate)
                if impact_pos + impact_dur < len(chain_t):
                    impact_t = np.linspace(0, 0.03, impact_dur)
                    # Metallic frequency
                    impact = 0.18 * np.sin(2 * np.pi * 2200 * impact_t)
                    impact += 0.12 * np.sin(2 * np.pi * 3100 * impact_t)
                    impact *= np.exp(-impact_t * 40)
                    chain_sound[impact_pos:impact_pos + impact_dur] += impact
            audio[start:start + dur] += chain_sound

    # === DISTANT SCREECH/HOWL ===
    howl_time = 8.5
    start = int(howl_time * sample_rate)
    dur = int(1.2 * sample_rate)
    if start + dur < len(audio):
        howl_t = np.linspace(0, 1.2, dur)
        # Rising then falling pitch
        howl_freq = 400 + 200 * np.sin(np.pi * howl_t / 1.2)
        howl_sound = 0.14 * np.sin(2 * np.pi * howl_freq * howl_t)
        howl_env = np.sin(np.pi * howl_t / 1.2) * np.exp(-howl_t * 0.5)
        audio[start:start + dur] += howl_sound * howl_env

    # === BIG IMPACT/CRASH at 6 seconds (middle section) ===
    # This WILL register as an event - loud transient
    crash_time = 6.0
    start = int(crash_time * sample_rate)
    dur = int(0.5 * sample_rate)
    if start + dur < len(audio):
        crash_t = np.linspace(0, 0.5, dur)
        # Metallic crash with noise burst
        crash_sound = 0.6 * np.random.randn(len(crash_t))  # White noise burst
        # Add metallic ringing
        for freq in [1200, 2400, 3600, 4800]:
            crash_sound += 0.3 * np.sin(2 * np.pi * freq * crash_t) * np.exp(-crash_t * 8)
        # Sharp attack, fast decay
        crash_env = np.exp(-crash_t * 6)
        audio[start:start + dur] += crash_sound * crash_env * 0.7

    return audio

if __name__ == "__main__":
    audio = generate_effects_layer()
    wavfile.write('effects_layer.wav', 44100, (audio / np.max(np.abs(audio)) * 0.85 * 32767).astype(np.int16))
    print("✓ Effects layer created")
