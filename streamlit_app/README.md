# BrainJam Streamlit GUI

Interactive graphical interface for the BrainJam performance system.

## Overview

This Streamlit application provides a visual, interactive demonstration of the BrainJam system, allowing users to:

- Understand the system architecture and design philosophy
- Explore signal generation and feature extraction
- Experiment with different mapping strategies
- Hear how control parameters affect sound synthesis
- Try the complete performance pipeline
- Connect the system to research and artistic use cases

## Structure

```
streamlit_app/
│
├── app.py                  # Main entry point
│
├── pages/                  # Multi-page application
│   ├── 1_Overview.py      # System introduction and architecture
│   ├── 2_Signals.py       # Signal simulation and visualization
│   ├── 3_Mapping.py       # Control mapping exploration
│   ├── 4_Sound_Engine.py  # Sound synthesis demonstration
│   ├── 5_Live_Performance.py  # Complete system demo
│   └── 6_Use_Cases.py     # Research and artistic applications
│
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── signal_utils.py    # Signal generation utilities
│   ├── plot_utils.py      # Visualization helpers
│   └── audio_utils.py     # Audio generation and playback
│
├── assets/                 # Static assets (images, etc.)
│
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.8+
- Dependencies from main repository

### Setup

```bash
# From the repository root
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `streamlit>=1.28.0` for the GUI framework
- `plotly>=5.14.0` for interactive visualizations
- All existing BrainJam dependencies

## Usage

### Running the App

```bash
# From the repository root
streamlit run streamlit_app/app.py
```

Or if you're in the streamlit_app directory:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

### Navigation

1. **Start at the main page** (app.py) for an overview
2. **Use the sidebar** to navigate between pages
3. **Follow the recommended order**: Overview → Signals → Mapping → Sound Engine → Live Performance → Use Cases

### Interactive Features

- **Sliders**: Adjust parameters in real-time
- **Buttons**: Generate audio, reset systems, etc.
- **Plots**: Interactive Plotly visualizations
- **Audio players**: Listen to generated sounds
- **Self-report measures**: Experience evaluation tools

## Pages

### 1. Overview
**Purpose**: Conceptual orientation

- System architecture diagram
- Core concepts and framing
- What BrainJam is (and isn't)
- Performance-centered philosophy

### 2. Signals
**Purpose**: EEG/fNIRS simulation

- Mock signal generation
- Time series visualization
- Band power extraction
- Control parameter normalization

**Key controls**:
- Arousal, Focus, Variability sliders
- Duration adjustment
- Real-time signal generation

### 3. Mapping
**Purpose**: Control design exploration

- Different mapping types (Linear, Smoothed, Nonlinear, etc.)
- Responsiveness vs. stability trade-offs
- Parameter visualization
- Interactive testing

**Key controls**:
- Mapping type selector
- Smoothing, sensitivity, threshold sliders
- Test input slider

### 4. Sound Engine
**Purpose**: Audio synthesis demonstration

- Parametric synthesizer
- Control parameter effects
- Audio generation and playback
- Waveform visualization

**Key controls**:
- 4 control parameter sliders
- Duration selection
- Generate audio button

### 5. Live Performance
**Purpose**: Complete system MVP

- Full pipeline demonstration
- Signal → Features → Mapping → Sound
- Performance history tracking
- Simple self-assessment

**Key controls**:
- Signal source selection (Mock EEG / Manual)
- Start/pause/reset buttons
- Generate chunk button
- Self-report sliders

### 6. Use Cases
**Purpose**: WP1 alignment and research context

- Four detailed use cases
- Research questions and methods
- Interaction measures
- Future directions
- MishMash WP1 connection

## Design Principles

### Performance-Centered
- Not framed as brain decoding
- Emphasizes musical expression
- Focuses on performer agency

### Minimal & Clear
- Clean, uncluttered interface
- Focused explanations
- Progressive disclosure of complexity

### Interactive
- Hands-on exploration
- Immediate feedback
- Adjustable parameters

### Educational
- Clear explanations at each step
- Visual representations
- Conceptual grounding

### Research-Aware
- Connects to MishMash WP1
- Explains research questions
- Demonstrates evaluation methods

## Technical Details

### Signal Generation
- Mock EEG/fNIRS with controllable parameters
- Frequency band simulation (theta, alpha, beta)
- Adjustable arousal, focus, variability

### Mapping Models
- Linear transformation
- Temporal smoothing
- Nonlinear sigmoid
- Threshold-based

### Sound Synthesis
- Parametric additive synthesis
- Real-time parameter control
- WAV generation for browser playback

### Visualization
- Plotly for interactive plots
- Time series, bar charts, radar charts
- System architecture diagrams

## Performance Notes

### Latency
The GUI simulates the performance system but is **not optimized for real-time audio**:
- Chunk-based generation (not continuous)
- Browser audio playback (not PyAudio)
- Suitable for demonstration, not live performance

For real-time performance, use the main BrainJam system with PyAudio.

### Audio Format
- Sample rate: 44.1 kHz
- Format: 16-bit WAV
- Channels: Mono
- Playback: Browser HTML5 audio

## Limitations & Future Work

### Current Limitations
- Not continuous real-time (chunk-based)
- No PyAudio integration (browser only)
- Simplified mapping models
- No recording/session saving

### Future Enhancements
- Real-time audio streaming
- Advanced mapping models (trained MLPs)
- AI co-performer features
- Session recording and analysis
- Performance metrics dashboard

## Development

### Adding New Pages
1. Create new file in `pages/` directory
2. Name it `N_PageName.py` (N = order number)
3. Follow existing page structure
4. Import utilities from `utils/`

### Adding New Utilities
1. Add function to appropriate utility module
2. Update `utils/__init__.py` imports
3. Document with docstrings

### Testing
```bash
# Run the app and test manually
streamlit run streamlit_app/app.py

# Check for errors in terminal output
```

## Troubleshooting

### Port Already in Use
```bash
# Specify a different port
streamlit run streamlit_app/app.py --server.port 8502
```

### Module Import Errors
```bash
# Ensure you're in the repository root
cd /path/to/brainjam
streamlit run streamlit_app/app.py
```

### Audio Not Playing
- Check browser console for errors
- Ensure browser supports HTML5 audio
- Try a different browser

## Citation

If you use this GUI in research or publications:

```bibtex
@software{brainjam_gui2025,
  title={BrainJam Streamlit GUI: Interactive Performance System Demonstration},
  author={Eyyub Guven},
  year={2025},
  url={https://github.com/curiousbrutus/brainjam},
  note={Part of MishMash WP1: AI for Artistic Performances}
}
```

## Contact

**Researcher**: Eyyub Guven  
**Email**: eyyub.gvn@gmail.com  
**Project**: MishMash WP1

For questions, issues, or contributions, please open an issue on GitHub.

---

**Remember**: This is a **demonstration and exploration tool**, not a production performance system. For real-time performance, use the main BrainJam system with PyAudio.
