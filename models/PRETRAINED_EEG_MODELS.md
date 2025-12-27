# Pretrained EEG Models for Feature Extraction

This document outlines strategies for using pretrained EEG models in BrainJam.

## ⚠️ Important Framing

**BrainJam does NOT use EEG for semantic decoding or "mind reading".**

We use pretrained EEG models for:
- **Feature extraction** — learning compact signal representations
- **Dimensionality reduction** — from raw EEG to control latents
- **Temporal modeling** — capturing signal dynamics

We do NOT use them for:
- Mental state classification
- Thought decoding
- Cognitive content interpretation

Brain signals are treated as **continuous control sources**, like gesture or breath.

---

## Recommended Approach: Pretrained Encoders

Instead of training from scratch, we wrap pretrained models to extract control features.

### Strategy

```
Raw EEG → Pretrained Encoder → Control Latents → Musical Parameters
```

### Benefits

1. **No training data required** — Use existing models
2. **Learned representations** — Better than hand-crafted features
3. **Smooth latent spaces** — Good for continuous control
4. **Lightweight** — Fast enough for real-time (<100ms)

---

## Recommended Pretrained Models

### 1. EEGNet-Based Encoders

**What**: Compact CNN for EEG feature extraction

**Paper**: Lawhern et al. (2018) "EEGNet: A Compact Convolutional Neural Network for EEG-based Brain-Computer Interfaces"

**Why**: 
- Very lightweight (~5000 parameters)
- Pretrained on motor imagery/P300 tasks
- Easy to adapt as feature extractor
- Real-time capable

**Usage**:
```python
# Conceptual - not yet implemented
from braindecode.models import EEGNetv4
import torch

# Load pretrained model
encoder = EEGNetv4(
    n_chans=64,
    n_classes=4,
    input_window_samples=128
)

# Use as feature extractor (remove final classification layer)
encoder.eval()
with torch.no_grad():
    # Extract features from second-to-last layer
    features = encoder.forward_features(eeg_window)
    
# Map features to control parameters
control_latents = normalize(features)
```

**Where to Get**:
- `braindecode` library: https://github.com/braindecode/braindecode
- HuggingFace model hub (search "EEGNet")

---

### 2. Braindecode Pretrained Models

**What**: Library of pretrained deep learning models for EEG

**Repository**: https://github.com/braindecode/braindecode

**Models Available**:
- EEGNetv4
- ShallowFBCSPNet
- Deep4Net
- EEGResNet
- TIDNet

**Why**:
- Pretrained on motor imagery, sleep staging, or pathology detection
- Well-documented API
- PyTorch-based (integrates with our pipeline)
- Active development

**Usage**:
```python
from braindecode.models import ShallowFBCSPNet
from braindecode.util import set_random_seeds

# Load pretrained model
model = ShallowFBCSPNet(
    n_chans=22,
    n_classes=4,
    input_window_samples=1000,
    final_conv_length='auto'
)

# Extract features
def extract_control_features(eeg_data):
    with torch.no_grad():
        features = model.extract_features(eeg_data)
        # PCA or learned projection to control dims
        control_vector = pca.transform(features)
    return control_vector
```

**Installation**:
```bash
pip install braindecode
```

---

### 3. Self-Supervised EEG Encoders

**What**: Models trained with contrastive learning on unlabeled EEG

**Examples**:
- **BENDR** (Kostas et al., 2021) - Transformer for EEG
- **LaBraM** (Jiang et al., 2023) - Large brain model
- **BrainBERT** - BERT-style pretraining for EEG

**Why**:
- No task-specific bias (not trained for classification)
- Learn general temporal/spectral patterns
- Better for continuous control than supervised models

**Status**: 
- Research prototypes
- Require more engineering to deploy
- Future direction for BrainJam

**Conceptual Usage**:
```python
# Conceptual - requires custom implementation
from brain_models import BENDR

encoder = BENDR.from_pretrained('bendr-base')
encoder.eval()

# Extract contextualized features
with torch.no_grad():
    features = encoder.encode(eeg_stream)
    # Average or pool to get control vector
    control_latents = features.mean(dim=1)
```

---

## Fallback: Hand-Crafted Features

If pretrained models are too heavy or unavailable:

### Band-Power + PCA

**Current BrainJam approach** (in `performance_system/feature_shaping/`):

```python
# Compute band powers
theta_power = bandpower(eeg, fs, 4, 8)
alpha_power = bandpower(eeg, fs, 8, 13)
beta_power = bandpower(eeg, fs, 13, 30)
gamma_power = bandpower(eeg, fs, 30, 50)

# Stack as feature vector
features = [theta_power, alpha_power, beta_power, gamma_power]

# Optional: PCA for dimensionality reduction
control_latents = pca.transform(features)
```

