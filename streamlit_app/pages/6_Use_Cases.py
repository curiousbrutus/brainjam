"""
Page 6: Use Cases - WP1 Alignment
"""

import streamlit as st

st.set_page_config(page_title="Use Cases", page_icon="🎨", layout="wide")

st.title("🎨 Use Cases: Research & Artistic Applications")

st.markdown("""
---

## 🔬 MishMash WP1 Alignment

This page connects BrainJam to concrete **research questions** and **artistic use cases** 
relevant to **MishMash Work Package 1: AI for Artistic Performances**.

**Key Framing**: BrainJam is a **research platform** for studying human-AI interaction in 
creative performance contexts.

---
""")

# Overview section
st.markdown("## 🎯 Research Context")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    ### MishMash WP1 Goals
    
    **Work Package 1**: AI for Artistic Performances
    
    **Focus Areas**:
    - Human-AI collaboration in creative contexts
    - Real-time interaction and responsiveness
    - Performer agency and creative control
    - Artistic applications of AI technologies
    - Evaluation of interactive systems
    
    **BrainJam's Contribution**:
    - Concrete implementation of AI co-performance
    - Platform for studying embodied control
    - Test bed for interaction measures
    - Bridge between technology and artistic practice
    """)

with col2:
    st.markdown("""
    ### Research Questions
    
    1. **Agency & Control**
       - How do performers experience agency in AI-mediated systems?
       - What factors enhance/reduce sense of control?
    
    2. **Responsiveness & Timing**
       - What latency is acceptable for musical interaction?
       - How does system responsiveness affect performance?
    
    3. **Embodiment & Expression**
       - Can embodied signals provide meaningful musical control?
       - How do alternative control modalities affect expression?
    
    4. **Human-AI Partnership**
       - How do performer and AI mutually influence each other?
       - What makes AI feel like a "partner" vs. "tool"?
    
    5. **Learning & Mastery**
       - How do performers learn to control the system?
       - What role does practice play in performance quality?
    """)

st.markdown("---")

# Use Case 1
st.markdown("## 🎼 Use Case 1: AI as Co-Performer")

st.markdown("""
### Concept

The AI acts as a **responsive musical partner** that listens and reacts to the performer, 
rather than playing autonomously.

### Implementation in BrainJam

**Current**:
- Sound parameters respond directly to performer signals
- Continuous feedback loop allows mutual adaptation
- Performer learns system behavior through practice

**Future Extensions**:
- **Temporal prediction** — AI anticipates next moves
- **Call-and-response** — AI plays during performer pauses
- **Adaptive timing** — AI adjusts rhythm to performer patterns
- **Variation generation** — AI adds creative flourishes while maintaining coherence

### Research Questions

1. **Partnership Quality**
   - When does the AI feel like a partner vs. a tool?
   - What behaviors create sense of collaboration?
   
2. **Mutual Influence**
   - How does performer adapt to AI responses?
   - How should AI adapt to performer patterns?
   
3. **Creative Agency**
   - Does shared control enhance or reduce performer agency?
   - How much AI autonomy is desirable?

### Evaluation Methods

- **Questionnaires**: "The system felt like a musical partner" (1-10)
- **Behavioral**: Timing analysis of performer-AI interactions
- **Qualitative**: Interviews about partnership experience
- **Performance**: Audience perception of collaboration

### Artistic Applications

- **Improvised duets** between human and AI
- **Solo performances** with intelligent accompaniment
- **Ensemble contexts** where AI mediates between performers
- **Compositional tool** for exploring human-AI dialogue
""")

st.markdown("---")

# Use Case 2
st.markdown("## 🤲 Use Case 2: Alternative Embodied Control")

st.markdown("""
### Concept

Brain signals provide an **alternative embodied control channel** that complements 
(not replaces) traditional manual control.

### Why Alternative Embodiment Matters

**Traditional musical interfaces**:
- Hands: Keyboards, strings, buttons
- Breath: Wind instruments, breath controllers
- Body: Dance, motion capture
- Voice: Singing, vocal synthesis

**Brain signals offer**:
- **Hands-free control** — Useful for disabled musicians or when hands are occupied
- **Internal state** — Different from external gesture
- **Parallel channel** — Can be used alongside traditional controls
- **Novel aesthetic** — Different expressive qualities

