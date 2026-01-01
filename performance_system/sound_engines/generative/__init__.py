"""
Generative Sound Engines for BrainJam

This module provides adapters for generative AI music models.

Key Principle:
-------------
Brain signals do NOT generate music directly.
Brain signals MODULATE generation parameters.

Generative models are treated as:
- High-level sound engines
- Controllable via continuous parameters
- Partners in co-performance, not autonomous systems
"""

from .realtime_synth import RealtimeSynthAdapter
from .musicgen_adapter import MusicGenAdapter
from .suno_like_adapter import SunoLikeAdapter

__all__ = ['RealtimeSynthAdapter', 'MusicGenAdapter', 'SunoLikeAdapter']
