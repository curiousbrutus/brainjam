# Agent Design Philosophy

## Overview

This document describes the design philosophy for AI co-performers in the BrainJam system. These agents are designed to enhance musical performance through adaptive response to performer input, not to replace the performer or generate music autonomously.

## Core Principles

### 1. Performer-Led Systems

The fundamental principle is that **AI never generates autonomously**. Every output from an AI agent is a modulated reflection of performer input. This approach is grounded in the work of:

- **Tanaka, A. (2006)** - "Interaction, experience and the future of music" emphasizes that interactive music systems must preserve performer agency and intentionality. The performer should always feel in control of the musical outcome.

### 2. Hybrid Symbolic and Machine Learning Approach

The hybrid adaptive agent combines:

- **Symbolic Logic (Rules)**: For reliability and real-time responsiveness
  - Deterministic behavioral states based on observable patterns
  - Predictable responses that performers can learn and anticipate
  - Guaranteed safe operation even without ML components

- **Optional Machine Learning**: For rehearsal-based personalization
  - Learns subtle preferences from past performance sessions
  - Provides small adjustments (±10%) to rule-based outputs
  - Never overrides agency - all outputs are clamped to safe ranges
  - Graceful fallback to rules-only mode if unavailable

This approach is informed by:

- **Fiebrink, R. (2011)** - "Real-time human-computer interaction with machine learning" demonstrates that interactive ML systems work best when they augment, rather than replace, human control. The Wekinator system showed that performers can effectively co-adapt with ML systems when the learning is transparent and controllable.

## Hybrid Adaptive Agent

### Architecture

#### Short-Term Memory (Online Learning)

The agent maintains a **circular buffer** of recent performer control vectors:

- **Buffer Duration**: 10 seconds of history
- **Sampling Rate**: 10 Hz (100ms per sample)
- **Tracked Dimensions**:
  - Intensity (arousal/energy level)
  - Density (note density/activity)
  - Tension (harmonic complexity)
  - Variation (diversity/change rate)

**Exponential Moving Averages (EMA)** are computed in real-time for intensity and density to smooth out noise while remaining responsive to genuine changes in performer state.

#### Behavioral States

The agent operates in three distinct behavioral states, determined by EMA of intensity:

1. **Calm State** (`intensity < 0.3`):
   - Low response density (0.1–0.3)
   - Low harmonic tension
   - Slower tempo suggestions (60–80 BPM)
   - Creates space and breathing room in the performance

2. **Active State** (`intensity > 0.7`):
   - High response density (0.7–0.9)
   - Moderate to high harmonic tension
   - Faster tempo suggestions (100–140 BPM)
   - Energetic, driving musical responses

3. **Responsive State** (middle range):
   - Mirrors performer's recent density ±20%
   - Adapts harmonic tension to match performer
   - Moderate tempo suggestions (80–110 BPM)
   - Most adaptive and flexible mode

#### Long-Term Personalization (Offline Learning)

If a trained model exists at `models/adaptive_mapper.pth`, the agent loads a lightweight MLP:

- **Architecture**: 4 inputs → 8 hidden units (ReLU) → 4 outputs (Tanh)
- **Purpose**: Learn performer-specific preferences from rehearsal data
- **Constraint**: Outputs are small deltas (±10% adjustment range)
- **Safety**: Never overrides symbolic logic - only fine-tunes within safe bounds

The ML component is trained offline on recorded rehearsal sessions, allowing it to learn:
- Preferred response densities at different intensity levels
- Harmonic tension preferences
- Timing and fill patterns the performer finds most musically satisfying

### Output Interface

The agent's `respond(controls: dict) -> dict` method returns:

```python
{
    "note_density": float,          # 0.0–1.0 (how many notes to generate)
    "harmonic_tension": float,      # 0.0–1.0 (dissonance/complexity level)
    "tempo_suggestion": int,        # 60–140 BPM (suggested tempo)
    "fill_probability": float       # 0.0–1.0 (likelihood of rhythmic fills)
}
```

These parameters influence but do not dictate the sound generation. The final musical output is still primarily controlled by the performer's input signals.

## Integration and Safety

### Graceful Degradation

The system is designed to work reliably even when components fail:

1. **Missing PyTorch**: Falls back to symbolic rules only
2. **Missing ML Model**: Uses rule-based responses with a warning
3. **Invalid Control Input**: Uses sensible defaults (0.5 for all controls)
4. **ML Inference Error**: Silent fallback to rule-based output

### Agency Preservation

Multiple mechanisms ensure the performer never loses control:

- **Output Clamping**: All values constrained to valid ranges
- **Delta Limits**: ML adjustments limited to ±10%
- **State Transparency**: Behavioral state is observable and predictable
- **Continuous Response**: Agent responds every frame, providing consistent behavior
- **No Autonomous Generation**: Agent only modulates performer input, never creates independently

## Usage Examples

### Basic Usage (Rules Only)

```python
from performance_system.agents import HybridAdaptiveAgent

# Initialize agent
agent = HybridAdaptiveAgent()

# In performance loop
controls = {'control_1': 0.7, 'control_2': 0.5, 'control_3': 0.4, 'control_4': 0.6}
response = agent.respond(controls)

# Use response to modulate sound generation
note_density = response['note_density']
harmonic_tension = response['harmonic_tension']
tempo = response['tempo_suggestion']
```

### With ML Personalization

```python
# Agent automatically loads model if it exists
agent = HybridAdaptiveAgent(model_path="models/adaptive_mapper.pth")

# Same interface - ML personalization is transparent
response = agent.respond(controls)
```

### Inspecting Agent State

```python
state = agent.get_state()
print(f"State: {state['behavioral_state']}")
print(f"EMA Intensity: {state['ema_intensity']:.2f}")
print(f"ML Available: {state['ml_available']}")
```

## Future Directions

### Training the ML Component

To train the personalization model:

1. Record rehearsal sessions (performer controls + manual ratings)
2. Train small MLP to predict preferred adjustments
3. Save to `models/adaptive_mapper.pth`
4. Agent will automatically load and use it

### Extended Behavioral States

Future versions could include:

- **Exploratory State**: Introduces novel patterns to inspire performer
- **Supportive State**: Fills in complementary patterns to performer's playing
- **Challenge State**: Responds in contrasting ways to create tension/interest

### Multi-Modal Sensing

The agent architecture supports multiple input modalities:
- EEG band powers
- fNIRS cognitive load
- EMG muscle tension
- MIDI controller data
- Motion/gesture tracking

## References

1. **Fiebrink, R. (2011)**. "Real-time human-computer interaction with machine learning." *Proceedings of the International Computer Music Conference (ICMC)*.
   - Demonstrates effective patterns for interactive ML in musical performance
   - Shows importance of rapid feedback and user control in ML systems

2. **Tanaka, A. (2006)**. "Interaction, experience and the future of music." In *Music and Technology in the Twentieth Century*.
   - Establishes principles for preserving performer agency in interactive systems
   - Discusses the importance of embodied interaction and predictability

3. **Jordà, S. (2005)**. "Digital Lutherie: Crafting musical computers for new musics' performance and improvisation." PhD Thesis.
   - Explores design of new digital musical instruments
   - Emphasizes importance of learning curve and instrument playability

## Conclusion

The hybrid adaptive agent represents a balanced approach to AI-assisted musical performance: it provides intelligent, adaptive responses that enhance the performer's expressiveness while maintaining full performer agency and control. By combining reliable symbolic logic with optional personalized ML, it offers both predictability and adaptability, creating a system that performers can learn to "play" as they would any musical instrument.
