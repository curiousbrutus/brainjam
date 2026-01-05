"""
Page 5: Live Performance - MVP Demo
"""

import streamlit as st
import numpy as np
import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils import MockSignalGenerator, normalize_features, create_audio_player_html
from performance_system.sound_engines import ParametricSynth
from performance_system.mapping_models import LinearMapper

# Import BioSignalInference
try:
    from src.bridge.latent_mapper import BioSignalInference
    BIOSIGNAL_AVAILABLE = True
except ImportError:
    BIOSIGNAL_AVAILABLE = False

# Import HybridAdaptiveAgent
try:
    from performance_system.agents import HybridAdaptiveAgent
    HYBRID_AGENT_AVAILABLE = True
except ImportError:
    HYBRID_AGENT_AVAILABLE = False

# Constants
ML_MODEL_PATH = "models/adaptive_mapper.pth"

st.set_page_config(page_title="Live Performance", page_icon="🎭", layout="wide")

st.title("🎭 Live Performance: System MVP")

st.markdown("""
---

## 🎼 Complete System Demo

This page demonstrates the **full BrainJam pipeline** in action:

**Signal → Features → Mapping → Sound → Feedback**

This is the core MVP — a working performance system.

---
""")

# Initialize components in session state
if 'perf_signal_gen' not in st.session_state:
    st.session_state.perf_signal_gen = MockSignalGenerator(fs=250)
    
if 'perf_synth' not in st.session_state:
    st.session_state.perf_synth = ParametricSynth(sample_rate=44100, base_freq=220.0)
    
if 'perf_mapper' not in st.session_state:
    st.session_state.perf_mapper = LinearMapper(n_inputs=4, n_outputs=4)

if 'perf_biosignal' not in st.session_state and BIOSIGNAL_AVAILABLE:
    st.session_state.perf_biosignal = BioSignalInference(
        eeg_channels=8,
        fnirs_channels=2,
        emg_channels=1,
        sample_rate=250.0,
        buffer_size=500
    )

if 'perf_hybrid_agent' not in st.session_state and HYBRID_AGENT_AVAILABLE:
    st.session_state.perf_hybrid_agent = HybridAdaptiveAgent(
        buffer_duration=10.0,
        sample_rate=10.0,
        model_path=ML_MODEL_PATH
    )
    
if 'performance_running' not in st.session_state:
    st.session_state.performance_running = False
    
if 'performance_history' not in st.session_state:
    st.session_state.performance_history = {
        'time': [],
        'control_1': [],
        'control_2': [],
        'control_3': [],
        'control_4': [],
    }

# Sidebar controls
st.sidebar.markdown("## 🎛️ Performance Settings")

st.sidebar.markdown("### Signal Source")
signal_source = st.sidebar.selectbox(
    "Control source:",
    options=[
        "Mock EEG",
        "BioSignal Inference (Multi-modal)",
        "Manual Sliders",
        "Realtime EEG (LSL) - Experimental",
        "MIDI Controller - Experimental", 
        "OSC Controller - Experimental"
    ],
    index=0
)

# Show warning for experimental sources
if "Experimental" in signal_source:
    st.sidebar.warning(
        "⚠️ **Experimental / Placeholder**\n\n"
        "This device is not yet fully implemented. "
        "It will use mock data for now."
    )

# Show info for BioSignal Inference
if signal_source == "BioSignal Inference (Multi-modal)":
    if not BIOSIGNAL_AVAILABLE:
        st.sidebar.error("❌ BioSignal Inference module not available. Install dependencies.")
        signal_source = "Mock EEG"  # Fallback
    else:
        st.sidebar.success("✅ BioSignal Inference Module Active")
        st.sidebar.info("🧠 EEG (8ch) + 🩸 fNIRS (2ch) + 💪 EMG (1ch)")

if signal_source == "Mock EEG":
    st.sidebar.markdown("### Mock Signal Parameters")
    arousal = st.sidebar.slider("Arousal", 0.0, 1.0, 0.5, 0.1)
    focus = st.sidebar.slider("Focus", 0.0, 1.0, 0.5, 0.1)
    variability = st.sidebar.slider("Variability", 0.0, 1.0, 0.3, 0.1)
elif signal_source == "BioSignal Inference (Multi-modal)":
    st.sidebar.markdown("### BioSignal Parameters")
    biosig_eeg_arousal = st.sidebar.slider("EEG Arousal", 0.0, 1.0, 0.5, 0.05)
    biosig_fnirs_load = st.sidebar.slider("fNIRS Cognitive Load", -1.0, 1.0, 0.2, 0.1)
    biosig_emg_effort = st.sidebar.slider("EMG Effort", 0.0, 1.0, 0.4, 0.05)
    biosig_noise = st.sidebar.slider("Signal Noise", 0.0, 0.3, 0.1, 0.05)
