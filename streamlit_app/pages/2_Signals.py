"""
Page 2: Signals - EEG/fNIRS Simulation
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import MockSignalGenerator, normalize_features, plot_time_series, plot_band_powers, plot_control_parameters

st.set_page_config(page_title="Signals", page_icon="📊", layout="wide")

st.title("📊 Signals: EEG/fNIRS Simulation")

st.markdown("""
---

## 🧠 Making Abstract Signals Visible

This page lets you explore how **brain-like signals** vary over time and how they're 
transformed into **control parameters**.

**Key Concept**: These signals are continuous, noisy, and expressive — just like gesture or breath.

---
""")

# Initialize session state for signal generator
if 'signal_generator' not in st.session_state:
    st.session_state.signal_generator = MockSignalGenerator(fs=250)

# Control parameters
st.sidebar.markdown("## 🎛️ Signal Parameters")
st.sidebar.markdown("Adjust these to see how they affect the generated signals:")

arousal = st.sidebar.slider(
    "**Arousal** (activation level)",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Higher arousal → more beta activity, less alpha"
)

focus = st.sidebar.slider(
    "**Focus** (attention level)",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Higher focus → less theta, more beta"
)

variability = st.sidebar.slider(
    "**Variability** (signal noise)",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Higher variability → more noise in signal"
)

duration = st.sidebar.slider(
    "**Duration** (seconds)",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.5,
    help="How long to generate signal"
)

if st.sidebar.button("🔄 Reset Signal Generator", use_container_width=True):
    st.session_state.signal_generator.reset()
    st.rerun()

# Generate signal
time_vec, signal, features = st.session_state.signal_generator.generate_signal(
    duration=duration,
    arousal=arousal,
    focus=focus,
    variability=variability
)

# Normalize to control parameters
controls = normalize_features(features)

# Display
st.markdown("### 📈 Raw Signal (EEG-like)")
st.markdown("""
This is what a mock EEG signal might look like. Notice:
- **Oscillations** at different frequencies (theta, alpha, beta)
- **Noise** making it inherently unstable
- **Slow variations** as parameters change
""")

fig_signal = plot_time_series(time_vec, signal, title="Mock Brain Signal")
st.plotly_chart(fig_signal, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎚️ Band Powers")
    st.markdown("""
    Extracted features from the signal:
    - **Theta (4-8 Hz)**: Associated with relaxation, creativity
    - **Alpha (8-13 Hz)**: Associated with calm, eyes closed
    - **Beta (13-30 Hz)**: Associated with active thinking
    
    **Note**: These are simplified approximations, not real band-power analysis.
    """)
    fig_bands = plot_band_powers(features)
    st.plotly_chart(fig_bands, use_container_width=True)
    
    st.info("""
    **Remember**: We're not "decoding" mental states. These are just features 
    extracted from the signal for control purposes.
    """)

with col2:
    st.markdown("### 🎮 Control Parameters (Normalized)")
    st.markdown("""
    Band powers normalized to 0-1 range for control:
    - **Control 1**: From theta power
    - **Control 2**: From alpha power
    - **Control 3**: From beta power
    - **Control 4**: Combined theta + beta
    
    These are what drive the sound engine.
    """)
    fig_controls = plot_control_parameters(controls)
    st.plotly_chart(fig_controls, use_container_width=True)
    
    st.success(f"""
    **Current Control Values:**
    - Control 1: {controls['control_1']:.3f}
    - Control 2: {controls['control_2']:.3f}
    - Control 3: {controls['control_3']:.3f}
    - Control 4: {controls['control_4']:.3f}
    """)

st.markdown("---")

# Explanation
st.markdown("## 💡 Key Insights")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
    ### 🌊 Continuous Variation
    
    Brain signals vary **continuously** over time, not in discrete states.
    
    This makes them suitable for:
    - Expressive control
    - Smooth transitions
    - Nuanced performance
    
    But NOT suitable for:
    - Discrete commands
    - Mental state decoding
    - Thought reading
    """)

with col2:
    st.markdown("""
    ### 📊 Signal ≠ State
    
    We extract **features** (band powers), but we don't interpret them as 
    mental states.
    
    **These are control signals**, not:
    - Decoded intentions
    - Mental content
    - Cognitive processes
    
    Think of them like:
    - Gesture position
    - Breath pressure
    - Touch force
    """)

with col3:
    st.markdown("""
    ### 🎛️ Design Choice
    
    How we map these signals to sound is a **creative design decision**.
    
    We could map:
    - Linearly or nonlinearly
    - With smoothing or raw
    - Inverted or direct
    - To any sound parameter
    
    **This is explored on the Mapping page.**
    """)

st.markdown("---")

