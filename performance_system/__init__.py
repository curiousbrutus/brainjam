"""
BrainJam Performance System

An AI-mediated musical performance system where brain signals (EEG/fNIRS) serve as
optional expressive control signals, comparable to gesture, timing, or intensity.

This is NOT brain decoding or mind reading. It's an interactive musical instrument
designed for live performance.
"""

__version__ = "0.1.0"

from . import controllers
from . import sound_engines
from . import mapping_models

__all__ = ['controllers', 'sound_engines', 'mapping_models']
