"""
Demo 1: Brain → Continuous Sound

Random or EEG-like signal controls timbre & density.
No rhythm, just texture. Pure drone/ambient soundscape.
"""

import numpy as np
import time
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False
    print("Warning: soundfile not available for file output")

from performance_system.controllers import MockEEGController
from performance_system.feature_shaping import TemporalSmoother
from performance_system.sound_engines import DDSPSynth


def generate_continuous_texture(duration: float = 30.0, 
                                output_file: str = "demo1_continuous_texture.wav"):
    """
    Generate continuous textural sound controlled by brain-like signals.
    
    Args:
        duration: Total duration in seconds
        output_file: Output audio file path
    """
    print("=" * 70)
    print("Demo 1: Brain → Continuous Sound")
    print("=" * 70)
    print("\nGenerating continuous textural soundscape...")
    print(f"Duration: {duration}s")
    print("\nThis demo shows:")
    print("  • Brain-like signals controlling timbre and density")
    print("  • No discrete rhythm or notes - pure texture")
    print("  • Temporal smoothing for stable but evolving sound")
    print()
    
    # Initialize components
    controller = MockEEGController(fs=250)
    smoother = TemporalSmoother(n_features=4, window_size=10, 
                               smoothing_mode='exponential')
    synth = DDSPSynth(sample_rate=44100, base_freq=110.0)  # Low drone
    
    # Generate audio in chunks
    chunk_duration = 0.1  # 100ms chunks for low latency
    n_chunks = int(duration / chunk_duration)
    
    audio_chunks = []
    
    print("Generating audio chunks...")
    start_time = time.time()
    
    for i in range(n_chunks):
        # Get control signal
        raw_controls = controller.get_control_vector(duration=0.5)
        
        # Apply temporal smoothing
        smoothed_controls = smoother.update(raw_controls)
        
        # Generate audio
        audio_chunk = synth.generate(chunk_duration, smoothed_controls)
        audio_chunks.append(audio_chunk)
        
        # Progress indicator
        if (i + 1) % 50 == 0:
            progress = (i + 1) / n_chunks * 100
            elapsed = time.time() - start_time
            print(f"  Progress: {progress:.1f}% ({i+1}/{n_chunks} chunks) "
                  f"- Elapsed: {elapsed:.1f}s")
    
    # Concatenate all chunks
    audio = np.concatenate(audio_chunks)
    
    elapsed = time.time() - start_time
    print(f"\nGeneration complete in {elapsed:.2f}s")
    print(f"Real-time factor: {duration/elapsed:.2f}x")
    
    # Save to file
    if SOUNDFILE_AVAILABLE:
        sf.write(output_file, audio, 44100)
        print(f"\nAudio saved to: {output_file}")
    else:
        print("\nCould not save audio (soundfile not available)")
    
    # Print statistics
    print("\n" + "=" * 70)
    print("Audio Statistics:")
    print("=" * 70)
    print(f"  Duration: {len(audio) / 44100:.2f}s")
    print(f"  Samples: {len(audio)}")
    print(f"  Peak amplitude: {np.max(np.abs(audio)):.3f}")
    print(f"  RMS level: {np.sqrt(np.mean(audio**2)):.3f}")
    print("=" * 70)
    
    print("\n✓ Demo 1 complete!")
    print("\nThis demonstrates:")
    print("  → Brain signals as continuous control (NOT discrete notes)")
    print("  → Textural, ambient sound generation")
    print("  → Low-latency performance capability (<100ms per chunk)")
    print("  → Temporal smoothing for musical stability")
    
    return audio


if __name__ == "__main__":
    print("\nRunning Demo 1: Brain → Continuous Sound\n")
    audio = generate_continuous_texture(duration=30.0)
    print("\nDemo completed successfully!")