# Interactive exploration
st.markdown("## 🔬 Explore Signal Behavior")

st.markdown("""
Try adjusting the parameters in the sidebar to see how they affect the signal:

### Experiments to Try:

1. **Low Arousal, High Focus** → See reduced alpha, steady beta
2. **High Arousal, Low Focus** → See increased beta and theta
3. **High Variability** → Notice how noise makes control harder
4. **Low Variability** → Signal becomes more predictable

### What You'll Notice:

- Signals are **never stable** — always varying
- Features change **slowly** — good for smooth control
- Noise creates **unpredictability** — part of the instrument's character
- Different parameter combinations create **different control profiles**

This variability is **not a bug** — it's what makes the system expressive!
""")

st.markdown("---")

# Signal source types
st.markdown("## 🎚️ Signal Source Types in BrainJam")

st.markdown("""
BrainJam is designed to work with multiple signal sources, each with different characteristics:
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ### 🧪 **Mock Signals** (Current)
    
    **Status**: ✅ Fully Implemented
    
    What you're seeing on this page:
    - Simulated brain-like signals
    - Structured test data
    - Perfect for development and demos
    - No hardware required
    
    **Use Cases**:
    - System development
    - Mapping design
    - Performance rehearsal
    - Educational demonstrations
    """)
    
    st.markdown("""
    ### 🧠 **Real-Time EEG (LSL)** 
    
    **Status**: ⚠️ Experimental / Placeholder
    
    Future integration via Lab Streaming Layer:
    - Consumer EEG headsets (Muse, OpenBCI, etc.)
    - Medical-grade EEG systems
    - Band-power feature extraction
    - <100ms latency
    
    **Requirements**:
    - Hardware: EEG headset
    - Software: `pylsl` library
    - Setup: Stream configuration
    """)

with col2:
    st.markdown("""
    ### 🎹 **MIDI Controllers**
    
    **Status**: ⚠️ Experimental / Placeholder
    
    Standard MIDI control integration:
    - Keyboards, pads, breath controllers
    - CC (Continuous Controller) mapping
    - Combine with brain signals
    - Familiar interface for musicians
    
    **Requirements**:
    - Hardware: MIDI controller
    - Software: `mido` or `python-rtmidi`
    - Setup: Port configuration
    """)
    
    st.markdown("""
    ### 📡 **OSC (Open Sound Control)**
    
    **Status**: ⚠️ Experimental / Placeholder
    
    Network-based control protocol:
    - TouchOSC, Lemur, Max/MSP
    - Flexible address mapping
    - Multi-device support
    - Over WiFi or ethernet
    
    **Requirements**:
    - Software: `python-osc` library
    - Setup: IP address and port
    - Controller app on phone/tablet
    """)

st.info("""
**Note**: Experimental devices currently use mock data. They demonstrate the interface 
but don't connect to real hardware yet. This shows how BrainJam is designed for 
**modularity** and **future expansion**.
""")

st.markdown("---")

# Comparison to other modalities
st.markdown("## 🎸 Comparison to Other Control Modalities")

st.markdown("""
| Modality | Continuous? | Noisy? | Latency | Expressiveness |
|----------|-------------|--------|---------|----------------|
| **EEG/fNIRS** | ✅ Yes | ⚠️ High | ~50ms | Medium-High |
| **Keyboard/MIDI** | ✅ Yes | ✅ Low | ~10ms | High |
| **Gesture (IMU)** | ✅ Yes | ⚠️ Medium | ~20ms | High |
| **Breath Controller** | ✅ Yes | ✅ Low | ~15ms | High |
| **Touch/Pressure** | ✅ Yes | ✅ Low | ~5ms | High |
| **OSC** | ✅ Yes | ✅ Low | ~20ms | High |

**Key Point**: Brain signals are **noisier and slower** than traditional controls, 
but offer **alternative embodiment** — hands-free, internal, different motor pathways.

**This is not about being "better"** — it's about offering a **different expressive dimension**.
""")

st.markdown("---")

st.markdown("""
## 🎼 The Instrument Metaphor

Think of these signals like a traditional instrument:

- **Guitar strings** vibrate continuously and unpredictably
- **Breath** varies with each moment
- **Vocal cords** produce noisy, complex vibrations
- **Fingers on keys** never hit exactly the same spot

The **imperfection and variation** are part of what makes instruments expressive.

BrainJam embraces signal variability as **expressive potential**, not error.

---

👈 **Next**: Go to **3. Mapping** to see how these signals become control parameters.
""")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
## 📊 Signals Page

Explore how mock brain signals:
- Vary over time
- Respond to parameters
- Transform to controls

### Current Settings
Adjust sliders above to explore signal behavior.
""")
