"""
BrainJam Streamlit GUI
Main entry point for the Streamlit application
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="BrainJam Performance System",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page content
st.title("🎛️🎶 BrainJam Performance System")

st.markdown("""
---

## Welcome to BrainJam

**BrainJam is a playable, rehearseable, performable musical instrument** where:

- **Brain signals** (EEG/fNIRS) serve as **expressive control signals**
- **AI systems** act as **responsive musical partners**, not autonomous generators
- **Performers** maintain **agency, timing, and creative control**

### 🎯 Purpose of this Interface

This GUI allows you to:

✅ **See** how brain-like signals become expressive control  
✅ **Hear** how AI sound responds in real time  
✅ **Understand** the system architecture visually  
✅ **Experiment** with different mappings and behaviors  
✅ **Explore** concrete artistic use-cases

---

## 🧭 Navigation

Use the sidebar to navigate between pages:

### 📖 **1. Overview**
Conceptual orientation — understand what BrainJam is and isn't

### 📊 **2. Signals**
EEG/fNIRS simulation — see how abstract signals vary over time

### 🔀 **3. Mapping**
Control design — explore different ways signals become parameters

### 🔊 **4. Sound Engine**
AI/generative audio — hear the effect of control parameters

### 🎭 **5. Live Performance**
MVP demo — perform with the system in real time

### 🎨 **6. Use Cases**
WP1 alignment — artistic and research applications

---

## 🚫 What BrainJam Is NOT

- ❌ **NOT brain decoding** — We do not decode thoughts or intentions
- ❌ **NOT mind reading** — Brain signals are noisy, continuous control parameters
- ❌ **NOT focused on accuracy** — Optimization is for musical expression, not classification
- ❌ **NOT clinical or therapeutic** — This is a performance instrument, not a medical device

---

## 🎼 Key Concept

**Brain signals are treated as continuous expressive control signals**, similar to:
- Gesture sensors
- Breath controllers
- Pressure-sensitive pads
- Any other embodied control mechanism

The system is an **instrument + AI co-performer**, not a decoder.

---

## 🚀 Getting Started

👈 **Select a page from the sidebar** to begin exploring the system.

We recommend starting with **1. Overview** for a conceptual foundation, then moving through the pages in order.

---

*Part of MishMash WP1: AI for Artistic Performances*
""")

# Sidebar info
st.sidebar.title("🎛️ BrainJam")
st.sidebar.markdown("""
### Navigation
Use the pages above to explore different aspects of the system.

### Quick Links
- [GitHub Repository](https://github.com/curiousbrutus/brainjam)
- [MishMash WP1](https://mishmash.no/wp1/)

---

**Researcher**: Eyyub Guven  
**Email**: eyyub.gvn@gmail.com
""")
