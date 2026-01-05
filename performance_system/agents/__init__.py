"""
BrainJam Performance System - Agents Module

This module provides AI co-performers that respond to performer input
with adaptive behavior. Agents never generate autonomously - they always
modulate and reflect performer control signals.
"""

from .hybrid_adaptive_agent import HybridAdaptiveAgent

__all__ = ['HybridAdaptiveAgent']
