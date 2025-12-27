"""
Temporal Smoother

Sliding window-based temporal smoothing and embedding for stable control signals.
Reduces jitter and provides temporal context.
"""

import numpy as np
from typing import Dict, Optional, Union
from collections import deque


class TemporalSmoother:
    """
    Temporal smoothing with sliding window for stable, low-jitter control.
    
    Maintains a history of control values and applies smoothing operations
    to reduce rapid fluctuations while preserving meaningful trends.
    """
    
    def __init__(self, n_features: int = 4, window_size: int = 10, 
                 smoothing_mode: str = 'exponential'):
        """
        Initialize temporal smoother.
        
        Args:
            n_features: Number of input features
            window_size: Size of the sliding window
            smoothing_mode: 'exponential', 'moving_average', or 'median'
        """
        self.n_features = n_features
        self.window_size = window_size
        self.smoothing_mode = smoothing_mode
        
        # History buffer
        self.history = deque(maxlen=window_size)
        
        # Exponential smoothing state
        self.ema_state = None
        self.alpha = 0.7  # EMA smoothing factor
        
        # For embedding mode
        self.embedding_dim = min(8, window_size * n_features)
    
    def update(self, x: Union[np.ndarray, Dict[str, float]]) -> Dict[str, float]:
        """
        Update history and return smoothed values.
        
        Args:
            x: New input features (dict or array)
            
        Returns:
            Dictionary of smoothed control values (0-1 range)
        """
        # Convert dict to array if needed
        if isinstance(x, dict):
            x_array = np.array([x.get(f'control_{i+1}', 0.5) 
                               for i in range(self.n_features)])
        else:
            x_array = np.asarray(x)
        
        # Add to history
        self.history.append(x_array.copy())
        
        # Apply smoothing
        if self.smoothing_mode == 'exponential':
            smoothed = self._exponential_smoothing(x_array)
        elif self.smoothing_mode == 'moving_average':
            smoothed = self._moving_average()
        elif self.smoothing_mode == 'median':
            smoothed = self._median_filter()
        else:
            smoothed = x_array
        
        # Convert to dict
        return {f'control_{i+1}': float(np.clip(smoothed[i], 0.0, 1.0)) 
                for i in range(self.n_features)}
    
    def _exponential_smoothing(self, x_new: np.ndarray) -> np.ndarray:
        """
        Apply exponential moving average (EMA) smoothing.
        
        Args:
            x_new: New input values
            
        Returns:
            Smoothed values
        """
        if self.ema_state is None:
            self.ema_state = x_new.copy()
        else:
            self.ema_state = self.alpha * self.ema_state + (1 - self.alpha) * x_new
        
        return self.ema_state
    
    def _moving_average(self) -> np.ndarray:
        """
        Apply simple moving average smoothing.
        
        Returns:
            Smoothed values
        """
        if len(self.history) == 0:
            return np.zeros(self.n_features)
        
        # Convert history to array and compute mean
        history_array = np.array(list(self.history))
        return np.mean(history_array, axis=0)
    
    def _median_filter(self) -> np.ndarray:
        """
        Apply median filter smoothing.
        
        Returns:
            Smoothed values
        """
        if len(self.history) == 0:
            return np.zeros(self.n_features)
        
        # Convert history to array and compute median
        history_array = np.array(list(self.history))
        return np.median(history_array, axis=0)
    
    def get_embedding(self) -> Dict[str, float]:
        """
        Get temporal embedding from sliding window.
        
        This flattens the recent history into a single vector,
        providing temporal context for downstream models.
        
        Returns:
            Dictionary with embedded features
        """
        if len(self.history) == 0:
            # Return zeros if no history
            return {f'embed_{i+1}': 0.0 for i in range(self.embedding_dim)}
        
        # Flatten history
        history_array = np.array(list(self.history))
        flat = history_array.flatten()
        
        # Take first embedding_dim values or pad with zeros
        if len(flat) >= self.embedding_dim:
            embedding = flat[:self.embedding_dim]
        else:
            embedding = np.pad(flat, (0, self.embedding_dim - len(flat)), 
                             mode='constant', constant_values=0)
        
        return {f'embed_{i+1}': float(np.clip(embedding[i], 0.0, 1.0)) 
                for i in range(self.embedding_dim)}
    
    def get_velocity(self) -> Dict[str, float]:
        """
        Compute velocity (rate of change) of control parameters.
        
        Returns:
            Dictionary with velocity values
        """
        if len(self.history) < 2:
            return {f'velocity_{i+1}': 0.0 for i in range(self.n_features)}
        
        # Compute difference between last two values
        current = self.history[-1]
        previous = self.history[-2]
        velocity = current - previous
        
        return {f'velocity_{i+1}': float(velocity[i]) 
                for i in range(self.n_features)}
    
    def reset(self):
        """Reset smoother state."""
        self.history.clear()
        self.ema_state = None
    
    def set_alpha(self, alpha: float):
        """
        Set exponential smoothing factor.
        
        Args:
            alpha: Smoothing factor (0-1), higher = more smoothing
        """
        self.alpha = np.clip(alpha, 0.0, 1.0)
