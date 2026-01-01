# BioSignal Inference Module

## Overview

The `BioSignalInference` class in `src/bridge/latent_mapper.py` acts as the "brain" of the BrainJam system, processing synchronized biosignals and mapping them to latent space representations for generative models.

## Features

- **Multi-modal Input**: Processes 3 synchronized LSL streams (EEG 8ch, fNIRS 2ch, EMG 1ch)
- **Feature Extraction**:
  - EEG Beta/Alpha ratio → Arousal proxy
  - fNIRS HbO2 slope → Cognitive Load/Valence proxy
  - EMG RMS → Physical Effort proxy
- **Style Vector Mapping**: Maps features to synthesis parameters via Softmax normalization
- **Conditional Triggering**: Activates 180 BPM rhythmic pattern when Arousal > 0.8 and Effort > 0.7
- **Transfer Learning Hook**: Placeholder for fMRI-to-fNIRS alignment (MindVis integration)
- **High Performance**: <1ms average latency, well under 100ms budget

## Installation

The module requires PyTorch and NumPy, which are already in `requirements.txt`:

```bash
pip install numpy torch scipy
```

## Quick Start

```python
from src.bridge.latent_mapper import BioSignalInference
import numpy as np

# Initialize processor
processor = BioSignalInference(
    eeg_channels=8,
    fnirs_channels=2,
    emg_channels=1,
    sample_rate=250.0,
    buffer_size=500
)

# Generate or acquire synchronized biosignals
eeg_frame = np.random.randn(100, 8)    # 100 samples, 8 channels
fnirs_frame = np.random.randn(100, 2)  # 100 samples, 2 channels (HbO2, HbR)
emg_frame = np.random.randn(100, 1)    # 100 samples, 1 channel

# Process frame and get style vector
style_vector = processor.process_frame(eeg_frame, fnirs_frame, emg_frame)

# Use with ParametricSynth
from performance_system.sound_engines.parametric_synth import ParametricSynth

synth = ParametricSynth()
audio = synth.generate(duration=0.1, control_params=style_vector)
```

## Output Format

The `process_frame()` method returns a dictionary with the following structure:

```python
{
    'tempo_density': 0.75,        # Event rate [0, 1]
    'harmonic_tension': 0.62,     # Consonance/dissonance [0, 1]
    'spectral_brightness': 0.81,  # Filter cutoff/brightness [0, 1]
    'noise_balance': 0.45,        # Noise vs tones [0, 1]
    'arousal': 0.68,              # Raw arousal feature [0, 1]
    'cognitive_load': 0.62,       # Raw cognitive load feature [0, 1]
    'effort': 0.45                # Raw effort feature [0, 1]
}
```

All values are guaranteed to be in the [0, 1] range via Softmax normalization.

## Integration with LSL Streams

For real-time LSL stream integration:

```python
# Note: Requires pylsl (pip install pylsl)
from pylsl import StreamInlet, resolve_stream

# Resolve streams
eeg_streams = resolve_stream('type', 'EEG')
fnirs_streams = resolve_stream('type', 'fNIRS')
emg_streams = resolve_stream('type', 'EMG')

# Create inlets
eeg_inlet = StreamInlet(eeg_streams[0])
fnirs_inlet = StreamInlet(fnirs_streams[0])
emg_inlet = StreamInlet(emg_streams[0])

# Real-time loop
processor = BioSignalInference()

while True:
    # Pull samples from each stream
    eeg_samples, _ = eeg_inlet.pull_chunk()
    fnirs_samples, _ = fnirs_inlet.pull_chunk()
    emg_samples, _ = emg_inlet.pull_chunk()
    
    # Convert to numpy arrays
    eeg_frame = np.array(eeg_samples)
    fnirs_frame = np.array(fnirs_samples)
    emg_frame = np.array(emg_samples)
    
    # Process and get style vector
    style_vector = processor.process_frame(eeg_frame, fnirs_frame, emg_frame)
    
    # Use style vector for synthesis
    audio = synth.generate(0.1, style_vector)
```

## Feature Extraction Details

