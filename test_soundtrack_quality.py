#!/usr/bin/env python3
"""
Test-driven development for music composition.
Define what makes a good spooky soundtrack, then test if we meet those criteria.
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fft import fft, fftfreq
import json

class SoundtrackAnalyzer:
    def __init__(self, audio_file):
        self.sr, self.audio = wavfile.read(audio_file)
        if len(self.audio.shape) > 1:
            self.audio = self.audio[:, 0]  # Convert to mono if stereo
        self.audio = self.audio.astype(np.float32) / 32767
        self.duration = len(self.audio) / self.sr

    def test_frequency_coverage(self):
        """Test: Should have presence across sub-bass, bass, mid, and high ranges."""
        fft_data = np.abs(fft(self.audio))
        freqs = fftfreq(len(self.audio), 1/self.sr)

        # Define frequency bands
        bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250),
            'low_mid': (250, 500),
            'mid': (500, 2000),
            'high_mid': (2000, 6000),
            'high': (6000, 12000)
        }

        results = {}
        for band_name, (low, high) in bands.items():
            mask = (np.abs(freqs) >= low) & (np.abs(freqs) <= high)
            energy = np.sum(fft_data[mask])
            results[band_name] = float(energy)

        total_energy = sum(results.values())
        percentages = {k: v/total_energy * 100 for k, v in results.items()}

        # Requirements for spooky soundtrack
        checks = {
            'has_sub_bass': percentages['sub_bass'] > 15,  # Strong sub presence
            'has_bass': percentages['bass'] > 20,
            'has_mids': percentages['mid'] > 10,
            'has_highs': percentages['high_mid'] > 5,  # Some shimmer
            'not_too_mid_heavy': percentages['mid'] < 40  # Avoid muddy
        }

        return {
            'test': 'frequency_coverage',
            'passed': all(checks.values()),
            'details': percentages,
            'checks': checks
        }

    def test_dynamic_range(self):
        """Test: Should have variation - not too flat, not too compressed."""
        rms = np.sqrt(np.mean(self.audio ** 2))
        peak = np.max(np.abs(self.audio))
        crest_factor = peak / rms if rms > 0 else 0

        # Good dynamic range for cinematic audio: 4-12 dB
        crest_db = 20 * np.log10(crest_factor) if crest_factor > 0 else 0

        checks = {
            'has_dynamics': crest_db > 4,  # Not too flat/compressed
            'not_over_dynamic': crest_db < 15,  # Not too sparse
            'adequate_volume': rms > 0.1  # Loud enough
        }

        return {
            'test': 'dynamic_range',
            'passed': all(checks.values()),
            'details': {
                'crest_factor_db': float(crest_db),
                'rms_level': float(rms),
                'peak_level': float(peak)
            },
            'checks': checks
        }

    def test_activity_distribution(self):
        """Test: Should have consistent activity, not too much silence."""
        # Segment into 0.5s windows
        window_size = int(0.5 * self.sr)
        num_windows = len(self.audio) // window_size

        active_windows = 0
        window_energies = []

        for i in range(num_windows):
            window = self.audio[i*window_size:(i+1)*window_size]
            energy = np.sum(window ** 2)
            window_energies.append(energy)
            if energy > 0.001:  # Threshold for "active"
                active_windows += 1

        activity_ratio = active_windows / num_windows if num_windows > 0 else 0
        energy_std = np.std(window_energies)

        checks = {
            'mostly_active': activity_ratio > 0.85,  # 85%+ should have sound
            'has_variation': energy_std > 0.01  # Not monotonous
        }

        return {
            'test': 'activity_distribution',
            'passed': all(checks.values()),
            'details': {
                'activity_ratio': float(activity_ratio),
                'energy_variation': float(energy_std)
            },
            'checks': checks
        }

    def test_spectral_variety(self):
        """Test: Should have changing timbre over time (not static)."""
        # Analyze spectral centroid over time
        window_size = int(0.5 * self.sr)
        hop_size = window_size // 2
        num_windows = (len(self.audio) - window_size) // hop_size

        centroids = []
        for i in range(num_windows):
            start = i * hop_size
            window = self.audio[start:start + window_size]

            # Compute spectral centroid
            fft_data = np.abs(fft(window))
            freqs = fftfreq(len(window), 1/self.sr)
            freqs = np.abs(freqs[:len(freqs)//2])
            magnitudes = fft_data[:len(fft_data)//2]

            if np.sum(magnitudes) > 0:
                centroid = np.sum(freqs * magnitudes) / np.sum(magnitudes)
                centroids.append(centroid)

        centroid_std = np.std(centroids) if centroids else 0

        checks = {
            'has_timbral_variety': centroid_std > 200  # Spectrum changes over time
        }

        return {
            'test': 'spectral_variety',
            'passed': all(checks.values()),
            'details': {
                'spectral_centroid_std': float(centroid_std),
                'min_centroid': float(min(centroids)) if centroids else 0,
                'max_centroid': float(max(centroids)) if centroids else 0
            },
            'checks': checks
        }

    def test_pacing(self):
        """Test: Should have events distributed throughout, not clustered."""
        # Detect transients (sudden energy increases)
        window_size = int(0.1 * self.sr)
        hop_size = window_size // 2
        num_windows = (len(self.audio) - window_size) // hop_size

        energies = []
        for i in range(num_windows):
            start = i * hop_size
            window = self.audio[start:start + window_size]
            energy = np.sum(window ** 2)
            energies.append(energy)

        # Find peaks (events)
        energies = np.array(energies)
        threshold = np.mean(energies) + 1.5 * np.std(energies)
        peaks = energies > threshold
        event_count = np.sum(peaks)

        # Check distribution across timeline
        thirds = len(energies) // 3
        events_per_third = [
            np.sum(peaks[:thirds]),
            np.sum(peaks[thirds:2*thirds]),
            np.sum(peaks[2*thirds:])
        ]

        # All thirds should have some events
        well_distributed = all(count > 0 for count in events_per_third)

        checks = {
            'has_events': event_count > 5,  # Multiple events
            'well_distributed': well_distributed
        }

        return {
            'test': 'pacing',
            'passed': all(checks.values()),
            'details': {
                'total_events': int(event_count),
                'events_per_third': [int(x) for x in events_per_third]
            },
            'checks': checks
        }

    def run_all_tests(self):
        """Run all quality tests and generate report."""
        tests = [
            self.test_frequency_coverage(),
            self.test_dynamic_range(),
            self.test_activity_distribution(),
            self.test_spectral_variety(),
            self.test_pacing()
        ]

        all_passed = all(t['passed'] for t in tests)

        return {
            'overall': 'PASS' if all_passed else 'FAIL',
            'score': f"{sum(t['passed'] for t in tests)}/{len(tests)}",
            'tests': tests
        }


def generate_review(results):
    """Generate human-readable review with suggestions."""
    print("\n" + "="*60)
    print("🎃 SPOOKY SOUNDTRACK QUALITY REPORT 👻")
    print("="*60)
    print(f"\nOverall Score: {results['score']} tests passed")
    print(f"Status: {results['overall']}\n")

    for test in results['tests']:
        status = "✓" if test['passed'] else "✗"
        print(f"{status} {test['test'].upper()}")

        for check_name, passed in test['checks'].items():
            check_status = "  ✓" if passed else "  ✗"
            print(f"{check_status} {check_name}")

        if test['details']:
            print(f"  Details: {test['details']}")
        print()

    # Generate improvement suggestions
    print("="*60)
    print("IMPROVEMENT SUGGESTIONS:")
    print("="*60)

    suggestions = []
    for test in results['tests']:
        if not test['passed']:
            if test['test'] == 'frequency_coverage':
                if not test['checks'].get('has_sub_bass'):
                    suggestions.append("- Add more sub-bass content (20-60Hz) for visceral impact")
                if not test['checks'].get('has_highs'):
                    suggestions.append("- Add high-frequency shimmer or effects for airiness")

            if test['test'] == 'dynamic_range':
                if not test['checks'].get('has_dynamics'):
                    suggestions.append("- Increase dynamic variation - add quieter and louder moments")

            if test['test'] == 'spectral_variety':
                suggestions.append("- Add more timbral changes over time - vary the sound palette")

            if test['test'] == 'pacing':
                suggestions.append("- Distribute events more evenly throughout the timeline")

    if not suggestions:
        print("✓ No improvements needed - soundtrack meets all quality criteria!")
    else:
        for suggestion in suggestions:
            print(suggestion)

    print("\n" + "="*60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python test_soundtrack_quality.py <audio_file.wav>")
        sys.exit(1)

    analyzer = SoundtrackAnalyzer(sys.argv[1])
    results = analyzer.run_all_tests()
    generate_review(results)

    # Save JSON report
    with open('soundtrack_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\n✓ Detailed analysis saved to soundtrack_analysis.json")
