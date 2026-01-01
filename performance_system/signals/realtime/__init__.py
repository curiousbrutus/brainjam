"""
Real-time device interfaces for BrainJam.

These are experimental stubs and placeholders for future integration.
Real-time devices include EEG (via LSL), MIDI, and OSC controllers.
"""

from .base_device import BaseDevice
from .eeg_lsl_stub import EEGLSLDevice
from .midi_stub import MIDIDevice
from .osc_stub import OSCDevice

__all__ = ['BaseDevice', 'EEGLSLDevice', 'MIDIDevice', 'OSCDevice']
