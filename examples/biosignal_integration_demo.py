"""
Example: BioSignalInference Integration with ParametricSynth

Demonstrates real-time biosignal processing and audio synthesis using the
BioSignalInference module with BrainJam's existing ParametricSynth.
"""

import sys
import os
import numpy as np
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bridge.latent_mapper import BioSignalInference
from performance_system.sound_engines.parametric_synth import ParametricSynth


def simulate_biosignal_stream(duration=5.0, sample_rate=250):
    """
    Simulate a realistic biosignal stream for demonstration.
    
    Args:
        duration: Total duration in seconds
        sample_rate: Sampling rate in Hz
        
    Yields:
        Tuples of (eeg_frame, fnirs_frame, emg_frame) every 100ms
    """
    chunk_duration = 0.1  # 100ms chunks for real-time feel
    chunk_samples = int(chunk_duration * sample_rate)
    total_chunks = int(duration / chunk_duration)
    
    t_offset = 0.0
    
    for chunk_idx in range(total_chunks):
        # Simulate gradual changes in biosignals over time
        progress = chunk_idx / total_chunks
        
        # EEG: Gradually increasing arousal (more beta)
        t = t_offset + np.arange(chunk_samples) / sample_rate
        eeg = np.zeros((chunk_samples, 8))
        for ch in range(8):
            # Alpha band (8-13 Hz)
            alpha = (1.0 - progress * 0.5) * np.sin(2 * np.pi * 10 * t + ch * 0.5)
            # Beta band (13-30 Hz) - increases over time
            beta = (0.5 + progress) * np.sin(2 * np.pi * 20 * t + ch * 0.3)
            # Add some noise
            noise = 0.1 * np.random.randn(chunk_samples)
            eeg[:, ch] = alpha + beta + noise
        
        # fNIRS: Positive slope indicating increasing cognitive load
        fnirs = np.zeros((chunk_samples, 2))
        fnirs[:, 0] = 0.5 + progress * 0.3 + 0.1 * (t - t_offset) + 0.05 * np.random.randn(chunk_samples)  # HbO2
        fnirs[:, 1] = 0.5 - progress * 0.1 - 0.05 * (t - t_offset) + 0.05 * np.random.randn(chunk_samples)  # HbR
        
        # EMG: Gradually increasing effort
        emg = np.zeros((chunk_samples, 1))
        emg[:, 0] = (0.3 + progress * 0.5) + 0.2 * np.sin(2 * np.pi * 5 * t) + 0.1 * np.random.randn(chunk_samples)
        
        t_offset += chunk_duration
        
        yield eeg, fnirs, emg


def main():
    """Run the integrated demo."""
    print("=" * 70)
    print("BioSignal Inference → ParametricSynth Integration Demo")
    print("=" * 70)
    print()
    print("This demo simulates real-time biosignal processing and audio synthesis.")
    print("Biosignals gradually increase in arousal and effort over 5 seconds.")
    print("Watch for the conditional trigger when Arousal > 0.8 and Effort > 0.7")
    print()
    
    # Initialize components
    print("Initializing components...")
    processor = BioSignalInference(
        eeg_channels=8,
        fnirs_channels=2,
        emg_channels=1,
        sample_rate=250.0,
        buffer_size=500
    )
    
    synth = ParametricSynth(sample_rate=44100, base_freq=220.0)
    
    print(f"  ✓ BioSignalInference initialized (device: {processor.device})")
    print(f"  ✓ ParametricSynth initialized (sample_rate: {synth.sample_rate} Hz)")
    print()
    
    # Run simulation
    print("Starting real-time simulation (5 seconds)...")
    print("-" * 70)
    print(f"{'Time':>6} | {'Arousal':>7} | {'CogLoad':>7} | {'Effort':>7} | {'Density':>7} | {'Trigger':>7}")
    print("-" * 70)
    
    total_audio_samples = 0
    start_time = time.time()
    trigger_activated = False
    
    for idx, (eeg, fnirs, emg) in enumerate(simulate_biosignal_stream(duration=5.0)):
        # Process biosignals
        style_vector = processor.process_frame(eeg, fnirs, emg)
        
        # Generate audio
        audio = synth.generate(duration=0.1, control_params=style_vector)
        total_audio_samples += len(audio)
        
        # Display progress
        elapsed = time.time() - start_time
        arousal = style_vector['arousal']
        cognitive = style_vector['cognitive_load']
        effort = style_vector['effort']
        density = style_vector['tempo_density']
        
        # Check for trigger
        is_triggered = (arousal > processor.arousal_threshold and 
                       effort > processor.effort_threshold)
        trigger_status = "⚡ YES" if is_triggered else "   no"
        
        if is_triggered and not trigger_activated:
            trigger_activated = True
        
        print(f"{elapsed:5.1f}s | {arousal:7.3f} | {cognitive:7.3f} | {effort:7.3f} | {density:7.3f} | {trigger_status}")
        
        # Small delay to simulate real-time (optional, for readability)
        time.sleep(0.05)
    
    print("-" * 70)
    print()
    
    # Performance summary
    stats = processor.get_performance_stats()
    
    print("Performance Summary:")
    print(f"  Total audio samples generated: {total_audio_samples}")
    print(f"  Audio duration: {total_audio_samples / synth.sample_rate:.2f} seconds")
    print()
    print(f"  Mean processing latency: {stats['mean_latency_ms']:.2f} ms")
    print(f"  Std processing latency:  {stats['std_latency_ms']:.2f} ms")
    print(f"  Max processing latency:  {stats['max_latency_ms']:.2f} ms")
    print(f"  P95 processing latency:  {stats['p95_latency_ms']:.2f} ms")
    print()
    
    if stats['p95_latency_ms'] < 100:
        print(f"  ✓ Latency within budget: {stats['p95_latency_ms']:.2f}ms < 100ms")
    else:
        print(f"  ✗ Latency exceeds budget: {stats['p95_latency_ms']:.2f}ms > 100ms")
    print()
    
    if trigger_activated:
        print("  ⚡ Conditional trigger was activated (180 BPM rhythm)")
    else:
        print("  ℹ Conditional trigger was not activated in this run")
    print()
    
    print("=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
