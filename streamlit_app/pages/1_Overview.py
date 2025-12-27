"""
Page 1: Overview - Conceptual Orientation
"""

import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import create_system_diagram

st.set_page_config(page_title="Overview", page_icon="📖", layout="wide")

st.title("📖 Overview: What is BrainJam?")

st.markdown("""
---

## 🎼 Core Concept

**BrainJam is a performance instrument and AI co-performer.**

It treats brain signals (or any continuous control signals) as **expressive input**, 
similar to how a musician uses gesture, breath, or touch to control their instrument.

---
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ### ✅ What BrainJam IS
    
    - **A musical instrument** that can be played, practiced, and performed
    - **An expressive control system** using continuous signals
    - **An AI co-performer** that responds to the human performer
    - **A research platform** for human-AI musical interaction
    - **Performance-focused** with real-time constraints (<100ms latency)
    
    ### 🎯 Design Goals
    
    1. **Responsiveness** — System reacts in real-time
    2. **Controllability** — Performer has agency over sound
    3. **Expressiveness** — Rich, nuanced control possible
    4. **Playability** — Learnable, rehearseable, performable
    5. **Partnership** — AI as collaborator, not automation
    """)

with col2:
    st.markdown("""
    ### ❌ What BrainJam is NOT
    
    - ❌ **NOT brain decoding** — We don't read thoughts or intentions
    - ❌ **NOT mind reading** — Signals are noisy, continuous parameters
    - ❌ **NOT focused on accuracy** — We optimize for expression, not classification
    - ❌ **NOT clinical/therapeutic** — This is art/performance, not medicine
    - ❌ **NOT neuroscience research** — We study interaction, not brains
    
    ### 🔑 Key Insight
    
    > **"Brain signals are treated as control signals, not semantic content."**
    
    Just as a breath controller doesn't "decode breathing," BrainJam doesn't 
    decode mental states. It uses signal variations for expressive control.
    
    **This could be EEG, but it could also be gesture — the system doesn't care.**
    """)

st.markdown("---")

# System diagram
st.subheader("🏗️ System Architecture")

st.markdown("""
The BrainJam pipeline transforms signals into sound through multiple stages, 
with each stage designed for **real-time performance**:
""")

# Display diagram
fig = create_system_diagram()
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### Pipeline Stages

1. **Signal Input** (10-40ms)
   - EEG/fNIRS sensors (optional)
   - Mock signal generators (for testing)
   - Keyboard/MIDI (for comparison)
   
2. **Feature Extraction** (10-30ms)
   - Band power computation
   - Temporal smoothing
   - Normalization to 0-1 range
   
3. **Mapping Model** (<5ms)
   - Linear mapping (simple)
   - MLP mapping (nonlinear)
   - Smoothing filters
   
4. **Sound Engine** (20-50ms)
   - Parametric synthesis
   - Real-time audio generation
   - Expressive control parameters
   
5. **Audio Output**
   - To performer (for feedback)
   - To audience (for listening)
   
6. **Feedback Loop**
   - Performer hears and adjusts
   - System responds to changes
   - **This is what makes it an instrument**

---

## 🎭 Performance Framing

### This is an Instrument

Like learning any instrument, BrainJam requires:
- **Practice** — Learning how signals map to sound
- **Rehearsal** — Developing control strategies
- **Performance** — Real-time expressive playing

### AI as Co-Performer

The AI component:
- **Responds** to performer signals
- **Adapts** timing and texture
- **Negotiates** with the performer
- **Does NOT** play autonomously

### Signals ≠ Meaning

Brain signals are:
- **Continuous** — Always varying
- **Noisy** — Inherently unstable
- **Non-semantic** — Not representing thoughts
- **Expressive** — Rich in variation

---

## 🔬 Research Context

### MishMash WP1: AI for Artistic Performances

BrainJam is developed as part of the MishMash research project, specifically:

**Work Package 1**: AI for Artistic Performances

**Research Questions**:
- How do performers experience agency in AI-mediated systems?
- What latency is acceptable for musical interaction?
- How do performer and AI mutually influence each other?
- Can embodied signals provide meaningful musical control?

**Methodology**:
- Practice-based research
- User studies with musicians
- Interaction measures (agency, flow, timing)
- Live demonstrations

---

## 🧭 How to Use This Interface

### Recommended Path

1. **Start here** (Overview) — Understand the concept
2. **Signals** — See how mock signals vary
3. **Mapping** — Explore signal-to-control transformations
4. **Sound Engine** — Hear the effect of control
5. **Live Performance** — Try the complete system
6. **Use Cases** — Connect to research applications

### Interactive Elements

Each page contains:
- **Sliders** — Adjust parameters in real-time
- **Plots** — Visualize signals and mappings
- **Audio players** — Hear synthesis results
- **Explanatory text** — Understand design choices

---

## 💡 Remember

> **BrainJam is about exploration, experimentation, and expression.**  
> **It's a musical instrument that happens to use brain-like signals.**  
> **The goal is performance, not accuracy.**

---

👈 **Use the sidebar to navigate to the next page: Signals**
""")

# Sidebar
st.sidebar.markdown("""
## 📖 Overview

This page introduces:
- What BrainJam is (and isn't)
- System architecture
- Performance framing
- Research context

---

**Next**: Go to **2. Signals** to see how mock signals are generated.
""")
