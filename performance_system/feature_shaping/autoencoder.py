"""
Simple Autoencoder

Small PyTorch autoencoder for learning latent representations of control signals.
This is for expressive control, NOT decoding mental states.
"""

import numpy as np
from typing import Dict, Optional, Union

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available. Install with: pip install torch")


if TORCH_AVAILABLE:
    class AutoencoderNet(nn.Module):
        """
        Simple autoencoder network for dimensionality reduction.
        """
        
        def __init__(self, input_dim: int = 4, latent_dim: int = 2, hidden_dim: int = 8):
            """
            Initialize autoencoder.
            
            Args:
                input_dim: Input feature dimension
                latent_dim: Latent space dimension
                hidden_dim: Hidden layer dimension
            """
            super(AutoencoderNet, self).__init__()
            
            # Encoder
            self.encoder = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.Tanh(),
                nn.Linear(hidden_dim, latent_dim),
            )
            
            # Decoder
            self.decoder = nn.Sequential(
                nn.Linear(latent_dim, hidden_dim),
                nn.Tanh(),
                nn.Linear(hidden_dim, input_dim),
            )
        
        def forward(self, x):
            """Forward pass through autoencoder."""
            latent = self.encoder(x)
            reconstructed = self.decoder(latent)
            return latent, reconstructed
        
        def encode(self, x):
            """Encode input to latent space."""
            return self.encoder(x)


class SimpleAutoencoder:
    """
    Simple autoencoder for learning low-dimensional control representations.
    
    This learns to compress noisy signals into a small latent space that
    captures the essential variations for musical control.
    """
    
    def __init__(self, input_dim: int = 4, latent_dim: int = 2, 
                 hidden_dim: int = 8, device: str = 'cpu'):
        """
        Initialize autoencoder.
        
        Args:
            input_dim: Input feature dimension
            latent_dim: Latent space dimension (2-8 control parameters)
            hidden_dim: Hidden layer dimension
            device: Device to run on ('cpu' or 'cuda')
        """
        if not TORCH_AVAILABLE:
            raise RuntimeError("PyTorch is required for SimpleAutoencoder. "
                             "Install with: pip install torch")
        
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.device = device
        
        # Create network
        self.model = AutoencoderNet(input_dim, latent_dim, hidden_dim).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.criterion = nn.MSELoss()
        
        self.is_fitted = False
        
        # For normalization
        self.running_min = None
        self.running_max = None
        self.alpha = 0.99
    
    def fit(self, X: np.ndarray, epochs: int = 100, batch_size: int = 32, 
            verbose: bool = True):
        """
        Train autoencoder on data.
        
        Args:
            X: Training data (n_samples, n_features)
            epochs: Number of training epochs
            batch_size: Batch size
            verbose: Whether to print progress
        """
        X_tensor = torch.FloatTensor(X).to(self.device)
        n_samples = X.shape[0]
        
        self.model.train()
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            n_batches = 0
            
            # Mini-batch training
            indices = torch.randperm(n_samples)
            for i in range(0, n_samples, batch_size):
                batch_indices = indices[i:i+batch_size]
                batch = X_tensor[batch_indices]
                
                # Forward pass
                latent, reconstructed = self.model(batch)
                loss = self.criterion(reconstructed, batch)
                
                # Backward pass
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                
                epoch_loss += loss.item()
                n_batches += 1
            
            if verbose and epoch % 20 == 0:
                print(f"Epoch {epoch}, Loss: {epoch_loss/n_batches:.6f}")
        
        self.is_fitted = True
        
        # Initialize running statistics
        self.model.eval()
        with torch.no_grad():
            latent, _ = self.model(X_tensor)
            latent_np = latent.cpu().numpy()
            self.running_min = np.min(latent_np, axis=0)
            self.running_max = np.max(latent_np, axis=0)
    
    def transform(self, x: Union[np.ndarray, Dict[str, float]]) -> Dict[str, float]:
        """
        Transform input to latent space.
        
        Args:
            x: Input features (dict or array)
            
        Returns:
            Dictionary of normalized latent controls (0-1 range)
        """
        if not self.is_fitted:
            raise RuntimeError("Autoencoder must be fitted before transforming")
        
        # Convert dict to array if needed
        if isinstance(x, dict):
            x_array = np.array([x.get(f'control_{i+1}', 0.5) 
                               for i in range(self.input_dim)])
        else:
            x_array = np.asarray(x)
        
        # Convert to tensor
        x_tensor = torch.FloatTensor(x_array).unsqueeze(0).to(self.device)
        
        # Encode
        self.model.eval()
        with torch.no_grad():
            latent = self.model.encode(x_tensor)
            latent_np = latent.cpu().numpy()[0]
        
        # Update running statistics
        if self.running_min is not None:
            self.running_min = self.alpha * self.running_min + (1 - self.alpha) * latent_np
            self.running_max = self.alpha * self.running_max + (1 - self.alpha) * latent_np
        
        # Normalize to [0, 1]
        latent_normalized = self._normalize(latent_np)
        
        # Convert to dict
        return {f'latent_{i+1}': float(latent_normalized[i]) 
                for i in range(self.latent_dim)}
    
    def _normalize(self, latent: np.ndarray) -> np.ndarray:
        """
        Normalize latent values to [0, 1] range.
        
        Args:
            latent: Latent values
            
        Returns:
            Normalized latent values
        """
        if self.running_min is None or self.running_max is None:
            # Fallback: use tanh + scale
            return (np.tanh(latent) + 1.0) / 2.0
        
        # Min-max normalization
        range_vals = self.running_max - self.running_min + 1e-8
        normalized = (latent - self.running_min) / range_vals
        
        return np.clip(normalized, 0.0, 1.0)
    
    def reset_stats(self):
        """Reset running statistics."""
        if self.is_fitted:
            self.running_min = None
            self.running_max = None


# Dummy class when PyTorch is not available
if not TORCH_AVAILABLE:
    class SimpleAutoencoder:
        """Dummy autoencoder when PyTorch is not available."""
        
        def __init__(self, *args, **kwargs):
            raise RuntimeError("PyTorch is required for SimpleAutoencoder. "
                             "Install with: pip install torch")
