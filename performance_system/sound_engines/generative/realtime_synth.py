"""
Real-Time Synthesis Adapter

Wraps existing BrainJam synthesis engines (parametric, DDSP, symbolic)
with a unified generative backend interface.

This adapter makes traditional synthesis engines compatible with
the generative backend API for consistent control.
"""

from typing import Dict, Optional
import numpy as np


class RealtimeSynthAdapter:
    """
    Adapter for real-time synthesis engines.
    
    Wraps parametric/DDSP synthesizers to expose generative-style control.
    This provides a consistent interface across all sound engines.
    """
    
    def __init__(self, synth_type: str = 'parametric', sample_rate: int = 44100):
        """
        Initialize real-time synth adapter.
        
        Args:
            synth_type: Type of synthesis ('parametric', 'ddsp', 'symbolic')
            sample_rate: Audio sample rate in Hz
        """
        self.synth_type = synth_type
        self.sample_rate = sample_rate
        
        # Import and instantiate the appropriate synthesizer
        if synth_type == 'parametric':
            from ..parametric_synth import ParametricSynth
            self.synth = ParametricSynth(sample_rate=sample_rate)
        elif synth_type == 'ddsp':
            from ..ddsp_synth import DDSPSynth
            self.synth = DDSPSynth(sample_rate=sample_rate)
        elif synth_type == 'symbolic':
            from ..symbolic_synth import SymbolicSynth
            self.synth = SymbolicSynth(sample_rate=sample_rate)
        else:
            raise ValueError(f"Unknown synth_type: {synth_type}")
    
    def generate(
        self,
        duration: float,
        control_params: Dict[str, float],
        prompt: Optional[str] = None
    ) -> np.ndarray:
        """
        Generate audio using control parameters.
        
        Args:
            duration: Duration in seconds
            control_params: Dict of control parameters (0-1 range):
                - intensity: Overall activation/energy
                - density: Event rate/texture density
                - variation: Temporal variability
                - brightness: Spectral quality
            prompt: Optional text prompt (ignored for real-time synths)
        
        Returns:
            audio: Generated audio array (sample_rate * duration,)
        """
        # Map generic control params to synth-specific params
        if self.synth_type == 'parametric':
            synth_params = {
                'tempo_density': control_params.get('density', 0.5),
                'harmonic_tension': control_params.get('intensity', 0.5),
                'spectral_brightness': control_params.get('brightness', 0.5),
                'noise_balance': control_params.get('variation', 0.3)
            }
        else:
            # For DDSP and symbolic, use params directly
            synth_params = control_params
        
        # Generate audio
        audio = self.synth.generate(duration, synth_params)
        
        return audio
    
    def get_info(self) -> Dict[str, str]:
        """
        Get information about this sound engine.
        
        Returns:
            Dict with engine metadata
        """
        return {
            "type": "realtime_synth",
            "synth_backend": self.synth_type,
            "sample_rate": str(self.sample_rate),
            "latency": "<100ms",
            "description": f"Real-time {self.synth_type} synthesis with continuous control"
        }
    
    def get_control_parameters(self) -> Dict[str, str]:
        """
        Get description of control parameters.
        
        Returns:
            Dict mapping parameter names to descriptions
        """
        return {
            "intensity": "Overall activation/energy (0=quiet, 1=intense)",
            "density": "Event rate/texture density (0=sparse, 1=dense)",
            "variation": "Temporal variability (0=stable, 1=chaotic)",
            "brightness": "Spectral quality (0=dark, 1=bright)"
        }
