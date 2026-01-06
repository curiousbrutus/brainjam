"""
Performance Metrics Logger

Logs interaction measures during performance:
- Latency measurements
- Stability metrics
- Controllability assessment
- Performer-rated agency
- Perceived responsiveness
"""

import numpy as np
import time
import json
from typing import Dict, List, Optional
from collections import deque


class PerformanceLogger:
    """
    Logs performance metrics for interaction evaluation.
    
    This is NOT clinical assessment - it measures system performance
    and performer experience during artistic practice.
    """
    
    def __init__(self, window_size: int = 100):
        """
        Initialize performance logger.
        
        Args:
            window_size: Size of rolling window for statistics
        """
        self.window_size = window_size
        
        # Latency tracking
        self.latencies = deque(maxlen=window_size)
        
        # Stability tracking
        self.parameter_history = deque(maxlen=window_size)
        
        # Controllability tracking
        self.control_output_pairs = deque(maxlen=window_size)
        
        # Subjective ratings (collected periodically)
        self.agency_ratings = []
        self.responsiveness_ratings = []
        self.rating_times = []
        
        # Session metadata
        self.session_start = time.time()
        self.total_frames = 0
        
    def log_frame(self, control_input: Dict[str, float], 
                  mapped_output: Dict[str, float],
                  frame_start_time: float,
                  frame_end_time: float):
        """
        Log a single frame of performance.
        
        Args:
            control_input: Input control parameters
            mapped_output: Output parameters after mapping
            frame_start_time: Start time of frame processing
            frame_end_time: End time of frame processing
        """
        # Log latency
        latency_ms = (frame_end_time - frame_start_time) * 1000
        self.latencies.append(latency_ms)
        
        # Log parameters for stability analysis
        output_array = np.array([mapped_output.get(f'control_{i}', 0.5) 
                                for i in range(1, 5)])
        self.parameter_history.append(output_array)
        
        # Log control/output pairs for controllability
        control_array = np.array([control_input.get(f'control_{i}', 0.5) 
                                 for i in range(1, 5)])
        self.control_output_pairs.append((control_array, output_array))
        
        self.total_frames += 1
    
    def add_subjective_rating(self, agency: float, responsiveness: float):
        """
        Add subjective performer ratings.
        
        Args:
            agency: Agency rating (0-10)
            responsiveness: Responsiveness rating (0-10)
        """
        current_time = time.time() - self.session_start
        self.agency_ratings.append(agency)
        self.responsiveness_ratings.append(responsiveness)
        self.rating_times.append(current_time)
    
    def get_latency_stats(self) -> Dict[str, float]:
        """
        Get latency statistics.
        
        Returns:
            Dictionary with latency metrics
        """
        if len(self.latencies) == 0:
            return {
                'mean_ms': 0.0,
                'std_ms': 0.0,
                'min_ms': 0.0,
                'max_ms': 0.0,
                'p95_ms': 0.0,
            }
        
        latencies_array = np.array(list(self.latencies))
        
        return {
            'mean_ms': float(np.mean(latencies_array)),
            'std_ms': float(np.std(latencies_array)),
            'min_ms': float(np.min(latencies_array)),
            'max_ms': float(np.max(latencies_array)),
            'p95_ms': float(np.percentile(latencies_array, 95)),
        }
    
    def get_stability_metric(self) -> float:
        """
        Compute parameter stability metric.
        
        Returns:
            Stability score (0-1, higher = more stable)
        """
        if len(self.parameter_history) < 2:
            return 0.0
        
        params = np.array(list(self.parameter_history))
        
        # Compute variance across time for each parameter
        variances = np.var(params, axis=0)
        
        # Stability is inverse of variance
        # High variance = low stability
        mean_variance = np.mean(variances)
        stability = 1.0 / (1.0 + mean_variance)
        
        return float(stability)
    
    def get_controllability_metric(self) -> float:
        """
        Compute controllability metric (correlation between input and output).
        
        Returns:
            Controllability score (0-1, higher = more controllable)
        """
        if len(self.control_output_pairs) < 10:
            return 0.0
        
        # Extract controls and outputs
        controls = np.array([pair[0] for pair in self.control_output_pairs])
        outputs = np.array([pair[1] for pair in self.control_output_pairs])
        
        # Compute correlation for each parameter
        correlations = []
        for i in range(min(controls.shape[1], outputs.shape[1])):
            corr = np.corrcoef(controls[:, i], outputs[:, i])[0, 1]
            if not np.isnan(corr):
                correlations.append(abs(corr))
        
        return float(np.mean(correlations)) if correlations else 0.0
    
    def get_subjective_metrics(self) -> Dict[str, float]:
        """
        Get subjective rating metrics.
        
        Returns:
            Dictionary with rating statistics
        """
        if len(self.agency_ratings) == 0:
            return {
                'mean_agency': 0.0,
                'mean_responsiveness': 0.0,
                'n_ratings': 0,
            }
        
        return {
            'mean_agency': float(np.mean(self.agency_ratings)),
            'mean_responsiveness': float(np.mean(self.responsiveness_ratings)),
            'n_ratings': len(self.agency_ratings),
        }
    
    def get_summary(self) -> Dict:
        """
        Get complete performance summary.
        
        Returns:
            Dictionary with all metrics
        """
        session_duration = time.time() - self.session_start
        
        return {
            'session': {
                'duration_s': session_duration,
                'total_frames': self.total_frames,
                'avg_fps': self.total_frames / session_duration if session_duration > 0 else 0,
            },
            'latency': self.get_latency_stats(),
            'stability': self.get_stability_metric(),
            'controllability': self.get_controllability_metric(),
            'subjective': self.get_subjective_metrics(),
        }
    
    def save_log(self, filepath: str):
        """
        Save log to JSON file.
        
        Args:
            filepath: Path to save log
        """
        summary = self.get_summary()
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Performance log saved to: {filepath}")
    
    def print_summary(self):
        """Print performance summary to console."""
        summary = self.get_summary()
        
        print("\n" + "=" * 70)
        print("Performance Metrics Summary")
        print("=" * 70)
        
        print("\nSession:")
        print(f"  Duration: {summary['session']['duration_s']:.1f}s")
        print(f"  Total frames: {summary['session']['total_frames']}")
        print(f"  Average FPS: {summary['session']['avg_fps']:.1f}")
        
        print("\nLatency:")
        print(f"  Mean: {summary['latency']['mean_ms']:.2f}ms")
        print(f"  Std: {summary['latency']['std_ms']:.2f}ms")
        print(f"  95th percentile: {summary['latency']['p95_ms']:.2f}ms")
        print(f"  Target: <100ms {'✓' if summary['latency']['p95_ms'] < 100 else '✗'}")
        
        print("\nStability:")
        print(f"  Score: {summary['stability']:.3f} (0-1, higher is better)")
        
        print("\nControllability:")
        print(f"  Score: {summary['controllability']:.3f} (0-1, higher is better)")
        
        if summary['subjective']['n_ratings'] > 0:
            print("\nSubjective Ratings:")
            print(f"  Agency: {summary['subjective']['mean_agency']:.1f}/10")
            print(f"  Responsiveness: {summary['subjective']['mean_responsiveness']:.1f}/10")
            print(f"  Number of ratings: {summary['subjective']['n_ratings']}")
        
        print("=" * 70)
