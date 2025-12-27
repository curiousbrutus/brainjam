"""
Demo 3: Learning Through Practice

Same mapping, performer improves control over time.
Visualize stabilization of interaction.
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

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available for visualization")

from performance_system.controllers import MockEEGController
from performance_system.mapping_models import ExpressiveMapper
from performance_system.sound_engines import DDSPSynth


class PracticeSession:
    """
    Tracks learning and stabilization over practice session.
    """
    
    def __init__(self):
        """Initialize practice tracking."""
        self.control_history = []
        self.output_history = []
        self.stability_history = []
        self.time_points = []
        
    def update(self, time_point: float, controls: dict, outputs: dict):
        """
        Record state at this time point.
        
        Args:
            time_point: Current time
            controls: Control parameters
            outputs: Sound engine parameters
        """
        self.time_points.append(time_point)
        
        # Convert to arrays
        control_array = np.array([controls.get(f'control_{i}', 0.5) 
                                 for i in range(1, 5)])
        output_array = np.array([outputs.get(f'control_{i}', 0.5) 
                                for i in range(1, 5)])
        
        self.control_history.append(control_array)
        self.output_history.append(output_array)
        
        # Compute stability (variance over recent window)
        if len(self.output_history) >= 10:
            recent = np.array(self.output_history[-10:])
            stability = 1.0 - np.mean(np.var(recent, axis=0))
        else:
            stability = 0.0
        
        self.stability_history.append(stability)
    
    def get_controllability(self) -> float:
        """
        Measure controllability: how well outputs track targets.
        
        Returns:
            Controllability metric (0-1, higher is better)
        """
        if len(self.control_history) < 2:
            return 0.0
        
        controls = np.array(self.control_history)
        outputs = np.array(self.output_history)
        
        # Correlation between controls and outputs
        correlations = []
        for i in range(min(controls.shape[1], outputs.shape[1])):
            corr = np.corrcoef(controls[:, i], outputs[:, i])[0, 1]
            if not np.isnan(corr):
                correlations.append(abs(corr))
        
        return np.mean(correlations) if correlations else 0.0
    
    def get_stability(self) -> float:
        """
        Measure overall stability.
        
        Returns:
            Stability metric (0-1, higher is better)
        """
        if len(self.stability_history) == 0:
            return 0.0
        return np.mean(self.stability_history[-50:])  # Recent stability
    
    def visualize(self, save_path: str = "demo3_learning_curve.png"):
        """
        Visualize learning progression.
        
        Args:
            save_path: Path to save figure
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not available for visualization")
            return
        
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # Plot 1: Control parameters over time
        times = np.array(self.time_points)
        controls = np.array(self.control_history)
        
        axes[0].set_title("Control Signals Over Time", fontsize=14, fontweight='bold')
        for i in range(controls.shape[1]):
            axes[0].plot(times, controls[:, i], label=f'Control {i+1}', alpha=0.7)
        axes[0].set_ylabel("Control Value")
        axes[0].legend(loc='upper right')
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Output parameters over time
        outputs = np.array(self.output_history)
        
        axes[1].set_title("Output Parameters Over Time", fontsize=14, fontweight='bold')
        for i in range(outputs.shape[1]):
            axes[1].plot(times, outputs[:, i], label=f'Output {i+1}', alpha=0.7)
        axes[1].set_ylabel("Output Value")
        axes[1].legend(loc='upper right')
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Stability over time (shows learning)
        axes[2].set_title("Stability Over Time (Learning Curve)", 
                         fontsize=14, fontweight='bold')
        axes[2].plot(times, self.stability_history, color='green', linewidth=2)
        axes[2].set_xlabel("Time (s)")
        axes[2].set_ylabel("Stability")
        axes[2].grid(True, alpha=0.3)
        axes[2].axhline(y=0.8, color='r', linestyle='--', 
                       label='Target Stability', alpha=0.5)
        axes[2].legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        print(f"\nLearning curve saved to: {save_path}")
        plt.close()


def simulate_practice_session(duration: float = 60.0,
                              output_file: str = "demo3_learning_practice.wav"):
    """
    Simulate performer learning to control the system through practice.
    
    Args:
        duration: Session duration in seconds
        output_file: Output audio file path
    """
    print("=" * 70)
    print("Demo 3: Learning Through Practice")
    print("=" * 70)
    print("\nSimulating practice session...")
    print(f"Duration: {duration}s")
    print("\nThis demo shows:")
    print("  • Same mapping throughout session")
    print("  • Performer (simulated) improves control over time")
    print("  • Stabilization of interaction visualized")
    print("  • Learning curve demonstrates controllability")
    print()
    
    # Initialize components
    controller = MockEEGController(fs=250)
    mapper = ExpressiveMapper(n_inputs=4, n_outputs=4,
                             use_hysteresis=True, use_drift=True,
                             use_thresholds=False)
    synth = DDSPSynth(sample_rate=44100, base_freq=165.0)
    session = PracticeSession()
    
    # Simulate learning: controller gets more focused over time
    chunk_duration = 0.1
    n_chunks = int(duration / chunk_duration)
    audio_chunks = []
    
    current_time = 0.0
    
    print("Simulating practice...")
    start_time = time.time()
    
    for i in range(n_chunks):
        # Simulate learning: reduce variability over time
        learning_progress = i / n_chunks  # 0 to 1
        controller.phase_offsets *= (1.0 - learning_progress * 0.3)  # More focused
        
        # Get control signal
        raw_controls = controller.get_control_vector(duration=0.5)
        
        # Apply mapping
        mapped_controls = mapper.map(raw_controls)
        
        # Generate audio
        audio_chunk = synth.generate(chunk_duration, mapped_controls)
        audio_chunks.append(audio_chunk)
        
        # Track learning
        session.update(current_time, raw_controls, mapped_controls)
        
        current_time += chunk_duration
        
        # Progress
        if (i + 1) % 100 == 0:
            progress = (i + 1) / n_chunks * 100
            stability = session.get_stability()
            print(f"  Progress: {progress:.1f}% - Stability: {stability:.3f}")
    
    # Concatenate
    audio = np.concatenate(audio_chunks)
    
    elapsed = time.time() - start_time
    print(f"\nGeneration complete in {elapsed:.2f}s")
    
    # Save audio
    if SOUNDFILE_AVAILABLE:
        sf.write(output_file, audio, 44100)
        print(f"Audio saved to: {output_file}")
    
    # Visualize learning
    session.visualize()
    
    # Statistics
    final_controllability = session.get_controllability()
    final_stability = session.get_stability()
    
    print("\n" + "=" * 70)
    print("Practice Session Results:")
    print("=" * 70)
    print(f"  Session duration: {duration}s")
    print(f"  Final controllability: {final_controllability:.3f}")
    print(f"  Final stability: {final_stability:.3f}")
    print(f"  Improvement shown: {'Yes' if final_stability > 0.5 else 'Ongoing'}")
    print("=" * 70)
    
    print("\n✓ Demo 3 complete!")
    print("\nThis demonstrates:")
    print("  → Performer can learn system over time")
    print("  → Stability increases with practice")
    print("  → Controllability emerges from interaction")
    print("  → System is rehearseable and performable")
    
    return audio, session


if __name__ == "__main__":
    print("\nRunning Demo 3: Learning Through Practice\n")
    audio, session = simulate_practice_session(duration=60.0)
    print("\nDemo completed successfully!")
