"""
Mock signal sources for development and testing.

These generators produce structured test signals that simulate
real-time control sources without requiring hardware.
"""

from .mock_eeg import MockEEGController

__all__ = ['MockEEGController']
