"""
Symbolic MIDI Synthesizer

Converts control parameters to MIDI-like symbolic events, then synthesizes to audio.
This provides a stable, low-latency path: brain → symbolic → audio.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional


class SymbolicSynth:
    """
    Symbolic synthesizer using simple additive synthesis.
    
    Control parameters influence:
    - note_density: How many notes are triggered (0=sparse, 1=dense)
    - pitch_center: Central pitch of generated notes (0=low, 1=high)
    - note_duration: How long notes sustain (0=short, 1=long)
    - harmonic_complexity: Number of harmonics per note (0=simple, 1=complex)
    """
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialize symbolic synthesizer.
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        self.time = 0.0
        self.active_notes = []  # List of (pitch, amplitude, start_time, duration)
        
        # MIDI-like parameters
        self.scale = [0, 2, 4, 5, 7, 9, 11]  # Major scale (C major)
        self.base_midi = 60  # C4
        
        # Smoothed parameters
        self.smoothed_params = {
            'note_density': 0.3,
            'pitch_center': 0.5,
            'note_duration': 0.5,
            'harmonic_complexity': 0.5,
        }
        self.smoothing_alpha = 0.9
        
        # Event generation state
        self.last_event_time = 0.0
        self.event_threshold = 0.5
    
    def generate(self, duration: float, control_params: Dict[str, float]) -> np.ndarray:
        """
        Generate audio from control parameters via symbolic representation.
        
        Args:
            duration: Duration in seconds
            control_params: Dictionary with control parameters (0-1 range)
            
        Returns:
            Audio samples as numpy array (float32)
        """
        n_samples = int(duration * self.sample_rate)
        
        # Map control parameters
        note_density = self._smooth_param('note_density',
                                         control_params.get('latent_1',
                                                           control_params.get('control_1', 0.3)))
        pitch_center = self._smooth_param('pitch_center',
                                         control_params.get('latent_2',
                                                           control_params.get('control_2', 0.5)))
        note_duration = self._smooth_param('note_duration',
                                          control_params.get('latent_3',
                                                            control_params.get('control_3', 0.5)))
        harmonic_complexity = self._smooth_param('harmonic_complexity',
                                                control_params.get('latent_4',
                                                              control_params.get('control_4', 0.5)))
        
        # Decide if new notes should be triggered
        time_since_last = self.time - self.last_event_time
        event_interval = 0.1 + (1.0 - note_density) * 0.9  # 0.1s to 1s
        
        if time_since_last >= event_interval:
            # Trigger new note(s)
            n_notes = 1 + int(note_density * 2)  # 1-3 notes
            for _ in range(n_notes):
                self._trigger_note(pitch_center, note_duration)
            self.last_event_time = self.time
        
        # Render active notes
        audio = self._render_notes(n_samples, harmonic_complexity)
        
        # Advance time
        self.time += duration
        
        # Normalize and apply fade
        audio = self._normalize_and_fade(audio)
        
        return audio.astype(np.float32)
    
    def _smooth_param(self, name: str, new_value: float) -> float:
        """Apply exponential smoothing to parameter."""
        current = self.smoothed_params.get(name, new_value)
        smoothed = self.smoothing_alpha * current + (1 - self.smoothing_alpha) * new_value
        self.smoothed_params[name] = smoothed
        return smoothed
    
    def _trigger_note(self, pitch_center: float, duration_param: float):
        """
        Trigger a new note based on parameters.
        
        Args:
            pitch_center: Central pitch (0-1)
            duration_param: Note duration parameter (0-1)
        """
        # Convert pitch_center to MIDI note
        octave_range = 2  # ±2 octaves
        midi_offset = int((pitch_center - 0.5) * 12 * octave_range)
        
        # Pick a note from the scale
        scale_degree = np.random.randint(len(self.scale))
        midi_note = self.base_midi + midi_offset + self.scale[scale_degree]
        
        # Convert to frequency
        frequency = 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
        
        # Determine duration
        note_duration = 0.1 + duration_param * 0.9  # 0.1s to 1s
        
        # Random amplitude
        amplitude = 0.3 + 0.2 * np.random.rand()
        
        # Add to active notes
        self.active_notes.append({
            'frequency': frequency,
            'amplitude': amplitude,
            'start_time': self.time,
            'duration': note_duration,
        })
    
    def _render_notes(self, n_samples: int, harmonic_complexity: float) -> np.ndarray:
        """
        Render all active notes to audio.
        
        Args:
            n_samples: Number of samples to generate
            harmonic_complexity: Harmonic richness (0-1)
            
        Returns:
            Audio samples
        """
        audio = np.zeros(n_samples)
        t = np.arange(n_samples) / self.sample_rate
        
        # Remove expired notes and render active ones
        active_notes_new = []
        
        for note in self.active_notes:
            note_age = self.time - note['start_time']
            
            if note_age < note['duration']:
                # Note is still active
                active_notes_new.append(note)
                
                # Generate envelope (ADSR-like)
                envelope = self._generate_envelope(t, note_age, note['duration'])
                
                # Generate harmonics
                note_audio = self._generate_note_harmonics(
                    t, note['frequency'], harmonic_complexity
                )
                
                # Apply envelope and amplitude
                audio += note['amplitude'] * envelope * note_audio
        
        self.active_notes = active_notes_new
        
        return audio
    
    def _generate_envelope(self, t: np.ndarray, note_age: float, 
                          duration: float) -> np.ndarray:
        """
        Generate ADSR-like envelope for a note.
        
        Args:
            t: Time vector (relative to current chunk)
            note_age: Age of the note
            duration: Total note duration
            
        Returns:
            Envelope values
        """
        attack_time = 0.01
        decay_time = 0.05
        sustain_level = 0.7
        release_time = 0.1
        
        envelope = np.ones_like(t)
        
        for i, t_val in enumerate(t):
            age = note_age + t_val
            
            if age < attack_time:
                # Attack
                envelope[i] = age / attack_time
            elif age < attack_time + decay_time:
                # Decay
                decay_progress = (age - attack_time) / decay_time
                envelope[i] = 1.0 - (1.0 - sustain_level) * decay_progress
            elif age < duration - release_time:
                # Sustain
                envelope[i] = sustain_level
            else:
                # Release
                release_progress = (age - (duration - release_time)) / release_time
                envelope[i] = sustain_level * (1.0 - release_progress)
        
        return np.clip(envelope, 0.0, 1.0)
    
    def _generate_note_harmonics(self, t: np.ndarray, frequency: float,
                                complexity: float) -> np.ndarray:
        """
        Generate harmonic content for a note.
        
        Args:
            t: Time vector
            frequency: Fundamental frequency
            complexity: Harmonic complexity (0-1)
            
        Returns:
            Audio with harmonics
        """
        n_harmonics = int(1 + complexity * 5)  # 1 to 6 harmonics
        
        audio = np.zeros_like(t)
        for h in range(1, n_harmonics + 1):
            amp = 1.0 / h  # Natural harmonic rolloff
            audio += amp * np.sin(2 * np.pi * frequency * h * t)
        
        return audio
    
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
        audio *= 0.2
        
        return audio
    
    def reset(self):
        """Reset synthesizer state."""
        self.time = 0.0
        self.active_notes = []
        self.last_event_time = 0.0
        self.smoothed_params = {
            'note_density': 0.3,
            'pitch_center': 0.5,
            'note_duration': 0.5,
            'harmonic_complexity': 0.5,
        }
