# BrainJam Quick Start Guide

Get up and running with BrainJam in 5 minutes!

---

## Installation

```bash
# Clone repository
git clone https://github.com/curiousbrutus/brainjam.git
cd brainjam

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Quick Test: Run the Demos

### Option 1: Run All Demos
```bash
python performance_system/interaction_demos/run_all_demos.py
```

This will run all three MVP demonstrations:
1. **Brain → Continuous Sound** (30s ambient texture)
2. **AI as Co-Performer** (40s call-and-response)
3. **Learning Through Practice** (60s with learning curve)

### Option 2: Run Individual Demos
```bash
# Demo 1: Continuous textural sound
python performance_system/interaction_demos/demo1_continuous_sound.py

# Demo 2: AI co-performance
python performance_system/interaction_demos/demo2_ai_coperformer.py

# Demo 3: Learning simulation
python performance_system/interaction_demos/demo3_learning_practice.py
```

Each demo generates audio files (`.wav`) and Demo 3 creates a visualization (`.png`).

---

## Quick Test: Interactive GUI

```bash
streamlit run streamlit_app/app.py
```

Then open your browser to `http://localhost:8501`

### GUI Pages to Explore:
1. **Overview** - Understand the system
2. **Signals** - See mock EEG generation
3. **Mapping** - Control design strategies
4. **Sound Engine** - Try all three synthesizers
5. **Live Performance** - Complete system demo
6. **Use Cases** - Research applications
7. **Feature Shaping** - Signal processing visualization (NEW!)

---

## Quick Test: Python Code

```python
from performance_system.controllers import MockEEGController
from performance_system.feature_shaping import TemporalSmoother
from performance_system.mapping_models import ExpressiveMapper
from performance_system.sound_engines import DDSPSynth
import soundfile as sf

# Initialize components
controller = MockEEGController()
smoother = TemporalSmoother(n_features=4, smoothing_mode='exponential')
mapper = ExpressiveMapper(n_inputs=4, n_outputs=4)
synth = DDSPSynth(sample_rate=44100, base_freq=110.0)

# Generate 5 seconds of audio
audio_chunks = []
for _ in range(50):  # 50 chunks of 0.1s = 5s
    # Get control signal
    controls = controller.get_control_vector(duration=0.5)
    
    # Apply feature shaping
    smoothed = smoother.update(controls)
    
    # Apply expressive mapping
    mapped = mapper.map(smoothed)
    
    # Generate audio
    chunk = synth.generate(0.1, mapped)
    audio_chunks.append(chunk)

# Save
import numpy as np
audio = np.concatenate(audio_chunks)
sf.write('my_first_brainjam.wav', audio, 44100)
print("✓ Audio saved to my_first_brainjam.wav")
```

---

## System Architecture (Simplified)

```
Brain Signal (Mock/Real)
    ↓
Feature Shaping (PCA/Autoencoder/Temporal)
    ↓
Expressive Mapping (Hysteresis/Drift/Thresholds)
    ↓
Sound Synthesis (Parametric/DDSP/Symbolic)
    ↓
Audio Output
```

**Latency**: <100ms end-to-end ✓

---

## Available Components

### Feature Shapers (Signal → Latents)
- **PCAReducer**: Dimensionality reduction
- **SimpleAutoencoder**: Neural compression (PyTorch)
- **TemporalSmoother**: Sliding window smoothing

### Mappers (Latents → Sound Parameters)
- **LinearMapper**: Simple affine transform
- **MLPMapper**: Small neural network
- **ExpressiveMapper**: Hysteresis, drift, thresholds

### Sound Engines (Parameters → Audio)
- **ParametricSynth**: Additive/subtractive (drones)
- **DDSPSynth**: Harmonic + noise (expressive)
- **SymbolicSynth**: Note-based (melodic)

---

## Performance Logging

```python
from interaction_measures.performance_logger import PerformanceLogger

logger = PerformanceLogger()

# During performance
import time
start = time.time()
# ... process frame ...
logger.log_frame(input_controls, output_params, start, time.time())

# Add subjective ratings
logger.add_subjective_rating(agency=7.5, responsiveness=8.0)

# Get summary
logger.print_summary()
logger.save_log('performance_log.json')
```

---

## Key Concepts

### 🎯 This is NOT:
- ❌ Brain decoding or mind reading
- ❌ Reconstructing thoughts or melodies
- ❌ Clinical or therapeutic
- ❌ Optimized for classification accuracy

### ✅ This IS:
- ✅ An artistic performance instrument
- ✅ Brain signals as expressive control (like gesture)
- ✅ AI as responsive co-performer
- ✅ Designed for rehearsal and live performance
- ✅ Open-source and free

---

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the right directory
cd /path/to/brainjam

# Reinstall dependencies
pip install -r requirements.txt
```

### PyTorch Issues
```bash
# Install CPU-only version (smaller, faster)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Audio Playback
```bash
# For real-time audio (optional)
pip install pyaudio

# If PyAudio fails, demos still work (save to .wav files)
```

---

## Next Steps

1. **Read the Documentation**:
   - [`README.md`](README.md) - Full system overview
   - [`performance_system/sound_engines/README.md`](performance_system/sound_engines/README.md) - Sound engine details
   - [`ML_DL_IMPLEMENTATION_SUMMARY.md`](ML_DL_IMPLEMENTATION_SUMMARY.md) - Implementation details

2. **Explore the Code**:
   - `performance_system/` - Core system modules
   - `streamlit_app/` - Interactive GUI
   - `interaction_measures/` - Performance metrics

3. **Try the Demos**:
   - Experiment with different parameters
   - Modify mappings and sound engines
   - Create your own performance scripts

4. **Join the Research**:
   - This is part of MishMash WP1: AI for Artistic Performances
   - Contact: eyyub.gvn@gmail.com

---

## License

Open source for academic and educational purposes.

---

**Happy performing! 🎵🧠🎶**
