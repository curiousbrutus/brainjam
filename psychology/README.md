# Psychology Module

This module contains psychological measures, behavioral tasks, and validation frameworks for studying emotion, agency, creativity, and well-being in brain-mediated music research.

## Overview

The psychology module provides comprehensive tools for measuring psychological constructs that are critical to understanding creative experiences and validating AI-mediated interventions.

### Core Psychological Constructs

1. **Emotion**: Affective states during creative processes
2. **Agency**: Sense of control and authorship
3. **Creativity**: Divergent thinking, originality, flow states
4. **Well-being**: Psychological health, satisfaction, flourishing

## Module Structure

```
psychology/
├── questionnaires/          # Self-report measures and scales
├── behavioral_tasks/        # Task-based assessments
├── brain_measures/          # Neural markers of psychological states
├── experimental_designs/    # Study templates and methodologies
├── multimodal_fusion/       # Integration of multiple data modalities
└── validation/              # Ethical validation frameworks
```

## Questionnaires

Self-report measures for quantifying subjective experiences:

- **PANAS**: Positive and Negative Affect Schedule for mood assessment
- **SAM**: Self-Assessment Manikin for valence, arousal, and dominance
- **Flow State Scale**: Measuring optimal experience during creativity
- **Agency/Ownership**: Sense of control and authorship questionnaires
- **Aesthetic Emotions**: Measuring emotional responses to creative outputs

See: [`questionnaires/README.md`](questionnaires/README.md)

## Behavioral Tasks

Objective measures of psychological constructs through behavior:

- **Creative thinking tasks**: Alternative Uses Test, divergent thinking
- **Reaction time paradigms**: Measuring cognitive processing
- **Decision-making tasks**: Choice behavior and preference
- **Agency manipulation tasks**: Testing sense of control
- **Music perception tasks**: Measuring aesthetic responses

See: [`behavioral_tasks/README.md`](behavioral_tasks/README.md)

## Brain-Based Measures

Neural markers of psychological states:

### EEG Markers
- **Affect**: Frontal alpha asymmetry, theta power
- **Engagement**: Frontal midline theta, alpha suppression
- **Flow states**: Transient hypofrontality markers
- **Prediction error**: P300, N400, mismatch negativity

### fNIRS Markers
- **Prefrontal engagement**: Dorsolateral PFC activation
- **Creative thinking**: Widespread cortical activation patterns
- **Emotional processing**: Orbitofrontal cortex responses

### fMRI Markers
- **Creativity networks**: Default mode network, executive control network
- **Prediction**: Predictive coding signals in temporal cortex
- **Aesthetic experience**: Reward circuitry activation

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

Ethical validation of AI-mediated creative interventions:

- **Efficacy validation**: Does the intervention work as intended?
- **Safety validation**: Are there adverse psychological effects?
- **Agency validation**: Does it enhance or diminish creative control?
- **Well-being validation**: Long-term effects on psychological health
- **Equity validation**: Who benefits and who might be excluded?

See: [`validation/README.md`](validation/README.md)

## Getting Started

### Prerequisites

```bash
# Install additional psychology-specific packages
pip install psychopy>=2023.1.0  # For behavioral tasks
pip install pingouin>=0.5.3     # For statistical analysis
```

### Quick Start

1. **Measure emotion**: Start with `questionnaires/panas_notebook.ipynb`
2. **Assess agency**: Use `questionnaires/agency_ownership_notebook.ipynb`
3. **Test creativity**: Try `behavioral_tasks/divergent_thinking_notebook.ipynb`
4. **Extract neural markers**: See `brain_measures/eeg_affect_markers.ipynb`
5. **Design a study**: Review `experimental_designs/within_subjects_template.ipynb`

## Best Practices

### Measurement Selection

- **Multi-method assessment**: Combine self-report, behavioral, and neural measures
- **Validated instruments**: Use established, psychometrically sound scales
- **Context-appropriate**: Choose measures suitable for your research context
- **Pilot testing**: Test your measurement protocol before main study

### Data Quality

- **Attention checks**: Include validity items in questionnaires
- **Practice trials**: Allow participants to familiarize with tasks
- **Quality control**: Monitor data quality in real-time
- **Missing data**: Plan for handling incomplete responses

### Ethical Considerations

- **Informed consent**: Participants understand all measures
- **Privacy**: Protect sensitive psychological data
- **Debriefing**: Explain purpose of measures after study
- **Support resources**: Provide contacts if distress occurs
- **Cultural sensitivity**: Adapt measures for diverse populations

## Analysis Approaches

### Descriptive Statistics
- Central tendency and variability
- Distribution checks (normality, outliers)
- Reliability analysis (Cronbach's alpha, test-retest)

### Inferential Statistics
- Group comparisons (t-tests, ANOVA)
- Correlations and associations
- Regression and prediction models
- Mediation and moderation analyses

### Advanced Methods
- Factor analysis and structural equation modeling
- Multilevel modeling for nested data
- Time series analysis for longitudinal data
- Machine learning for classification and prediction

## Integration with BrainJam

The psychology module integrates with other BrainJam components:

- **Neural signals** (`brain_measures/`) ↔ **Signal processing** (`notebooks/`)
- **Questionnaires** ↔ **Validation** (`validation/`)
- **Experimental designs** ↔ **Ethics** (`ethics.md`)
- **Multimodal fusion** ↔ **Brain-music mapping** (`notebooks/`)

## Resources

### Recommended Reading

**Emotion Measurement**
- Bradley & Lang (1994): "Measuring emotion: The Self-Assessment Manikin"
- Watson et al. (1988): "Development and validation of brief measures of positive and negative affect: The PANAS scales"

**Agency and Ownership**
- Gallagher (2000): "Philosophical conceptions of the self: implications for cognitive science"
- Haggard & Chambon (2012): "Sense of agency"

**Creativity Assessment**
- Guilford (1967): "The nature of human intelligence"
- Dietrich (2004): "Neurocognitive mechanisms underlying the experience of flow"

**Flow States**
- Csikszentmihalyi (1990): "Flow: The Psychology of Optimal Experience"
- Jackson & Eklund (2002): "Assessing flow in physical activity: The Flow State Scale-2"

**Aesthetic Emotions**
- Scherer & Zentner (2008): "Music evoked emotions are different"
- Pelowski et al. (2017): "Move me, astonish me... delight my eyes and brain"

**Well-being**
- Ryff (1989): "Happiness is everything, or is it? Explorations on the meaning of psychological well-being"
- Seligman (2011): "Flourish: A visionary new understanding of happiness and well-being"

### Online Resources

- **Questionnaire databases**: PhenX Toolkit, Mental Measurements Yearbook
- **Open materials**: OSF, Open Science Framework
- **Statistical tools**: JASP, jamovi, R packages (psych, lavaan)

## Contributing

When adding new measures or tasks:

1. Include clear documentation of psychometric properties
2. Provide example notebooks with simulated data
3. Add references to validation studies
4. Consider cross-cultural applicability
5. Update this README with new content

## Citation

If you use measures from this module, please cite both the original scale developers and this repository:

```bibtex
@misc{brainjam_psychology2024,
  title={BrainJam Psychology Module: Measures for Creative Neuroscience},
  author={BrainJam Contributors},
  year={2024},
  howpublished={\url{https://github.com/curiousbrutus/brainjam}}
}
```

## Contact

For questions about psychological measures or study design, please open an issue or contact the research team.
