"""
BrainJam Performance System - Sound Engines Module

Sound engines that can be controlled by continuous parameters from controllers.
"""

from .parametric_synth import ParametricSynth
from .ddsp_synth import DDSPSynth
from .symbolic_synth import SymbolicSynth
from .ddsp_piano_synth import DDSPPianoSynth
from .ddsp_guitar_synth import DDSPGuitarSynth
from .beat_generator import BeatGenerator

__all__ = [
    'ParametricSynth', 
    'DDSPSynth', 
    'SymbolicSynth',
    'DDSPPianoSynth',
    'DDSPGuitarSynth',
    'BeatGenerator'
]
