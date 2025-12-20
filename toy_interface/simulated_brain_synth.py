#!/usr/bin/env python3
"""
Simulated Brain-Controlled Synthesizer

A proof-of-concept real-time audio synthesizer driven by simulated brain signals.
This demonstrates the basic pipeline: signal → features → mapping → synthesis.

For educational/research purposes only.
"""

import numpy as np
import time
import sys
from collections import deque

try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    print("Warning: PyAudio not available. Install with: pip install pyaudio")
    AUDIO_AVAILABLE = False


class BrainSimulator:
    """Simulates brain signals with varying cognitive states"""
    
    def __init__(self, fs=250):
        self.fs = fs
        self.t = 0
        
    def generate_window(self, duration=0.5):
        """Generate simulated EEG-like data"""
        n_samples = int(duration * self.fs)
        time_vec = self.t + np.arange(n_samples) / self.fs
        
        # Simulate frequency bands with time-varying amplitudes
        # Theta (4-8 Hz) - creativity, meditation
        theta = 15 * np.sin(2 * np.pi * 6 * time_vec)
        theta *= (1 + 0.5 * np.sin(2 * np.pi * 0.1 * time_vec))  # Slow modulation
        
        # Alpha (8-13 Hz) - relaxation
        alpha = 12 * np.sin(2 * np.pi * 10 * time_vec)
        alpha *= (1 + 0.3 * np.cos(2 * np.pi * 0.15 * time_vec))
        
        # Beta (13-30 Hz) - active thinking
        beta = 8 * np.sin(2 * np.pi * 20 * time_vec)
        beta *= (1 + 0.4 * np.sin(2 * np.pi * 0.2 * time_vec))
        
        # Combine with noise
        signal = theta + alpha + beta + 5 * np.random.randn(n_samples)
        
        self.t += duration
        return signal
    
    def extract_features(self, signal):
        """Extract simplified brain features"""
        # Compute power in different bands (simplified)
        fft_vals = np.fft.fft(signal)
        freqs = np.fft.fftfreq(len(signal), 1/self.fs)
        psd = np.abs(fft_vals) ** 2
        
        # Band power (approximate)
        theta_power = np.mean(psd[(freqs >= 4) & (freqs <= 8)])
        alpha_power = np.mean(psd[(freqs >= 8) & (freqs <= 13)])
        beta_power = np.mean(psd[(freqs >= 13) & (freqs <= 30)])
        
        # Derived features
        engagement = beta_power / (theta_power + alpha_power + 1e-10)
        relaxation = alpha_power / (beta_power + 1e-10)
        creativity = theta_power / (alpha_power + 1e-10)
        activation = np.var(signal)
        
        return {
            'engagement': engagement,
            'relaxation': relaxation,
            'creativity': creativity,
            'activation': activation,
        }


class SimpleSynthesizer:
    """Simple additive synthesizer with brain-controlled parameters"""
    
    def __init__(self, fs=44100):
        self.fs = fs
        self.phase = 0
        self.smoothed_params = {}
        
    def smooth_param(self, param_name, new_value, alpha=0.95):
        """Exponential smoothing for stable parameters"""
        if param_name not in self.smoothed_params:
            self.smoothed_params[param_name] = new_value
        else:
            self.smoothed_params[param_name] = (alpha * self.smoothed_params[param_name] + 
                                                (1 - alpha) * new_value)
        return self.smoothed_params[param_name]
    
    def synthesize(self, duration, brain_features):
        """Generate audio from brain features"""
        n_samples = int(duration * self.fs)
        t = (self.phase + np.arange(n_samples)) / self.fs
        
        # Map brain features to synthesis parameters
        base_freq = 220  # A3
        
        # Engagement affects frequency (pitch rises with engagement)
        freq = base_freq * (1 + 0.5 * self.smooth_param('engagement', 
                                                         brain_features['engagement']))
        
        # Creativity affects harmonic content
        creativity = self.smooth_param('creativity', brain_features['creativity'])
        harmonics = [1, 2, 3, 4, 5]
        harmonic_amps = [1.0, 0.5 * creativity, 0.3 * creativity, 
                        0.2 * creativity, 0.1 * creativity]
        
        # Generate harmonics
        audio = np.zeros(n_samples)
        for h, amp in zip(harmonics, harmonic_amps):
            audio += amp * np.sin(2 * np.pi * freq * h * t)
        
        # Activation affects amplitude
        activation = self.smooth_param('activation', brain_features['activation'] / 1000)
        activation = np.clip(activation, 0.1, 1.0)
        audio *= activation
        
        # Relaxation affects reverb (simplified as delay)
        relaxation = self.smooth_param('relaxation', brain_features['relaxation'])
        delay_samples = int(0.1 * self.fs)
        if delay_samples < n_samples:
            delayed = np.zeros(n_samples)
            delayed[delay_samples:] = audio[:-delay_samples]
            audio += 0.3 * relaxation * delayed
        
        # Normalize and add fade to avoid clicks
        audio = audio / (np.max(np.abs(audio)) + 1e-10)
        audio *= 0.3  # Master volume
        
        # Apply fade in/out to avoid clicks
        fade_len = min(100, n_samples // 10)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        audio[:fade_len] *= fade_in
        audio[-fade_len:] *= fade_out
        
        self.phase += n_samples
        
        return audio.astype(np.float32)


def main():
    """Main real-time synthesis loop"""
    print("=" * 60)
    print("Simulated Brain-Controlled Synthesizer")
    print("=" * 60)
    print("\nThis prototype generates audio driven by simulated brain signals.")
    print("Watch how the sound changes as 'brain states' vary over time.\n")
    
    if not AUDIO_AVAILABLE:
        print("ERROR: PyAudio not available. Cannot generate audio.")
        print("Install with: pip install pyaudio")
        return
    
    # Initialize components
    brain = BrainSimulator(fs=250)
    synth = SimpleSynthesizer(fs=44100)
    
    # Audio setup
    chunk_duration = 0.1  # 100ms chunks
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=synth.fs,
            output=True,
            frames_per_buffer=int(chunk_duration * synth.fs)
        )
        
        print("Audio stream started. Press Ctrl+C to stop.\n")
        print("Brain Features → Audio Parameters:")
        print("-" * 60)
        
        while True:
            # Generate and process brain signal
            brain_signal = brain.generate_window(duration=0.5)
            features = brain.extract_features(brain_signal)
            
            # Display features
            print(f"\rEngagement: {features['engagement']:5.2f} | "
                  f"Relaxation: {features['relaxation']:5.2f} | "
                  f"Creativity: {features['creativity']:5.2f} | "
                  f"Activation: {features['activation']:6.1f}",
                  end='', flush=True)
            
            # Generate audio
            audio = synth.synthesize(chunk_duration, features)
            
            # Play audio
            stream.write(audio.tobytes())
            
    except KeyboardInterrupt:
        print("\n\nStopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Audio stream closed.")


if __name__ == "__main__":
    main()
