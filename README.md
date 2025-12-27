# BrainJam: AI-Mediated Musical Performance System

A performance instrument and AI co-performer exploring human–AI interaction in live music.
Developeding AI for Artistic Performances.

[![Performance System](https://img.shields.io/badge/System-Performance_Instrument-blue)]()
[![Research](https://img.shields.io/badge/Research-MishMash_WP1-green)]()
[![Status](https://img.shields.io/badge/Status-PhD_Prototype-yellow)]()

---

## What BrainJam Is

**BrainJam is a playable, rehearseable, performable musical instrument** where:

- **Brain signals** (EEG/fNIRS) serve as **optional expressive control signals**
- **AI systems** act as **responsive musical partners**, not autonomous generators
- **Performers** maintain **agency, timing, and creative control**
- The system is designed for **live performance** with real-time constraints (<100ms latency)

### Core Framing

- **Brain signals are control inputs** — comparable to gesture, breath, or touch
- **NOT brain reading or decoding** — we do not interpret semantic content
- **AI is a co-performer** — responding to and engaging with the performer
- **Psychology evaluates the system** — measuring agency, flow, and responsiveness

### Key Goals

1. Create a **responsive, low-latency** musical performance system
2. Explore **performer–AI feedback loops** in real time
3. Maintain **performer agency** and creative control
4. Make the system **meaningful for musicians and audiences**

---

## What BrainJam Is NOT

🚫 **NOT brain decoding** — We do not decode thoughts, intentions, or mental content

🚫 **NOT mind reading** — Brain signals are noisy, continuous control parameters

🚫 **NOT focused on signal accuracy** — Optimization is for musical expression, not classification

🚫 **NOT clinical or therapeutic** — This is a performance instrument, not a medical device

🚫 **NOT neuroscience research** — Psychology supports evaluation, not the primary focus

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BRAINJAM PERFORMANCE SYSTEM               │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   CONTROLLERS    │  ← Input Layer: Various control signals
├──────────────────┤
│ • Mock EEG       │     Structured test signals
│ • Keyboard       │     Manual control for testing/comparison
│ • Real EEG/fNIRS │     Optional biophysical input
│ • MIDI/OSC       │     Standard music interfaces
└──────────────────┘
        ↓
┌──────────────────┐
│ MAPPING MODELS   │  ← Mapping Layer: Control → Parameters
├──────────────────┤
│ • Linear         │     Simple affine transform
│ • MLP            │     Nonlinear mapping
│ • Smoothing      │     Temporal stability
└──────────────────┘
        ↓
┌──────────────────┐
│  SOUND ENGINES   │  ← Synthesis Layer: Generate audio
├──────────────────┤
│ • Parametric     │     Real-time synthesis
│ • DDSP-style     │     Differentiable DSP
│ • Diffusion      │     Generative models (offline)
└──────────────────┘
        ↓
┌──────────────────┐
│   AUDIO OUTPUT   │  ← Output: To performer and audience
└──────────────────┘
        ↓
┌──────────────────┐
│ PERFORMER        │  ← Feedback loop closes here
└──────────────────┘
```

### Latency Budget

Target: **< 100ms** end-to-end

- Signal acquisition: 10-40ms
- Feature extraction: 10-30ms
- Mapping: <5ms
- Sound synthesis: 20-50ms
- **Total**: ~50-120ms

---

## Live Performance MVP

### Current Implementation

A working real-time system with:

1. **Mock EEG controller** — Generates realistic control signals for development
2. **Parametric synthesizer** — Controllable parameters:
   - `tempo_density` — Event rate (0=sparse, 1=dense)
   - `harmonic_tension` — Consonance/dissonance
   - `spectral_brightness` — Timbral quality
   - `noise_balance` — Textural character
3. **Real-time loop** — Input → Mapping → Synthesis → Audio (<100ms)

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the real-time demo
jupyter notebook notebooks/real_time_control_to_sound.ipynb
```

### Demo Notebooks

1. **`real_time_control_to_sound.ipynb`**
   - Keyboard or mock EEG controls sound in real time
   - Visualize control parameters
   - Hear audio feedback immediately

2. **`ai_co_performer_demo.ipynb`**
   - Performer input influences AI timing and density
   - AI responds musically (call-and-response patterns)
   - Demonstrates performer–system interaction

---

## Relation to MishMash WP1

**MishMash WP1**: "AI for Artistic Performances"  
🔗 https://mishmash.no/wp1/  
🔗 https://www.jobbnorge.no/en/available-jobs/job/291081/doctoral-research-fellow-phd-in-creative-human-ai-interaction

### Alignment with WP1 Goals

| WP1 Theme | BrainJam Implementation |
|-----------|------------------------|
| **AI for artistic performance** | AI as responsive co-performer, not autonomous system |
| **Human–AI interaction** | Real-time feedback loops, performer agency |
| **Creative technology** | Expressive control through embodied signals |
| **Performance systems** | Playable, rehearseable, performable live |
| **Evaluation** | Agency, flow, responsiveness metrics |

### Research Questions

1. **Agency**: How do performers experience control in AI-mediated systems?
2. **Responsiveness**: What latency is acceptable for musical interaction?
3. **Feedback loops**: How do performer and AI mutually influence each other?
4. **Expressiveness**: Can biophysical signals provide meaningful musical control?
5. **Audience perception**: How is AI co-performance experienced by audiences?

### Methodological Approach

- **Practice-based research** — Build and perform with the system
- **User studies** — Evaluate with musicians and performers
- **Interaction measures** — Agency, flow, timing metrics
- **Live demonstrations** — Public performances and showcases

---

## Project Structure

```
brainjam/
│
├── performance_system/         # Core performance system
│   ├── controllers/            # Input: EEG, keyboard, MIDI, etc.
│   ├── sound_engines/          # Synthesis and generation
│   ├── mapping_models/         # Control → parameter mapping
│   └── interaction_demos/      # Working demos and examples
│
├── interaction_measures/       # Evaluation: agency, flow, responsiveness
│   ├── questionnaires/         # Simple self-report measures
│   ├── behavioral_tasks/       # Timing and interaction metrics
│   └── validation/             # System evaluation frameworks
│
├── ethics_and_access/          # Ethics: consent, transparency, accessibility
│
├── notebooks/                  # Jupyter notebooks and demos
│   ├── real_time_control_to_sound.ipynb
│   └── ai_co_performer_demo.ipynb
│
├── models/                     # Documentation of AI models
├── literature/                 # Curated research papers
│
├── README.md                   # This file
├── ethics.md                   # Ethical considerations
└── requirements.txt            # Python dependencies
```

---

## Installation

### Prerequisites

- Python 3.8+
- (Optional) PyAudio for real-time audio
- (Optional) Jupyter for notebooks

### Setup

```bash
# Clone the repository
git clone https://github.com/curiousbrutus/brainjam.git
cd brainjam

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Install PyAudio for real-time audio
pip install pyaudio
```

### Verify Installation

```python
# Test the performance system
from performance_system.controllers import MockEEGController
from performance_system.sound_engines import ParametricSynth

controller = MockEEGController()
synth = ParametricSynth()

# Get control vector
controls = controller.get_control_vector()
print(f"Controls: {controls}")

# Generate audio (0.1 seconds)
audio = synth.generate(0.1, controls)
print(f"Audio shape: {audio.shape}")
```

---

## Usage

### Real-Time Performance

```python
import numpy as np
import pyaudio
from performance_system.controllers import MockEEGController
from performance_system.sound_engines import ParametricSynth

# Initialize system
controller = MockEEGController()
synth = ParametricSynth(sample_rate=44100)

# Audio setup
chunk_duration = 0.1  # 100ms chunks
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, 
                rate=44100, output=True)

# Performance loop
try:
    while True:
        # Get control signal
        controls = controller.get_control_vector(duration=0.5)
        
        # Generate audio
        audio = synth.generate(chunk_duration, controls)
        
        # Output audio
        stream.write(audio.tobytes())
except KeyboardInterrupt:
    stream.close()
    p.terminate()
```

### Custom Mappings

```python
from performance_system.mapping_models import LinearMapper

# Create custom mapping
mapper = LinearMapper(n_inputs=4, n_outputs=4)

# Map controller output to synth parameters
raw_controls = controller.get_control_vector()
mapped_controls = mapper.map(raw_controls)

# Use mapped controls
audio = synth.generate(0.1, mapped_controls)
```

---

## ML/DL Pipeline

### Stage 1: Controller Layer

**Purpose**: Convert raw signals to low-dimensional control vectors

**Supported inputs**:
- Mock EEG (structured random signals)
- Keyboard (manual control)
- Real EEG/fNIRS (optional)

**Processing**:
- Band-power extraction (for EEG)
- Temporal smoothing
- Normalization to [0, 1]

**Output**: 4D control vector (continuous, 0-1 range)

### Stage 2: Mapping Layer

**Purpose**: Map controls → synthesis parameters

**Models**:
- Linear regression (baseline)
- Small MLP (8 hidden units)
- Temporal smoothing filter

**Optimization objectives**:
- ✓ Smoothness (minimize frame-to-frame jitter)
- ✓ Stability (consistent behavior)
- ✓ Controllability (full parameter range coverage)
- ✗ NOT accuracy or classification performance

### Stage 3: Sound Generation

**Purpose**: Generate audio from control parameters

**Engines**:
- Parametric synth (real-time, <50ms)
- DDSP-style (planned)
- Diffusion models (offline prototypes)

**Controllable parameters**:
- Tempo/density
- Harmonic tension
- Spectral brightness
- Noise/tone balance

### Stage 4: Real-Time Loop

```
Input (10-40ms) → Extract Features (10-30ms) → 
Map (<5ms) → Synthesize (20-50ms) → 
Audio Output → Performer Feedback
```

---

## Evaluation: Interaction Measures

Evaluation focuses on **performer experience** and **system responsiveness**:

### Primary Measures

1. **Agency**
   - "I felt in control of the sounds" (1-10)
   - "The system responded to my intentions" (1-10)

2. **Responsiveness**
   - Measured latency (ms)
   - Perceived predictability (1-10)

3. **Flow**
   - "I was fully engaged" (1-10)
   - "Time passed quickly" (1-10)

4. **Timing Variability**
   - System response consistency
   - Control parameter stability

### NOT Clinical Assessment

- ✗ No diagnostic claims
- ✗ No therapeutic goals
- ✗ No mental state decoding

See: [`interaction_measures/README.md`](interaction_measures/README.md)

---

## Ethics: Performer-Centered

Ethics centers on **performer consent, transparency, and accessibility**:

### Core Principles

1. **Performer Consent**
   - Clear explanation of system behavior
   - Transparent data use
   - Right to withdraw

2. **System Transparency**
   - Performers understand control mappings
   - No hidden automation
   - Explainable AI behavior

3. **Unpredictability in Performance**
   - Some randomness is performative, not a bug
   - Performers can embrace or constrain variability

4. **Accessibility**
   - Design for neurodivergent performers
   - Consider disabled musicians
   - Avoid normative assumptions about "correct" signals

### NOT Clinical Ethics

- ✗ Not medical device regulations
- ✗ Not therapeutic intervention ethics
- ✗ Not diagnostic testing guidelines

See: [`ethics.md`](ethics.md)

---

## Development Roadmap

### Phase 1: Foundation (Current)
- [x] Mock controller system
- [x] Real-time synthesizer
- [x] Simple mapping models
- [x] Working demos

### Phase 2: AI Co-Performer (Next)
- [ ] Temporal prediction models
- [ ] Call-and-response patterns
- [ ] Adaptive timing
- [ ] Multi-agent interaction

### Phase 3: User Studies
- [ ] Pilot with 5-10 musicians
- [ ] Agency and flow evaluation
- [ ] Iterate on mappings
- [ ] Public demonstrations

### Phase 4: Advanced Features
- [ ] Real EEG/fNIRS integration
- [ ] DDSP-based synthesis
- [ ] Diffusion model exploration
- [ ] Multi-performer systems

---

## Contributing

BrainJam is research software for a PhD project. Contributions are welcome:

### How to Contribute

1. **Report issues** — Bug reports, feature requests
2. **Improve documentation** — Clarify usage, add examples
3. **Add controllers** — New input modalities
4. **Design mappings** — Creative control strategies
5. **Create sounds** — New synthesis engines

### Development Principles

- **Keep latency low** — Target <100ms end-to-end
- **Maintain performer agency** — Human remains in control
- **Make it performable** — Real-time, stable, rehearseable
- **Be transparent** — Clear system behavior
- **Stay critical** — Avoid hype, embrace limitations

---

## Citation

If you use BrainJam in your research:

```bibtex
@software{brainjam2025,
  title={BrainJam: AI-Mediated Musical Performance System},
  author={Eyyub Guven},
  year={2025},
  url={https://github.com/curiousbrutus/brainjam},
  note={PhD research project for MishMash WP1}
}
```

---

## License

This project is open source for academic and educational purposes.  
See [LICENSE](LICENSE) for details.

---

## Contact

**Researcher**: Eyyub Guven  
**Email**: eyyub.gvn@gmail.com  

For questions, collaborations, or performance inquiries, please open an issue or contact directly.

---

**Remember**: BrainJam is a **performance instrument**, not a neuroscience experiment.  
Brain signals are **expressive controls**, not decoded thoughts.  
AI is a **musical partner**, not an autonomous system.