### Implementation in BrainJam

**Integration Options**:
- **Pure brain control** — All parameters from brain signals
- **Hybrid control** — Keyboard/MIDI for some parameters, brain for others
- **Modulation** — Brain signals modulate manually-played sounds
- **Meta-control** — Brain signals control effect parameters

### Research Questions

1. **Embodiment**
   - How do performers experience brain-based control differently?
   - What control strategies emerge?
   
2. **Complementarity**
   - How do brain and manual controls interact?
   - Which parameters work best for each modality?
   
3. **Accessibility**
   - Can this expand musical participation?
   - How to design for neurodivergent performers?

### Evaluation Methods

- **Comparative studies**: Brain vs. keyboard vs. hybrid control
- **Expertise effects**: How control improves with practice
- **Accessibility**: Studies with disabled musicians
- **Phenomenology**: Lived experience of alternative control

### Artistic Applications

- **Expanded instrumental technique** — Add brain control to traditional playing
- **Disability access** — Performance opportunities for motor-impaired musicians
- **New performance genres** — Brain-based live coding, meditation music
- **Therapeutic contexts** — Music-making for rehabilitation
""")

st.markdown("---")

# Use Case 3
st.markdown("## 🎲 Use Case 3: Improvisation & Uncertainty")

st.markdown("""
### Concept

Signal **variability and unpredictability** become **artistic features**, not bugs. 
The system embraces uncertainty as part of the improvisational process.

### Uncertainty in Performance

**Traditional instruments have inherent uncertainty**:
- Guitar strings buzz and rattle
- Breath control varies moment-to-moment
- Fingers slip on keys
- Vocal pitch wavers

**BrainJam's uncertainty**:
- Brain signals are inherently noisy
- Control is never perfectly stable
- System responses vary subtly
- Feedback creates emergent behavior

### Aesthetic Framing

> **"Negotiation between performer and system"**

- Performer proposes actions (via signals)
- System interprets and responds (via sound)
- Neither has full control
- Creative space emerges in the negotiation

### Implementation in BrainJam

**Embracing Unpredictability**:
- Minimal smoothing for responsive but jittery control
- Stochastic elements in synthesis
- AI variation generation
- Glitches as expressive features

**Balancing Control**:
- Adjustable stability/responsiveness
- Performer can choose control style
- Different mappings for different uncertainty levels

### Research Questions

1. **Aesthetic Preference**
   - Do performers/audiences value unpredictability?
   - When is variability expressive vs. frustrating?
   
2. **Flow & Challenge**
   - Does uncertainty enhance engagement?
   - How much unpredictability is optimal?
   
3. **Creative Process**
   - How does uncertainty affect improvisation?
   - Do performers develop uncertainty strategies?

### Evaluation Methods

- **Preference studies**: Stable vs. variable systems
- **Flow measures**: Engagement during uncertain control
- **Creativity assessment**: Novelty and variety in performances
- **Discourse analysis**: How performers talk about uncertainty

### Artistic Applications

- **Improvised music** — Uncertainty as creative partner
- **Algorithmic composition** — Human-AI co-creation
- **Live coding** — Code + brain signals + stochasticity
- **Experimental genres** — Noise, glitch, ambient
""")

st.markdown("---")

# Use Case 4
st.markdown("## 🎓 Use Case 4: Rehearsal & Exploration")

st.markdown("""
### Concept

BrainJam is **learnable and rehearseable** — performers can practice, develop strategies, 
and improve control over time.

### Learning as Performance Practice

**Like any instrument**:
- Requires practice to master
- Control improves with time
- Performers develop personal techniques
- Rehearsal enables complex performances

**BrainJam learning stages**:
1. **Discovery** — Exploring parameter ranges
2. **Control** — Developing basic strategies
3. **Fluency** — Smooth, confident control
4. **Mastery** — Expressive, nuanced performance

### Implementation in BrainJam

**Practice Features**:
- **Visual feedback** — See control parameters in real-time
- **Parameter history** — Review past performances
- **Recording** — Save and analyze sessions
- **Difficulty levels** — Adjustable responsiveness/stability
- **Goals** — Specific control targets to achieve