else:
    st.sidebar.markdown("### Manual Controls")
    manual_c1 = st.sidebar.slider("Control 1", 0.0, 1.0, 0.5, 0.05)
    manual_c2 = st.sidebar.slider("Control 2", 0.0, 1.0, 0.3, 0.05)
    manual_c3 = st.sidebar.slider("Control 3", 0.0, 1.0, 0.6, 0.05)
    manual_c4 = st.sidebar.slider("Control 4", 0.0, 1.0, 0.2, 0.05)

st.sidebar.markdown("### Mapping")
use_smoothing = st.sidebar.checkbox("Apply smoothing", value=True)
smoothing_alpha = st.sidebar.slider("Smoothing amount", 0.0, 0.95, 0.7, 0.05) if use_smoothing else 0.0

st.sidebar.markdown("### AI Co-Performer")
enable_hybrid_agent = st.sidebar.checkbox(
    "Enable Hybrid Adaptive Agent",
    value=False,
    help="Use adaptive AI co-performer with behavioral states"
)

if enable_hybrid_agent:
    enable_ml_personalization = st.sidebar.checkbox(
        "Enable ML personalization (requires trained model)",
        value=False,
        help=f"Load trained ML model from {ML_MODEL_PATH} for personalized responses"
    )
    
    if enable_ml_personalization:
        st.sidebar.info(
            f"🤖 ML personalization will be used if the model file exists at "
            f"`{ML_MODEL_PATH}`. Otherwise, symbolic rules will be used."
        )
else:
    enable_ml_personalization = False

