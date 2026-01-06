"""
DDSP Guitar Synthesizer

Implements a DDSP-based guitar synthesizer inspired by erl-j/ddsp-guitar.
Features polyphonic synthesis with realistic guitar-like timbre and expression.
Supports multiple playing techniques (pluck, strum, harmonics).

Reference: https://github.com/erl-j/ddsp-guitar
"""

import numpy as np
from typing import Dict, Optional, List, Tuple


class DDSPGuitarSynth:
    """
    DDSP-based guitar synthesizer with polyphonic capability and expressive control.
    
    Features:
    - Polyphonic synthesis (up to 6 strings)
    - Realistic pluck and strum articulations
    - String modeling with decay and damping
    - Fret noise and body resonance
    - MIDI pitch control with standard guitar tuning
    - Expressive parameters (pick position, force, muting)
    
    Control Parameters:
    - pitch: MIDI note number or string/fret specification
    - velocity: Pick/pluck force (0.0-1.0)
    - pick_position: Position along string (0.0=bridge, 1.0=neck)
    - damping: String damping amount (0.0=open, 1.0=muted)
    - tone: Tone control (0.0=dark, 1.0=bright)
    - technique: Playing technique (pluck, strum, harmonic)
    """
    
    # Standard guitar tuning (E2, A2, D3, G3, B3, E4)
    STRING_TUNINGS = [40, 45, 50, 55, 59, 64]  # MIDI notes
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize DDSP guitar synthesizer.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.num_strings = 6
        self.active_notes = {}
        
        # Guitar-specific parameters
        self.num_harmonics = 32
        self.body_resonance_freqs = [100, 200, 400]  # Body resonance peaks
        
    def midi_to_freq(self, midi_note: float) -> float:
        """Convert MIDI note to frequency."""
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
    
    def _generate_pluck(
        self,
        freq: float,
        duration: float,
        velocity: float,
        pick_position: float,
        tone: float
    ) -> np.ndarray:
        """
        Generate plucked string sound using Karplus-Strong inspired synthesis.
        
        Args:
            freq: Fundamental frequency in Hz
            duration: Duration in seconds
            velocity: Pluck force (0.0-1.0)
            pick_position: Pick position (0.0=bridge, 1.0=neck)
            tone: Tone control (0.0-1.0)
            
        Returns:
            Audio signal of plucked string
        """
        n_samples = int(duration * self.sample_rate)
        t = np.linspace(0, duration, n_samples, endpoint=False)
        
        # Initialize output
        signal = np.zeros(n_samples)
        
        # Generate harmonics with guitar-like spectral envelope
        for h in range(1, self.num_harmonics + 1):
            harmonic_freq = freq * h
            
            # Skip if above Nyquist
            if harmonic_freq > self.sample_rate / 2:
                break
            
            # Guitar harmonic amplitude envelope
            # Pick position affects odd/even harmonic balance
            if h % 2 == 1:
                # Odd harmonics (more prominent with neck pickup)
                position_factor = 0.5 + pick_position * 0.5
            else:
                # Even harmonics (more prominent with bridge pickup)
                position_factor = 1.5 - pick_position * 0.5
            
            # Base amplitude with rolloff
            base_amp = 1.0 / (h ** (1.2 - tone * 0.4)) * position_factor
            
            # Velocity affects harmonic content
            velocity_factor = 0.7 + velocity * 0.3 * (1.0 - h / self.num_harmonics)
            
            amplitude = base_amp * velocity_factor
            
            # Add slight randomness for realistic timbre
            phase_offset = np.random.uniform(0, 2 * np.pi)
            
            # Generate harmonic with decay
            decay_rate = 2.0 + h * 0.5  # Higher harmonics decay faster
            decay_envelope = np.exp(-decay_rate * t)
            
            harmonic = amplitude * np.sin(2 * np.pi * harmonic_freq * t + phase_offset)
            signal += harmonic * decay_envelope
        
        # Normalize
        if np.max(np.abs(signal)) > 0:
            signal = signal / np.max(np.abs(signal))
        
        return signal
    
    def _apply_pluck_envelope(
        self,
        signal: np.ndarray,
        velocity: float,
        damping: float,
        duration: float
    ) -> np.ndarray:
        """
        Apply guitar pluck envelope with natural decay.
        
        Args:
            signal: Input audio signal
            velocity: Pluck velocity (0.0-1.0)
            damping: Damping amount (0.0-1.0)
            duration: Total duration in seconds
            
        Returns:
            Signal with envelope applied
        """
        n_samples = len(signal)
        t = np.linspace(0, duration, n_samples, endpoint=False)
        
        # Fast attack (pluck is immediate)
        attack_time = 0.002
        attack_samples = int(attack_time * self.sample_rate)
        
        # Decay characteristics
        # Higher velocity = longer sustain before decay
        # Higher damping = faster decay
        base_decay_time = 1.5 + velocity * 1.5
        decay_rate = (1.0 + damping * 3.0) / base_decay_time
        
        # Build envelope
        envelope = np.ones(n_samples)
        
        # Fast attack
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Exponential decay
        if attack_samples < n_samples:
            decay_t = t[attack_samples:]
            envelope[attack_samples:] = np.exp(-decay_rate * decay_t)
        
        # Apply velocity to overall amplitude
        envelope = envelope * (0.4 + velocity * 0.6)
        
        return signal * envelope
    
    def _add_body_resonance(
        self,
        signal: np.ndarray,
        duration: float,
        resonance_amount: float = 0.15
    ) -> np.ndarray:
        """
        Add guitar body resonance (subtle peaks at body cavity frequencies).
        
        Args:
            signal: Input audio signal
            duration: Duration in seconds
            resonance_amount: Amount of resonance to add
            
        Returns:
            Signal with body resonance
        """
        n_samples = len(signal)
        t = np.linspace(0, duration, n_samples, endpoint=False)
        
        resonance = np.zeros(n_samples)
        
        for freq in self.body_resonance_freqs:
            # Bandpass-like resonance
            resonant_wave = np.sin(2 * np.pi * freq * t)
            # Decay over time
            decay = np.exp(-2 * t)
            resonance += resonant_wave * decay
        
        # Mix in subtle resonance
        return signal + resonance_amount * resonance * np.max(np.abs(signal))
    
    def _add_fret_noise(
        self,
        signal: np.ndarray,
        velocity: float,
        noise_amount: float = 0.02
    ) -> np.ndarray:
        """
        Add subtle fret noise for realism.
        
        Args:
            signal: Input audio signal
            velocity: Pluck velocity
            noise_amount: Amount of noise to add
            
        Returns:
            Signal with fret noise
        """
        n_samples = len(signal)
        
        # Generate noise burst at attack
        noise = np.random.randn(n_samples) * noise_amount * velocity
        
        # Apply envelope (only at attack)
        noise_envelope = np.exp(-np.linspace(0, 100, n_samples))
        noise = noise * noise_envelope
        
        return signal + noise
    
    def generate_note(
        self,
        midi_note: float,
        duration: float,
        velocity: float = 0.7,
        pick_position: float = 0.5,
        damping: float = 0.0,
        tone: float = 0.6,
        technique: str = 'pluck'
    ) -> np.ndarray:
        """
        Generate a single guitar note.
        
        Args:
            midi_note: MIDI note number
            duration: Duration in seconds
            velocity: Pick/pluck force (0.0-1.0)
            pick_position: Pick position (0.0=bridge, 1.0=neck)
            damping: String damping (0.0-1.0)
            tone: Tone control (0.0-1.0)
            technique: Playing technique ('pluck', 'strum', 'harmonic')
            
        Returns:
            Audio signal for the note
        """
        # Clamp parameters
        velocity = np.clip(velocity, 0.0, 1.0)
        pick_position = np.clip(pick_position, 0.0, 1.0)
        damping = np.clip(damping, 0.0, 1.0)
        tone = np.clip(tone, 0.0, 1.0)
        
        # Convert to frequency
        freq = self.midi_to_freq(midi_note)
        
        # Generate based on technique
        if technique == 'harmonic':
            # Natural harmonic (emphasize specific harmonics)
            signal = self._generate_pluck(freq * 2, duration, velocity * 0.5, pick_position, tone)
        else:
            # Standard pluck
            signal = self._generate_pluck(freq, duration, velocity, pick_position, tone)
        
        # Apply envelope
        signal = self._apply_pluck_envelope(signal, velocity, damping, duration)
        
        # Add body resonance
        signal = self._add_body_resonance(signal, duration)
        
        # Add fret noise
        signal = self._add_fret_noise(signal, velocity)
        
        # Final normalization
        if np.max(np.abs(signal)) > 0:
            signal = signal * 0.7 / np.max(np.abs(signal))
        
        return signal
    
    def generate_chord(
        self,
        midi_notes: List[float],
        duration: float,
        velocity: float = 0.7,
        strum_time: float = 0.02,
        **kwargs
    ) -> np.ndarray:
        """
        Generate a chord with optional strumming.
        
        Args:
            midi_notes: List of MIDI notes to play
            duration: Duration in seconds
            velocity: Pick force
            strum_time: Time between string hits (0=simultaneous)
            **kwargs: Additional parameters passed to generate_note
            
        Returns:
            Audio signal for the chord
        """
        n_samples = int(duration * self.sample_rate)
        signal = np.zeros(n_samples)
        
        for i, note in enumerate(midi_notes):
            # Generate note
            note_signal = self.generate_note(note, duration, velocity, **kwargs)
            
            # Apply strum delay
            delay_samples = int(i * strum_time * self.sample_rate)
            if delay_samples < n_samples:
                # Add with delay
                available_samples = min(len(note_signal), n_samples - delay_samples)
                signal[delay_samples:delay_samples + available_samples] += note_signal[:available_samples]
        
        # Normalize
        if np.max(np.abs(signal)) > 0:
            signal = signal * 0.8 / np.max(np.abs(signal))
        
        return signal
    
    def generate(self, duration: float, control_params: Dict[str, float]) -> np.ndarray:
        """
        Generate audio from control parameters (compatible with BrainJam interface).
        
        Args:
            duration: Duration in seconds
            control_params: Dictionary with control parameters:
                - control_1: Maps to MIDI pitch
                - control_2: Maps to velocity
                - control_3: Maps to tone
                - control_4: Maps to pick_position
                Or specific guitar controls:
                - pitch/midi_note: MIDI note
                - velocity: Pick force
                - pick_position: Pick position
                - damping: String damping
                - tone: Tone control
                - technique: Playing technique
                
        Returns:
            Generated audio signal
        """
        # Map generic controls to guitar parameters
        if 'pitch' in control_params or 'midi_note' in control_params:
            midi_note = control_params.get('pitch', control_params.get('midi_note', 55))
        else:
            # Map control_1 to guitar range (E2 to E5)
            control_1 = control_params.get('control_1', 0.5)
            midi_note = 40 + control_1 * 36  # E2 to E5
        
        velocity = control_params.get('velocity', control_params.get('control_2', 0.7))
        tone = control_params.get('tone', control_params.get('control_3', 0.6))
        pick_position = control_params.get('pick_position', control_params.get('control_4', 0.5))
        damping = control_params.get('damping', 0.0)
        technique = control_params.get('technique', 'pluck')
        
        return self.generate_note(
            midi_note=midi_note,
            duration=duration,
            velocity=velocity,
            pick_position=pick_position,
            damping=damping,
            tone=tone,
            technique=technique
        )
    
    def reset(self):
        """Reset synthesizer state."""
        self.active_notes.clear()
