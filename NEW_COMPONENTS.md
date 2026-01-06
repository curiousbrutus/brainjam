# New Components Documentation

This document describes the 5 new components added to the BrainJam performance system.

## Overview

These components expand BrainJam's capabilities with:
1. **DDSP Piano Synth** - Realistic piano synthesis
2. **DDSP Guitar Synth** - Polyphonic guitar synthesis  
3. **Beat Generator** - Rule-based rhythm patterns
4. **Agent Memory** - GRU-based musical dialogue learning
5. **EEG Mapper** - EEGNet-based EEG-to-control mapping

All components integrate seamlessly with the existing BrainJam architecture and the Hybrid Adaptive Agent.

---

## 1. DDSP Piano Synth

### Overview
DDSP-based piano synthesizer with realistic envelope and harmonic structure. Inspired by [lrenault/ddsp-piano](https://github.com/lrenault/ddsp-piano).

### Features
- Harmonic additive synthesis with piano-like partials
- ADSR envelope with piano-characteristic decay
- Velocity-sensitive timbre and dynamics
- MIDI pitch control (A0-C8, MIDI 21-108)
- Sympathetic resonance modeling
- Lightweight (<5ms generation time)

### Usage

```python
from performance_system.sound_engines import DDSPPianoSynth

# Initialize
piano = DDSPPianoSynth(sample_rate=44100)

# Generate a note
audio = piano.generate_note(
    midi_note=60,      # Middle C
    duration=2.0,      # 2 seconds
    velocity=0.8,      # Hard hit
    brightness=0.7,    # Bright timbre
    sustain=0.5,       # Sustain pedal half-down
    resonance=0.3      # Sympathetic resonance
)

# Or use control interface
audio = piano.generate(duration=2.0, control_params={
    'control_1': 0.5,  # Maps to pitch
    'control_2': 0.8,  # Maps to velocity
    'control_3': 0.7,  # Maps to brightness
    'control_4': 0.3   # Maps to resonance
})
```

### Parameters
- **midi_note** (21-108): MIDI note number (float for pitch bend)
- **velocity** (0.0-1.0): Key velocity (harder = brighter, louder)
- **brightness** (0.0-1.0): Harmonic content (0=dark, 1=bright)
- **sustain** (0.0-1.0): Sustain pedal amount
- **resonance** (0.0-1.0): Sympathetic resonance amount

---

## 2. DDSP Guitar Synth

### Overview
DDSP-based guitar synthesizer with polyphonic capability. Inspired by [erl-j/ddsp-guitar](https://github.com/erl-j/ddsp-guitar).

### Features
- Polyphonic synthesis (up to 6 strings)
- Realistic pluck and strum articulations
- String modeling with decay and damping
- Fret noise and body resonance
- Multiple playing techniques (pluck, strum, harmonic)
- Expressive control parameters

### Usage

```python
from performance_system.sound_engines import DDSPGuitarSynth

# Initialize
guitar = DDSPGuitarSynth(sample_rate=44100)

# Generate a single note
audio = guitar.generate_note(
    midi_note=55,         # G
    duration=2.0,
    velocity=0.7,
    pick_position=0.5,    # Middle of string
    damping=0.0,          # Open string
    tone=0.6,             # Medium tone
    technique='pluck'     # or 'strum', 'harmonic'
)

# Generate a chord
chord_notes = [55, 59, 62]  # G major (G, B, D)
audio = guitar.generate_chord(
    chord_notes,
    duration=2.0,
    velocity=0.7,
    strum_time=0.02       # 20ms strum delay
)

# Or use control interface
audio = guitar.generate(duration=2.0, control_params={
    'control_1': 0.5,  # Maps to pitch
    'control_2': 0.7,  # Maps to velocity
    'control_3': 0.6,  # Maps to tone
    'control_4': 0.5   # Maps to pick_position
})
```

### Parameters
- **midi_note**: MIDI note number
- **velocity** (0.0-1.0): Pick/pluck force
- **pick_position** (0.0-1.0): 0=bridge (bright), 1=neck (warm)
- **damping** (0.0-1.0): String damping (0=open, 1=muted)
- **tone** (0.0-1.0): Tone control (0=dark, 1=bright)
- **technique**: 'pluck', 'strum', or 'harmonic'

---

## 3. Beat Generator

### Overview
Rule-based rhythm pattern generator. No ML dependencies for maximum reliability.

### Features
- Multiple rhythm patterns (4/4, 3/4, 6/8, breakbeat, etc.)
- Tempo-adaptive (60-180 BPM)
- Kick, snare, hi-hat synthesis
- Swing and groove control
- Pattern variation and fills
- Deterministic and reliable

### Usage

```python
from performance_system.sound_engines import BeatGenerator

# Initialize
beats = BeatGenerator(sample_rate=44100)

# Generate a pattern
audio = beats.generate_pattern(
    duration=4.0,
    tempo=120,
    pattern_style='four_on_floor',  # or 'rock_beat', 'breakbeat', etc.
    intensity=0.8,                  # Pattern density
    swing=0.2,                      # Swing amount
    fill_prob=0.3                   # Probability of fills
)

# Or use control interface
audio = beats.generate(duration=4.0, control_params={
    'control_1': 0.5,  # Maps to tempo (60-180 BPM)
    'control_2': 0.8,  # Maps to intensity
    'control_3': 0.2,  # Maps to swing
    'control_4': 0.3   # Maps to fill_prob
})
```

### Available Patterns
- **four_on_floor**: Dance/electronic kick on every beat
- **rock_beat**: Standard rock backbeat
- **breakbeat**: Syncopated breakbeat pattern
- **minimal**: Sparse, minimal techno
- **waltz**: 3/4 time signature

### Parameters
- **tempo** (60-180): Beats per minute
- **pattern_style**: Rhythm pattern type
- **intensity** (0.0-1.0): Pattern density/activity
- **swing** (0.0-1.0): Swing timing amount
- **fill_prob** (0.0-1.0): Probability of drum fills

---

## 4. Agent Memory (GRU)

### Overview
GRU-based musical dialogue learning for agent memory. Learns patterns from JSB Chorales dataset.

### Features
- GRU architecture (2 layers, 16 hidden units)
- <5ms inference time
- Context window of last 10 control vectors
- Predicts likely musical responses
- Optional blending with rule-based systems
- Compatible with HybridAdaptiveAgent

### Usage

```python
from performance_system.agents import AgentMemory, blend_memory_response

# Initialize
memory = AgentMemory(context_length=10)

# Add control vectors over time
for controls in control_sequence:
    memory.add_context(controls)

# Predict next response
prediction = memory.predict_response()

# Blend with rule-based output
rule_output = {'control_1': 0.5, 'control_2': 0.6, ...}
final_output = blend_memory_response(
    rule_based_output=rule_output,
    memory_prediction=prediction,
    blend_weight=0.2  # 20% memory, 80% rules
)

# Get memory state
state = memory.get_memory_state()
```

### Architecture
- **Input**: 4-dimensional control vector (intensity, density, tension, variation)
- **GRU**: 2 layers, 16 hidden units per layer
- **Output**: 4-dimensional response prediction
- **Training**: JSB Chorales dataset (Bach chorales)

### Model File
Place trained model at `models/dialogue_gru.pth` for automatic loading.

---

## 5. EEG Mapper

### Overview
EEGNet-based EEG-to-control mapping for real EEG hardware and OpenMIIR dataset compatibility.

### Features
- EEGNet architecture (~5000 parameters)
- Real EEG hardware compatible
- <10ms inference time
- OpenMIIR dataset trained (optional)
- Simple bandpower fallback when model unavailable
- 4 control outputs mapped from brain activity

### Usage

```python
from performance_system.mapping_models import EEGMapper

# Initialize
eeg_mapper = EEGMapper(
    n_channels=8,
    sample_rate=250.0,
    window_size=0.5
)

# Map EEG data to controls
eeg_data = np.random.randn(8, 125)  # [n_channels, n_samples]
controls = eeg_mapper.map_eeg_to_controls(eeg_data)
# Returns: {'control_1': 0.7, 'control_2': 0.5, ...}

# Get mapper info
info = eeg_mapper.get_mapper_info()
```

### Control Outputs
- **control_1**: Arousal/intensity (from beta/gamma activity)
- **control_2**: Focus/attention (from alpha suppression)
- **control_3**: Valence/emotion (from frontal asymmetry)
- **control_4**: Engagement (from theta/alpha ratio)

### EEGNet Architecture
- Temporal convolution (learns frequency filters)
- Depthwise convolution (learns spatial filters)
- Separable convolution (feature extraction)
- Dense layers (control parameter mapping)

### Model File
Place trained model at `models/eegnet_mapper.pth` for automatic loading.

### Fallback Mode
When model unavailable, uses simple bandpower features:
- Variance-based activity estimation
- Spatial variation detection
- Safe and predictable fallback

---

## Integration with Hybrid Adaptive Agent

All components work seamlessly with the Hybrid Adaptive Agent:

```python
from performance_system.agents import HybridAdaptiveAgent, AgentMemory
from performance_system.sound_engines import DDSPPianoSynth, BeatGenerator
from performance_system.mapping_models import EEGMapper

# Initialize components
agent = HybridAdaptiveAgent()
memory = AgentMemory()
piano = DDSPPianoSynth()
beats = BeatGenerator()
eeg_mapper = EEGMapper()

# Performance loop
for eeg_window in eeg_stream:
    # Map EEG to controls
    controls = eeg_mapper.map_eeg_to_controls(eeg_window)
    
    # Agent responds
    response = agent.respond(controls)
    
    # Add to memory
    memory.add_context(controls)
    
    # Generate audio
    piano_audio = piano.generate(0.5, {
        'midi_note': 60 + response['note_density'] * 24,
        'velocity': response['harmonic_tension']
    })
    
    beat_audio = beats.generate(0.5, {
        'tempo': response['tempo_suggestion'],
        'intensity': response['note_density']
    })
    
    # Mix and output
    output = 0.5 * piano_audio + 0.5 * beat_audio
```

---

## Performance Characteristics

| Component | Inference Time | Parameters | Dependencies |
|-----------|---------------|------------|--------------|
| Piano Synth | <5ms | N/A (DSP) | numpy |
| Guitar Synth | <5ms | N/A (DSP) | numpy |
| Beat Generator | <10ms | N/A (rules) | numpy |
| Agent Memory | <5ms | ~2K | torch (optional) |
| EEG Mapper | <10ms | ~5K | torch (optional) |

All components designed for real-time performance with <100ms total latency.

---

## References

### DDSP Piano
- [lrenault/ddsp-piano](https://github.com/lrenault/ddsp-piano)
- DDSP: Engel et al. (2020) "DDSP: Differentiable Digital Signal Processing"

### DDSP Guitar
- [erl-j/ddsp-guitar](https://github.com/erl-j/ddsp-guitar)
- Karplus-Strong: Karplus & Strong (1983) "Digital Synthesis of Plucked-String and Drum Timbres"

### Agent Memory (GRU)
- JSB Chorales Dataset: Bach chorales from music21
- GRU: Cho et al. (2014) "Learning Phrase Representations using RNN Encoder-Decoder"

### EEG Mapper (EEGNet)
- EEGNet: Lawhern et al. (2018) "EEGNet: A Compact Convolutional Neural Network for EEG-based Brain-Computer Interfaces"
- OpenMIIR: Kaneshiro et al. (2015) "A reproducible EEG study of the OpenMIIR Dataset"

---

## See Also

- `test_new_components.py` - Individual component tests
- `demo_integrated_performance.py` - Full integration demo
- `models/agent_design_philosophy.md` - Agent design principles
- `models/PRETRAINED_EEG_MODELS.md` - EEG model information
