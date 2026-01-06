# BrainJam Examples

This directory contains practical examples demonstrating how to use BrainJam components.

## 🎬 Available Examples

### 1. **demo_integrated_performance.py**
Complete integrated performance demonstration showing all components working together:
- EEG Mapper → Hybrid Agent → Sound Engines
- 20-second musical performance generation
- Real-time behavioral state adaptation
- Piano + Guitar + Beats mixing

**Run it:**
```bash
python examples/demo_integrated_performance.py
```

**What it demonstrates:**
- Full pipeline from EEG signals to audio output
- Agent Memory learning from control history
- Multiple sound engines synchronized
- Performance statistics and logging

---

### 2. **test_new_components.py**
Systematic testing of all 5 new components:
- Individual component testing
- Integration tests
- Performance benchmarking

**Run it:**
```bash
python examples/test_new_components.py
```

**What it tests:**
- DDSP Piano Synth generation
- DDSP Guitar Synth (single notes and chords)
- Beat Generator patterns
- Agent Memory predictions
- EEG Mapper control extraction

---

### 3. **biosignal_integration_demo.py**
Multi-modal biosignal integration example:
- EEG + fNIRS + EMG fusion
- BioSignal Inference module
- Real-time feature extraction

**Run it:**
```bash
python examples/biosignal_integration_demo.py
```

**What it demonstrates:**
- Multi-modal signal processing
- Latent space mapping
- Style vector generation

---

## 🚀 Quick Start

```python
# Basic usage pattern for all examples
from performance_system.agents import HybridAdaptiveAgent
from performance_system.sound_engines import DDSPPianoSynth

# Initialize
agent = HybridAdaptiveAgent()
piano = DDSPPianoSynth()

# Generate
controls = {'control_1': 0.5, 'control_2': 0.7, 'control_3': 0.6, 'control_4': 0.4}
response = agent.respond(controls)
audio = piano.generate(1.0, {'midi_note': 60, 'velocity': response['harmonic_tension']})
```

---

## 📖 Documentation

For detailed component documentation, see:
- [`../docs/architecture/NEW_COMPONENTS.md`](../docs/architecture/NEW_COMPONENTS.md)
- [`../docs/architecture/agent_design_philosophy.md`](../docs/architecture/agent_design_philosophy.md)

For research context:
- [`../docs/research/`](../docs/research/)

For getting started:
- [`../QUICK_START.md`](../QUICK_START.md)

---

## 🎯 Learning Path

1. **Start here**: Run `test_new_components.py` to see each component individually
2. **Then try**: Run `demo_integrated_performance.py` to see full integration
3. **Finally explore**: Modify examples or create your own based on these templates

---

## 💡 Tips

- Examples generate audio files (if `soundfile` is installed)
- All examples work without PyTorch (graceful fallback to symbolic rules)
- Check console output for performance statistics
- Examples are designed to be self-contained and educational

---

## 🐛 Troubleshooting

**No audio output?**
→ Install `soundfile`: `pip install soundfile`

**PyTorch warnings?**
→ Optional - system works without it using symbolic fallbacks

**Import errors?**
→ Ensure you're running from repository root: `python examples/demo_name.py`

---

Happy experimenting! 🎵🧠🤖
