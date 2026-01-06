"""
Rule-Based Beat Generator

Generates rhythmic patterns using rule-based algorithms.
No ML dependencies for maximum reliability and low latency.
Tempo-adaptive with various pattern styles.
"""

import numpy as np
from typing import Dict, Optional, List, Tuple


class BeatGenerator:
    """
    Rule-based beat/rhythm pattern generator.
    
    Features:
    - Multiple rhythm patterns (4/4, 3/4, 6/8, etc.)
    - Tempo-adaptive generation
    - Kick, snare, hi-hat synthesis
    - Swing and groove control
    - Pattern variation and fills
    - No ML dependencies (deterministic and reliable)
    
    Control Parameters:
    - tempo: BPM (40-200)
    - pattern_style: Rhythm pattern type
    - intensity: Pattern density (0.0-1.0)
    - swing: Swing amount (0.0=straight, 1.0=heavy swing)
    - fill_prob: Probability of fills (0.0-1.0)
    """
    
    # Predefined rhythm patterns (kick, snare, hihat)
    PATTERNS = {
        'four_on_floor': {
            'kick': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            'hihat': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        },
        'rock_beat': {
            'kick': [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            'hihat': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        },
        'breakbeat': {
            'kick': [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            'snare': [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
            'hihat': [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
        },
        'minimal': {
            'kick': [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            'snare': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            'hihat': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        },
        'waltz': {  # 3/4 time
            'kick': [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            'snare': [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            'hihat': [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
        },
    }
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize beat generator.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.current_pattern = 'four_on_floor'
        self.beat_position = 0
        
    def _synthesize_kick(self, duration: float = 0.15) -> np.ndarray:
        """
        Synthesize kick drum sound.
        
        Args:
            duration: Duration in seconds
            
        Returns:
            Kick drum audio
        """
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples, endpoint=False)
        
        # Frequency sweep from 150Hz to 40Hz
        freq_start = 150
        freq_end = 40
        freq = freq_start * np.exp(-8 * t / duration) + freq_end
        
        # Generate tone
        phase = 2 * np.pi * np.cumsum(freq) / self.sample_rate
        tone = np.sin(phase)
        
        # Envelope (fast attack, exponential decay)
        envelope = np.exp(-12 * t / duration)
        
        # Add click at attack
        click = np.random.randn(n_samples) * 0.3
        click_env = np.exp(-200 * t / duration)
        click = click * click_env
        
        return (tone * envelope + click) * 0.8
    
    def _synthesize_snare(self, duration: float = 0.12) -> np.ndarray:
        """
        Synthesize snare drum sound.
        
        Args:
            duration: Duration in seconds
            
        Returns:
            Snare drum audio
        """
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples, endpoint=False)
        
        # Tone component (200Hz)
        tone_freq = 200
        tone = np.sin(2 * np.pi * tone_freq * t)
        tone_env = np.exp(-15 * t / duration)
        
        # Noise component (snare wires)
        noise = np.random.randn(n_samples)
        noise_env = np.exp(-8 * t / duration)
        
        # Mix tone and noise
        return (0.3 * tone * tone_env + 0.7 * noise * noise_env) * 0.6
    
    def _synthesize_hihat(self, duration: float = 0.05, open: bool = False) -> np.ndarray:
        """
        Synthesize hi-hat sound.
        
        Args:
            duration: Duration in seconds
            open: Whether hi-hat is open (longer decay)
            
        Returns:
            Hi-hat audio
        """
        if open:
            duration = duration * 4
        
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples, endpoint=False)
        
        # High-frequency noise
        noise = np.random.randn(n_samples)
        
        # Bandpass filter (simulate metallic resonance)
        # Simple approximation using multiple sine waves
        resonance = (
            np.sin(2 * np.pi * 8000 * t) +
            np.sin(2 * np.pi * 10000 * t) +
            np.sin(2 * np.pi * 12000 * t)
        )
        
        # Mix noise and resonance
        signal = 0.7 * noise + 0.3 * resonance
        
        # Envelope
        if open:
            envelope = np.exp(-4 * t / duration)
        else:
            envelope = np.exp(-40 * t / duration)
        
        return signal * envelope * 0.3
    
    def _apply_swing(self, pattern: List[int], swing_amount: float) -> List[Tuple[int, float]]:
        """
        Apply swing timing to pattern.
        
        Args:
            pattern: Binary pattern (0s and 1s)
            swing_amount: Amount of swing (0.0-1.0)
            
        Returns:
            List of (hit, timing_offset) tuples
        """
        result = []
        for i, hit in enumerate(pattern):
            if hit:
                # Apply swing to off-beats
                if i % 2 == 1:
                    offset = swing_amount * 0.1  # Delay off-beats
                else:
                    offset = 0.0
                result.append((i, offset))
        return result
    
    def generate_pattern(
        self,
        duration: float,
        tempo: int = 120,
        pattern_style: str = 'four_on_floor',
        intensity: float = 0.7,
        swing: float = 0.0,
        fill_prob: float = 0.0
    ) -> np.ndarray:
        """
        Generate a rhythmic pattern.
        
        Args:
            duration: Duration in seconds
            tempo: Tempo in BPM
            pattern_style: Pattern type (four_on_floor, rock_beat, breakbeat, minimal, waltz)
            intensity: Pattern density (0.0-1.0)
            swing: Swing amount (0.0-1.0)
            fill_prob: Probability of adding fills (0.0-1.0)
            
        Returns:
            Generated beat audio
        """
        # Get pattern
        if pattern_style not in self.PATTERNS:
            pattern_style = 'four_on_floor'
        
        pattern = self.PATTERNS[pattern_style]
        
        # Calculate timing
        beat_duration = 60.0 / tempo  # Duration of one quarter note
        step_duration = beat_duration / 4  # 16th note duration
        
        # Calculate number of pattern repetitions
        pattern_length = len(pattern['kick'])
        pattern_duration = step_duration * pattern_length
        num_repeats = int(np.ceil(duration / pattern_duration))
        
        # Generate audio
        n_samples = int(duration * self.sample_rate)
        output = np.zeros(n_samples)
        
        for repeat in range(num_repeats):
            # Decide if this repeat should have a fill
            is_fill = (repeat == num_repeats - 1) and (np.random.rand() < fill_prob)
            
            for step in range(pattern_length):
                # Calculate time position
                time_pos = repeat * pattern_duration + step * step_duration
                
                if time_pos >= duration:
                    break
                
                sample_pos = int(time_pos * self.sample_rate)
                
                # Generate kick
                if pattern['kick'][step] and np.random.rand() < intensity:
                    kick = self._synthesize_kick()
                    end_pos = min(sample_pos + len(kick), n_samples)
                    output[sample_pos:end_pos] += kick[:end_pos - sample_pos]
                
                # Generate snare
                if pattern['snare'][step] and np.random.rand() < intensity:
                    snare = self._synthesize_snare()
                    end_pos = min(sample_pos + len(snare), n_samples)
                    output[sample_pos:end_pos] += snare[:end_pos - sample_pos]
                
                # Generate hi-hat
                if pattern['hihat'][step] and np.random.rand() < (intensity * 0.8 + 0.2):
                    # Occasionally open hi-hat on accents
                    is_open = (step % 4 == 2) and (np.random.rand() < 0.3)
                    hihat = self._synthesize_hihat(open=is_open)
                    end_pos = min(sample_pos + len(hihat), n_samples)
                    output[sample_pos:end_pos] += hihat[:end_pos - sample_pos]
                
                # Add fill on last repeat
                if is_fill and step >= pattern_length - 4:
                    # Rapid snare hits
                    if step % 2 == 0:
                        snare = self._synthesize_snare() * 0.7
                        end_pos = min(sample_pos + len(snare), n_samples)
                        output[sample_pos:end_pos] += snare[:end_pos - sample_pos]
        
        # Normalize
        if np.max(np.abs(output)) > 0:
            output = output * 0.8 / np.max(np.abs(output))
        
        return output
    
    def generate(self, duration: float, control_params: Dict[str, float]) -> np.ndarray:
        """
        Generate audio from control parameters (compatible with BrainJam interface).
        
        Args:
            duration: Duration in seconds
            control_params: Dictionary with control parameters:
                - control_1: Maps to tempo (normalized 0-1 → 60-180 BPM)
                - control_2: Maps to intensity (0-1)
                - control_3: Maps to swing (0-1)
                - control_4: Maps to fill_prob (0-1)
                Or specific beat controls:
                - tempo: BPM
                - pattern_style: Pattern type
                - intensity: Density
                - swing: Swing amount
                - fill_prob: Fill probability
                
        Returns:
            Generated beat audio
        """
        # Map generic controls to beat parameters
        if 'tempo' in control_params:
            tempo = int(control_params['tempo'])
        else:
            # Map control_1 to tempo range
            control_1 = control_params.get('control_1', 0.5)
            tempo = int(60 + control_1 * 120)  # 60 to 180 BPM
        
        pattern_style = control_params.get('pattern_style', self.current_pattern)
        intensity = control_params.get('intensity', control_params.get('control_2', 0.7))
        swing = control_params.get('swing', control_params.get('control_3', 0.0))
        fill_prob = control_params.get('fill_prob', control_params.get('control_4', 0.0))
        
        return self.generate_pattern(
            duration=duration,
            tempo=tempo,
            pattern_style=pattern_style,
            intensity=intensity,
            swing=swing,
            fill_prob=fill_prob
        )
    
    def set_pattern(self, pattern_style: str):
        """Set the current pattern style."""
        if pattern_style in self.PATTERNS:
            self.current_pattern = pattern_style
    
    def reset(self):
        """Reset generator state."""
        self.beat_position = 0
