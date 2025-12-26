"""
BrainJam Performance System - Controllers Module

This module provides expressive control signals for musical performance.
Controllers are NOT treated as semantic "brain reading" but as continuous
control signals comparable to gesture, timing, or intensity in traditional instruments.
"""

from .mock_eeg import MockEEGController
from .keyboard_controller import KeyboardController

__all__ = ['MockEEGController', 'KeyboardController']
