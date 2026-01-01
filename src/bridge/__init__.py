"""
Bridge Module

Connects bio-signal processing to latent space mappings for generative models.
"""

from .latent_mapper import BioSignalInference

__all__ = ['BioSignalInference']