**Rehearsal Tools**:
- **Looping** — Practice specific passages
- **Isolated parameters** — Work on one control at a time
- **Metronome/backing** — Practice with timing reference
- **Performance mode** — Full system, minimal UI

### Research Questions

1. **Learning Curves**
   - How quickly do performers gain control?
   - What factors predict learning success?
   
2. **Practice Strategies**
   - What techniques do performers develop?
   - How do experts differ from novices?
   
3. **Transfer**
   - Do skills transfer between mapping types?
   - Can training accelerate learning?
   
4. **Retention**
   - How long do control skills persist?
   - What maintains vs. degrades with breaks?

### Evaluation Methods

- **Longitudinal studies**: Track learning over weeks/months
- **Skill assessment**: Objective control metrics (accuracy, stability)
- **Practice logs**: What performers work on
- **Comparative**: Instrument learning parallels

### Artistic Applications

- **Education** — Teaching human-AI interaction
- **Workshops** — Introducing brain-based performance
- **Artist residencies** — Developing new works
- **Documentation** — Sharing learning journeys
""")

st.markdown("---")

# Interaction measures
st.markdown("## 📊 Interaction Measures & Evaluation")

st.markdown("""
### Psychology-Informed Evaluation

BrainJam uses **interaction measures** to evaluate the system without clinical framing:

#### Primary Measures

**1. Agency & Control**
- "I felt in control of the sounds" (1-10)
- "The system responded to my intentions" (1-10)
- Behavioral: Control precision, parameter coverage

**2. Responsiveness**
- Measured latency (ms)
- Perceived predictability (1-10)
- Behavioral: Reaction time analysis

**3. Flow & Engagement**
- "I was fully engaged" (1-10)
- "Time passed quickly" (1-10)
- Behavioral: Performance duration, breaks

**4. Expressiveness**
- "I could express my musical ideas" (1-10)
- "The system offered rich control" (1-10)
- Behavioral: Parameter variation, dynamic range

#### NOT Clinical Assessment

- ✗ No mental state decoding
- ✗ No diagnostic measures
- ✗ No therapeutic goals
- ✗ No cognitive testing

**Focus**: Performer experience and system usability, not brain function.
""")

st.markdown("---")

# Simple self-report demo
st.markdown("## 🧪 Example: Simple Self-Report")

st.markdown("""
After using BrainJam, performers would complete brief questionnaires like this:
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### **Sense of Agency**")
    
    control = st.slider(
        "I felt in control of the sounds",
        min_value=1, max_value=10, value=5, key="uc_control"
    )
    
    intentions = st.slider(
        "The system responded to my intentions",
        min_value=1, max_value=10, value=5, key="uc_intentions"
    )
    
    st.markdown("### **Responsiveness**")
    
    predictable = st.slider(
        "The system was predictable",
        min_value=1, max_value=10, value=5, key="uc_predictable"
    )
    
    responsive = st.slider(
        "The system felt responsive",
        min_value=1, max_value=10, value=5, key="uc_responsive"
    )

with col2:
    st.markdown("### **Flow & Engagement**")
    
    engaged = st.slider(
        "I was fully engaged with the system",
        min_value=1, max_value=10, value=5, key="uc_engaged"
    )
    
    time_flew = st.slider(
        "Time passed quickly",
        min_value=1, max_value=10, value=5, key="uc_time"
    )
    
    st.markdown("### **Expressiveness**")
    
    expressive = st.slider(
        "I could express my musical ideas",
        min_value=1, max_value=10, value=5, key="uc_expressive"
    )
    
    rich = st.slider(
        "The system offered rich control",
        min_value=1, max_value=10, value=5, key="uc_rich"
    )

if st.button("📊 View Summary", key="uc_summary"):
    avg_agency = (control + intentions) / 2
    avg_responsive = (predictable + responsive) / 2
    avg_flow = (engaged + time_flew) / 2
    avg_expressive = (expressive + rich) / 2
    
    st.success(f"""
    **Summary Scores** (out of 10):
    - Agency: {avg_agency:.1f}
    - Responsiveness: {avg_responsive:.1f}
    - Flow: {avg_flow:.1f}
    - Expressiveness: {avg_expressive:.1f}
    
    (These would be analyzed across multiple performers in a real study)
    """)

