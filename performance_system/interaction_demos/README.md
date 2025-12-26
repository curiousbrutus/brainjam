# Interaction Demos

Working demonstrations of the BrainJam performance system.

## Overview

This directory contains **runnable demos** that showcase different aspects of the BrainJam performance instrument:

- Real-time audio synthesis
- Control signal mapping
- AI co-performance
- System responsiveness

## Available Demos

### 1. `simulated_brain_synth.py`

**Command-line real-time demo** that runs a continuous performance loop.

```bash
python simulated_brain_synth.py
```

**Features**:
- Mock EEG control signals (structured, not random)
- Real-time audio synthesis with PyAudio
- Visual feedback of control parameters
- < 100ms latency

**What you'll hear**:
- Continuously evolving soundscape
- Parameters change slowly over time
- Demonstrates the performance loop

**Note**: Requires PyAudio (`pip install pyaudio`)

---

### 2. Notebook Demos

See the `notebooks/` directory for interactive Jupyter notebook demos:

- **`real_time_control_to_sound.ipynb`**
  - Step-by-step demonstration
  - Visualizations of control-sound mapping
  - Latency measurements
  - Manual parameter control

- **`ai_co_performer_demo.ipynb`**
  - AI as responsive musical partner
  - Call-and-response patterns
  - Interaction analysis
  - Strategy comparisons

---

## Quick Start

### Command-Line Demo

```bash
# Install dependencies
pip install numpy pyaudio

# Run the demo
cd performance_system/interaction_demos
python simulated_brain_synth.py
```

You'll see control parameters updating in real-time:
```
Engagement: 0.52 | Relaxation: 0.48 | Creativity: 0.61 | Activation: 453.2
```

Press `Ctrl+C` to stop.

### Jupyter Notebook Demos

```bash
# Install Jupyter if needed
pip install jupyter matplotlib

# Launch notebook
jupyter notebook ../../notebooks/real_time_control_to_sound.ipynb
```

---

## Understanding the Demos

### What These Demos Are

✓ **Performance instruments** — Playable in real-time  
✓ **Interactive systems** — Respond to control input  
✓ **Musical tools** — Designed for creative expression  
✓ **Educational** — Show how the system works

### What These Demos Are NOT

✗ **Not brain decoding** — Control signals are not interpreted thoughts  
✗ **Not autonomous AI** — Performer maintains control  
✗ **Not neuroscience** — No attempt to study brain mechanisms  
✗ **Not clinical tools** — Not for medical or therapeutic use

---

## Demo Details

### Control Parameters

All demos use 4 continuous control parameters (0-1 range):

1. **Control 1** → Tempo/Density (event rate)
2. **Control 2** → Harmonic Tension (consonance/dissonance)
3. **Control 3** → Spectral Brightness (timbre)
4. **Control 4** → Noise Balance (texture)

### Synthesis Parameters

The parametric synthesizer provides:
- Additive/subtractive synthesis
- Harmonic series with controllable tension
- Temporal density envelopes
- Noise texture blending

### Latency

Target: **< 100ms** end-to-end
- Signal generation: ~10ms
- Feature extraction: ~10ms
- Mapping: <1ms
- Synthesis: ~30ms
- Audio output: ~20-40ms
- **Typical total**: 70-90ms

---

## Customization

### Modify Control Mappings

Edit the mapping in `simulated_brain_synth.py`:

```python
# Current mapping
freq = base_freq * (1 + 0.5 * engagement)

# Try different mapping
freq = base_freq * (2 ** creativity)  # Exponential pitch control
```

### Change Synthesis Parameters

Adjust the synthesizer settings:

```python
synth = SimpleSynthesizer(fs=44100)

# Modify in synthesize() method:
base_freq = 440  # Change base pitch (A4 instead of A3)
harmonics = [1, 2, 3, 5, 7, 9]  # Add more harmonics
```

### Add Your Own Controller

Create a new controller in `performance_system/controllers/`:

```python
class MyController:
    def get_control_vector(self):
        # Your control logic
        return {
            'control_1': value1,
            'control_2': value2,
            'control_3': value3,
            'control_4': value4,
        }
```

---

## Troubleshooting

### No Audio Output

**Problem**: Demo runs but no sound  
**Solutions**:
- Check PyAudio installation: `pip install pyaudio`
- Verify audio output device is working
- Check system volume
- Try a different audio API (edit PyAudio settings)

### High Latency / Audio Glitches

**Problem**: Sound is choppy or delayed  
**Solutions**:
- Increase buffer size in PyAudio (trades latency for stability)
- Close other audio applications
- Check CPU usage
- Reduce synthesis complexity

### Import Errors

**Problem**: `ModuleNotFoundError`  
**Solutions**:
- Install requirements: `pip install -r requirements.txt`
- Check Python path includes parent directory
- Run from correct directory

---

## Performance Tips

### For Smooth Real-Time Performance

1. **Close unnecessary applications** — Free up CPU
2. **Use headphones** — Reduce feedback/latency
3. **Start simple** — Test with mock EEG before real hardware
4. **Monitor latency** — Use notebook demos to measure
5. **Adjust buffer size** — Balance latency vs. stability

### For Live Performance

1. **Rehearse** — Get familiar with control-sound relationships
2. **Have fallback** — Keyboard control as backup
3. **Test audio setup** — Verify levels and routing
4. **Explain to audience** — Frame as instrument, not mind reading
5. **Embrace unpredictability** — Some randomness is performative

---

## Next Steps

After trying these demos:

1. **Experiment with mappings** — Find what feels expressive
2. **Try keyboard control** — Compare to mock EEG
3. **Test with real EEG** — If hardware is available
4. **Customize synthesis** — Add your own sound engine
5. **Perform live** — Share with an audience!

---

## Technical Details

### System Requirements

- **Python**: 3.8+
- **CPU**: Multi-core recommended for real-time
- **RAM**: 4GB minimum
- **Audio**: Low-latency audio interface (optional but recommended)

### Dependencies

Core:
- `numpy` — Numerical computations
- `pyaudio` — Real-time audio output

Optional:
- `jupyter` — Interactive notebooks
- `matplotlib` — Visualizations
- `pygame` — Keyboard controller

### Architecture

```
Controller → Feature Extraction → Mapping → Synthesis → Audio Out
   ↓              ↓                   ↓          ↓           ↓
 Mock EEG     Band powers         Parameters   Additive   PyAudio
 Keyboard     Smoothing           Neural net   Synthesis  Stream
 Real EEG     Normalization       Linear map   DDSP
```

---

## Contributing

Want to add a demo?

1. **Keep it simple** — Focus on one concept
2. **Document clearly** — Explain what it does
3. **Test thoroughly** — Verify it runs on fresh install
4. **Update README** — Add your demo to this file

---

**Remember**: These demos showcase a **performance instrument**,  
not a neuroscience experiment or autonomous AI system.
