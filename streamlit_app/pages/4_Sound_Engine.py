"""
Page 4: Sound Engine - AI/Generative Audio
"""

import streamlit as st
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add performance_system to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils import plot_sound_parameters, create_audio_player_html
from performance_system.sound_engines import ParametricSynth

st.set_page_config(page_title="Sound Engine", page_icon="🔊", layout="wide")

st.title("🔊 Sound Engine: AI/Generative Audio")

st.markdown("""
---

## 🎵 From Control to Sound

This page demonstrates how control parameters drive the sound synthesis engine.

**Key Concept**: Sound parameters are **continuously controllable** — small changes in control create smooth variations in sound.

---
""")

# Initialize synthesizer
if 'synth' not in st.session_state:
    st.session_state.synth = ParametricSynth(sample_rate=44100, base_freq=220.0)

# Control parameters
st.sidebar.markdown("## 🎛️ Control Parameters")
st.sidebar.markdown("These would come from the mapping stage in a live performance:")

control_1 = st.sidebar.slider(
    "**Control 1** → Tempo/Density",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05,
    help="Event rate: 0=sparse, 1=dense"
)

control_2 = st.sidebar.slider(
    "**Control 2** → Harmonic Tension",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.05,
    help="Dissonance: 0=consonant, 1=dissonant"
)

control_3 = st.sidebar.slider(
    "**Control 3** → Spectral Brightness",
    min_value=0.0,
    max_value=1.0,
    value=0.6,
    step=0.05,
    help="Timbre: 0=dark, 1=bright"
)

control_4 = st.sidebar.slider(
    "**Control 4** → Noise Balance",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.05,
    help="Texture: 0=pure tones, 1=noisy"
)

duration = st.sidebar.slider(
    "**Duration** (seconds)",
    min_value=0.5,
    max_value=5.0,
    value=2.0,
    step=0.5,
    help="How long to generate audio"
)

if st.sidebar.button("🔄 Reset Synthesizer", use_container_width=True):
    st.session_state.synth.reset()
    st.rerun()

# Create control dict
controls = {
    'control_1': control_1,
    'control_2': control_2,
    'control_3': control_3,
    'control_4': control_4,
}

# Display sound parameters
st.markdown("### 🎚️ Sound Parameters")

sound_params = {
    'tempo_density': control_1,
    'harmonic_tension': control_2,
    'spectral_brightness': control_3,
    'noise_balance': control_4,
}

col1, col2 = st.columns([1, 1])

with col1:
    fig_params = plot_sound_parameters(sound_params)
    st.plotly_chart(fig_params, use_container_width=True)

with col2:
    st.markdown("""
    #### Parameter Meanings
    
    **Tempo/Density** (Control 1)
    - Controls event rate and rhythmic activity
    - Low: Sparse, slow events
    - High: Dense, rapid events
    
    **Harmonic Tension** (Control 2)
    - Controls consonance/dissonance
    - Low: Simple, consonant harmonics
    - High: Complex, dissonant partials
    
    **Spectral Brightness** (Control 3)
    - Controls timbral quality
    - Low: Dark, mellow tone
    - High: Bright, sharp tone
    
    **Noise Balance** (Control 4)
    - Controls texture character
    - Low: Pure, tonal
    - High: Noisy, textural
    """)

st.markdown("---")

# Generate audio button
st.markdown("### 🎧 Generate Audio")

st.markdown("""
Click the button below to generate audio with the current control parameters.
Listen to how different settings affect the sound.
""")