st.markdown("---")

# Future directions
st.markdown("## 🚀 Future Research Directions")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
    ### Technical
    
    - **Real EEG/fNIRS integration**
    - **Advanced AI models** (DDSP, diffusion)
    - **Multi-performer systems**
    - **Network performance** (distributed)
    - **Mobile platforms**
    - **VR/AR integration**
    """)

with col2:
    st.markdown("""
    ### Artistic
    
    - **Composer residencies**
    - **Public performances**
    - **Gallery installations**
    - **Documentary films**
    - **Educational workshops**
    - **Disability access programs**
    """)

with col3:
    st.markdown("""
    ### Research
    
    - **User studies** (n=20-50)
    - **Longitudinal learning studies**
    - **Comparative control studies**
    - **Audience perception research**
    - **Practice-based research**
    - **Ethnographic studies**
    """)

st.markdown("---")

# Conclusion
st.markdown("## 💡 Synthesis: WP1 Contribution")

st.markdown("""
### How BrainJam Advances WP1 Goals

**1. Concrete Implementation**
- Working system, not just concept
- Demonstrates feasibility of brain-AI performance
- Platform for testing research questions

**2. Performance-Centered Framing**
- Explicitly NOT neuroscience
- Focuses on artistic interaction
- Maintains performer agency

**3. Methodological Contribution**
- Interaction measures for creative systems
- Bridges HCI, music, and AI research
- Respects artistic practice

**4. Critical Perspective**
- Acknowledges limitations
- Avoids hype and overstatement
- Considers ethical implications

**5. Practical Value**
- Usable by real performers
- Extendable by other researchers
- Educates about human-AI interaction

### Research Impact

BrainJam contributes to:
- **Human-AI Interaction** — Novel interaction paradigm
- **Music Technology** — Alternative control modalities
- **Creative AI** — Co-performance vs. generation
- **Disability Studies** — Accessible music-making
- **Performance Studies** — Embodiment and agency

### Artistic Impact

BrainJam enables:
- **New performance genres** — Brain-based improvisation
- **Expanded access** — Music-making for all
- **Aesthetic exploration** — Uncertainty and co-creation
- **Critical practice** — Questioning AI in art

---

## 🎭 Final Thoughts

> **BrainJam is a performance instrument, a research platform, and a critical intervention.**

It demonstrates that:
- Brain signals can drive musical performance
- AI can be a partner, not just a tool
- Human agency can be preserved in AI systems
- Creative practice informs technical research

**This is MishMash WP1** — AI for Artistic Performances.

---

## 📚 Related Work & Resources

### Key References

**Human-AI Co-Creation**
- Louie, R., et al. (2020). "Novice-AI Music Co-Creation via AI-Steering Tools"
- Franceschelli, G., et al. (2022). "Creativity and AI"

**BCI Music**
- Miranda, E. R. (2014). "Brain-Computer Music Interfacing"
- Grierson, M. (2008). "Composing with brainwaves"

**Performance Studies**
- Leman, M. (2008). "Embodied Music Cognition"
- Godøy, R. I. (2010). "Gestural-Sonorous Objects"

### External Links

- **MishMash Project**: [https://mishmash.no](https://mishmash.no)
- **WP1 Details**: [https://mishmash.no/wp1/](https://mishmash.no/wp1/)
- **GitHub Repository**: [https://github.com/curiousbrutus/brainjam](https://github.com/curiousbrutus/brainjam)

---

## ✅ Conclusion

You've completed the BrainJam GUI tour!

You should now understand:
- ✅ What BrainJam is (and isn't)
- ✅ How signals transform into sound
- ✅ How mapping affects playability
- ✅ How the complete system works
- ✅ Why this matters for research and art

**Thank you for exploring BrainJam!**

For questions, collaborations, or performance inquiries:  
📧 eyyub.gvn@gmail.com
""")

# Sidebar
st.sidebar.markdown("""
## 🎨 Use Cases Page

Connects BrainJam to:
- MishMash WP1 goals
- Research questions
- Artistic applications
- Evaluation methods

This shows **why** the system matters, not just **how** it works.
""")
