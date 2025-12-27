"""
Signal Generation Utilities

Mock signal generators for the Streamlit GUI
"""

import numpy as np


class MockSignalGenerator:
    """
    Generate mock EEG/fNIRS-like signals with controllable parameters
    """
    
    def __init__(self, fs=250):
        """
        Initialize signal generator
        
        Args:
            fs: Sampling frequency in Hz
        """
        self.fs = fs
        self.t = 0.0
        
    def generate_signal(self, duration, arousal=0.5, focus=0.5, variability=0.5):
        """
        Generate mock brain-like signal
        
        Args:
            duration: Duration in seconds
            arousal: Arousal level (0-1)
            focus: Focus level (0-1)
            variability: Variability level (0-1)
            
        Returns:
            time_array, signal_array, features_dict
        """
        n_samples = int(duration * self.fs)
        time_vec = self.t + np.arange(n_samples) / self.fs
        
        # Generate band-like oscillations
        # Theta (4-8 Hz) - varies with relaxation/creativity
        theta_amp = 15 * (1 - focus * 0.5)
        theta = theta_amp * np.sin(2 * np.pi * 6 * time_vec)
        
        # Alpha (8-13 Hz) - varies inversely with arousal
        alpha_amp = 12 * (1 - arousal * 0.6)
        alpha = alpha_amp * np.sin(2 * np.pi * 10 * time_vec)
        
        # Beta (13-30 Hz) - increases with arousal and focus
        beta_amp = 8 * (0.5 + arousal * 0.3 + focus * 0.2)
        beta = beta_amp * np.sin(2 * np.pi * 20 * time_vec)
        
        # Add noise based on variability
        noise_amp = 5 * variability
        noise = noise_amp * np.random.randn(n_samples)
        
        # Combine
        signal = theta + alpha + beta + noise
        
        # Extract features (simplified band powers)
        features = self._extract_features(signal, theta_amp, alpha_amp, beta_amp)
        
        self.t += duration
        
        return time_vec, signal, features
    
    def _extract_features(self, signal, theta_amp, alpha_amp, beta_amp):
        """Extract simplified features from signal"""
        # In a real system, would use FFT/bandpass filters
        # Here we use the known amplitudes with some noise
        return {
            'theta_power': float(theta_amp + 2 * np.random.randn()),
            'alpha_power': float(alpha_amp + 2 * np.random.randn()),
            'beta_power': float(beta_amp + 2 * np.random.randn()),
        }
    
    def reset(self):
        """Reset time counter"""
        self.t = 0.0


def normalize_features(features):
    """
    Normalize features to 0-1 range for control
    
    Args:
        features: Dict of raw features
        
    Returns:
        Dict of normalized control values (0-1)
    """
    # Simple min-max normalization with reasonable ranges
    theta_norm = np.clip(features['theta_power'] / 20.0, 0, 1)
    alpha_norm = np.clip(features['alpha_power'] / 20.0, 0, 1)
    beta_norm = np.clip(features['beta_power'] / 15.0, 0, 1)
    
    # Derive additional control parameters
    control_1 = float(theta_norm)
    control_2 = float(alpha_norm)
    control_3 = float(beta_norm)
    control_4 = float(np.clip((theta_norm + beta_norm) / 2, 0, 1))
    
    return {
        'control_1': control_1,
        'control_2': control_2,
        'control_3': control_3,
        'control_4': control_4,
    }
