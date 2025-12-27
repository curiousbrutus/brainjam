"""
Expressive Mapper

Advanced mapping with many-to-one mappings, hysteresis, parameter drift,
and threshold-based controls. Follows Miranda (2014) philosophy:
expressivity emerges from interaction, not precision.
"""

import numpy as np
from typing import Dict, Optional, List


class ExpressiveMapper:
    """
    Expressive mapper with intentional ambiguity and instability.
    
    Features:
    - Many-to-one mappings (multiple inputs affect each output)
    - Hysteresis (depends on history, not just current state)
    - Parameter drift (slow autonomous change)
    - Thresholds (discrete regions instead of continuous precision)
    - Inertia (resistance to rapid change)
    """
    
    def __init__(self, n_inputs: int = 4, n_outputs: int = 4,
                 use_hysteresis: bool = True, use_drift: bool = True,
                 use_thresholds: bool = True):
        """
        Initialize expressive mapper.
        
        Args:
            n_inputs: Number of input features
            n_outputs: Number of output parameters
            use_hysteresis: Enable hysteresis behavior
            use_drift: Enable autonomous parameter drift
            use_thresholds: Enable threshold-based regions
        """
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.use_hysteresis = use_hysteresis
        self.use_drift = use_drift
        self.use_thresholds = use_thresholds
        
        # Many-to-one mapping weights (each output influenced by multiple inputs)
        self.W = np.random.randn(n_outputs, n_inputs) * 0.3
        # Bias each output to different ranges
        self.b = np.linspace(0.2, 0.8, n_outputs)
        
        # Hysteresis state
        self.prev_input = None
        self.prev_output = None
        self.hysteresis_strength = 0.3
        
        # Drift state
        self.drift_phase = np.random.rand(n_outputs) * 2 * np.pi
        self.drift_rate = 0.05  # Slow drift
        
        # Inertia (resistance to change)
        self.inertia_alpha = 0.85  # Higher = more inertia
        
        # Threshold regions
        self.threshold_levels = 3  # Divide range into N regions
        
    def map(self, input_features: Dict[str, float]) -> Dict[str, float]:
        """
        Map inputs to outputs with expressive characteristics.
        
        Args:
            input_features: Dictionary of input features
            
        Returns:
            Dictionary of output parameters (0-1 range)
        """
        # Convert to array
        x = np.array([input_features.get(f'control_{i+1}', 0.5) 
                     for i in range(self.n_inputs)])
        
        # Many-to-one mapping
        y = self._many_to_one_transform(x)
        
        # Apply hysteresis
        if self.use_hysteresis:
            y = self._apply_hysteresis(x, y)
        
        # Apply drift
        if self.use_drift:
            y = self._apply_drift(y)
        
        # Apply thresholds
        if self.use_thresholds:
            y = self._apply_thresholds(y)
        
        # Apply inertia
        y = self._apply_inertia(y)
        
        # Clip to valid range
        y = np.clip(y, 0.0, 1.0)
        
        # Update state
        self.prev_input = x.copy()
        self.prev_output = y.copy()
        
        # Convert to dict
        return {f'control_{i+1}': float(y[i]) for i in range(self.n_outputs)}
    
    def _many_to_one_transform(self, x: np.ndarray) -> np.ndarray:
        """
        Many-to-one transformation: each output is a weighted sum of all inputs.
        
        Args:
            x: Input array
            
        Returns:
            Transformed output
        """
        # Linear combination
        y = self.W @ x + self.b
        
        # Apply sigmoid for 0-1 range
        y = 1.0 / (1.0 + np.exp(-y))
        
        return y
    
    def _apply_hysteresis(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Apply hysteresis: output depends on direction of change.
        
        Args:
            x: Current input
            y: Current output (before hysteresis)
            
        Returns:
            Output with hysteresis
        """
        if self.prev_input is None or self.prev_output is None:
            return y
        
        # Compute input change direction
        input_change = x - self.prev_input
        input_direction = np.sign(input_change)
        
        # Modify output based on direction and previous output
        # If moving in same direction as before, easier to change
        # If reversing direction, harder to change (hysteresis)
        for i in range(len(y)):
            if input_direction[i] != 0:
                prev_direction = np.sign(self.prev_output[i] - 0.5)
                
                if input_direction[i] == prev_direction:
                    # Same direction: easier to change
                    y[i] = (1 - self.hysteresis_strength) * y[i] + \
                           self.hysteresis_strength * self.prev_output[i]
                else:
                    # Opposite direction: harder to change (more hysteresis)
                    y[i] = (1 - 2 * self.hysteresis_strength) * y[i] + \
                           (2 * self.hysteresis_strength) * self.prev_output[i]
        
        return y
    
    def _apply_drift(self, y: np.ndarray) -> np.ndarray:
        """
        Apply autonomous parameter drift.
        
        Args:
            y: Output array
            
        Returns:
            Output with drift
        """
        # Slow sinusoidal drift
        drift = 0.05 * np.sin(self.drift_phase)
        
        # Update drift phase
        self.drift_phase += self.drift_rate
        
        return y + drift
    
    def _apply_thresholds(self, y: np.ndarray) -> np.ndarray:
        """
        Apply threshold-based discretization.
        
        Args:
            y: Output array
            
        Returns:
            Thresholded output
        """
        # Divide [0, 1] range into discrete regions
        thresholds = np.linspace(0, 1, self.threshold_levels + 1)
        
        y_thresh = np.zeros_like(y)
        for i, val in enumerate(y):
            # Find which region this value falls into
            region = np.digitize(val, thresholds) - 1
            region = np.clip(region, 0, self.threshold_levels - 1)
            
            # Map to center of that region
            region_center = (thresholds[region] + thresholds[region + 1]) / 2
            
            # Smooth transition (not completely discrete)
            smoothness = 0.3
            y_thresh[i] = smoothness * val + (1 - smoothness) * region_center
        
        return y_thresh
    
    def _apply_inertia(self, y: np.ndarray) -> np.ndarray:
        """
        Apply inertia: resistance to rapid change.
        
        Args:
            y: Output array
            
        Returns:
            Output with inertia
        """
        if self.prev_output is None:
            return y
        
        # Exponential smoothing
        return self.inertia_alpha * self.prev_output + (1 - self.inertia_alpha) * y
    
    def set_hysteresis_strength(self, strength: float):
        """Set hysteresis strength (0-1)."""
        self.hysteresis_strength = np.clip(strength, 0.0, 1.0)
    
    def set_drift_rate(self, rate: float):
        """Set drift rate."""
        self.drift_rate = np.clip(rate, 0.0, 0.5)
    
    def set_inertia(self, alpha: float):
        """Set inertia factor (0-1, higher = more inertia)."""
        self.inertia_alpha = np.clip(alpha, 0.0, 0.99)
    
    def reset(self):
        """Reset mapper state."""
        self.prev_input = None
        self.prev_output = None
        self.drift_phase = np.random.rand(self.n_outputs) * 2 * np.pi
