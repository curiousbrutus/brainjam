"""
Mock EEG Controller

Generates structured but random EEG-like signals for testing and demonstration.
This is NOT brain decoding - it's a test signal generator for developing
and evaluating the performance system.
"""

import numpy as np
from typing import Dict


class MockEEGController:
    """
    Mock EEG controller that generates realistic-looking control signals.
    
    This generates band-power features that vary over time in a structured way,
    simulating the kind of continuous control signals one might extract from EEG.
    These are NOT decoded thoughts - they are simple time-varying parameters.
    """
    
    def __init__(self, fs: int = 250, n_channels: int = 1):
        """
        Initialize mock EEG controller.
        
        Args:
            fs: Sampling frequency in Hz
            n_channels: Number of simulated channels
        """
        self.fs = fs
        self.n_channels = n_channels
        self.t = 0.0
        self.phase_offsets = np.random.uniform(0, 2*np.pi, n_channels)
        
    def get_control_vector(self, duration: float = 0.5) -> Dict[str, float]:
        """
        Generate a control vector from mock EEG signal.
        
        Args:
            duration: Duration of signal window in seconds
            
        Returns:
            Dictionary of normalized control parameters (0-1 range)
        """
        # Generate time-varying oscillations that look EEG-ish
        n_samples = int(duration * self.fs)
        t = self.t + np.arange(n_samples) / self.fs
        
        # Simulate different "band powers" with slow modulation
        # These are just continuous control signals, not decoded mental states
        theta_mod = 0.5 + 0.3 * np.sin(2 * np.pi * 0.1 * self.t)  # ~10s period
        alpha_mod = 0.5 + 0.4 * np.cos(2 * np.pi * 0.15 * self.t)  # ~6.7s period
        beta_mod = 0.5 + 0.35 * np.sin(2 * np.pi * 0.2 * self.t)   # ~5s period
        
        # Apply temporal smoothing (these values change slowly)
        control_1 = np.clip(theta_mod + 0.05 * np.random.randn(), 0, 1)
        control_2 = np.clip(alpha_mod + 0.05 * np.random.randn(), 0, 1)
        control_3 = np.clip(beta_mod + 0.05 * np.random.randn(), 0, 1)
        control_4 = np.clip(0.3 + 0.2 * np.sin(2 * np.pi * 0.25 * self.t) + 
                           0.05 * np.random.randn(), 0, 1)
        
        self.t += duration
        
        return {
            'control_1': float(control_1),  # Slow varying parameter
            'control_2': float(control_2),  # Medium varying parameter
            'control_3': float(control_3),  # Medium-fast varying parameter
            'control_4': float(control_4),  # Faster varying parameter
        }
    
    def get_control_frame(self) -> Dict[str, float]:
        """
        Get control parameters using BaseDevice-compatible interface.
        
        Returns:
            Dictionary of control parameters with standardized names (0-1 range)
        """
        # Get raw control vector
        controls = self.get_control_vector(duration=0.05)
        
        # Map to standardized parameter names
        return {
            'intensity': controls['control_1'],
            'density': controls['control_2'],
            'variation': controls['control_3'],
            'brightness': controls['control_4']
        }
    
    def get_raw_features(self, duration: float = 0.5) -> Dict[str, float]:
        """
        Get raw band-power features (for visualization/debugging).
        
        Args:
            duration: Duration of signal window
            
        Returns:
            Dictionary with band power estimates
        """
        n_samples = int(duration * self.fs)
        t = self.t + np.arange(n_samples) / self.fs
        
        # Simulate band power variations
        theta_power = 15 * (1 + 0.5 * np.sin(2 * np.pi * 0.1 * self.t))
        alpha_power = 12 * (1 + 0.3 * np.cos(2 * np.pi * 0.15 * self.t))
        beta_power = 8 * (1 + 0.4 * np.sin(2 * np.pi * 0.2 * self.t))
        
        # Add realistic noise
        theta_power += 2 * np.random.randn()
        alpha_power += 2 * np.random.randn()
        beta_power += 2 * np.random.randn()
        
        return {
            'theta_power': max(0, float(theta_power)),
            'alpha_power': max(0, float(alpha_power)),
            'beta_power': max(0, float(beta_power)),
        }
    
    def reset(self):
        """Reset the controller state."""
        self.t = 0.0
        self.phase_offsets = np.random.uniform(0, 2*np.pi, self.n_channels)
