"""
BrainJam Performance System - Feature Shaping Module

Lightweight ML models for reducing noisy signals into 2-8 continuous latent controls.
These latents represent intensity, tension, volatility, density, timing bias - NOT mental states.
"""

from .pca_reducer import PCAReducer
from .autoencoder import SimpleAutoencoder
from .temporal_smoother import TemporalSmoother

__all__ = ['PCAReducer', 'SimpleAutoencoder', 'TemporalSmoother']
