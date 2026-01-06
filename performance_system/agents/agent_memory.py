"""
GRU Agent Memory Module

Implements GRU-based musical dialogue learning for agent memory.
Trained on JSB Chorales dataset for learning musical patterns and response.
Provides <5ms inference time for real-time performance.

This module enhances the hybrid adaptive agent with learned musical memory
that can anticipate and respond to performer patterns based on past musical context.
"""

import numpy as np
from typing import Dict, Optional, List, Tuple
from collections import deque

# Optional PyTorch for GRU implementation
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    nn = None


class MusicalDialogueGRU(nn.Module if TORCH_AVAILABLE else object):
    """
    GRU-based model for learning musical dialogue patterns.
    
    Architecture:
    - Input: 4-dimensional control vector (intensity, density, tension, variation)
    - GRU: 2 layers, 16 hidden units per layer
    - Output: 4-dimensional response prediction
    
    Trained on JSB Chorales to learn call-and-response patterns in music.
    Optimized for <5ms inference time on CPU.
    """
    
    def __init__(
        self, 
        input_dim: int = 4, 
        hidden_dim: int = 16, 
        output_dim: int = 4,
        num_layers: int = 2
    ):
        """
        Initialize GRU-based dialogue model.
        
        Args:
            input_dim: Input dimension (control parameters)
            hidden_dim: Hidden state dimension
            output_dim: Output dimension (response parameters)
            num_layers: Number of GRU layers
        """
        if not TORCH_AVAILABLE:
            return
        
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_layers = num_layers
        
        # GRU layers
        self.gru = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.0  # No dropout for inference
        )
        
        # Output projection
        self.output_layer = nn.Sequential(
            nn.Linear(hidden_dim, output_dim),
            nn.Tanh()  # Output in [-1, 1], will be scaled
        )
        
        # Initialize hidden state
        self.hidden = None
    
    def forward(self, x, hidden=None):
        """
        Forward pass through GRU.
        
        Args:
            x: Input tensor [batch, seq_len, input_dim] or [seq_len, input_dim]
            hidden: Optional hidden state
            
        Returns:
            output: Predicted response [batch, seq_len, output_dim] or [seq_len, output_dim]
            hidden: Updated hidden state
        """
        # Handle single sequence input
        if x.dim() == 2:
            x = x.unsqueeze(0)  # Add batch dimension
            squeeze_output = True
        else:
            squeeze_output = False
        
        # GRU forward
        gru_out, hidden = self.gru(x, hidden)
        
        # Project to output
        output = self.output_layer(gru_out)
        
        # Remove batch dimension if input was single sequence
        if squeeze_output:
            output = output.squeeze(0)
        
        return output, hidden
    
    def reset_hidden(self):
        """Reset hidden state."""
        self.hidden = None


