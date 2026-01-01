"""
Latent Mapper - BioSignal to Latent Space Bridge

This module acts as the 'brain' of the BrainJam system, processing synchronized
biosignals (EEG, fNIRS, EMG) and mapping them to style vectors for latent diffusion models.

High-performance implementation using NumPy/PyTorch to maintain <100ms latency budget.
"""

import numpy as np
import torch
import torch.nn.functional as F
from typing import Dict, Optional, Tuple, List
from collections import deque


class BioSignalInference:
    """
    Real-time biosignal inference engine that processes synchronized LSL streams
    and maps them to latent space representations for generative models.
    
    Input: 3 synchronized LSL streams (EEG 8ch, fNIRS 2ch, EMG 1ch)
    Output: Style vector [0, 1] for ParametricSynth with conditional triggers
    
    Features:
    - EEG Beta/Alpha ratio → Arousal proxy
    - fNIRS HbO2 slope → Cognitive Load/Valence proxy
    - EMG RMS → Physical Effort proxy
    - Softmax normalization for [0,1] range
    - Conditional tempo/density trigger (180 BPM)
    - Transfer learning hook for fMRI-to-fNIRS alignment
    """
    
    def __init__(
        self,
        eeg_channels: int = 8,
        fnirs_channels: int = 2,
        emg_channels: int = 1,
        sample_rate: float = 250.0,
        buffer_size: int = 500,
        device: str = 'cpu',
        use_gpu: bool = False
    ):
        """
        Initialize BioSignalInference processor.
        
        Args:
            eeg_channels: Number of EEG channels (default: 8)
            fnirs_channels: Number of fNIRS channels (default: 2, HbO2/HbR)
            emg_channels: Number of EMG channels (default: 1)
            sample_rate: Sampling rate in Hz (default: 250)
            buffer_size: Number of samples to buffer for processing (default: 500, ~2s at 250Hz)
            device: PyTorch device ('cpu' or 'cuda')
            use_gpu: Whether to use GPU acceleration if available
        """
        self.eeg_channels = eeg_channels
        self.fnirs_channels = fnirs_channels
        self.emg_channels = emg_channels
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        
        # Device selection for PyTorch operations
        if use_gpu and torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device(device)
        
        # Ring buffers for each signal type (using deque for efficient append/pop)
        self.eeg_buffer = deque(maxlen=buffer_size)
        self.fnirs_buffer = deque(maxlen=buffer_size)
        self.emg_buffer = deque(maxlen=buffer_size)
        
        # EEG band definitions (Hz)
        self.eeg_bands = {
            'alpha': (8.0, 13.0),
            'beta': (13.0, 30.0),
            'theta': (4.0, 8.0),
            'delta': (0.5, 4.0)
        }
        
        # Tempo trigger thresholds
        self.arousal_threshold = 0.8
        self.effort_threshold = 0.7
        self.triggered_bpm = 180
        
        # Softmax temperature for normalization
        self.softmax_temp = 1.0
        
        # Transfer learning projection matrix placeholder
        self.mindvis_projection_matrix = None
        
        # Performance tracking
        self.processing_times = deque(maxlen=100)
        
    def process_frame(
        self,
        eeg_frame: np.ndarray,
        fnirs_frame: np.ndarray,
        emg_frame: np.ndarray
    ) -> Dict[str, float]:
        """
        Process a single frame of synchronized biosignals.
        
        Args:
            eeg_frame: EEG data (n_samples, eeg_channels)
            fnirs_frame: fNIRS data (n_samples, fnirs_channels)
            emg_frame: EMG data (n_samples, emg_channels)
            
        Returns:
            Style vector dictionary with normalized parameters [0, 1]
        """
        import time
        start_time = time.perf_counter()
        
        # Update buffers with new data
        self._update_buffers(eeg_frame, fnirs_frame, emg_frame)
        
        # Extract features from each modality
        arousal = self._compute_eeg_arousal()
        cognitive_load = self._compute_fnirs_load()
        effort = self._compute_emg_effort()
        
        # Map to style vector
        style_vector = self._map_to_style_vector(arousal, cognitive_load, effort)
        
        # Track processing time
        elapsed = (time.perf_counter() - start_time) * 1000  # ms
        self.processing_times.append(elapsed)
        
        return style_vector
    
    def _update_buffers(
        self,
        eeg_frame: np.ndarray,
        fnirs_frame: np.ndarray,
        emg_frame: np.ndarray
    ) -> None:
        """Update ring buffers with new data frames."""
        # Ensure correct shape
        if eeg_frame.ndim == 1:
            eeg_frame = eeg_frame.reshape(-1, self.eeg_channels)
        if fnirs_frame.ndim == 1:
            fnirs_frame = fnirs_frame.reshape(-1, self.fnirs_channels)
        if emg_frame.ndim == 1:
            emg_frame = emg_frame.reshape(-1, self.emg_channels)
        
        # Append samples to buffers
        for sample in eeg_frame:
            self.eeg_buffer.append(sample)
        for sample in fnirs_frame:
            self.fnirs_buffer.append(sample)
        for sample in emg_frame:
            self.emg_buffer.append(sample)
    
    def _compute_eeg_arousal(self) -> float:
        """
        Compute EEG-based arousal proxy via Beta/Alpha ratio.
        
        Higher beta relative to alpha suggests increased arousal/activation.
        
        Returns:
            Arousal level [0, 1]
        """
        if len(self.eeg_buffer) < 100:  # Need minimum samples
            return 0.5
        
        # Convert buffer to array for processing
        eeg_data = np.array(self.eeg_buffer)  # (n_samples, n_channels)
        
        # Compute power spectral density for each channel using Welch's method
        # For performance, use simple FFT-based approach
        alpha_power = self._compute_band_power(eeg_data, *self.eeg_bands['alpha'])
        beta_power = self._compute_band_power(eeg_data, *self.eeg_bands['beta'])
        
        # Beta/Alpha ratio as arousal proxy
        # Add small epsilon to avoid division by zero
        ratio = beta_power / (alpha_power + 1e-8)
        
        # Normalize to [0, 1] using sigmoid-like transformation
        arousal = 1.0 / (1.0 + np.exp(-2.0 * (ratio - 1.0)))
        
        return float(np.clip(arousal, 0.0, 1.0))
    
    def _compute_fnirs_load(self) -> float:
        """
        Compute fNIRS-based cognitive load proxy via HbO2 slope.
        
        Positive HbO2 slope suggests increased cognitive engagement.
        Assumes channel 0 is HbO2, channel 1 is HbR.
        
        Returns:
            Cognitive load/valence [0, 1]
        """
        if len(self.fnirs_buffer) < 50:  # Need minimum samples
            return 0.5
        
        # Convert buffer to array
        fnirs_data = np.array(self.fnirs_buffer)  # (n_samples, n_channels)
        
        # Extract HbO2 channel (assuming channel 0)
        hbo2 = fnirs_data[:, 0]
        
        # Compute slope using linear regression
        n = len(hbo2)
        x = np.arange(n)
        
        # Simple least-squares slope: slope = cov(x,y) / var(x)
        slope = np.cov(x, hbo2)[0, 1] / (np.var(x) + 1e-8)
        
        # Normalize slope to [0, 1]
        # Typical fNIRS slopes are in range [-0.01, 0.01] per sample
        normalized_slope = (np.tanh(slope * 100) + 1.0) / 2.0
        
        return float(np.clip(normalized_slope, 0.0, 1.0))
    
    def _compute_emg_effort(self) -> float:
        """
        Compute EMG-based physical effort proxy via RMS.
        
        Root mean square of EMG signal correlates with muscle activation.
        
        Returns:
            Physical effort [0, 1]
        """
        if len(self.emg_buffer) < 50:  # Need minimum samples
            return 0.5
        
        # Convert buffer to array
        emg_data = np.array(self.emg_buffer)  # (n_samples, n_channels)
        
        # Compute RMS across all channels
        rms = np.sqrt(np.mean(emg_data ** 2))
        
        # Normalize RMS to [0, 1]
        # Typical EMG RMS ranges from 0 to ~100 µV
        # Using adaptive normalization with sigmoid
        normalized_rms = 1.0 / (1.0 + np.exp(-5.0 * (rms - 0.5)))
        
        return float(np.clip(normalized_rms, 0.0, 1.0))
    
    def _compute_band_power(
        self,
        signal: np.ndarray,
        low_freq: float,
        high_freq: float
    ) -> float:
        """
        Compute average power in frequency band using FFT.
        
        Args:
            signal: Signal array (n_samples, n_channels)
            low_freq: Lower frequency bound (Hz)
            high_freq: Upper frequency bound (Hz)
            
        Returns:
            Average band power across channels
        """
        # Use PyTorch for faster FFT computation
        signal_torch = torch.from_numpy(signal.T).float().to(self.device)  # (n_channels, n_samples)
        
        # Compute FFT
        fft = torch.fft.rfft(signal_torch, dim=1)
        power_spectrum = torch.abs(fft) ** 2
        
        # Frequency bins
        n_samples = signal.shape[0]
        freqs = torch.fft.rfftfreq(n_samples, d=1.0/self.sample_rate).to(self.device)
        
        # Find indices for band
        band_mask = (freqs >= low_freq) & (freqs <= high_freq)
        
        # Compute average power in band
        band_power = power_spectrum[:, band_mask].mean().cpu().item()
        
        return band_power
    
    def _map_to_style_vector(
        self,
        arousal: float,
        cognitive_load: float,
        effort: float
    ) -> Dict[str, float]:
        """
        Map extracted features to style vector for ParametricSynth.
        
        Uses softmax normalization to ensure outputs stay in [0, 1] range.
        Applies conditional logic for tempo/density triggering.
        
        Args:
            arousal: EEG-based arousal [0, 1]
            cognitive_load: fNIRS-based cognitive load [0, 1]
            effort: EMG-based physical effort [0, 1]
            
        Returns:
            Style vector with parameters for synthesis
        """
        # Create raw feature vector
        features = torch.tensor(
            [arousal, cognitive_load, effort],
            dtype=torch.float32,
            device=self.device
        )
        
        # Apply softmax for normalization (ensures sum to 1, all positive)
        # Note: We multiply by 3 after softmax to restore [0,1] individual ranges
        normalized = F.softmax(features / self.softmax_temp, dim=0) * 3.0
        normalized = torch.clamp(normalized, 0.0, 1.0)
        
        # Extract normalized values
        norm_arousal = normalized[0].cpu().item()
        norm_cognitive = normalized[1].cpu().item()
        norm_effort = normalized[2].cpu().item()
        
        # Map to synthesis parameters
        # tempo_density: driven by arousal and effort
        # harmonic_tension: driven by cognitive load
        # spectral_brightness: driven by arousal
        # noise_balance: driven by effort
        
        tempo_density = (norm_arousal * 0.6 + norm_effort * 0.4)
        harmonic_tension = norm_cognitive
        spectral_brightness = norm_arousal
        noise_balance = norm_effort
        
        # Conditional trigger: High arousal + High effort → 180 BPM rhythm
        if arousal > self.arousal_threshold and effort > self.effort_threshold:
            tempo_density = 1.0  # Maximum density for 180 BPM pattern
        
        return {
            'tempo_density': float(np.clip(tempo_density, 0.0, 1.0)),
            'harmonic_tension': float(np.clip(harmonic_tension, 0.0, 1.0)),
            'spectral_brightness': float(np.clip(spectral_brightness, 0.0, 1.0)),
            'noise_balance': float(np.clip(noise_balance, 0.0, 1.0)),
            # Additional metadata
            'arousal': float(arousal),
            'cognitive_load': float(cognitive_load),
            'effort': float(effort)
        }
    
    def align_with_mindvis_latent(self, vector: np.ndarray) -> np.ndarray:
        """
        Transfer learning placeholder for fMRI-to-fNIRS alignment.
        
        This function will eventually project fNIRS features into the latent space
        learned from fMRI data (e.g., using MindVis or similar fMRI encoding models).
        
        The projection would align the fNIRS feature space with a pre-trained
        fMRI latent representation, enabling transfer of learned mappings.
        
        Args:
            vector: fNIRS feature vector (n_features,)
            
        Returns:
            Projected vector in aligned latent space
            
        Example future implementation:
            ```python
            # Load pre-trained projection matrix from MindVis alignment
            self.mindvis_projection_matrix = np.load('mindvis_fnirs_projection.npy')
            
            # Apply projection
            aligned_vector = self.mindvis_projection_matrix @ vector
            
            # Optionally apply non-linear transformation
            aligned_vector = self.nonlinear_transform(aligned_vector)
            
            return aligned_vector
            ```
        """
        if self.mindvis_projection_matrix is not None:
            # Apply learned projection
            aligned = self.mindvis_projection_matrix @ vector
            return aligned
        else:
            # Placeholder: return identity mapping
            # In future, this will apply learned fMRI-to-fNIRS alignment
            return vector
    
    def get_performance_stats(self) -> Dict[str, float]:
        """
        Get processing performance statistics.
        
        Returns:
            Dictionary with latency metrics (in milliseconds)
        """
        if len(self.processing_times) == 0:
            return {
                'mean_latency_ms': 0.0,
                'std_latency_ms': 0.0,
                'max_latency_ms': 0.0,
                'p95_latency_ms': 0.0
            }
        
        times = np.array(self.processing_times)
        return {
            'mean_latency_ms': float(np.mean(times)),
            'std_latency_ms': float(np.std(times)),
            'max_latency_ms': float(np.max(times)),
            'p95_latency_ms': float(np.percentile(times, 95))
        }
    
    def reset_buffers(self) -> None:
        """Clear all signal buffers."""
        self.eeg_buffer.clear()
        self.fnirs_buffer.clear()
        self.emg_buffer.clear()
    
    def set_mindvis_projection(self, projection_matrix: np.ndarray) -> None:
        """
        Set the transfer learning projection matrix for fMRI-to-fNIRS alignment.
        
        Args:
            projection_matrix: Learned projection matrix (output_dim, input_dim)
        """
        self.mindvis_projection_matrix = projection_matrix
        print(f"MindVis projection matrix set: {projection_matrix.shape}")