if st.button("🎵 Generate Sound", type="primary", use_container_width=False):
    with st.spinner("Generating audio..."):
        # Generate audio
        audio = st.session_state.synth.generate(duration, controls)
        
        # Create audio player
        audio_html = create_audio_player_html(audio, sample_rate=44100)
        
        st.success("✅ Audio generated!")
        st.markdown(audio_html, unsafe_allow_html=True)
        
        # Display waveform
        import plotly.graph_objects as go
        
        # Downsample for visualization
        downsample_factor = 100
        audio_display = audio[::downsample_factor]
        time_display = np.arange(len(audio_display)) * downsample_factor / 44100
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_display,
            y=audio_display,
            mode='lines',
            name='Audio',
            line=dict(color='#1f77b4', width=1)
        ))
        fig.update_layout(
            title="Generated Audio Waveform",
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            height=250,
            margin=dict(l=50, r=20, t=50, b=50),
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Explanation of synthesis
st.markdown("## 🔬 How It Works")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ### Parametric Synthesis
    
    The sound engine uses **additive synthesis** with controllable parameters:
    
    1. **Oscillator Generation**
       - Multiple harmonic partials (1, 2, 3, 4, 5, 7, 9)
       - Amplitudes controlled by harmonic_tension
       - Slight detuning for dissonance
    
    2. **Spectral Filtering**
       - Simple moving average for brightness control
       - Low brightness → more filtering (darker)
       - High brightness → less filtering (brighter)
    
    3. **Noise Mixing**
       - White noise blended with tones
       - Balance controlled by noise_balance parameter
    
    4. **Temporal Envelope**
       - Pulsing amplitude based on tempo_density
       - Creates rhythmic structure
       - Varies from slow (0.5 Hz) to fast (5 Hz)
    
    5. **Smoothing & Normalization**
       - Parameter smoothing prevents clicks
       - Fade in/out on chunks
       - Normalization for consistent level
    """)

with col2:
    st.markdown("""
    ### Real-Time Considerations
    
    **Latency Budget**: ~20-50ms for synthesis
    
    **Optimizations**:
    - Simple algorithms (no FFT)
    - Pre-computed parameters
    - Efficient numpy operations
    - Small buffer sizes (0.1s chunks)
    
    **Trade-offs**:
    - ✅ Low latency
    - ✅ Controllable parameters
    - ✅ Expressive range
    - ⚠️ Limited timbral complexity
    - ⚠️ Fixed harmonic structure
    
    ### Alternative Engines
    
    **DDSP-style** (planned):
    - Neural audio synthesis
    - Learned timbres
    - Still differentiable
    
    **Diffusion models** (research):
    - High-quality audio
    - But too slow for real-time
    - Useful for offline generation
    """)

st.markdown("---")

# Interactive exploration
st.markdown("## 🎮 Exploration Exercises")

st.markdown("""
Try these parameter combinations and listen to the results:

### 1. Minimal Drone
- Tempo/Density: **0.2** (sparse)
- Harmonic Tension: **0.1** (consonant)
- Spectral Brightness: **0.3** (dark)
- Noise Balance: **0.1** (tonal)

**Result**: Calm, meditative drone with slow pulse

---

### 2. Busy Texture
- Tempo/Density: **0.9** (dense)
- Harmonic Tension: **0.7** (dissonant)
- Spectral Brightness: **0.8** (bright)
- Noise Balance: **0.6** (noisy)

**Result**: Active, complex texture with rapid events

---

### 3. Dynamic Melody
- Tempo/Density: **0.5** (medium)
- Harmonic Tension: **0.3** (slightly dissonant)
- Spectral Brightness: **0.7** (bright)
- Noise Balance: **0.2** (mostly tonal)

**Result**: Melodic, musical character with moderate activity

---

### 4. Ambient Pad
- Tempo/Density: **0.3** (slow)
- Harmonic Tension: **0.5** (medium)
- Spectral Brightness: **0.4** (mellow)
- Noise Balance: **0.4** (balanced)

**Result**: Atmospheric pad sound, slowly evolving

""")

st.markdown("---")

# Performance context
st.markdown("## 🎭 In Performance Context")

st.markdown("""
### How Control Affects Performance

In a live performance with BrainJam:

1. **Continuous Variation**
   - Control parameters change smoothly over time
   - Sound evolves organically
   - No discrete "states" — always transitioning

2. **Performer Feedback**
   - Performer hears the sound they're creating
   - Adjusts their control strategy (conscious or unconscious)
   - Creates a **feedback loop** between performer and system

3. **Learning the Instrument**
   - Over time, performers learn what control ranges work
   - Develop strategies for specific sounds
   - Build muscle memory (or "brain memory"!)

4. **AI Co-Performance** (future)
   - AI could modulate these parameters independently
   - Create call-and-response patterns
   - Add variation and surprise
   - While still responding to performer input

### Real-Time Feel

**Key requirement**: System must feel **responsive**

- Latency < 100ms for tight feedback
- Smooth parameter changes (no jumps)
- Predictable but not deterministic
- Room for exploration and surprise

This is what makes it a **playable instrument** rather than just "sound generation."
""")

st.markdown("---")

with st.expander("🔧 Technical Implementation Details"):
    st.markdown("""
    ### ParametricSynth Class
    
    ```python
    class ParametricSynth:
        def __init__(self, sample_rate=44100, base_freq=220.0):
            self.sample_rate = sample_rate
            self.base_freq = base_freq
            self.phase = 0.0
            self.smoothed_params = {}
            
        def generate(self, duration, control_params):
            # Map controls to synth parameters
            tempo_density = control_params['control_1']
            harmonic_tension = control_params['control_2']
            spectral_brightness = control_params['control_3']
            noise_balance = control_params['control_4']
            
            # Generate oscillators
            audio = self._generate_oscillators(t, harmonic_tension)
            
            # Apply filtering
            audio = self._apply_brightness_filter(audio, spectral_brightness)
            
            # Mix in noise
            audio = (1 - noise_balance) * audio + noise_balance * noise
            
            # Apply envelope
            audio *= self._generate_density_envelope(t, tempo_density)
            
            return audio
    ```
    
    ### Key Features
    
    - **Stateful**: Maintains phase for continuity between chunks
    - **Smoothed**: Parameters smoothed to avoid clicks
    - **Normalized**: Output always in valid range
    - **Efficient**: Pure NumPy operations, no external DSP libs
    
    ### Latency Analysis
    
    - Buffer size: 0.1s (4410 samples @ 44.1kHz)
    - Computation time: ~2-5ms per buffer
    - Total synthesis latency: ~20-50ms
    - Acceptable for real-time performance!
    """)

st.markdown("---")

st.markdown("""
## 💡 Key Takeaways

- **Control parameters drive sound generation** in real-time
- **Small changes create smooth variations** — good for continuous control
- **Different combinations create different characters** — wide expressive range
- **Real-time constraints matter** — must be fast enough for performance
- **This is just one possible sound engine** — many alternatives exist

The sound engine is **designed to be controllable**, not to sound "perfect."  
The goal is **expressive range**, not realism.

---

👈 **Next**: Go to **5. Live Performance** to see the complete system in action.
""")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
## 🔊 Sound Engine Page

Explore how control parameters affect sound:
- Adjust sliders above
- Generate audio samples
- Listen to variations

**Tip**: Try extreme settings to understand parameter ranges!
""")
