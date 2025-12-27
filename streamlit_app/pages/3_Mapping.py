"""
Page 3: Mapping - Control Design
"""

import streamlit as st
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import plot_mapping_curve

st.set_page_config(page_title="Mapping", page_icon="🔀", layout="wide")

st.title("🔀 Mapping: Control Design")

st.markdown("""
---

## 🎛️ From Signal to Control

This page explores how we **map** raw signal features to control parameters that drive the sound engine.

**Key Concept**: Mapping is a **design choice**, not a fixed transformation. Different mappings create different "playability."

---
""")

# Mapping parameters
st.sidebar.markdown("## ⚙️ Mapping Configuration")

mapping_type = st.sidebar.selectbox(
    "**Mapping Type**",
    options=["Linear", "Smoothed", "Nonlinear (Sigmoid)", "Threshold", "Inverted"],
    index=0,
    help="Choose how input signals map to output controls"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Mapping Parameters")

smoothing = st.sidebar.slider(
    "**Smoothing**",
    min_value=0.0,
    max_value=0.99,
    value=0.5,
    step=0.05,
    help="How much temporal smoothing to apply (higher = more stable, less responsive)"
)

sensitivity = st.sidebar.slider(
    "**Sensitivity**",
    min_value=0.1,
    max_value=2.0,
    value=1.0,
    step=0.1,
    help="Scale factor for input signal (higher = more responsive range)"
)

if mapping_type in ["Threshold", "Nonlinear (Sigmoid)"]:
    threshold = st.sidebar.slider(
        "**Threshold/Midpoint**",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Threshold or sigmoid midpoint"
    )
else:
    threshold = 0.5

latency_sim = st.sidebar.slider(
    "**Simulated Latency (ms)**",
    min_value=0,
    max_value=200,
    value=50,
    step=10,
    help="Simulated system latency for demonstration"
)

# Generate mapping curve
input_range = np.linspace(0, 1, 100)


def apply_mapping(x, mapping_type, sensitivity, smoothing, threshold):
    """Apply selected mapping transformation"""
    # Scale by sensitivity
    x = x * sensitivity
    
    # Apply mapping
    if mapping_type == "Linear":
        y = x
    elif mapping_type == "Smoothed":
        # Simulate temporal smoothing effect (simplified)
        y = x
    elif mapping_type == "Nonlinear (Sigmoid)":
        # Sigmoid centered at threshold
        y = 1.0 / (1.0 + np.exp(-10 * (x - threshold)))
    elif mapping_type == "Threshold":
        # Hard threshold
        y = np.where(x >= threshold, 1.0, 0.0)
    elif mapping_type == "Inverted":
        y = 1.0 - x
    else:
        y = x
    
    # Clip to valid range
    y = np.clip(y, 0, 1)
    
    # Apply smoothing (exponential moving average simulation)
    if smoothing > 0 and mapping_type == "Smoothed":
        y_smooth = np.zeros_like(y)
        y_smooth[0] = y[0]
        for i in range(1, len(y)):
            y_smooth[i] = smoothing * y_smooth[i-1] + (1 - smoothing) * y[i]
        y = y_smooth
    
    return y


output_values = apply_mapping(input_range, mapping_type, sensitivity, smoothing, threshold)

# Display mapping curve
st.markdown("### 📈 Mapping Curve")
st.markdown("""
This shows how input signals (0-1) map to output control parameters (0-1).

- **X-axis**: Input signal value
- **Y-axis**: Output control value
- **Gray dashed line**: Identity mapping (output = input)
- **Red line**: Selected mapping
""")

fig_mapping = plot_mapping_curve(input_range, output_values, 
                                  title=f"{mapping_type} Mapping")
st.plotly_chart(fig_mapping, use_container_width=True)

st.markdown("---")

# Explanation of different mappings
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("## 🎚️ Mapping Types")
    
    st.markdown("""
    ### Linear
    - **Direct 1:1 mapping**
    - Input = Output (scaled by sensitivity)
    - Most responsive, least stable
    - Good for: Precise control, experienced performers
    
    ### Smoothed
    - **Temporal smoothing applied**
    - Reduces jitter and noise
    - Makes control more stable but less responsive
    - Good for: Noisy signals, sustained tones
    
    ### Nonlinear (Sigmoid)
    - **S-curved transformation**
    - Creates "dead zone" near center
    - Compresses extremes, expands middle
    - Good for: Reducing accidental triggers, expressive dynamics
    
    ### Threshold
    - **Binary on/off**
    - Only outputs 0 or 1
    - Good for: Discrete events, triggers
    - Bad for: Continuous control
    
    ### Inverted
    - **Reverses the mapping**
    - High input → Low output
    - Good for: Inverse relationships (e.g., alpha → activity)
    """)

with col2:
    st.markdown("## 🎮 Playability Considerations")
    
    st.markdown("""
    ### Responsiveness vs. Stability
    
    There's a fundamental **tradeoff**:
    
    - **High Responsiveness** ⚡
      - Reacts quickly to signal changes
      - Allows nuanced control
      - BUT: Can be jittery and unstable
    
    - **High Stability** 🎯
      - Smooth, predictable behavior
      - Reduces accidental changes
      - BUT: Can feel sluggish and unresponsive
    
    ### Design Question
    
    > **"What kind of control do you want?"**
    
    Different musical contexts need different mappings:
    
    - **Percussive sounds** → High responsiveness
    - **Sustained pads** → High stability
    - **Melodic lines** → Balanced
    - **Ambient textures** → High stability
    
    ### Latency Impact
    
    System latency affects playability:
    
    - **<50ms**: Feels immediate
    - **50-100ms**: Noticeable but playable
    - **>100ms**: Feels delayed, hard to control
    - **>200ms**: Not usable for real-time
    
    BrainJam targets **<100ms end-to-end**.
    """)

st.markdown("---")

# Interactive demonstration
st.markdown("## 🧪 Interactive Test")

st.markdown("""
Use the slider below to simulate an input signal and see how it maps to output:
""")

test_input = st.slider(
    "**Test Input Signal**",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
    help="Simulate an input signal value"
)

test_output = apply_mapping(np.array([test_input]), mapping_type, 
                            sensitivity, smoothing, threshold)[0]

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.metric("Input Signal", f"{test_input:.3f}")

with col2:
    st.metric("Output Control", f"{test_output:.3f}", 
              delta=f"{test_output - test_input:+.3f}")

with col3:
    latency_color = "🟢" if latency_sim < 50 else "🟡" if latency_sim < 100 else "🔴"
    st.metric("Simulated Latency", f"{latency_sim} ms {latency_color}")

st.markdown("---")

# Comparison table
st.markdown("## 📊 Mapping Comparison")

st.markdown("""
| Mapping Type | Responsiveness | Stability | Use Case | Latency Impact |
|--------------|----------------|-----------|----------|----------------|
| **Linear** | ⭐⭐⭐⭐⭐ | ⭐⭐ | Precise control | Low |
| **Smoothed** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Sustained sounds | Medium (+smoothing delay) |
| **Nonlinear** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Expressive dynamics | Low |
| **Threshold** | ⭐⭐⭐⭐⭐ | ⭐ | Triggers/events | Low |
| **Inverted** | ⭐⭐⭐⭐⭐ | ⭐⭐ | Inverse control | Low |

**Note**: These ratings are approximate and depend on signal characteristics.
""")

st.markdown("---")

# Real-world examples
st.markdown("## 🎼 Real-World Examples")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
    ### Example 1: Drone Synthesizer
    
    **Goal**: Stable, slowly-evolving textures
    
    **Mapping**:
    - High smoothing (0.9)
    - Low sensitivity (0.5)
    - Linear or smoothed
    
    **Result**: Calm, meditative soundscape
    """)

with col2:
    st.markdown("""
    ### Example 2: Percussive Triggers
    
    **Goal**: Responsive event triggering
    
    **Mapping**:
    - No smoothing (0.0)
    - High sensitivity (1.5)
    - Threshold at 0.6
    
    **Result**: Sharp, controlled hits
    """)

with col3:
    st.markdown("""
    ### Example 3: Expressive Melody
    
    **Goal**: Nuanced pitch/timbre control
    
    **Mapping**:
    - Medium smoothing (0.5)
    - Normal sensitivity (1.0)
    - Nonlinear sigmoid
    
    **Result**: Musical, controllable phrases
    """)

st.markdown("---")

# Technical details
with st.expander("🔬 Technical Details: Mapping Models"):
    st.markdown("""
    ### Implementation Options
    
    #### 1. Linear Mapper
    ```python
    output = W @ input + b
    output = sigmoid(output)  # Constrain to 0-1
    ```
    - Simple affine transformation
    - Fast (<1ms)
    - Interpretable
    
    #### 2. MLP Mapper
    ```python
    hidden = tanh(W1 @ input + b1)
    output = sigmoid(W2 @ hidden + b2)
    ```
    - Nonlinear capacity
    - Still fast (<5ms with small network)
    - Trainable on performer data
    
    #### 3. Temporal Smoothing
    ```python
    output[t] = alpha * output[t-1] + (1 - alpha) * raw[t]
    ```
    - Exponential moving average
    - Reduces high-frequency noise
    - Adds ~10-30ms latency depending on alpha
    
    ### Training (Optional)
    
    Mappers can be trained on recorded data:
    - **Input**: Recorded signal features
    - **Target**: Desired control values
    - **Objective**: Smooth, responsive mapping
    
    But **hand-designed mappings work well** for most cases!
    """)

st.markdown("---")

st.markdown("""
## 💡 Design Philosophy

> **"Mapping is an artistic decision, not a technical optimization."**

There is no "correct" mapping. Different choices create different instruments:

- **Stable mapping** → Predictable, learnable instrument
- **Responsive mapping** → Expressive, nuanced instrument
- **Nonlinear mapping** → Unique character and dynamics

The best mapping depends on:
- Musical context
- Performer skill
- Signal characteristics
- Aesthetic goals

**Experimentation is key!**

---

👈 **Next**: Go to **4. Sound Engine** to hear how controls affect sound.
""")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
## 🔀 Mapping Page

Explore different mapping strategies:
- Linear vs nonlinear
- Smoothed vs responsive
- Sensitivity adjustments

Try different configurations and observe the mapping curve!
""")