**Advantages**:
- Fast (real-time capable)
- Interpretable
- No pretrained model required
- Works with any channel count

**Disadvantages**:
- Loses temporal structure
- Less expressive than learned features
- Hand-tuned frequency bands

---

## Implementation Roadmap

### Phase 1: ✅ Current (Hand-Crafted)
- Band-power extraction
- Simple normalization
- Works with mock signals

### Phase 2: 🔜 Wrapper API (Next)
Create unified interface:
```python
from performance_system.feature_extraction import FeatureExtractor

# Choose backend
extractor = FeatureExtractor(
    method='bandpower',  # or 'eegnet', 'braindecode', 'bendr'
    n_outputs=4  # control dimensions
)

# Extract features
control_latents = extractor.extract(eeg_window)
```

### Phase 3: 🔮 Pretrained Models (Future)
- Download pretrained EEGNet from braindecode
- Fine-tune for smooth control (optional)
- Benchmark latency vs. accuracy

### Phase 4: 🔮 Custom Training (Advanced)
- If we collect real performance data:
- Train autoencoder for smooth latent space
- Train contrastive model for expressive features

---

## Model Selection Criteria

When choosing a pretrained model:

1. **Latency**: Can it run <50ms on target hardware?
2. **Channel count**: Does it match our EEG setup?
3. **Latent space**: Are features continuous and smooth?
4. **Availability**: Is it easy to download and use?
5. **License**: Can we use it for research/performance?

**Priority**: **Lightweight > Accuracy**

We care more about real-time performance than classification accuracy.

---

## Wrapper API Design (Proposed)

```python
# performance_system/feature_extraction/eeg_encoder.py

class EEGEncoder:
    """
    Unified interface for EEG feature extraction.
    """
    
    def __init__(self, method='bandpower', n_channels=64, n_controls=4):
        self.method = method
        self.n_channels = n_channels
        self.n_controls = n_controls
        
        if method == 'bandpower':
            self.backend = BandPowerExtractor()
        elif method == 'eegnet':
            self.backend = EEGNetExtractor()
        elif method == 'braindecode':
            self.backend = BraindecodeExtractor()
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def extract_features(self, eeg_window):
        """
        Extract control features from EEG window.
        
        Args:
            eeg_window: (n_channels, n_samples) array
            
        Returns:
            control_vector: (n_controls,) normalized 0-1
        """
        raw_features = self.backend.extract(eeg_window)
        control_vector = normalize_to_controls(raw_features, self.n_controls)
        return control_vector
```

---

## What Pretrained Models Provide

✅ **Smooth embeddings** — Continuous latent representations

✅ **Temporal dynamics** — Learned patterns over time

✅ **Robustness** — Less sensitive to noise than raw band powers

✅ **Expressiveness** — Richer feature space for control

---

## What They Do NOT Provide

❌ **Semantics** — No "thoughts" or "intentions"

❌ **Mental states** — Not decoding cognitive content

❌ **Ground truth** — Features are abstract, not interpretable

❌ **Perfect control** — Still noisy, still need smoothing

---

## Key References

1. **EEGNet**: Lawhern et al. (2018) "EEGNet: A Compact Convolutional Neural Network"
2. **Braindecode**: Schirrmeister et al. (2017) "Deep learning with convolutional neural networks for EEG decoding"
3. **BENDR**: Kostas et al. (2021) "BENDR: Using transformers and a contrastive self-supervised learning task"
4. **LaBraM**: Jiang et al. (2023) "LaBraM: Large Brain Model for Learning Generic Representations"

---

## Current Status in BrainJam

**Implemented**:
- ✅ Band-power feature extraction
- ✅ PCA for dimensionality reduction
- ✅ Mock signals for testing

**Planned**:
- 🔜 Wrapper API for multiple backends
- 🔜 EEGNet integration via braindecode
- 🔜 Optional pretrained encoder plugin

**Future**:
- 🔮 Self-supervised model training
- 🔮 Custom autoencoder for smooth control
- 🔮 Online adaptation during performance

---

## Conclusion

**Pretrained models are optional plugins, not core requirements.**

BrainJam prioritizes:
1. **Modularity** — Swap backends easily
2. **Lightweight** — Real-time capable
3. **Honesty** — No false promises about "mind reading"
4. **Playability** — Smooth, expressive control

Pretrained models **enhance** the system but are **not necessary** for basic functionality.

---

*For implementation details, see `performance_system/feature_shaping/` and `models/README.md`*
