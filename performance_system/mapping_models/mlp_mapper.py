"""
MLP Mapper

Small multi-layer perceptron for nonlinear mapping from controller features
to control parameters. Optimizes for smoothness and controllability.
"""

import numpy as np
from typing import Dict, Optional


class MLPMapper:
    """
    Simple MLP for mapping input features to control parameters.
    
    This provides nonlinear mapping capacity while remaining small and fast
    enough for real-time performance.
    """
    
    def __init__(self, n_inputs: int = 4, n_hidden: int = 8, n_outputs: int = 4):
        """
        Initialize MLP mapper.
        
        Args:
            n_inputs: Number of input features
            n_hidden: Number of hidden units
            n_outputs: Number of output control parameters
        """
        self.n_inputs = n_inputs
        self.n_hidden = n_hidden
        self.n_outputs = n_outputs
        
        # Initialize weights with small random values
        self.W1 = np.random.randn(n_inputs, n_hidden) * 0.1
        self.b1 = np.zeros(n_hidden)
        self.W2 = np.random.randn(n_hidden, n_outputs) * 0.1
        self.b2 = np.zeros(n_outputs)
        
        # Temporal smoothing
        self.prev_output = None
        self.smoothing_alpha = 0.9
    
    def map(self, input_features: Dict[str, float]) -> Dict[str, float]:
        """
        Map input features to output control parameters using MLP.
        
        Args:
            input_features: Dictionary of input features
            
        Returns:
            Dictionary of control parameters (0-1 range)
        """
        # Convert dict to array
        x = np.array([input_features.get(f'control_{i+1}', 0.5) 
                     for i in range(self.n_inputs)])
        
        # Forward pass
        h = np.tanh(x @ self.W1 + self.b1)  # Hidden layer with tanh activation
        y = 1.0 / (1.0 + np.exp(-(h @ self.W2 + self.b2)))  # Output with sigmoid
        
        # Temporal smoothing
        if self.prev_output is not None:
            y = self.smoothing_alpha * self.prev_output + (1 - self.smoothing_alpha) * y
        self.prev_output = y
        
        # Convert back to dict
        output = {f'control_{i+1}': float(y[i]) for i in range(self.n_outputs)}
        
        return output
    
    def train(self, X: np.ndarray, Y: np.ndarray, 
             learning_rate: float = 0.01, n_iterations: int = 100,
             smoothness_weight: float = 0.1):
        """
        Train the MLP with gradient descent.
        
        Args:
            X: Input features (n_samples, n_inputs)
            Y: Target outputs (n_samples, n_outputs)
            learning_rate: Learning rate for gradient descent
            n_iterations: Number of training iterations
            smoothness_weight: Weight for temporal smoothness penalty
        """
        n_samples = X.shape[0]
        
        for iteration in range(n_iterations):
            # Forward pass
            H = np.tanh(X @ self.W1 + self.b1)
            Y_pred = 1.0 / (1.0 + np.exp(-(H @ self.W2 + self.b2)))
            
            # Compute loss
            loss = np.mean((Y_pred - Y) ** 2)
            
            # Add smoothness penalty
            if smoothness_weight > 0 and n_samples > 1:
                Y_diff = np.diff(Y_pred, axis=0)
                smoothness_loss = np.mean(Y_diff ** 2)
                loss += smoothness_weight * smoothness_loss
            
            # Backward pass (gradient descent)
            # Output layer gradients
            dY = (Y_pred - Y) / n_samples
            dY_pred = dY * Y_pred * (1 - Y_pred)  # Sigmoid derivative
            
            dW2 = H.T @ dY_pred
            db2 = np.sum(dY_pred, axis=0)
            
            # Hidden layer gradients
            dH = dY_pred @ self.W2.T
            dH = dH * (1 - H ** 2)  # tanh derivative
            
            dW1 = X.T @ dH
            db1 = np.sum(dH, axis=0)
            
            # Update weights
            self.W2 -= learning_rate * dW2
            self.b2 -= learning_rate * db2
            self.W1 -= learning_rate * dW1
            self.b1 -= learning_rate * db1
            
            # Print progress occasionally
            if iteration % 20 == 0:
                print(f"Iteration {iteration}, Loss: {loss:.6f}")
        
        # Reset smoothing state
        self.prev_output = None
    
    def reset(self):
        """Reset the mapper state."""
        self.prev_output = None
