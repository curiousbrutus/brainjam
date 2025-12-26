"""
Parametric Synthesizer

A simple but expressive additive/subtractive synthesizer with continuously
controllable parameters suitable for real-time performance.
"""

import numpy as np
from typing import Dict, Optional


class ParametricSynth:
    """
    Parametric synthesizer with real-time controllable parameters.
    
    Controllable parameters:
    - tempo_density: How many events/notes per second (0=sparse, 1=dense)
    - harmonic_tension: Amount of dissonance (0=consonant, 1=dissonant)
    - spectral_brightness: Filter cutoff/brightness (0=dark, 1=bright)
    - noise_balance: Mix of noise vs tones (0=pure tones, 1=noisy)
    """
    
    def __init__(self, sample_rate: int = 44100, base_freq: float = 220.0):
        """
        Initialize synthesizer.
        
        Args:
            sample_rate: Audio sample rate in Hz
            base_freq: Base frequency in Hz (default A3)
        """
        self.sample_rate = sample_rate
        self.base_freq = base_freq
        self.phase = 0.0
        self.event_phase = 0.0
        
        # Smoothed parameter state (for avoiding clicks)
        self.smoothed_params = {
            'tempo_density': 0.5,
            'harmonic_tension': 0.3,
            'spectral_brightness': 0.6,
            'noise_balance': 0.2,
        }
        self.smoothing_alpha = 0.95  # Higher = more smoothing
        
    def generate(self, duration: float, control_params: Dict[str, float]) -> np.ndarray:
        """
        Generate audio based on control parameters.
        
        Args:
            duration: Duration in seconds
            control_params: Dictionary with control parameters (0-1 range)
            
        Returns:
            Audio samples as numpy array (float32)
        """
        n_samples = int(duration * self.sample_rate)
        t = (self.phase + np.arange(n_samples)) / self.sample_rate
        
        # Map generic control parameters to synth parameters
        # This mapping can be customized for different expressive goals
        tempo_density = self._smooth_param('tempo_density', 
                                          control_params.get('control_1', 0.5))
        harmonic_tension = self._smooth_param('harmonic_tension', 
                                             control_params.get('control_2', 0.3))
        spectral_brightness = self._smooth_param('spectral_brightness', 
                                                control_params.get('control_3', 0.6))
        noise_balance = self._smooth_param('noise_balance', 
                                          control_params.get('control_4', 0.2))
        
        # Generate base oscillator
        audio = self._generate_oscillators(t, harmonic_tension)
        
        # Apply spectral filtering
        audio = self._apply_brightness_filter(audio, spectral_brightness)
        
        # Mix in noise
        noise = np.random.randn(n_samples) * 0.1
        audio = (1 - noise_balance) * audio + noise_balance * noise
        
        # Apply temporal density envelope
        envelope = self._generate_density_envelope(t, tempo_density)
        audio *= envelope
        
        # Normalize and apply fade
        audio = self._normalize_and_fade(audio)
        
        self.phase += n_samples
        self.event_phase += duration
        
        return audio.astype(np.float32)
    
    def _smooth_param(self, name: str, new_value: float) -> float:
        """
        Apply exponential smoothing to parameter for stable transitions.
        
        Args:
            name: Parameter name
            new_value: New parameter value
            
        Returns:
            Smoothed parameter value
        """
        current = self.smoothed_params.get(name, new_value)
        smoothed = self.smoothing_alpha * current + (1 - self.smoothing_alpha) * new_value
        self.smoothed_params[name] = smoothed
        return smoothed
    
    def _generate_oscillators(self, t: np.ndarray, tension: float) -> np.ndarray:
        """
        Generate harmonic oscillators with controllable tension.
        
        Args:
            t: Time vector
            tension: Amount of harmonic dissonance (0-1)
            
        Returns:
            Mixed oscillator output
        """
        # Base frequency with slight modulation
        freq_mod = 1.0 + 0.02 * np.sin(2 * np.pi * 0.5 * self.event_phase)
        base_freq = self.base_freq * freq_mod
        
        # Harmonic series with tension-dependent amplitudes
        harmonics = [1, 2, 3, 4, 5, 7, 9]
        
        # Low tension = simple harmonics, high tension = complex/inharmonic
        if tension < 0.5:
            # Consonant: standard harmonic series
            amps = [1.0, 0.5, 0.3, 0.2, 0.15, 0.1, 0.05]
        else:
            # Dissonant: emphasize odd harmonics and add microtonal shifts
            amps = [1.0, 0.3, 0.6, 0.2, 0.5, 0.4, 0.3]
            # Add slight detuning for tension
            harmonics = [h * (1 + (tension - 0.5) * 0.1 * (h % 2)) 
                        for h in harmonics]
        
        # Scale amplitudes by (1 - tension) for higher partials
        amps = [a * (1 - 0.5 * tension) ** i for i, a in enumerate(amps)]
        
        # Generate and sum harmonics
        audio = np.zeros_like(t)
        for harmonic, amp in zip(harmonics, amps):
            audio += amp * np.sin(2 * np.pi * base_freq * harmonic * t)
        
        return audio
    
    def _apply_brightness_filter(self, audio: np.ndarray, brightness: float) -> np.ndarray:
        """
        Apply simple brightness filter (simplified low-pass).
        
        Args:
            audio: Input audio
            brightness: Filter brightness (0=dark, 1=bright)
            
        Returns:
            Filtered audio
        """
        # Simple moving average for low-pass effect
        # Higher brightness = less filtering
        if brightness < 0.95:
            window_size = int(5 * (1 - brightness) + 1)
            if window_size > 1:
                kernel = np.ones(window_size) / window_size
                # Pad to avoid edge effects
                padded = np.pad(audio, window_size, mode='edge')
                filtered = np.convolve(padded, kernel, mode='same')
                audio = filtered[window_size:-window_size]
        
        return audio
    
    def _generate_density_envelope(self, t: np.ndarray, density: float) -> np.ndarray:
        """
        Generate temporal envelope based on density parameter.
        
        Args:
            t: Time vector
            density: Tempo/event density (0=sparse, 1=dense)
            
        Returns:
            Amplitude envelope
        """
        # Map density to event rate (events per second)
        event_rate = 0.5 + density * 4.5  # 0.5 to 5 Hz
        
        # Generate pulsing envelope
        pulse = 0.5 + 0.5 * np.sin(2 * np.pi * event_rate * t)
        
        # Add some randomness for organic feel
        noise_mod = 1.0 + 0.1 * np.sin(2 * np.pi * 0.3 * self.event_phase)
        
        envelope = pulse * noise_mod
        
        # Ensure minimum amplitude for audibility
        envelope = 0.3 + 0.7 * envelope
        
        return envelope
    
    def _normalize_and_fade(self, audio: np.ndarray) -> np.ndarray:
        """
        Normalize audio and apply fade in/out to avoid clicks.
        
        Args:
            audio: Input audio
            
        Returns:
            Normalized and faded audio
        """
        # Normalize
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val
        
        # Apply fade to avoid clicks
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
        self.event_phase = 0.0
        self.smoothed_params = {
            'tempo_density': 0.5,
            'harmonic_tension': 0.3,
            'spectral_brightness': 0.6,
            'noise_balance': 0.2,
        }
