# Interaction Measures Module

This module provides measures for evaluating performer agency, flow, responsiveness,
and engagement in BrainJam performance sessions.

## Purpose

**Psychology supports evaluation in this project - it does not dominate it.**

These measures help us understand:

- **Agency**: Does the performer feel in control?
- **Flow**: Is the performer in an optimal state of engagement?
- **Responsiveness**: How quickly and predictably does the system respond?
- **Engagement**: Is the interaction meaningful and sustained?

## NOT Clinical or Diagnostic

These measures are for:
- ✓ Evaluating performance system design
- ✓ Understanding performer experience  
- ✓ Improving human-AI interaction
- ✗ NOT clinical assessment
- ✗ NOT therapeutic intervention
- ✗ NOT diagnostic tools

## Module Structure

```
interaction_measures/
├── questionnaires/          # Simple self-report measures for agency and flow
├── behavioral_tasks/        # Timing and interaction metrics
├── brain_measures/          # Optional neural correlates (not required)
├── experimental_designs/    # Study templates for performance research
├── multimodal_fusion/       # Integration of multiple data streams
└── validation/              # Frameworks for system evaluation
```

### Core Constructs for Performance Evaluation

1. **Agency**: Sense of control and authorship in performance
2. **Flow**: Optimal experience during creative interaction
3. **Responsiveness**: System latency and predictability
4. **Engagement**: Sustained, meaningful interaction

## Quick Start

For simple agency assessment after a performance session:

```python
# Example: Simple post-performance survey
questions = [
    "I felt in control of the sounds being generated (1-10)",
    "The system responded predictably to my input (1-10)",
    "I felt like I was making music (1-10)",
]
```

## Questionnaires

Simple self-report measures for performance evaluation:

- **Agency/Ownership**: Sense of control during performance
- **Flow State Scale**: Measuring optimal experience
- **Responsiveness**: Perceived system latency and predictability
- **Aesthetic Engagement**: Satisfaction with musical output

See: [`questionnaires/README.md`](questionnaires/README.md)

## Behavioral Measures

Objective metrics for evaluating performance interaction:

- **Timing variability**: Consistency of system response
- **Control range coverage**: How much of parameter space is accessible
- **Interaction patterns**: Temporal dynamics of performer-system exchange

See: [`behavioral_tasks/README.md`](behavioral_tasks/README.md)

## Brain Measures (Optional)

Neural correlates can provide additional context but are NOT required:

- **Engagement markers**: Frontal activity patterns
- **Flow indicators**: Neural signatures of optimal experience

**Note**: Brain signals are control inputs, not diagnostic measures.

See: [`brain_measures/README.md`](brain_measures/README.md)

## Experimental Designs

Templates and methodologies for rigorous studies:

- **Within-subjects designs**: Repeated measures, crossover studies
- **Between-subjects designs**: Control vs. intervention groups
- **Mixed designs**: Combining within and between factors
- **Longitudinal studies**: Tracking changes over time
- **Single-case experimental designs**: N-of-1 trials

See: [`experimental_designs/README.md`](experimental_designs/README.md)

## Multimodal Data Fusion

Integrating multiple data sources for comprehensive assessment:

- **Sensor fusion**: Combining EEG, fNIRS, behavioral data
- **Triangulation**: Cross-validating across modalities
- **Machine learning approaches**: Multi-view learning, ensemble methods
- **Temporal alignment**: Synchronizing different data streams
- **Feature integration**: Creating composite measures

See: [`multimodal_fusion/README.md`](multimodal_fusion/README.md)

## Validation Frameworks

For evaluating the performance system:

- **Agency validation**: Does it enhance or diminish creative control?
- **Responsiveness validation**: Is latency acceptable for performance?
- **Safety validation**: Monitor for frustration or negative experiences

**NOT for clinical validation or therapeutic claims.**

See: [`validation/README.md`](validation/README.md)

## Integration with BrainJam Performance System

These measures help answer:
- Does the performer feel they are making the music?
- Is the system responsive enough for real-time performance?
- Are control mappings intuitive or frustrating?
- Does the system enhance or inhibit creative expression?

## Best Practices

### For Performance Evaluation
- **Keep it simple**: Short questionnaires, < 5 minutes
- **Timing**: Assess immediately after performance while experience is fresh
- **Context**: Distinguish technical issues from design issues
- **Iteration**: Use feedback to improve mappings and system design

### What to Measure
- **Essential**: Agency, responsiveness, satisfaction
- **Optional**: Flow, engagement, aesthetic quality
- **Avoid**: Clinical constructs, diagnostic frameworks

---

**Note**: The subdirectories contain comprehensive psychological research tools.
The above guidance emphasizes their use for performance system evaluation.
