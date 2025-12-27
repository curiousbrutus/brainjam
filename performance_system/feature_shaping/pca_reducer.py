"""
PCA Reducer

Uses Principal Component Analysis to reduce high-dimensional noisy signals
into a small number of latent control parameters.

This is NOT decoding mental states - it's dimensionality reduction for control.
"""

import numpy as np
from typing import Dict, Optional, Union
from sklearn.decomposition import PCA


class PCAReducer:
    """
    PCA-based feature reducer for signal dimensionality reduction.
    
    Reduces noisy, high-dimensional signals to 2-8 continuous control parameters.
    These latents represent intensity, volatility, etc. - NOT decoded thoughts.
    """
    
    def __init__(self, n_components: int = 4, whiten: bool = True):
        """
        Initialize PCA reducer.
        
        Args:
            n_components: Number of principal components (latent controls)
            whiten: Whether to whiten the components (decorrelate and normalize)
        """
        self.n_components = n_components
        self.whiten = whiten
        self.pca = PCA(n_components=n_components, whiten=whiten)
        self.is_fitted = False
        
        # For online normalization
        self.running_min = None
        self.running_max = None
        self.alpha = 0.99  # Smoothing for running stats
        
    def fit(self, X: np.ndarray):
        """
        Fit PCA on training data.
        
        Args:
            X: Training data (n_samples, n_features)
        """
        self.pca.fit(X)
        self.is_fitted = True
        
        # Initialize running statistics
        transformed = self.pca.transform(X)
        self.running_min = np.min(transformed, axis=0)
        self.running_max = np.max(transformed, axis=0)
        
    def transform(self, x: Union[np.ndarray, Dict[str, float]]) -> Dict[str, float]:
        """
        Transform input features to latent controls.
        
        Args:
            x: Input features (dict or array)
            
        Returns:
            Dictionary of normalized latent controls (0-1 range)
        """
        if not self.is_fitted:
            raise RuntimeError("PCAReducer must be fitted before transforming")
        
        # Convert dict to array if needed
        if isinstance(x, dict):
            x_array = np.array([x.get(f'control_{i+1}', 0.5) 
                               for i in range(len(x))])
        else:
            x_array = np.asarray(x)
        
        # Reshape for sklearn
        x_array = x_array.reshape(1, -1)
        
        # Transform
        latent = self.pca.transform(x_array)[0]
        
        # Update running statistics
        if self.running_min is not None:
            self.running_min = self.alpha * self.running_min + (1 - self.alpha) * latent
            self.running_max = self.alpha * self.running_max + (1 - self.alpha) * latent
        
        # Normalize to [0, 1] range
        latent_normalized = self._normalize(latent)
        
        # Convert to dict
        return {f'latent_{i+1}': float(latent_normalized[i]) 
                for i in range(self.n_components)}
    
    def _normalize(self, latent: np.ndarray) -> np.ndarray:
        """
        Normalize latent values to [0, 1] range using running statistics.
        
        Args:
            latent: Latent values
            
        Returns:
            Normalized latent values
        """
        if self.running_min is None or self.running_max is None:
            # Fallback: assume standard normal distribution
            return 1.0 / (1.0 + np.exp(-latent))  # Sigmoid
        
        # Min-max normalization with running statistics
        range_vals = self.running_max - self.running_min + 1e-8
        normalized = (latent - self.running_min) / range_vals
        
        # Clip to [0, 1]
        return np.clip(normalized, 0.0, 1.0)
    
    def get_explained_variance_ratio(self) -> np.ndarray:
        """
        Get the explained variance ratio for each component.
        
        Returns:
            Array of explained variance ratios
        """
        if not self.is_fitted:
            raise RuntimeError("PCAReducer must be fitted first")
        return self.pca.explained_variance_ratio_
    
    def reset_stats(self):
        """Reset running statistics."""
        if self.is_fitted:
            self.running_min = None
            self.running_max = None
