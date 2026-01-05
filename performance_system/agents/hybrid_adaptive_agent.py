"""
Hybrid Adaptive Agent - Co-Performer with Symbolic and Optional ML

This agent combines:
1. Symbolic logic (for reliability and real-time responsiveness)
2. Optional lightweight ML (for personalization based on rehearsal data)

The agent maintains short-term memory of performer control patterns and adapts
its response behavior based on observed intensity and density. It never generates
autonomously - every output is a modulated reflection of performer input.

Design Philosophy:
- Online symbolic adaptation for real-time responsiveness
- Optional offline ML for rehearsal-based personalization
- Never generates autonomously—every output is a modulated reflection of performer input

References:
- Fiebrink, R. (2011). Real-time human-computer interaction with machine learning
- Tanaka, A. (2006). Interaction, experience and the future of music
"""

import numpy as np
from typing import Dict, Optional, List, Any
from collections import deque
import os

# Optional PyTorch for ML personalization
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
    
    class AdaptiveMapperMLP(nn.Module):
        """
        Tiny MLP for personalization adjustment.
        Maps 4 control inputs -> 4 small deltas [-0.1, +0.1]
        """
        def __init__(self, input_dim: int = 4, output_dim: int = 4, hidden_dim: int = 8):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, output_dim),
                nn.Tanh()  # Output in [-1, 1], scaled to [-0.1, 0.1]
            )
        
        def forward(self, x):
            return self.net(x) * 0.1  # Scale to [-0.1, +0.1]
    
except ImportError:
    TORCH_AVAILABLE = False
    AdaptiveMapperMLP = None  # Define as None when torch not available