class AgentMemory:
    """
    Agent memory system with GRU-based musical dialogue learning.
    
    Features:
    - Short-term context window (last 10 control vectors)
    - GRU-based pattern prediction
    - <5ms inference time
    - Learns from JSB Chorales patterns
    - Compatible with HybridAdaptiveAgent
    
    The memory predicts likely musical responses based on recent performer
    control patterns, learned from Bach chorale progressions.
    """
    
    def __init__(
        self,
        context_length: int = 10,
        model_path: Optional[str] = None
    ):
        """
        Initialize agent memory.
        
        Args:
            context_length: Number of past control vectors to remember
            model_path: Path to trained GRU model (optional)
        """
        self.context_length = context_length
        self.context_buffer = deque(maxlen=context_length)
        
        # GRU model
        self.gru_model = None
        self.model_available = False
        
        # Try to load model
        if model_path is None:
            model_path = "models/dialogue_gru.pth"
        
        if TORCH_AVAILABLE and torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu") if TORCH_AVAILABLE else None
        
        if TORCH_AVAILABLE:
            try:
                self.gru_model = MusicalDialogueGRU()
                if self.device:
                    self.gru_model = self.gru_model.to(self.device)
                    self.gru_model.eval()
                
                # Try to load weights if file exists
                import os
                if os.path.exists(model_path):
                    self.gru_model.load_state_dict(
                        torch.load(model_path, map_location=self.device)
                    )
                    self.model_available = True
                    print(f"✓ Loaded GRU dialogue model from {model_path}")
                else:
                    print(f"ℹ GRU model file not found at {model_path}, using untrained model")
                    # Model is initialized but not trained - will give random predictions
            except Exception as e:
                print(f"⚠ Could not load GRU model: {e}")
                self.gru_model = None
                self.model_available = False
        else:
            print("ℹ PyTorch not available, agent memory disabled")
    
    def add_context(self, control_vector: Dict[str, float]):
        """
        Add a control vector to the context buffer.
        
        Args:
            control_vector: Dictionary with control_1, control_2, control_3, control_4
        """
        # Convert to numpy array
        vector = np.array([
            control_vector.get('control_1', 0.5),
            control_vector.get('control_2', 0.5),
            control_vector.get('control_3', 0.5),
            control_vector.get('control_4', 0.5)
        ], dtype=np.float32)
        
        self.context_buffer.append(vector)
    
    def predict_response(self) -> Optional[Dict[str, float]]:
        """
        Predict next musical response based on context.
        
        Returns:
            Predicted response vector or None if model unavailable
        """
        if not self.model_available or not self.gru_model:
            return None
        
        # Need at least some context
        if len(self.context_buffer) == 0:
            return None
        
        try:
            # Convert context to tensor
            context_array = np.array(list(self.context_buffer))
            context_tensor = torch.from_numpy(context_array).float()
            
            if self.device:
                context_tensor = context_tensor.to(self.device)
            
            # Predict (no gradient needed for inference)
            with torch.no_grad():
                prediction, _ = self.gru_model(context_tensor)
                
                # Take last prediction
                pred_vector = prediction[-1].cpu().numpy()
            
            # Scale from [-1, 1] to [0, 1] and clamp
            pred_vector = np.clip((pred_vector + 1.0) / 2.0, 0.0, 1.0)
            
            return {
                'control_1': float(pred_vector[0]),
                'control_2': float(pred_vector[1]),
                'control_3': float(pred_vector[2]),
                'control_4': float(pred_vector[3])
            }
        
        except Exception as e:
            print(f"⚠ Prediction failed: {e}")
            return None
    
    def get_memory_state(self) -> Dict[str, any]:
        """
        Get current memory state for debugging.
        
        Returns:
            Dictionary with memory statistics
        """
        return {
            'context_length': len(self.context_buffer),
            'max_context': self.context_length,
            'model_available': self.model_available,
            'device': str(self.device) if self.device else 'none'
        }
    
    def reset(self):
        """Reset memory state."""
        self.context_buffer.clear()
        if self.gru_model and hasattr(self.gru_model, 'reset_hidden'):
            self.gru_model.reset_hidden()


def blend_memory_response(
    rule_based_output: Dict[str, float],
    memory_prediction: Optional[Dict[str, float]],
    blend_weight: float = 0.2
) -> Dict[str, float]:
    """
    Blend rule-based output with memory prediction.
    
    Args:
        rule_based_output: Output from symbolic rules
        memory_prediction: Output from GRU memory
        blend_weight: Weight for memory prediction (0.0-1.0)
        
    Returns:
        Blended output
    """
    if memory_prediction is None:
        return rule_based_output
    
    # Blend each control parameter
    blended = {}
    for key in rule_based_output:
        if key in memory_prediction:
            rule_val = rule_based_output[key]
            mem_val = memory_prediction[key]
            blended[key] = (1 - blend_weight) * rule_val + blend_weight * mem_val
        else:
            blended[key] = rule_based_output[key]
    
    return blended
