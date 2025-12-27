"""
Page 7: Feature Shaping - Latent Control Generation
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from performance_system.controllers.mock_eeg import MockEEGController
from performance_system.feature_shaping import PCAReducer, TemporalSmoother

st.set_page_config(page_title="Feature Shaping", page_icon="🔬", layout="wide")

st.title("🔬 Feature Shaping: Latent Control Generation")

st.markdown("""
---

## 🧠 From Noisy Signals to Expressive Controls

**Feature shaping** transforms high-dimensional, noisy brain signals into 2-8 clean latent controls.

These latents represent:
- Intensity
- Tension
- Volatility
- Density
- Timing bias

**NOT mental states** — just continuous control parameters for artistic expression.

---
""")

# Initialize components
if 'signal_gen' not in st.session_state or not isinstance(st.session_state.signal_gen, MockEEGController):
    st.session_state.signal_gen = MockEEGController(fs=250)

# Sidebar controls
st.sidebar.markdown("## 🎛️ Feature Shaping Settings")

shaping_method = st.sidebar.radio(
    "Method:",
    options=["Temporal Smoothing", "PCA Reduction"],
    index=0
)

if shaping_method == "Temporal Smoothing":
    window_size = st.sidebar.slider("Window size", 5, 50, 10)
    smoothing_mode = st.sidebar.selectbox(
        "Smoothing mode",
        options=["exponential", "moving_average", "median"]
    )
    
    if 'smoother' not in st.session_state or \
       st.session_state.get('smoother_window') != window_size or \
       st.session_state.get('smoother_mode') != smoothing_mode:
        st.session_state.smoother = TemporalSmoother(
            n_features=4,
            window_size=window_size,
            smoothing_mode=smoothing_mode
        )
        st.session_state.smoother_window = window_size
        st.session_state.smoother_mode = smoothing_mode

elif shaping_method == "PCA Reduction":
    n_components = st.sidebar.slider("Number of components", 2, 8, 4)
    
    if 'pca' not in st.session_state or \
       st.session_state.get('pca_components') != n_components:
        # Generate training data
        training_data = []
        temp_gen = MockEEGController(fs=250)
        for _ in range(100):
            features = temp_gen.get_control_vector(duration=0.5)
            feature_array = np.array([features.get(f'control_{i}', 0.5) 
                                     for i in range(1, 5)])
            training_data.append(feature_array)
        
        X_train = np.array(training_data)
        
        # Fit PCA
        pca = PCAReducer(n_components=n_components, whiten=True)
        pca.fit(X_train)
        st.session_state.pca = pca
        st.session_state.pca_components = n_components

# Signal simulation
st.sidebar.markdown("## 📊 Signal Simulation")
arousal = st.sidebar.slider("Arousal", 0.0, 1.0, 0.5, 0.1)
focus = st.sidebar.slider("Focus", 0.0, 1.0, 0.5, 0.1)

# Generate and process signal
n_samples = 100
raw_signals = []
shaped_outputs = []

for _ in range(n_samples):
    # Generate raw signal features
    features = st.session_state.signal_gen.get_control_vector(duration=0.5)
    
    # Convert features to array for processing
    feature_array = np.array([features.get(f'control_{i}', 0.5) for i in range(1, 5)])
    
    # Apply shaping
    if shaping_method == "Temporal Smoothing":
        shaped_dict = st.session_state.smoother.update(feature_array)
        shaped_output = np.array([shaped_dict.get(f'control_{i}', 0.5) for i in range(1, 5)])
    else:  # PCA
        shaped_dict = st.session_state.pca.transform(feature_array)
        # Extract values from dict - PCA returns latent_1, latent_2, etc.
        n_latents = len(shaped_dict)
        shaped_output = np.array([shaped_dict.get(f'latent_{i+1}', 0.5) for i in range(n_latents)])
    
    raw_signals.append(feature_array)
    shaped_outputs.append(shaped_output)

raw_signals = np.array(raw_signals)
shaped_outputs = np.array(shaped_outputs)

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📉 Raw Signals (Before Shaping)")
    
    fig_raw = go.Figure()
    time_axis = np.arange(n_samples) * 0.1
    
    for i in range(4):
        fig_raw.add_trace(go.Scatter(
            x=time_axis,
            y=raw_signals[:, i],
            mode='lines',
            name=f'Control {i+1}',
            line=dict(width=1.5)
        ))
    
    fig_raw.update_layout(
        xaxis_title="Time (s)",
        yaxis_title="Value",
        height=400,
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig_raw, use_container_width=True)
    
    st.info("""
    **Raw signals** are noisy and rapidly varying.
    This is typical of brain signal features (band powers, etc.).
    """)

with col2:
    st.markdown("### 📈 Shaped Latents (After Shaping)")
    
    fig_shaped = go.Figure()
    
    n_outputs = shaped_outputs.shape[1]
    for i in range(n_outputs):
        fig_shaped.add_trace(go.Scatter(
            x=time_axis,
            y=shaped_outputs[:, i],
            mode='lines',
            name=f'Latent {i+1}',
            line=dict(width=2)
        ))
    
    fig_shaped.update_layout(
        xaxis_title="Time (s)",
        yaxis_title="Value",
        height=400,
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig_shaped, use_container_width=True)
    
    st.success("""
    **Shaped latents** are smoother and more stable.
    These are suitable for expressive musical control.
    """)

# Statistics
st.markdown("---")
st.markdown("### 📊 Statistical Comparison")

col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.metric(
        "Raw Signal Variance",
        f"{np.mean(np.var(raw_signals, axis=0)):.4f}",
        help="Higher variance = more noise"
    )

with col_stat2:
    st.metric(
        "Shaped Signal Variance",
        f"{np.mean(np.var(shaped_outputs, axis=0)):.4f}",
        delta=f"{(np.mean(np.var(shaped_outputs, axis=0)) - np.mean(np.var(raw_signals, axis=0))):.4f}",
        delta_color="inverse",
        help="Lower is better for stability"
    )

with col_stat3:
    st.metric(
        "Variance Reduction",
        f"{(1 - np.mean(np.var(shaped_outputs, axis=0)) / np.mean(np.var(raw_signals, axis=0))) * 100:.1f}%",
        help="Percentage reduction in variance"
    )

# Explanation
st.markdown("---")
st.markdown("### 💡 Why Feature Shaping?")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    st.markdown("""
    **Problems with raw signals:**
    - 🔴 High noise and jitter
    - 🔴 Rapid, unpredictable changes
    - 🔴 Difficult to control musically
    - 🔴 May have many redundant dimensions
    """)

with col_exp2:
    st.markdown("""
    **Benefits of feature shaping:**
    - ✅ Smooth, stable control
    - ✅ Reduced dimensionality (easier to learn)
    - ✅ Captures essential variations
    - ✅ Musical expressivity preserved
    """)

st.markdown("""
---

## 🎯 Key Insight

Feature shaping is **NOT decoding mental states**. It's **signal processing** to create 
better control signals for musical performance.

The goal is **controllability and expressivity**, not accuracy or classification.

This aligns with Miranda (2014): *Brain-Computer Music Interfacing*, where:
- Brain signals are control signals (like gesture or breath)
- Meaning emerges through practice and mapping
- Unpredictability can be artistically valuable
""")

# Methods comparison
st.markdown("---")
st.markdown("### 🔬 Available Methods")

method_comparison = {
    "Method": ["Temporal Smoothing", "PCA Reduction", "Autoencoder (PyTorch)"],
    "Latency": ["<5ms", "<10ms", "~10-20ms"],
    "Dimensionality": ["Same as input", "2-8", "2-8"],
    "Training Required": ["No", "Yes (fast)", "Yes (slow)"],
    "Best For": ["Real-time stability", "Decorrelation", "Complex patterns"]
}

import pandas as pd
df = pd.DataFrame(method_comparison)
st.table(df)

st.markdown("""
---

**💡 Try different methods and parameters** to see how they affect signal stability!
""")
