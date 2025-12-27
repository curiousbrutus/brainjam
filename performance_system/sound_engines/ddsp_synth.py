"""
DDSP-Style Synthesizer

Differentiable Digital Signal Processing inspired synthesis.
Uses harmonic oscillator + filtered noise for expressive, real-time sound.
"""

import numpy as np
from typing import Dict, Optional


class DDSPSynth:
    """
    DDSP-style parametric synthesizer with harmonic + noise components.
    
    Controllable parameters:
    - pitch_range: Base pitch modulation (0=low, 1=high)
    - brightness: Harmonic rolloff / spectral centroid (0=dark, 1=bright)
    - roughness: Amount of noise/inharmonicity (0=smooth, 1=rough)
    - amplitude: Overall volume (0=quiet, 1=loud)
    """
    
    def __init__(self, sample_rate: int = 44100, base_freq: float = 220.0):
        """
        Initialize DDSP synthesizer.
        
        Args:
            sample_rate: Audio sample rate in Hz
            base_freq: Base frequency in Hz (default A3)
        """
        self.sample_rate = sample_rate
        self.base_freq = base_freq
        self.phase = 0.0
        self.noise_phase = 0.0
        
        # Smoothed parameter state
        self.smoothed_params = {
            'pitch_range': 0.5,
            'brightness': 0.6,
            'roughness': 0.3,
            'amplitude': 0.5,
        }
        self.smoothing_alpha = 0.95
        
    def generate(self, duration: float, control_params: Dict[str, float]) -> np.ndarray:
        """
        Generate audio using DDSP-style synthesis.
        
        Args:
            duration: Duration in seconds
            control_params: Dictionary with control parameters (0-1 range)
            
        Returns:
            Audio samples as numpy array (float32)
        """
        n_samples = int(duration * self.sample_rate)
        t = (self.phase + np.arange(n_samples)) / self.sample_rate
        
        # Map control parameters
        pitch_range = self._smooth_param('pitch_range', 
                                        control_params.get('latent_1', 
                                                          control_params.get('control_1', 0.5)))
        brightness = self._smooth_param('brightness',
                                       control_params.get('latent_2',
                                                         control_params.get('control_2', 0.6)))
        roughness = self._smooth_param('roughness',
                                      control_params.get('latent_3',
                                                        control_params.get('control_3', 0.3)))
        amplitude = self._smooth_param('amplitude',
                                      control_params.get('latent_4',
                                                        control_params.get('control_4', 0.5)))
        
        # Generate harmonic component
        harmonic_audio = self._generate_harmonics(t, pitch_range, brightness, roughness)
        
        # Generate noise component
        noise_audio = self._generate_filtered_noise(n_samples, brightness, roughness)
        
        # Mix components
        mix_ratio = 0.7 - 0.5 * roughness  # More roughness = more noise
        audio = mix_ratio * harmonic_audio + (1 - mix_ratio) * noise_audio
        
        # Apply amplitude envelope
        envelope = amplitude * (0.8 + 0.2 * np.sin(2 * np.pi * 2.0 * t))
        audio *= envelope
        
        # Normalize and apply fade
        audio = self._normalize_and_fade(audio)
        
        self.phase += n_samples
        return audio.astype(np.float32)
    
    def _smooth_param(self, name: str, new_value: float) -> float:
        """Apply exponential smoothing to parameter."""
        current = self.smoothed_params.get(name, new_value)
        smoothed = self.smoothing_alpha * current + (1 - self.smoothing_alpha) * new_value
        self.smoothed_params[name] = smoothed
        return smoothed
    
    def _generate_harmonics(self, t: np.ndarray, pitch_range: float,
                           brightness: float, roughness: float) -> np.ndarray:
        """
        Generate harmonic oscillator component.
        
        Args:
            t: Time vector
            pitch_range: Pitch modulation (0-1)
            brightness: Spectral brightness (0-1)
            roughness: Inharmonicity amount (0-1)
            
        Returns:
            Harmonic audio
        """
        # Map pitch_range to frequency multiplier
        pitch_mult = 0.5 + 1.5 * pitch_range  # 0.5x to 2x base frequency
        freq = self.base_freq * pitch_mult
        
        # Number of harmonics based on brightness
        n_harmonics = int(3 + brightness * 12)  # 3 to 15 harmonics
        
        # Harmonic amplitude rolloff based on brightness
        rolloff = 0.3 + 0.7 * brightness  # Brighter = less rolloff
        
        # Generate harmonics
        audio = np.zeros_like(t)
        for h in range(1, n_harmonics + 1):
            # Harmonic frequency with optional inharmonicity
            h_freq = freq * h * (1.0 + roughness * 0.1 * (h - 1))
            
            # Amplitude rolloff
            amp = (1.0 / h) ** rolloff
            
            # Add harmonic
            audio += amp * np.sin(2 * np.pi * h_freq * t)
        
        return audio
    
    def _generate_filtered_noise(self, n_samples: int, brightness: float,
                                 roughness: float) -> np.ndarray:
        """
        Generate filtered noise component.
        
        Args:
            n_samples: Number of samples
            brightness: Filter brightness (0-1)
            roughness: Amount of noise (0-1)
            
        Returns:
            Filtered noise audio
        """
        # Generate white noise
        noise = np.random.randn(n_samples)
        
        # Apply simple low-pass filter based on brightness
        if brightness < 0.9:
            window_size = int(2 + (1 - brightness) * 8)
            if window_size > 1:
                kernel = np.ones(window_size) / window_size
                padded = np.pad(noise, window_size, mode='edge')
                noise = np.convolve(padded, kernel, mode='same')[window_size:-window_size]
        
        # Scale by roughness
        noise *= roughness
        
        return noise
    
    def _normalize_and_fade(self, audio: np.ndarray) -> np.ndarray:
        """Normalize and apply fade to avoid clicks."""
        # Normalize
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val
        
        # Fade in/out
        fade_len = min(100, len(audio) // 10)
        if fade_len > 0:
            fade_in = np.linspace(0, 1, fade_len)
            fade_out = np.linspace(1, 0, fade_len)
            audio[:fade_len] *= fade_in
            audio[-fade_len:] *= fade_out
        
        # Master volume
        audio *= 0.3
        
        return audio
    
    def reset(self):
        """Reset synthesizer state."""
        self.phase = 0.0
        self.noise_phase = 0.0
        self.smoothed_params = {
            'pitch_range': 0.5,
            'brightness': 0.6,
            'roughness': 0.3,
            'amplitude': 0.5,
        }
