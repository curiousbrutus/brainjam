# BrainJam Repository Structure

Clean, professional organization for PhD research proposal.

## �� Directory Tree

```
brainjam/ (22MB total: 1MB code + 21MB media)
│
├── 📄 README.md (7KB)                    ← Start here
├── 📄 PROJECT_SUMMARY.md (13KB)          ← Complete overview
├── 📄 QUICK_START.md (6KB)               ← Getting started
├── 📄 LIMITATIONS.md (17KB)              ← Key limitations & constraints
├── 📄 IMPROVEMENTS.md (15KB)             ← Suggested improvements
├── 📄 requirements.txt (2KB)             ← Dependencies
├── 🔧 run_gui.sh                         ← Launch GUI
│
├── 🧠 performance_system/ (368KB)        ← Core system code
│   ├── agents/                           • Hybrid adaptive agent
│   │   ├── hybrid_adaptive_agent.py      • Agent memory (GRU)
│   │   └── agent_memory.py
│   ├── sound_engines/                    • Piano synth (DDSP)
│   │   ├── ddsp_piano_synth.py           • Guitar synth (DDSP)
│   │   ├── ddsp_guitar_synth.py          • Beat generator
│   │   ├── beat_generator.py             • Other synths
│   │   └── ...
│   ├── mapping_models/                   • EEG mapper (EEGNet)
│   │   ├── eeg_mapper.py                 • Other mappers
│   │   └── ...
│   ├── controllers/                      • Input devices
│   ├── signals/                          • Signal generation
│   └── interaction_demos/                • Built-in demos
│
├── 🎨 streamlit_app/ (164KB)             ← Interactive GUI
│   ├── app.py                            • Main application
│   └── pages/                            • 8 GUI pages
│       ├── 1_Overview.py
│       ├── 2_Signals.py
│       ├── 3_Mapping.py
│       ├── 4_Sound_Engine.py
│       ├── 5_Live_Performance.py
│       └── ...
│
├── 📚 examples/ (32KB)                   ← Usage examples
│   ├── README.md                         • Examples guide
│   ├── demo_integrated_performance.py    • Full system demo
│   ├── test_new_components.py            • Component tests
│   └── biosignal_integration_demo.py     • BioSignal demo
│
├── ✅ tests/ (16KB)                       ← Unit tests
│   └── test_hybrid_adaptive_agent.py     • 11/11 tests passing
│
├── 📖 docs/ (248KB)                      ← Documentation
│   ├── README.md                         • Documentation index
│   ├── architecture/                     • Technical design
│   │   ├── NEW_COMPONENTS.md             • Component docs
│   │   └── agent_design_philosophy.md    • Design principles
│   └── research/                         • Research context
│       ├── ethics.md                     • Ethics framework
│       ├── limitations.md                • Limitations
│       └── interaction_measures/         • Evaluation
│
├── 🤖 models/ (28KB)                     ← Model information
│   ├── README.md                         • Model overview
│   └── PRETRAINED_EEG_MODELS.md          • EEG model info
│
├── 📚 literature/ (36KB)                 ← Academic references
│   ├── bci_music.md                      • BCI research
│   ├── creativity_neuroscience.md        • Neuroscience
│   └── generative_audio.md               • Audio synthesis
│
├── 📓 notebooks/ (112KB)                 ← Jupyter notebooks
│   ├── README.md                         • Notebook guide
│   ├── 01_load_pretrained_models.ipynb   • Exploration
│   └── ... (7 notebooks total)
│
├── 🔗 src/ (40KB)                        ← Bridge modules
│   └── bridge/                           • BioSignal inference
│       └── latent_mapper.py
│
└── 🎬 media/ (21MB)                      ← Assets
    ├── gui_person.png                    • Screenshots
    ├── st-gui-*.png                      • GUI previews
    ├── vid_bj.mp4                        • Demo video
    └── BrainJam__Nervous_System_Music.mp4 • Concept video
```

---

## 📊 Size Breakdown

| Directory | Size | Contents |
|-----------|------|----------|
| `performance_system/` | 368KB | Core system code |
| `docs/` | 248KB | All documentation |
| `streamlit_app/` | 164KB | Interactive GUI |
| `notebooks/` | 112KB | Jupyter notebooks |
| `src/` | 40KB | Bridge modules |
| `literature/` | 36KB | References |
| `examples/` | 32KB | Usage demos |
| `models/` | 28KB | Model info |
| `tests/` | 16KB | Unit tests |
| **Code Total** | **~1MB** | All code |
| `media/` | **21MB** | Videos/images |
| **Grand Total** | **~22MB** | Complete repo |

---

## 🎯 Quick Navigation

### For First-Time Visitors
1. **README.md** - Project overview and quick start
2. **PROJECT_SUMMARY.md** - Comprehensive research summary
3. **QUICK_START.md** - Installation and first steps
4. **LIMITATIONS.md** - Understanding what the system can and cannot do

### For Researchers
1. **docs/research/** - Ethics, limitations, evaluation
2. **literature/** - Academic references
3. **PROJECT_SUMMARY.md** - Research framework
4. **IMPROVEMENTS.md** - Development roadmap and suggestions

### For Developers
1. **docs/architecture/** - Technical design
2. **examples/** - Code examples
3. **tests/** - Test suite

### For Users
1. **QUICK_START.md** - Getting started
2. **examples/README.md** - Usage guide
3. **streamlit_app/** - Interactive GUI

---

## ✨ Key Features

### Clean Organization
✅ No duplicate directories  
✅ No redundant files  
✅ Clear, logical structure  
✅ Professional naming  

### Complete Documentation
✅ 250KB organized docs  
✅ Technical + research  
✅ Examples + guides  
✅ Academic references  

### Working Code
✅ 6,000+ lines Python  
✅ 11/11 tests passing  
✅ <30ms latency  
✅ Complete system  

### PhD-Ready
✅ Clear research questions  
✅ Theoretical foundation  
✅ Evaluation framework  
✅ Future work outlined  

---

## 🔍 File Counts

```
Python files:        ~80 files
Documentation:       ~30 files
Tests:               1 comprehensive suite
Examples:            3 working demos
GUI pages:           8 interactive pages
Notebooks:           7 exploration notebooks
```

---

## 💾 Dependencies

See [`requirements.txt`](requirements.txt) for complete list.

**Core**: numpy, scipy, scikit-learn, streamlit  
**Optional**: torch (for ML components)  
**Audio**: soundfile (for saving audio)

---

## 🚀 Getting Started

```bash
# 1. Clone
git clone https://github.com/curiousbrutus/brainjam.git
cd brainjam

# 2. Install
pip install -r requirements.txt

# 3. Run GUI
streamlit run streamlit_app/app.py

# 4. Try examples
python examples/demo_integrated_performance.py
```

---

## 📧 Contact

**Project**: BrainJam - AI-Mediated Musical Performance  
**Affiliation**: MishMash WP1, Norway  
**Purpose**: PhD Research Application

**Status**: ✅ Complete, Clean, PhD-Ready

---

Built with 🧠 + 🎵 + 🤖
