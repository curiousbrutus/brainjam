"""
BrainJam Performance System - Controllers Module

This module provides expressive control signals for musical performance.
Controllers are NOT treated as semantic "brain reading" but as continuous
control signals comparable to gesture, timing, or intensity in traditional instruments.

NOTE: This module maintains backward compatibility. New code should use:
    from performance_system.signals.mock import MockEEGController
    from performance_system.signals.realtime import EEGLSLDevice, MIDIDevice, OSCDevice
"""

from .mock_eeg import MockEEGController
from .keyboard_controller import KeyboardController

# For convenience, also import from new signal module structure
try:
    from ..signals.realtime import BaseDevice, EEGLSLDevice, MIDIDevice, OSCDevice
    __all__ = ['MockEEGController', 'KeyboardController', 
               'BaseDevice', 'EEGLSLDevice', 'MIDIDevice', 'OSCDevice']
except ImportError:
    __all__ = ['MockEEGController', 'KeyboardController']
