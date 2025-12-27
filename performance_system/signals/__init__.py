"""
Signal sources for BrainJam performance system.

This module provides both mock and real-time signal sources for musical control.
All devices expose a unified interface for extracting control parameters.
"""

from .realtime.base_device import BaseDevice

__all__ = ['BaseDevice']
