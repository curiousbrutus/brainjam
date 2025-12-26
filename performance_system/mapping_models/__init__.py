"""
BrainJam Performance System - Mapping Models Module

Neural network models for mapping controller features to latent control parameters.
These models optimize for smoothness, stability, and controllability - NOT accuracy.
"""

from .linear_mapper import LinearMapper
from .mlp_mapper import MLPMapper

__all__ = ['LinearMapper', 'MLPMapper']
