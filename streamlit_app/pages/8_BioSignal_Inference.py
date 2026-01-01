"""
Page 8: BioSignal Inference - Multi-modal Brain Signal Processing

Demonstrates the BioSignalInference module that processes synchronized
EEG, fNIRS, and EMG signals into latent style vectors for audio synthesis.
"""

import streamlit as st
import numpy as np
import sys
import os
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.bridge.latent_mapper import BioSignalInference
from performance_system.sound_engines import ParametricSynth

st.set_page_config(page_title="BioSignal Inference", page_icon="🧠", layout="wide")

st.title("🧠 BioSignal Inference: Multi-Modal Processing")

st.markdown("""
---

## 🔬 Advanced Multi-Modal Signal Processing

This page demonstrates the **BioSignalInference module** — the "brain" of the BrainJam system.

### Key Features:
- 🧠 **EEG (8 channels)**: Beta/Alpha ratio → Arousal proxy
- 🩸 **fNIRS (2 channels)**: HbO2 slope → Cognitive Load/Valence proxy  
- 💪 **EMG (1 channel)**: RMS amplitude → Physical Effort proxy
- ⚡ **Conditional Trigger**: Activates 180 BPM rhythm when Arousal > 0.8 AND Effort > 0.7
- 🚀 **High Performance**: <1ms latency (170× under 100ms budget)

---
""")

# Initialize BioSignalInference processor in session state
if 'biosignal_processor' not in st.session_state:
    st.session_state.biosignal_processor = BioSignalInference(
        eeg_channels=8,
        fnirs_channels=2,
        emg_channels=1,
        sample_rate=250.0,
        buffer_size=500
    )
    
if 'biosignal_synth' not in st.session_state:
    st.session_state.biosignal_synth = ParametricSynth(sample_rate=44100, base_freq=220.0)

if 'biosignal_history' not in st.session_state:
    st.session_state.biosignal_history = {
        'arousal': [],
        'cognitive_load': [],
        'effort': [],
        'tempo_density': [],
        'trigger_active': []
    }

# Sidebar controls
st.sidebar.markdown("## 🎛️ Signal Parameters")

st.sidebar.markdown("### EEG Simulation")
eeg_arousal = st.sidebar.slider(
    "**Arousal Level**",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Higher arousal → more beta activity relative to alpha"
)

eeg_noise = st.sidebar.slider(
    "**EEG Noise**",
    min_value=0.0,
    max_value=0.5,
    value=0.1,
    step=0.05,
    help="Amount of random noise in EEG signal"
)

st.sidebar.markdown("### fNIRS Simulation")
fnirs_slope = st.sidebar.slider(
    "**Cognitive Load**",
    min_value=-1.0,
    max_value=1.0,
    value=0.2,
    step=0.1,
    help="Positive slope → increasing cognitive engagement"
)

fnirs_noise = st.sidebar.slider(
    "**fNIRS Noise**",
    min_value=0.0,
    max_value=0.3,
    value=0.05,
    step=0.01,
    help="Amount of random noise in fNIRS signal"
)

st.sidebar.markdown("### EMG Simulation")
emg_effort = st.sidebar.slider(
    "**Physical Effort**",
    min_value=0.0,
    max_value=1.0,
    value=0.4,
    step=0.05,
    help="EMG amplitude (muscle activation level)"
)