class HybridAdaptiveAgent:
    """
    Hybrid adaptive co-performer combining symbolic logic and optional ML.
    
    The agent maintains a circular buffer of recent performer control vectors
    and uses exponential moving averages to determine behavioral state:
    - "calm" state: low intensity → low response density
    - "active" state: high intensity → high density, moderate tension
    - "responsive" state: mirror performer's recent patterns
    
    Optional ML model can bias rule-based outputs based on learned preferences.
    """
    
    def __init__(
        self,
        buffer_duration: float = 10.0,
        sample_rate: float = 10.0,
        ema_alpha: float = 0.3,
        model_path: Optional[str] = None
    ):
        """
        Initialize hybrid adaptive agent.
        
        Args:
            buffer_duration: Duration of short-term memory buffer in seconds
            sample_rate: Sampling rate for control vectors in Hz
            ema_alpha: Alpha parameter for exponential moving average (0-1)
            model_path: Path to trained ML model (optional, defaults to models/adaptive_mapper.pth)
        """
        self.buffer_duration = buffer_duration
        self.sample_rate = sample_rate
        self.ema_alpha = ema_alpha
        
        # Short-term memory: circular buffer
        buffer_size = int(buffer_duration * sample_rate)
        self.intensity_buffer = deque(maxlen=buffer_size)
        self.density_buffer = deque(maxlen=buffer_size)
        self.tension_buffer = deque(maxlen=buffer_size)
        self.variation_buffer = deque(maxlen=buffer_size)
        
        # EMA state for intensity and density
        self.ema_intensity = 0.5
        self.ema_density = 0.5
        
        # Behavioral state
        self.state = "responsive"  # calm, active, or responsive
        
        # ML model (optional)
        self.ml_model = None
        self.ml_available = False
        
        # Try to load ML model
        if model_path is None:
            model_path = "models/adaptive_mapper.pth"
        
        if TORCH_AVAILABLE and os.path.exists(model_path):
            try:
                self.ml_model = AdaptiveMapperMLP()
                self.ml_model.load_state_dict(torch.load(model_path, map_location='cpu'))
                self.ml_model.eval()
                self.ml_available = True
                print(f"✓ Loaded ML personalization model from {model_path}")
            except Exception as e:
                print(f"⚠ Could not load ML model from {model_path}: {e}")
                self.ml_model = None
                self.ml_available = False
        elif TORCH_AVAILABLE and model_path:
            print(f"ℹ ML model not found at {model_path}, using rules only")
        elif not TORCH_AVAILABLE:
            print("ℹ PyTorch not available, using rules only")
    
    def _update_buffers(self, controls: Dict[str, float]) -> None:
        """
        Update circular buffers with new control vector.
        
        Args:
            controls: Dictionary with control_1, control_2, control_3, control_4
        """
        # Map controls to semantic dimensions
        # control_1 -> intensity (how energetic/aroused)
        # control_2 -> density (note density/activity level)
        # control_3 -> tension (harmonic tension/dissonance)
        # control_4 -> variation (amount of change/diversity)
        
        intensity = controls.get('control_1', 0.5)
        density = controls.get('control_2', 0.5)
        tension = controls.get('control_3', 0.5)
        variation = controls.get('control_4', 0.5)
        
        self.intensity_buffer.append(intensity)
        self.density_buffer.append(density)
        self.tension_buffer.append(tension)
        self.variation_buffer.append(variation)
    
    def _update_ema(self) -> None:
        """
        Update exponential moving averages for intensity and density.
        """
        if len(self.intensity_buffer) > 0:
            current_intensity = self.intensity_buffer[-1]
            self.ema_intensity = (self.ema_alpha * current_intensity + 
                                 (1 - self.ema_alpha) * self.ema_intensity)
        
        if len(self.density_buffer) > 0:
            current_density = self.density_buffer[-1]
            self.ema_density = (self.ema_alpha * current_density + 
                               (1 - self.ema_alpha) * self.ema_density)
    
    def _determine_state(self) -> str:
        """
        Determine behavioral state based on EMA of intensity.
        
        Returns:
            State string: "calm", "active", or "responsive"
        """
        if self.ema_intensity < 0.3:
            return "calm"
        elif self.ema_intensity > 0.7:
            return "active"
        else:
            return "responsive"
    
    def _rule_based_response(self, controls: Dict[str, float]) -> Dict[str, float]:
        """
        Generate response using symbolic rules based on behavioral state.
        
        Args:
            controls: Current performer control vector
            
        Returns:
            Dictionary with note_density, harmonic_tension, tempo_suggestion, fill_probability
        """
        # Update state
        self.state = self._determine_state()
        
        # Base response depends on state
        if self.state == "calm":
            # Low response density (0.1-0.3)
            note_density = np.clip(0.2 + np.random.uniform(-0.1, 0.1), 0.1, 0.3)
            harmonic_tension = np.clip(0.2 + controls.get('control_3', 0.5) * 0.2, 0.0, 1.0)
            tempo_suggestion = int(np.clip(60 + 20 * self.ema_intensity, 60, 140))
            fill_probability = np.clip(0.1 + 0.1 * self.ema_density, 0.0, 1.0)
            
        elif self.state == "active":
            # High density (0.7-0.9), moderate tension
            note_density = np.clip(0.8 + np.random.uniform(-0.1, 0.1), 0.7, 0.9)
            harmonic_tension = np.clip(0.5 + controls.get('control_3', 0.5) * 0.3, 0.0, 1.0)
            tempo_suggestion = int(np.clip(100 + 40 * self.ema_intensity, 60, 140))
            fill_probability = np.clip(0.6 + 0.3 * self.ema_density, 0.0, 1.0)
            
        else:  # responsive
            # Mirror performer's recent density ±20%
            recent_density = self.ema_density
            density_variation = np.random.uniform(-0.2, 0.2)
            note_density = np.clip(recent_density + density_variation, 0.0, 1.0)
            
            # Respond to performer's tension with slight modulation
            recent_tension = controls.get('control_3', 0.5)
            harmonic_tension = np.clip(recent_tension + np.random.uniform(-0.15, 0.15), 0.0, 1.0)
            
            # Tempo follows intensity
            tempo_suggestion = int(np.clip(80 + 50 * self.ema_intensity, 60, 140))
            
            # Fill probability based on variation
            fill_probability = np.clip(controls.get('control_4', 0.5) * 0.8, 0.0, 1.0)
        
        return {
            'note_density': float(note_density),
            'harmonic_tension': float(harmonic_tension),
            'tempo_suggestion': int(tempo_suggestion),
            'fill_probability': float(fill_probability)
        }
    
    def respond(self, controls: Dict[str, float]) -> Dict[str, float]:
        """
        Generate co-performer response to current control vector.
        
        This is the main interface method. It:
        1. Updates short-term memory buffers
        2. Updates EMAs
        3. Generates rule-based response
        4. Optionally applies ML-based adjustment
        5. Clamps all outputs to valid ranges
        
        Args:
            controls: Dictionary with control_1, control_2, control_3, control_4
            
        Returns:
            Dictionary with:
                - note_density: 0.0-1.0 (how many notes to play)
                - harmonic_tension: 0.0-1.0 (dissonance level)
                - tempo_suggestion: 60-140 BPM
                - fill_probability: 0.0-1.0 (chance of rhythmic fills)
        """
        # Update memory
        self._update_buffers(controls)
        self._update_ema()
        
        # Get rule-based response
        base_output = self._rule_based_response(controls)
        
        # Apply ML adjustment if available
        if self.ml_available and self.ml_model is not None:
            try:
                # Convert controls to tensor
                control_vector = np.array([
                    controls.get('control_1', 0.5),
                    controls.get('control_2', 0.5),
                    controls.get('control_3', 0.5),
                    controls.get('control_4', 0.5)
                ], dtype=np.float32)
                
                with torch.no_grad():
                    control_tensor = torch.from_numpy(control_vector).unsqueeze(0)
                    delta = self.ml_model(control_tensor).squeeze(0).numpy()
                
                # Apply deltas to base output (ML provides small adjustments)
                output_keys = ['note_density', 'harmonic_tension', 'fill_probability']
                for i, key in enumerate(output_keys):
                    if i < len(delta):
                        base_output[key] = np.clip(base_output[key] + delta[i], 0.0, 1.0)
                
                # Tempo adjustment (delta[3] if available, scaled appropriately)
                if len(delta) > 3:
                    tempo_delta = delta[3] * 20  # ±2 BPM (delta range [-0.1, 0.1])
                    base_output['tempo_suggestion'] = int(np.clip(
                        base_output['tempo_suggestion'] + tempo_delta, 60, 140
                    ))
                
            except Exception as e:
                # Silent fallback to rule-based output on ML error
                print(f"⚠ ML adjustment failed: {e}, using rules only")
                pass
        
        # Final safety clamps (never let ML override agency)
        final_output = {
            'note_density': float(np.clip(base_output['note_density'], 0.0, 1.0)),
            'harmonic_tension': float(np.clip(base_output['harmonic_tension'], 0.0, 1.0)),
            'tempo_suggestion': int(np.clip(base_output['tempo_suggestion'], 60, 140)),
            'fill_probability': float(np.clip(base_output['fill_probability'], 0.0, 1.0))
        }
        
        return final_output
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current internal state for debugging/visualization.
        
        Returns:
            Dictionary with internal state information
        """
        return {
            'behavioral_state': self.state,
            'ema_intensity': self.ema_intensity,
            'ema_density': self.ema_density,
            'buffer_length': len(self.intensity_buffer),
            'ml_available': self.ml_available,
        }
    
    def reset(self) -> None:
        """
        Reset agent state (clears buffers and EMAs).
        """
        self.intensity_buffer.clear()
        self.density_buffer.clear()
        self.tension_buffer.clear()
        self.variation_buffer.clear()
        self.ema_intensity = 0.5
        self.ema_density = 0.5
        self.state = "responsive"
