# BrainJam Sound Engines

This document describes the sound synthesis engines available in BrainJam.

All engines are designed for:
- **Low latency** (<50ms per chunk)
- **Real-time control** via continuous parameters
- **Expressive response** to brain/control signals
- **Free and open-source** (no proprietary APIs)

---

## Overview

BrainJam includes three synthesis engines, each with different sonic characteristics:

| Engine | Type | Latency | Best For |
|--------|------|---------|----------|
| **ParametricSynth** | Additive/Subtractive | ~20ms | Stable drones, harmonic textures |
| **DDSPSynth** | Harmonic + Noise | ~25ms | Expressive timbral control |
| **SymbolicSynth** | Note-based | ~30ms | Melodic/rhythmic patterns |

---

## 1. ParametricSynth

**Location**: `performance_system/sound_engines/parametric_synth.py`

### Description

Simple but expressive additive/subtractive synthesizer with continuously controllable parameters. Uses harmonic series with variable rolloff, spectral filtering, and temporal density modulation.

### Control Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `control_1` | 0-1 | **Tempo Density**: Event rate (0=sparse, 1=dense) |
| `control_2` | 0-1 | **Harmonic Tension**: Consonance to dissonance |
| `control_3` | 0-1 | **Spectral Brightness**: Timbral quality (0=dark, 1=bright) |
| `control_4` | 0-1 | **Noise Balance**: Tone vs noise (0=pure, 1=noisy) |

### Example Usage

```python
from performance_system.sound_engines import ParametricSynth

synth = ParametricSynth(sample_rate=44100, base_freq=220.0)

controls = {
    'control_1': 0.5,  # Medium density
    'control_2': 0.3,  # Low tension (consonant)
    'control_3': 0.7,  # Bright
    'control_4': 0.2,  # Mostly tonal
}

audio = synth.generate(duration=0.1, control_params=controls)
```

### Characteristics

- **Stable**: Smooth parameter transitions, no clicks
- **Harmonic**: Rich harmonic content with controllable complexity
- **Fast**: Lowest latency of all engines
- **Suitable for**: Ambient drones, sustained textures, meditation

---

## 2. DDSPSynth

**Location**: `performance_system/sound_engines/ddsp_synth.py`

### Description

DDSP-inspired synthesis using harmonic oscillators and filtered noise. Provides expressive timbral control with natural-sounding frequency-dependent amplitude envelopes.

### Control Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `latent_1` or `control_1` | 0-1 | **Pitch Range**: Base frequency modulation |
| `latent_2` or `control_2` | 0-1 | **Brightness**: Harmonic rolloff / spectral centroid |
| `latent_3` or `control_3` | 0-1 | **Roughness**: Inharmonicity / noise amount |
| `latent_4` or `control_4` | 0-1 | **Amplitude**: Overall volume envelope |

### Example Usage

```python
from performance_system.sound_engines import DDSPSynth

synth = DDSPSynth(sample_rate=44100, base_freq=110.0)  # Low drone

controls = {
    'latent_1': 0.3,   # Low pitch
    'latent_2': 0.8,   # Very bright
    'latent_3': 0.4,   # Some roughness
    'latent_4': 0.6,   # Medium amplitude
}

audio = synth.generate(duration=0.1, control_params=controls)
```

### Characteristics

- **Expressive**: Wide timbral range from smooth to rough
- **Harmonic + Noise**: Natural blend of tonal and textural elements
- **Low Latency**: ~25ms typical
- **Suitable for**: Expressive performance, timbral exploration, evolving textures

---

## 3. SymbolicSynth

**Location**: `performance_system/sound_engines/symbolic_synth.py`

### Description

Note-based synthesizer that generates discrete musical events (notes) based on control parameters. Uses major scale and simple additive synthesis with ADSR envelopes.

### Control Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `latent_1` or `control_1` | 0-1 | **Note Density**: Trigger rate (0=sparse, 1=dense) |
| `latent_2` or `control_2` | 0-1 | **Pitch Center**: Central pitch of notes (0=low, 1=high) |
| `latent_3` or `control_3` | 0-1 | **Note Duration**: Sustain length (0=short, 1=long) |
| `latent_4` or `control_4` | 0-1 | **Harmonic Complexity**: Number of harmonics (0=simple, 1=rich) |

### Example Usage

```python
from performance_system.sound_engines import SymbolicSynth

synth = SymbolicSynth(sample_rate=44100)

controls = {
    'latent_1': 0.7,   # Dense note triggering
    'latent_2': 0.5,   # Middle pitch range
    'latent_3': 0.4,   # Medium note length
    'latent_4': 0.6,   # Moderately complex harmonics
}

audio = synth.generate(duration=0.1, control_params=controls)
```

### Characteristics

- **Discrete**: Generates distinct note events
- **Musical**: Uses major scale (C major by default)
- **Polyphonic**: Multiple simultaneous notes
- **Suitable for**: Melodic patterns, rhythmic exploration, call-and-response

---

## Selecting an Engine

### For Ambient / Drone Music
→ Use **ParametricSynth** or **DDSPSynth**

### For Melodic / Rhythmic Performance
→ Use **SymbolicSynth**

### For Expressive Timbral Control
→ Use **DDSPSynth**

### For AI Co-Performance
→ Use **SymbolicSynth** (discrete events easier for AI response)

---

## Performance Considerations

### Latency Budget

All engines target <50ms synthesis time per 100ms audio chunk:

- **ParametricSynth**: ~20ms (fastest)
- **DDSPSynth**: ~25ms
- **SymbolicSynth**: ~30ms

### CPU Usage

All engines are CPU-efficient and suitable for real-time performance on standard hardware. No GPU required.

### Buffer Sizes

Recommended: 100ms chunks (4410 samples @ 44.1kHz)
- Balances latency and stability
- Allows for smooth parameter interpolation
- Matches typical audio interface settings

---

## Combining Engines

You can layer multiple engines for richer sonic palettes:

```python
from performance_system.sound_engines import DDSPSynth, SymbolicSynth
import numpy as np

ddsp = DDSPSynth(sample_rate=44100, base_freq=110.0)
symbolic = SymbolicSynth(sample_rate=44100)

# Generate from both
audio_ddsp = ddsp.generate(0.1, controls)
audio_symbolic = symbolic.generate(0.1, controls)

# Mix
audio_mixed = 0.6 * audio_ddsp + 0.4 * audio_symbolic
```

---

## Future Engines (Roadmap)

Planned additions:
- **Granular Synth**: Microsound synthesis
- **FM Synth**: Frequency modulation synthesis
- **Physical Models**: Waveguide/modal synthesis
- **Latent Audio Models**: VAE/pretrained model traversal (optional)

---

## Technical Notes

### Sample Rate

All engines default to 44.1kHz. Higher rates are supported but increase CPU load.

### Parameter Smoothing

All engines include internal parameter smoothing to avoid clicks and pops. Smoothing time constant is ~50-100ms.

### Thread Safety

Engines are **not thread-safe**. Use one engine instance per audio thread.

---

## References

- **DDSP**: Engel et al. (2020). "DDSP: Differentiable Digital Signal Processing"
- **Miranda (2014)**: "Brain-Computer Music Interfacing" - Philosophy of control vs decoding
- **Roads (2001)**: "Microsound" - Granular and synthesis techniques

---

**For more examples**, see:
- `performance_system/interaction_demos/demo1_continuous_sound.py`
- `performance_system/interaction_demos/demo2_ai_coperformer.py`
- `streamlit_app/pages/4_Sound_Engine.py`