emg_noise = st.sidebar.slider(
    "**EMG Noise**",
    min_value=0.0,
    max_value=0.3,
    value=0.1,
    step=0.05,
    help="Amount of random noise in EMG signal"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Processing")

chunk_duration = st.sidebar.slider(
    "**Processing Window (ms)**",
    min_value=50,
    max_value=500,
    value=100,
    step=50,
    help="Duration of signal chunk to process"
)

if st.sidebar.button("🔄 Reset Processor", use_container_width=True):
    st.session_state.biosignal_processor.reset_buffers()
    st.session_state.biosignal_history = {
        'arousal': [],
        'cognitive_load': [],
        'effort': [],
        'tempo_density': [],
        'trigger_active': []
    }
    st.rerun()


def generate_mock_biosignals(duration_sec=0.1):
    """Generate mock EEG, fNIRS, and EMG signals"""
    processor = st.session_state.biosignal_processor
    n_samples = int(duration_sec * processor.sample_rate)
    t = np.linspace(0, duration_sec, n_samples)
    
    # EEG: Generate alpha and beta components
    eeg = np.zeros((n_samples, processor.eeg_channels))
    for ch in range(processor.eeg_channels):
        # Alpha band (8-13 Hz) - inversely related to arousal
        alpha_amp = (1.0 - eeg_arousal) * 1.0
        alpha = alpha_amp * np.sin(2 * np.pi * 10 * t + ch * 0.5)
        
        # Beta band (13-30 Hz) - directly related to arousal
        beta_amp = eeg_arousal * 1.5
        beta = beta_amp * np.sin(2 * np.pi * 20 * t + ch * 0.3)
        
        # Noise
        noise = eeg_noise * np.random.randn(n_samples)
        
        eeg[:, ch] = alpha + beta + noise
    
    # fNIRS: Generate HbO2 and HbR with slope
    fnirs = np.zeros((n_samples, processor.fnirs_channels))
    fnirs[:, 0] = 0.5 + fnirs_slope * t + fnirs_noise * np.random.randn(n_samples)  # HbO2
    fnirs[:, 1] = 0.5 - fnirs_slope * 0.5 * t + fnirs_noise * np.random.randn(n_samples)  # HbR
    
    # EMG: Generate muscle activation signal
    emg = np.zeros((n_samples, processor.emg_channels))
    emg[:, 0] = emg_effort + 0.2 * np.sin(2 * np.pi * 5 * t) + emg_noise * np.random.randn(n_samples)
    
    return eeg, fnirs, emg


# Main processing demo
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 Real-Time Processing")
    
    if st.button("▶️ Process Signal Chunk", type="primary", use_container_width=True):
        # Generate mock signals
        duration = chunk_duration / 1000.0  # Convert ms to seconds
        eeg_frame, fnirs_frame, emg_frame = generate_mock_biosignals(duration)
        
        # Process with BioSignalInference
        start_time = time.perf_counter()
        style_vector = st.session_state.biosignal_processor.process_frame(
            eeg_frame, fnirs_frame, emg_frame
        )
        latency_ms = (time.perf_counter() - start_time) * 1000
        
        # Update history
        st.session_state.biosignal_history['arousal'].append(style_vector['arousal'])
        st.session_state.biosignal_history['cognitive_load'].append(style_vector['cognitive_load'])
        st.session_state.biosignal_history['effort'].append(style_vector['effort'])
        st.session_state.biosignal_history['tempo_density'].append(style_vector['tempo_density'])
        
        # Check if trigger is active
        trigger = (style_vector['arousal'] > st.session_state.biosignal_processor.arousal_threshold and 
                  style_vector['effort'] > st.session_state.biosignal_processor.effort_threshold)
        st.session_state.biosignal_history['trigger_active'].append(trigger)
        
        # Keep only last 50 samples
        max_history = 50
        for key in st.session_state.biosignal_history:
            if len(st.session_state.biosignal_history[key]) > max_history:
                st.session_state.biosignal_history[key] = st.session_state.biosignal_history[key][-max_history:]
        
        # Display current values
        st.markdown("#### Current Feature Extraction")
        
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric(
                "🧠 Arousal",
                f"{style_vector['arousal']:.3f}",
                help="Beta/Alpha ratio (higher = more activated)"
            )
        
        with metrics_col2:
            st.metric(
                "🩸 Cognitive Load",
                f"{style_vector['cognitive_load']:.3f}",
                help="fNIRS HbO2 slope (higher = more engaged)"
            )
        
        with metrics_col3:
            st.metric(
                "💪 Effort",
                f"{style_vector['effort']:.3f}",
                help="EMG RMS (higher = more muscle activation)"
            )
        
        with metrics_col4:
            st.metric(
                "⚡ Processing",
                f"{latency_ms:.2f} ms",
                help="Feature extraction latency"
            )
        
        st.markdown("#### Style Vector Output")
        
        style_col1, style_col2, style_col3, style_col4 = st.columns(4)
        
        with style_col1:
            st.metric(
                "🎵 Tempo Density",
                f"{style_vector['tempo_density']:.3f}",
                help="Event rate (0=sparse, 1=dense)"
            )
        
        with style_col2:
            st.metric(
                "🎼 Harmonic Tension",
                f"{style_vector['harmonic_tension']:.3f}",
                help="Consonance/dissonance"
            )
        
        with style_col3:
            st.metric(
                "✨ Spectral Brightness",
                f"{style_vector['spectral_brightness']:.3f}",
                help="Filter cutoff/brightness"
            )
        
        with style_col4:
            st.metric(
                "🔊 Noise Balance",
                f"{style_vector['noise_balance']:.3f}",
                help="Mix of noise vs tones"
            )
        
        # Show trigger status
        if trigger:
            st.success("⚡ **TRIGGER ACTIVE** — 180 BPM rhythm engaged! (Arousal > 0.8 AND Effort > 0.7)")
        else:
            st.info(f"Trigger conditions: Arousal={style_vector['arousal']:.2f} (need >0.8), Effort={style_vector['effort']:.2f} (need >0.7)")

with col2:
    st.markdown("### 📈 Performance Stats")
    
    stats = st.session_state.biosignal_processor.get_performance_stats()
    
    st.metric("Mean Latency", f"{stats['mean_latency_ms']:.2f} ms")
    st.metric("Std Latency", f"{stats['std_latency_ms']:.2f} ms")
    st.metric("Max Latency", f"{stats['max_latency_ms']:.2f} ms")
    st.metric("P95 Latency", f"{stats['p95_latency_ms']:.2f} ms")
    
    if stats['p95_latency_ms'] > 0:
        if stats['p95_latency_ms'] < 100:
            st.success(f"✅ {stats['p95_latency_ms']:.2f}ms < 100ms budget")
        else:
            st.error(f"❌ {stats['p95_latency_ms']:.2f}ms > 100ms budget")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Module Info")
    st.info(f"""
    **Channels:**
    - EEG: {st.session_state.biosignal_processor.eeg_channels}
    - fNIRS: {st.session_state.biosignal_processor.fnirs_channels}
    - EMG: {st.session_state.biosignal_processor.emg_channels}
    
    **Sample Rate:** {st.session_state.biosignal_processor.sample_rate} Hz  
    **Buffer Size:** {st.session_state.biosignal_processor.buffer_size} samples  
    **Device:** {st.session_state.biosignal_processor.device}
    """)

# History plot
if len(st.session_state.biosignal_history['arousal']) > 0:
    st.markdown("---")
    st.markdown("### 📉 Feature History")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Arousal (Beta/Alpha)', 'Cognitive Load (fNIRS)', 
                       'Effort (EMG RMS)', 'Tempo Density (Output)'),
        vertical_spacing=0.15
    )
    
    # Arousal
    fig.add_trace(
        go.Scatter(
            y=st.session_state.biosignal_history['arousal'],
            mode='lines+markers',
            name='Arousal',
            line=dict(color='#ff6b6b', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    fig.add_hline(y=0.8, line_dash="dash", line_color="red", row=1, col=1,
                  annotation_text="Trigger threshold")
    
    # Cognitive Load
    fig.add_trace(
        go.Scatter(
            y=st.session_state.biosignal_history['cognitive_load'],
            mode='lines+markers',
            name='Cognitive Load',
            line=dict(color='#4ecdc4', width=2),
            marker=dict(size=4)
        ),
        row=1, col=2
    )
    
    # Effort
    fig.add_trace(
        go.Scatter(
            y=st.session_state.biosignal_history['effort'],
            mode='lines+markers',
            name='Effort',
            line=dict(color='#f7b731', width=2),
            marker=dict(size=4)
        ),
        row=2, col=1
    )
    fig.add_hline(y=0.7, line_dash="dash", line_color="orange", row=2, col=1,
                  annotation_text="Trigger threshold")
    
    # Tempo Density (with trigger highlights)
    colors = ['red' if t else '#95a5a6' for t in st.session_state.biosignal_history['trigger_active']]
    fig.add_trace(
        go.Scatter(
            y=st.session_state.biosignal_history['tempo_density'],
            mode='lines+markers',
            name='Tempo Density',
            line=dict(color='#a29bfe', width=2),
            marker=dict(size=6, color=colors)
        ),
        row=2, col=2
    )
    
    fig.update_xaxes(title_text="Sample", row=2, col=1)
    fig.update_xaxes(title_text="Sample", row=2, col=2)
    fig.update_yaxes(title_text="Value", range=[0, 1], row=1, col=1)
    fig.update_yaxes(title_text="Value", range=[0, 1], row=1, col=2)
    fig.update_yaxes(title_text="Value", range=[0, 1], row=2, col=1)
    fig.update_yaxes(title_text="Value", range=[0, 1], row=2, col=2)
    
    fig.update_layout(
        height=600,
        showlegend=False,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Information section
st.markdown("---")
st.markdown("## 📚 Technical Details")

with st.expander("🔬 Feature Extraction Methods"):
    st.markdown("""
    ### EEG: Beta/Alpha Ratio (Arousal)
    
    **Method**: FFT-based power spectral density
    - **Alpha band**: 8-13 Hz (relaxation, lower arousal)
    - **Beta band**: 13-30 Hz (active thinking, higher arousal)
    - **Ratio**: `arousal = sigmoid(beta_power / alpha_power)`
    
    Higher values indicate increased arousal/activation state.
    
    ### fNIRS: HbO2 Slope (Cognitive Load)
    
    **Method**: Linear regression on oxygenated hemoglobin signal
    - Positive slope → increasing cognitive engagement
    - Negative slope → decreasing cognitive engagement
    - **Formula**: `load = tanh(slope × 100)`
    
    Reflects changes in cortical activation over the measurement window.
    
    ### EMG: RMS (Physical Effort)
    
    **Method**: Root Mean Square of EMG amplitude
    - **Formula**: `effort = sigmoid(rms × 5)`
    - Higher values indicate greater muscle activation
    
    Provides continuous measure of physical exertion level.
    """)

with st.expander("🎵 Style Vector Mapping"):
    st.markdown("""
    ### Mapping Features to Audio Parameters
    
    The extracted features are mapped to ParametricSynth control parameters:
    
    - **tempo_density** = arousal × 0.6 + effort × 0.4
      - Controls event rate (0=sparse, 1=dense)
      
    - **harmonic_tension** = cognitive_load
      - Controls consonance/dissonance
      
    - **spectral_brightness** = arousal
      - Controls filter cutoff/brightness
      
    - **noise_balance** = effort
      - Controls mix of noise vs tones
    
    ### Conditional Trigger
    
    When **both** conditions are met:
    - Arousal > 0.8 **AND**
    - Effort > 0.7
    
    The system automatically sets `tempo_density = 1.0`, triggering a 180 BPM rhythmic pattern.
    """)

with st.expander("⚡ Performance Characteristics"):
    st.markdown("""
    ### Latency Analysis
    
    The BioSignalInference module is optimized for real-time processing:
    
    - **Target**: < 100ms (musical performance requirement)
    - **Achieved**: ~0.6ms P95 latency
    - **Performance**: 170× faster than budget
    
    ### Optimization Strategies
    
    1. **Ring Buffers**: Efficient memory management with deque
    2. **NumPy FFT**: CPU-optimized fast Fourier transform
    3. **Named Constants**: Pre-computed normalization parameters
    4. **Independent Normalization**: Avoids expensive softmax operations
    
    ### Scalability
    
    - Can process 100ms chunks in ~0.6ms
    - Supports GPU acceleration for larger buffer sizes
    - Handles 8 EEG + 2 fNIRS + 1 EMG channels simultaneously
    """)

with st.expander("🔗 Integration with LSL"):
    st.markdown("""
    ### Lab Streaming Layer (LSL) Integration
    
    For real-time hardware integration:
    
    ```python
    from pylsl import StreamInlet, resolve_stream
    from src.bridge.latent_mapper import BioSignalInference
    
    # Resolve LSL streams
    eeg_streams = resolve_stream('type', 'EEG')
    fnirs_streams = resolve_stream('type', 'fNIRS')
    emg_streams = resolve_stream('type', 'EMG')
    
    # Create inlets
    eeg_inlet = StreamInlet(eeg_streams[0])
    fnirs_inlet = StreamInlet(fnirs_streams[0])
    emg_inlet = StreamInlet(emg_streams[0])
    
    # Initialize processor
    processor = BioSignalInference()
    
    # Real-time loop
    while True:
        eeg_samples, _ = eeg_inlet.pull_chunk()
        fnirs_samples, _ = fnirs_inlet.pull_chunk()
        emg_samples, _ = emg_inlet.pull_chunk()
        
        style_vector = processor.process_frame(
            np.array(eeg_samples),
            np.array(fnirs_samples),
            np.array(emg_samples)
        )
        
        # Use style_vector for synthesis...
    ```
    
    See `src/bridge/README.md` for complete documentation.
    """)

st.markdown("---")
st.markdown("""
### 🎯 Next Steps

1. **Experiment** with different signal parameters to see how they affect feature extraction
2. **Watch** for the conditional trigger when arousal and effort are both high
3. **Observe** the processing latency staying well under the 100ms budget
4. **Integrate** with real LSL streams for actual EEG/fNIRS/EMG hardware

For more information, see:
- `src/bridge/README.md` — Complete API documentation
- `examples/biosignal_integration_demo.py` — Integration example
- `validate_biosignal_inference.py` — Test suite
""")
