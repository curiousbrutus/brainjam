"""
Linear Mapper

Simple linear transformation from controller features to control parameters.
Optimizes for smoothness and range coverage.
"""

import numpy as np
from typing import Dict, Optional


class LinearMapper:
    """
    Linear mapping from input features to control parameters.
    
    This is the simplest mapping model, essentially a learned affine transformation.
    It can be useful as a baseline or when the relationship is approximately linear.
    """
    
    def __init__(self, n_inputs: int = 4, n_outputs: int = 4):
        """
        Initialize linear mapper.
        
        Args:
            n_inputs: Number of input features
            n_outputs: Number of output control parameters
        """
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        
        # Initialize with identity-like mapping
        self.W = np.eye(n_outputs, n_inputs)
        self.b = np.zeros(n_outputs)
        
        # Temporal smoothing
        self.prev_output = None
        self.smoothing_alpha = 0.9
    
    def map(self, input_features: Dict[str, float]) -> Dict[str, float]:
        """
        Map input features to output control parameters.
        
        Args:
            input_features: Dictionary of input features
            
        Returns:
            Dictionary of control parameters (0-1 range)
        """
        # Convert dict to array (assuming known order)
        x = np.array([input_features.get(f'control_{i+1}', 0.5) 
                     for i in range(self.n_inputs)])
        
        # Linear transformation
        y = self.W @ x + self.b
        
        # Apply sigmoid to ensure 0-1 range
        y = 1.0 / (1.0 + np.exp(-y))
        
        # Temporal smoothing
        if self.prev_output is not None:
            y = self.smoothing_alpha * self.prev_output + (1 - self.smoothing_alpha) * y
        self.prev_output = y
        
        # Convert back to dict
        output = {f'control_{i+1}': float(y[i]) for i in range(self.n_outputs)}
        
        return output
    
    def train(self, X: np.ndarray, Y: np.ndarray, 
             smoothness_weight: float = 0.1):
        """
        Train the linear mapper with optional smoothness regularization.
        
        Args:
            X: Input features (n_samples, n_inputs)
            Y: Target outputs (n_samples, n_outputs)
            smoothness_weight: Weight for temporal smoothness penalty
        """
        # Add bias term
        X_bias = np.column_stack([X, np.ones(X.shape[0])])
        
        # Compute temporal differences for smoothness penalty
        if smoothness_weight > 0 and X.shape[0] > 1:
            Y_diff = np.diff(Y, axis=0)
            
            # Regularized least squares with smoothness penalty
            # min ||Y - X @ W||^2 + lambda * ||diff(Y)||^2
            XtX = X_bias.T @ X_bias
            XtY = X_bias.T @ Y
            
            # Add smoothness penalty to diagonal
            reg_term = smoothness_weight * np.eye(X_bias.shape[1])
            reg_term[-1, -1] = 0  # Don't regularize bias
            
            W_full = np.linalg.solve(XtX + reg_term, XtY)
        else:
            # Standard least squares
            W_full = np.linalg.lstsq(X_bias, Y, rcond=None)[0]
        
        # Extract weight matrix and bias
        self.W = W_full[:-1, :].T
        self.b = W_full[-1, :]
        
        # Reset smoothing state
        self.prev_output = None
    
    def reset(self):
        """Reset the mapper state."""
        self.prev_output = None