st.sidebar.markdown("### Sound")
base_freq = st.sidebar.selectbox(
    "Base frequency",
    options=[110, 220, 440],
    index=1,
    format_func=lambda x: f"{x} Hz ({'A2' if x==110 else 'A3' if x==220 else 'A4'})"
)

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎮 Performance Controls")
    
    # Performance button
    if not st.session_state.performance_running:
        if st.button("▶️ Start Performance", type="primary", use_container_width=True):
            st.session_state.performance_running = True
            st.session_state.perf_synth.base_freq = base_freq
            st.session_state.perf_mapper.smoothing_alpha = smoothing_alpha
            st.rerun()
    else:
        if st.button("⏸️ Pause Performance", type="secondary", use_container_width=True):
            st.session_state.performance_running = False
            st.rerun()
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Reset System", use_container_width=True):
            st.session_state.perf_signal_gen.reset()
            st.session_state.perf_synth.reset()
            st.session_state.perf_mapper.reset()
            if 'perf_hybrid_agent' in st.session_state:
                st.session_state.perf_hybrid_agent.reset()
            st.session_state.performance_history = {
                'time': [],
                'control_1': [],
                'control_2': [],
                'control_3': [],
                'control_4': [],
            }
            st.rerun()
    
    with col_b:
        if st.button("🎵 Generate Chunk", use_container_width=True):
            # Generate one chunk of performance
            if signal_source == "Mock EEG":
                # Generate signal
                time_vec, signal, features = st.session_state.perf_signal_gen.generate_signal(
                    duration=1.0,
                    arousal=arousal,
                    focus=focus,
                    variability=variability
                )
                raw_controls = normalize_features(features)
            elif signal_source == "BioSignal Inference (Multi-modal)" and BIOSIGNAL_AVAILABLE:
                # Generate mock biosignals for BioSignalInference
                duration = 0.1
                n_samples = int(duration * st.session_state.perf_biosignal.sample_rate)
                t = np.linspace(0, duration, n_samples)
                
                # EEG
                eeg = np.zeros((n_samples, 8))
                for ch in range(8):
                    alpha = (1.0 - biosig_eeg_arousal) * np.sin(2 * np.pi * 10 * t + ch * 0.5)
                    beta = biosig_eeg_arousal * 1.5 * np.sin(2 * np.pi * 20 * t + ch * 0.3)
                    eeg[:, ch] = alpha + beta + biosig_noise * np.random.randn(n_samples)
                
                # fNIRS
                fnirs = np.zeros((n_samples, 2))
                fnirs[:, 0] = 0.5 + biosig_fnirs_load * t + biosig_noise * np.random.randn(n_samples)
                fnirs[:, 1] = 0.5 - biosig_fnirs_load * 0.5 * t + biosig_noise * np.random.randn(n_samples)
                
                # EMG
                emg = np.zeros((n_samples, 1))
                emg[:, 0] = biosig_emg_effort + 0.2 * np.sin(2 * np.pi * 5 * t) + biosig_noise * np.random.randn(n_samples)
                
                # Process with BioSignalInference
                style_vector = st.session_state.perf_biosignal.process_frame(eeg, fnirs, emg)
                
                # Use style vector directly (it's already in the right format for ParametricSynth)
                raw_controls = {
                    'tempo_density': style_vector['tempo_density'],
                    'harmonic_tension': style_vector['harmonic_tension'],
                    'spectral_brightness': style_vector['spectral_brightness'],
                    'noise_balance': style_vector['noise_balance']
                }
                
                # Show extracted features
                st.info(f"🧠 Arousal: {style_vector['arousal']:.2f} | "
                       f"🩸 Cognitive Load: {style_vector['cognitive_load']:.2f} | "
                       f"💪 Effort: {style_vector['effort']:.2f}")
                
                if style_vector['arousal'] > 0.8 and style_vector['effort'] > 0.7:
                    st.success("⚡ **TRIGGER ACTIVE** — 180 BPM rhythm!")
            else:
                raw_controls = {
                    'control_1': manual_c1,
                    'control_2': manual_c2,
                    'control_3': manual_c3,
                    'control_4': manual_c4,
                }
            
            # Apply mapping (skip for BioSignalInference as it already outputs mapped values)
            if signal_source == "BioSignal Inference (Multi-modal)" and BIOSIGNAL_AVAILABLE:
                mapped_controls = raw_controls  # Already mapped
            else:
                mapped_controls = st.session_state.perf_mapper.map(raw_controls)
            
            # Apply hybrid agent if enabled
            if enable_hybrid_agent and HYBRID_AGENT_AVAILABLE and 'perf_hybrid_agent' in st.session_state:
                # Get agent response
                agent_response = st.session_state.perf_hybrid_agent.respond(mapped_controls)
                agent_state = st.session_state.perf_hybrid_agent.get_state()
                
                # Blend agent response with performer controls
                # Agent modulates density and tension
                mapped_controls['control_2'] = agent_response['note_density']
                mapped_controls['control_3'] = agent_response['harmonic_tension']
                
                # Show agent state
                st.info(
                    f"🤖 AI Agent: **{agent_state['behavioral_state'].upper()}** | "
                    f"Intensity: {agent_state['ema_intensity']:.2f} | "
                    f"Density: {agent_state['ema_density']:.2f} | "
                    f"ML: {'✓' if agent_state['ml_available'] else '✗'}"
                )
            
            # Generate audio
            audio = st.session_state.perf_synth.generate(2.0, mapped_controls)
            
            # Display
            st.success("✅ Chunk generated!")
            audio_html = create_audio_player_html(audio, sample_rate=44100)
            st.markdown(audio_html, unsafe_allow_html=True)
            
            # Add to history
            current_time = len(st.session_state.performance_history['time'])
            st.session_state.performance_history['time'].append(current_time)
            st.session_state.performance_history['control_1'].append(mapped_controls['control_1'])
            st.session_state.performance_history['control_2'].append(mapped_controls['control_2'])
            st.session_state.performance_history['control_3'].append(mapped_controls['control_3'])
            st.session_state.performance_history['control_4'].append(mapped_controls['control_4'])

with col2:
    st.markdown("### 📊 System Status")
    
    if st.session_state.performance_running:
        st.success("🟢 **PERFORMING**")
    else:
        st.info("⚪ **PAUSED**")
    
    st.metric("Signal Source", signal_source)
    st.metric("Mapping", "Linear" + (" + Smoothing" if use_smoothing else ""))
    st.metric("Base Frequency", f"{base_freq} Hz")
    st.metric("Chunks Generated", len(st.session_state.performance_history['time']))

st.markdown("---")