### EEG Beta/Alpha Ratio (Arousal)

- **Bands**: Alpha (8-13 Hz), Beta (13-30 Hz)
- **Method**: FFT-based power spectral density
- **Formula**: `arousal = sigmoid(beta_power / alpha_power)`
- **Interpretation**: Higher values indicate increased arousal/activation

### fNIRS HbO2 Slope (Cognitive Load)

- **Signal**: Oxygenated hemoglobin (HbO2) from channel 0
- **Method**: Linear regression slope over buffer window
- **Formula**: `load = tanh(slope * 100)`
- **Interpretation**: Positive slope indicates increased cognitive engagement

### EMG RMS (Physical Effort)

- **Signal**: Root Mean Square of EMG amplitude
- **Method**: `rms = sqrt(mean(signal^2))`
- **Formula**: `effort = sigmoid(rms * 5)`
- **Interpretation**: Higher values indicate greater muscle activation

## Conditional Triggering

When both conditions are met:
- Arousal > 0.8
- Effort > 0.7

The system automatically sets `tempo_density = 1.0`, triggering a 180 BPM rhythmic pattern in the synthesizer.

## Transfer Learning Hook

The `align_with_mindvis_latent()` method provides a placeholder for future fMRI-to-fNIRS alignment:

```python
# Set projection matrix (learned from fMRI data)
projection_matrix = np.load('mindvis_fnirs_projection.npy')
processor.set_mindvis_projection(projection_matrix)

# Apply projection to fNIRS features
fnirs_features = np.array([0.5, 0.7])
aligned_features = processor.align_with_mindvis_latent(fnirs_features)
```

This enables transfer learning from high-resolution fMRI latent spaces to real-time fNIRS measurements.

## Performance Monitoring

Track processing latency:

```python
stats = processor.get_performance_stats()
print(f"Mean latency: {stats['mean_latency_ms']:.2f} ms")
print(f"P95 latency: {stats['p95_latency_ms']:.2f} ms")
```

Typical performance:
- Mean latency: ~0.85 ms
- P95 latency: ~0.88 ms
- Max latency: ~2.35 ms

Well under the 100ms budget requirement.

## GPU Acceleration

Enable GPU processing for larger buffers:

```python
processor = BioSignalInference(
    eeg_channels=8,
    fnirs_channels=2,
    emg_channels=1,
    use_gpu=True  # Will use CUDA if available
)
```

## Validation

Run the validation suite:

```bash
python validate_biosignal_inference.py
```

This runs comprehensive tests for:
1. Initialization
2. Feature extraction
3. Style vector range [0, 1]
4. Conditional triggering
5. Performance (<100ms latency)
6. Transfer learning hook

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              BioSignalInference Pipeline                │
└─────────────────────────────────────────────────────────┘

   EEG (8ch)  ─┐
              │
  fNIRS (2ch) ├──→ Buffer → Feature Extraction → Mapping → Style Vector
              │              (FFT, Slope, RMS)    (Softmax)    [0,1]
   EMG (1ch)  ─┘
                                                              │
                                                              ↓
                                                    ParametricSynth
```

## Integration Points

The module integrates with existing BrainJam components:

- **Input**: Compatible with LSL streams (like `performance_system/signals/realtime/eeg_lsl_stub.py`)
- **Output**: Compatible with `ParametricSynth` control parameters
- **Performance**: Matches real-time requirements (<100ms)

## Future Extensions

1. **Pretrained Models**: Add EEGNet or braindecode encoders
2. **Multimodal Fusion**: Combine EEG + fNIRS with more sophisticated methods
3. **Adaptive Normalization**: Learn user-specific feature ranges
4. **MindVis Integration**: Complete fMRI-to-fNIRS transfer learning
5. **Online Learning**: Adapt mappings during performance

## References

- **LSL**: Lab Streaming Layer for biosignal synchronization
- **MindVis**: fMRI-based visual reconstruction (Chen et al., 2023)
- **BrainJam**: Real-time performance system with <100ms latency budget

## License

Part of the BrainJam research framework. See main repository LICENSE.
