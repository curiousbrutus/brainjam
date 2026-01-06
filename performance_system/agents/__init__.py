"""
BrainJam Performance System - Agents Module

This module provides AI co-performers that respond to performer input
with adaptive behavior. Agents never generate autonomously - they always
modulate and reflect performer control signals.
"""

from .hybrid_adaptive_agent import HybridAdaptiveAgent
from .agent_memory import AgentMemory, MusicalDialogueGRU, blend_memory_response

__all__ = ['HybridAdaptiveAgent', 'AgentMemory', 'MusicalDialogueGRU', 'blend_memory_response']
