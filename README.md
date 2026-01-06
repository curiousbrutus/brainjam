# BrainJam: AI-Mediated Musical Performance System

> **PhD Research Project Proposal**  
> MishMash WP1: AI for Artistic Performances  
> Focus: Human-AI Interaction in Live Music Performance

[![Performance System](https://img.shields.io/badge/System-Live_Instrument-blue)]()
[![Research](https://img.shields.io/badge/Research-MishMash_WP1-green)]()
[![Status](https://img.shields.io/badge/Status-PhD_Prototype-yellow)]()

![BrainJam User Interface](media/gui_person.png)

---

## 🎯 Project Overview

**BrainJam** is a real-time musical performance system exploring **human-AI co-performance** through brain-computer interfaces. Unlike traditional AI music generation, BrainJam positions AI as a **responsive musical partner**, not an autonomous generator, while preserving complete **performer agency**.

### Core Research Questions

1. How can AI act as a responsive co-performer rather than an autonomous generator?
2. Can brain signals serve as expressive control inputs while maintaining performer agency?
3. What interaction patterns emerge when humans and AI collaborate musically in real-time?

### Key Innovation

- **Hybrid Adaptive Agent**: Combines symbolic logic (reliability) + optional ML (personalization)
- **Real-time Performance**: <30ms total latency for live performance
- **Performer-Led Design**: AI never generates autonomously—all outputs modulate performer input
- **BCI as Control**: EEG/fNIRS signals treated as expressive inputs, not semantic decoding

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BrainJam Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  Input Layer          │  AI Layer           │  Output Layer │
│  • EEG/fNIRS      ──► │  Hybrid Agent    ──► │  Piano Synth │
│  • MIDI/Keyboard  ──► │  • Agent Memory  ──► │  Guitar Synth│
│  • Mock Signals       │  • EEG Mapper        │  • Beats     │
└───────────────────────┴──────────────────────┴───────────────┘
```

### Core Components

1. **Hybrid Adaptive Agent** 🧠: Three behavioral states (calm/active/responsive), <5ms inference
2. **Sound Engines** 🎵: DDSP Piano, Guitar, Beat Generator
3. **Agent Memory** 💭: GRU-based dialogue learning (JSB Chorales)
4. **EEG Mapper** 🔬: EEGNet architecture, OpenMIIR compatible

---

## 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/curiousbrutus/brainjam.git
cd brainjam
pip install -r requirements.txt

# Run interactive GUI
streamlit run streamlit_app/app.py
```

### Example Usage

```python
from performance_system.agents import HybridAdaptiveAgent
from performance_system.sound_engines import DDSPPianoSynth, BeatGenerator

# Initialize
agent = HybridAdaptiveAgent()
piano = DDSPPianoSynth()
beats = BeatGenerator()

# Performance loop
for controls in signal_stream:
    response = agent.respond(controls)
    audio = piano.generate(0.5, {'midi_note': 60}) + beats.generate(0.5, {'tempo': 120})
```

---

## 📁 Repository Structure

```
brainjam/
├── performance_system/    # Core system (agents, synths, mappers)
├── streamlit_app/         # Interactive GUI
├── examples/              # Usage demos
├── tests/                 # Unit tests
├── docs/                  # Documentation
│   ├── architecture/      # Technical design
│   └── research/          # Research context
├── models/                # Model info
└── literature/            # Academic references
```

---

## 🎓 Academic Context

### MishMash WP1: AI for Artistic Performances

**Research Focus**: Human-AI collaboration in creative contexts

**Key Questions**:
- How to maintain performer agency with AI assistance?
- Can BCIs enable expressive musical control?
- What makes AI "feel" like a musical partner?

### Theoretical Framework

- **Performer-Led Systems** (Tanaka, 2006): AI responds, never overrides
- **Interactive ML** (Fiebrink, 2011): Real-time adaptation with user control
- **BCMIs** (Miranda & Castet, 2014): Brain signals as expressive input

---

## 📊 Research Contributions

### Technical Innovations
1. **Hybrid Agent Architecture**: Symbolic + ML with guaranteed agency
2. **Real-time BCI Integration**: <30ms latency, graceful fallbacks
3. **Musical Co-Performance**: Learned dialogue patterns from Bach chorales

### Research Outputs
- Fully functional prototype
- Evaluation framework for agency/flow/responsiveness
- Comprehensive documentation and demos

---

## 🔬 Evaluation Methods

**Planned User Studies**:
1. Agency Assessment (SAM + custom scales)
2. Flow State (FSS-2 questionnaire)
3. Performance Quality (expert + audience ratings)
4. Learning Curve (longitudinal study)

See [`docs/research/interaction_measures/`](docs/research/interaction_measures/) for details.

---

## 📖 Documentation

**For Researchers**: [`docs/research/`](docs/research/) - Ethics, limitations, evaluation
**For Developers**: [`docs/architecture/`](docs/architecture/) - Technical design, components
**For Users**: [`QUICK_START.md`](QUICK_START.md), [`examples/`](examples/)

---

## 🛠️ Technical Stack

- **Python 3.9+**, NumPy/SciPy, PyTorch (optional)
- **Streamlit** GUI, scikit-learn
- **Performance**: <30ms latency, 44.1kHz audio, 10Hz control rate

---

## 🚧 Status & Roadmap

### ✅ Completed (MVP)
- [x] Hybrid Adaptive Agent with 3 states
- [x] DDSP Piano/Guitar + Beat Generator
- [x] Agent Memory (GRU) + EEG Mapper (EEGNet)
- [x] Interactive GUI + documentation

### 🔄 In Progress
- [ ] User study design
- [ ] Model training (JSB Chorales, OpenMIIR)
- [ ] Real EEG hardware integration

---

## 📚 Key References

**BCI Music**: Tanaka (2006), Miranda & Castet (2014)  
**Interactive ML**: Fiebrink (2011), Lawhern et al. (2018)  
**Audio Synthesis**: Engel et al. (2020), Karplus & Strong (1983)

See [`literature/`](literature/) for detailed summaries.

---

## 📧 Contact

**Project**: BrainJam - AI-Mediated Musical Performance  
**Affiliation**: MishMash WP1, Norway  
**Purpose**: PhD Research Application

---

## 📄 License

Academic research project for PhD application. Contact for usage permissions.

---

**Built with 🧠 + 🎵 + 🤖 for exploring human-AI musical collaboration**
