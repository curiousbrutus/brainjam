# Toy Interface: Real-Time Brain→Sound Prototypes

This directory contains proof-of-concept implementations for real-time brain-mediated music systems.

## Overview

These are **research prototypes** demonstrating feasibility of brain→sound mapping in real-time. They prioritize simplicity and educational value over production quality.

## Components

### 1. `simulated_brain_synth.py`
Real-time audio synthesis driven by simulated brain signals.
- Generates synthetic EEG-like features
- Maps to audio synthesis parameters
- PyAudio-based real-time output

### 2. `eeg_osc_bridge.py`
Bridge between EEG devices and audio software via OSC (Open Sound Control).
- Reads from EEG devices (or simulated stream)
- Extracts real-time features
- Sends via OSC to DAWs/synthesizers

### 3. `web_interface/`
Simple web-based visualization and control.
- Real-time brain feature display
- Audio parameter visualization
- Manual override controls

## Quick Start

### Prerequisites
```bash
# Install dependencies
pip install numpy scipy pyaudio python-osc flask

# For EEG hardware support (optional)
pip install mne pylsl
```

### Run Simulated Demo
```bash
python simulated_brain_synth.py
```

This will:
1. Generate simulated brain signals
2. Extract features in real-time
3. Synthesize audio based on features
4. Play audio through speakers

### With Real EEG
```bash
# Make sure EEG device is connected and streaming via LSL
python eeg_osc_bridge.py --device muse
```

## Architecture

```
Brain Signal → Feature Extraction → Mapping → Audio Synthesis
     ↓              ↓                   ↓            ↓
  EEG/fMRI    Band Powers           Parameters    Sound
              Connectivity          Latent Vec    Output
              etc.                  etc.
```

## Features

### Simulated Brain Synth
- Multiple oscillators with brain-controlled parameters
- Amplitude modulation from "engagement"
- Filter cutoff from "attention"
- Reverb from "relaxation"
- Real-time parameter smoothing

### EEG-OSC Bridge
- Low-latency feature extraction (<50ms)
- OSC output compatible with Max/MSP, Pure Data, Ableton, etc.
- Configurable feature set
- Recording capability for offline analysis

### Web Interface
- Live waveform display
- Feature timeline plots
- Parameter knobs for manual control
- WebSocket communication

## Design Principles

1. **Low Latency**: Target <100ms end-to-end
2. **Stability**: Smooth parameter changes, no abrupt jumps
3. **Transparency**: User can see all mappings
4. **Control**: Manual override always available
5. **Safety**: Volume limiting, graceful degradation

## Mappings (Default)

### Brain Feature → Audio Parameter
- **Engagement** (beta/theta+alpha) → Tempo/Energy
- **Frontal Asymmetry** → Harmonic mode (major/minor tendency)
- **Theta/Alpha Ratio** → Filter resonance/complexity
- **Overall Activation** → Master volume
- **Alpha Power** → Reverb amount (inversely)

These are **defaults** - users should explore and customize!

## Limitations

⚠️ **These are prototypes**:
- Not medical devices
- Not tested for long-term use
- No guarantees of stability
- Educational/research purposes only

⚠️ **Technical limitations**:
- Simulated data doesn't capture real brain complexity
- Artifact rejection is minimal
- Individual calibration not implemented
- Single-user, single-device only

⚠️ **Ethical considerations**:
- See `ethics.md` for full discussion
- Always prioritize user agency
- Make mappings transparent
- Allow manual control
- Respect privacy of neural data

## Customization

### Adding New Features
Edit the feature extraction functions in `feature_extraction.py`:
```python
def extract_custom_feature(eeg_window):
    # Your feature extraction code
    return feature_value
```

### Changing Mappings
Modify mapping functions in `brain_to_audio.py`:
```python
def map_to_audio_params(brain_features):
    params = {}
    params['frequency'] = your_mapping(brain_features)
    return params
```

### New Synthesis
Create new synthesizer classes in `synthesizers.py`:
```python
class CustomSynth:
    def generate_audio(self, params):
        # Your synthesis code
        return audio_samples
```

## Testing

### Unit Tests
```bash
pytest tests/
```

### Integration Test
```bash
python test_pipeline.py
```

### Latency Test
```bash
python benchmark_latency.py
```

Expected latency budget:
- Signal acquisition: 4-40ms (depends on buffer size)
- Feature extraction: 10-30ms
- Mapping: <1ms
- Audio synthesis: 10-50ms (depends on buffer)
- **Total**: 25-120ms

## Troubleshooting

### Audio Glitches
- Increase buffer size (trades latency for stability)
- Reduce feature complexity
- Check CPU usage

### No Sound
- Check PyAudio device selection
- Verify audio output settings
- Test with simulated mode first

### High Latency
- Reduce EEG sampling rate
- Simplify feature extraction
- Use smaller audio buffers (if stable)

## Future Enhancements

- [ ] Multi-user support
- [ ] Advanced artifact rejection
- [ ] Personalized calibration routine
- [ ] More synthesis algorithms
- [ ] Recording/playback of sessions
- [ ] Integration with music generation models
- [ ] Mobile/web-based version

## Contributing

When adding new features:
1. Keep code simple and documented
2. Add tests for core functionality
3. Update this README
4. Consider latency impact
5. Maintain user control/transparency

## References

- PyAudio: https://people.csail.mit.edu/hubert/pyaudio/
- python-osc: https://python-osc.readthedocs.io/
- MNE-Python: https://mne.tools/
- Lab Streaming Layer: https://labstreaminglayer.readthedocs.io/

## Support

For issues or questions, please open an issue on GitHub.
Remember: These are research prototypes for exploration, not production systems!