# Visualization
if len(st.session_state.performance_history['time']) > 0:
    st.markdown("### 📈 Control Parameter History")
    
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    for i, control in enumerate(['control_1', 'control_2', 'control_3', 'control_4'], 1):
        fig.add_trace(go.Scatter(
            x=st.session_state.performance_history['time'],
            y=st.session_state.performance_history[control],
            mode='lines+markers',
            name=f'Control {i}',
            line=dict(color=colors[i-1], width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="Control Parameters Over Time",
        xaxis_title="Chunk Number",
        yaxis_title="Control Value (0-1)",
        yaxis_range=[0, 1],
        height=400,
        margin=dict(l=50, r=20, t=50, b=50),
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👆 Click **'Generate Chunk'** to start creating audio and see control history.")

st.markdown("---")

# Instructions
st.markdown("## 📖 How to Use")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
    ### 1. Configure
    
    - Choose signal source (Mock EEG or Manual)
    - Adjust signal/mapping parameters
    - Set base frequency
    
    These settings affect the character of your performance.
    """)

with col2:
    st.markdown("""
    ### 2. Generate
    
    - Click **"Generate Chunk"** to create audio
    - Listen to the result
    - Observe control parameter values
    
    Each chunk is ~2 seconds of audio.
    """)

with col3:
    st.markdown("""
    ### 3. Explore
    
    - Try different parameter combinations
    - Watch how controls evolve over time
    - Notice the feedback relationship
    
    Build an intuition for the instrument!
    """)

st.markdown("---")

# Performance context
st.markdown("## 🎭 Understanding Performance")

st.markdown("""
### What You're Experiencing

This simplified demo shows the **core performance loop**:

1. **Signal** is generated (mock EEG or manual)
2. **Features** are extracted and normalized
3. **Mapping** transforms features to controls
4. **Sound** is synthesized based on controls
5. **Feedback** — you hear the result and adjust

### In a Real Performance

In a full BrainJam performance:

- **Continuous loop** — No button clicks, real-time stream
- **Real-time audio** — Immediate playback, <100ms latency
- **Live biofeedback** — Actual EEG/fNIRS signals (optional)
- **Visual feedback** — Real-time display of parameters
- **Extended duration** — Minutes to hours, not just chunks
- **Audience** — Public performance context

### The "Instrument" Emerges

As you use the system:

- You learn which **signal ranges** create which **sounds**
- You develop **control strategies** (conscious or not)
- The system becomes **predictable but not deterministic**
- You feel **agency** over the output
- You enter **flow state** during successful performance

This is what makes it a **playable instrument**.
""")

st.markdown("---")

# Limitations and future
with st.expander("⚠️ Current Limitations & Future Work"):
    st.markdown("""
    ### This Demo's Limitations
    
    - **Not continuous** — Chunk-based generation
    - **No real audio output** — Browser playback only
    - **Simplified mapping** — Linear only
    - **No AI co-performance** — Static synthesis
    - **No recording** — Can't save sessions
    
    ### Full System Features (Future)
    
    #### Real-Time Audio
    - PyAudio integration
    - Continuous streaming
    - <100ms latency
    - Buffer management
    
    #### Advanced Mapping
    - MLP nonlinear mapping
    - Adaptive smoothing
    - Personalized training
    
    #### AI Co-Performer
    - Temporal prediction
    - Call-and-response patterns
    - Adaptive timing
    - Variation generation
    
    #### Performance Tools
    - Recording and playback
    - Session analysis
    - Practice mode
    - Performance mode
    
    #### Interaction Measures
    - Agency tracking
    - Flow assessment
    - Latency measurement
    - Control stability metrics
    """)

st.markdown("---")

# Evaluation
st.markdown("## 📊 Simple Self-Assessment")

st.markdown("""
After using this system for a while, reflect on your experience:
""")

col1, col2 = st.columns([1, 1])

with col1:
    sense_of_control = st.slider(
        "**Sense of Control**  \n'I felt in control of the sounds'",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = No control, 10 = Full control"
    )
    
    responsiveness = st.slider(
        "**Responsiveness**  \n'The system responded predictably'",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = Unpredictable, 10 = Very predictable"
    )

with col2:
    engagement = st.slider(
        "**Engagement**  \n'I was fully engaged with the system'",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = Not engaged, 10 = Fully engaged"
    )
    
    enjoyment = st.slider(
        "**Enjoyment**  \n'I enjoyed using this system'",
        min_value=1,
        max_value=10,
        value=5,
        help="1 = Not at all, 10 = Very much"
    )

if st.button("📝 Submit Feedback", use_container_width=False):
    st.success(f"""
    **Thank you for your feedback!**
    
    Your responses:
    - Sense of Control: {sense_of_control}/10
    - Responsiveness: {responsiveness}/10
    - Engagement: {engagement}/10
    - Enjoyment: {enjoyment}/10
    
    (In a real study, this would be recorded for analysis)
    """)

st.markdown("---")

st.markdown("""
## 💡 Key Insights

- **This is a complete performance pipeline** — All components working together
- **Simplicity enables understanding** — You can trace signal → sound
- **Iteration reveals playability** — The more you use it, the more controllable it feels
- **Feedback is essential** — Without hearing the result, you can't learn the instrument
- **Variability is expressive** — Imperfection creates character

This demo proves the **concept works** — signals can drive musical performance.

---

👈 **Next**: Go to **6. Use Cases** to see how this connects to research and artistic practice.
""")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
## 🎭 Live Performance Page

The complete system in action:
- Generate audio chunks
- Adjust parameters live
- Build control intuition
- Experience the feedback loop

**This is the MVP!**
""")
