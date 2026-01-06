# Brain-Based Measures

Neural markers of emotion, agency, creativity, engagement, and prediction from EEG, fNIRS, and fMRI.

## Overview

Brain-based measures provide objective neural markers of psychological states. These measures complement self-report and behavioral data, offering insights into underlying cognitive and affective processes.

## EEG Markers

### Affective States

#### Frontal Alpha Asymmetry
- **Measure**: Relative alpha power difference between left and right frontal regions (F4-F3)
- **Interpretation**: 
  - Positive asymmetry (left > right): Approach motivation, positive affect
  - Negative asymmetry (right > left): Avoidance motivation, negative affect
- **Frequency**: 8-13 Hz alpha band
- **Regions**: F3/F4, AF3/AF4
- **Reference**: Davidson (1992, 2004)

#### Theta Power
- **Measure**: Frontal midline theta (Fz) power
- **Interpretation**: Emotional arousal, cognitive control
- **Frequency**: 4-7 Hz theta band
- **Applications**: Monitoring affective engagement during music

**Notebook**: [`eeg_affect_markers.ipynb`](eeg_affect_markers.ipynb)

### Engagement and Attention

#### Alpha Suppression
- **Measure**: Reduction in posterior alpha power
- **Interpretation**: Visual attention, active processing
- **Frequency**: 8-13 Hz alpha band
- **Regions**: O1/O2, P3/P4
- **Application**: Measuring engagement with visual/musical stimuli

#### Beta Power
- **Measure**: Sensorimotor beta (C3/C4) power
- **Interpretation**: Motor preparation, active engagement
- **Frequency**: 13-30 Hz beta band
- **Application**: Tracking motor involvement in music-making

**Notebook**: [`eeg_engagement_markers.ipynb`](eeg_engagement_markers.ipynb)

### Flow States and Creativity

#### Transient Hypofrontality
- **Measure**: Reduced frontal theta/alpha power during flow
- **Interpretation**: Reduced self-monitoring and cognitive control
- **Regions**: Frontal sites (F3, Fz, F4)
- **Application**: Detecting flow states during creative activities

#### Alpha/Theta Ratio
- **Measure**: Ratio of alpha to theta power
- **Interpretation**: Relaxed alertness, creative ideation
- **Application**: Monitoring creative cognitive states

#### Gamma Synchronization
- **Measure**: Increased gamma (30-100 Hz) coherence
- **Interpretation**: Feature binding, integration, insight
- **Application**: Detecting "aha" moments in creativity

**Notebook**: [`eeg_flow_creativity.ipynb`](eeg_flow_creativity.ipynb)

### Prediction and Error Processing

#### P300 (P3)
- **Measure**: Event-related potential ~300-500ms post-stimulus
- **Interpretation**: Attention allocation, surprise, significance
- **Application**: Detecting unexpected musical events

#### N400
- **Measure**: Event-related potential ~400ms post-stimulus
- **Interpretation**: Semantic incongruity, expectation violation
- **Application**: Musical expectancy and prediction errors

#### Mismatch Negativity (MMN)
- **Measure**: Automatic deviance detection ~100-250ms
- **Interpretation**: Pre-attentive prediction error
- **Application**: Implicit learning, predictive processing

#### Error-Related Negativity (ERN)
- **Measure**: Response-locked ERP ~50-100ms after error
- **Interpretation**: Error detection, performance monitoring
- **Application**: Agency and control during music-making

**Notebook**: [`eeg_prediction_error.ipynb`](eeg_prediction_error.ipynb)

## fNIRS Markers

### Prefrontal Engagement

#### Dorsolateral PFC (DLPFC)
- **Regions**: Left/right DLPFC (F3, F4 approximate locations)
- **Measure**: Oxygenated hemoglobin (HbO) concentration
- **Interpretation**: 
  - Executive control
  - Working memory
  - Creative problem-solving
- **Application**: Monitoring cognitive effort during music creation

#### Ventrolateral PFC (VLPFC)
- **Regions**: Inferior frontal gyrus
- **Measure**: HbO changes
- **Interpretation**: 
  - Inhibitory control
  - Emotion regulation
  - Response selection
- **Application**: Tracking self-regulation during creative tasks

**Notebook**: [`fnirs_prefrontal_engagement.ipynb`](fnirs_prefrontal_engagement.ipynb)

### Creative Thinking Patterns

#### Widespread Cortical Activation
- **Pattern**: Diffuse prefrontal and temporal activation
- **Interpretation**: Divergent thinking, idea generation
- **Contrast**: Focused activation during convergent thinking

#### Connectivity Patterns
- **Measure**: Functional connectivity between prefrontal regions
- **Interpretation**: Integration of information, creative synthesis
- **Application**: Differentiating creative vs. routine processing

**Notebook**: [`fnirs_creative_patterns.ipynb`](fnirs_creative_patterns.ipynb)

### Emotional Processing

#### Orbitofrontal Cortex (OFC)
- **Regions**: Medial OFC
- **Measure**: HbO changes
- **Interpretation**: Reward processing, emotional valuation
- **Application**: Aesthetic pleasure, musical reward

#### Anterior Prefrontal Cortex
- **Regions**: Frontopolar cortex
- **Measure**: HbO changes
- **Interpretation**: Self-referential processing, metacognition
- **Application**: Agency awareness, creative self-reflection

**Notebook**: [`fnirs_emotion.ipynb`](fnirs_emotion.ipynb)

## fMRI Markers

### Creativity Networks

#### Default Mode Network (DMN)
- **Regions**: 
  - Medial prefrontal cortex (mPFC)
  - Posterior cingulate cortex (PCC)
  - Angular gyrus
  - Medial temporal lobe
- **Function**: 
  - Spontaneous thought
  - Imagination
  - Autobiographical memory
- **In creativity**: Active during idea generation, divergent thinking

#### Executive Control Network (ECN)
- **Regions**:
  - Dorsolateral PFC
  - Posterior parietal cortex
  - Anterior cingulate cortex (ACC)
- **Function**:
  - Goal-directed cognition
  - Cognitive control
  - Evaluation
- **In creativity**: Active during idea evaluation, convergent thinking

#### Salience Network (SN)
- **Regions**:
  - Anterior insula
  - Dorsal ACC
- **Function**:
  - Attention switching
  - Network coordination
- **In creativity**: Facilitates switching between DMN and ECN

**Notebook**: [`fmri_creativity_networks.ipynb`](fmri_creativity_networks.ipynb)

### Predictive Coding

#### Hierarchical Prediction Errors
- **Regions**: Temporal cortex hierarchy (A1 → STG → STS)
- **Measure**: Activity reflecting prediction errors at multiple levels
- **Interpretation**: Predictive processing of musical structure

#### Reward Prediction Errors
- **Regions**: Ventral striatum, midbrain dopamine system
- **Measure**: BOLD response to unexpected rewards/pleasure
- **Application**: Musical pleasure, aesthetic reward

**Notebook**: [`fmri_predictive_coding.ipynb`](fmri_predictive_coding.ipynb)

### Aesthetic Experience

#### Reward Circuitry
- **Regions**:
  - Nucleus accumbens (NAcc)
  - Ventral tegmental area (VTA)
  - Orbitofrontal cortex
- **Function**: Pleasure, motivation, reward
- **Application**: Musical pleasure, aesthetic appreciation

#### Mirror Neuron System
- **Regions**: Inferior frontal gyrus, inferior parietal lobule
- **Function**: Action observation/execution, empathy
- **Application**: Musical embodiment, emotional resonance

**Notebook**: [`fmri_aesthetic_experience.ipynb`](fmri_aesthetic_experience.ipynb)

## Multimodal Integration

### EEG + fNIRS
- **Complementarity**: EEG (temporal) + fNIRS (spatial, metabolic)
- **Advantages**: 
  - Better spatiotemporal resolution than either alone
  - Cross-validate findings
  - Distinguish neural from hemodynamic effects

### EEG + fMRI
- **Simultaneous recording**: Challenging but possible
- **Sequential recording**: More common approach
- **Advantages**: Full brain coverage with high temporal resolution

**Notebook**: [`multimodal_integration.ipynb`](../multimodal_fusion/integration_examples.ipynb)

## Data Preprocessing

### EEG Preprocessing Pipeline

```python
def preprocess_eeg(raw_data):
    \"\"\"Standard EEG preprocessing pipeline\"\"\"
    # 1. Filter
    filtered = bandpass_filter(raw_data, low=0.5, high=50)
    
    # 2. Remove bad channels
    cleaned = remove_bad_channels(filtered)
    
    # 3. Artifact rejection (ICA for eye blinks, etc.)
    corrected = run_ica(cleaned)
    
    # 4. Re-reference
    rereferenced = rereference(corrected, method='average')
    
    # 5. Epoch/segment
    epochs = create_epochs(rereferenced)
    
    return epochs
```

### fNIRS Preprocessing Pipeline

```python
def preprocess_fnirs(raw_data):
    \"\"\"Standard fNIRS preprocessing pipeline\"\"\"
    # 1. Convert to optical density
    od = raw_to_od(raw_data)
    
    # 2. Motion artifact correction
    corrected = motion_correction(od)
    
    # 3. Bandpass filter (removes cardiac, respiration)
    filtered = bandpass_filter(corrected, low=0.01, high=0.2)
    
    # 4. Convert to hemoglobin concentration
    hb = od_to_hb(filtered)
    
    return hb
```

## Feature Extraction

### EEG Features

```python
def extract_eeg_features(epochs):
    \"\"\"Extract common EEG features\"\"\"
    features = {}
    
    # Spectral features
    features['alpha_power'] = compute_band_power(epochs, 8, 13)
    features['theta_power'] = compute_band_power(epochs, 4, 7)
    features['beta_power'] = compute_band_power(epochs, 13, 30)
    
    # Asymmetry
    features['frontal_asymmetry'] = compute_asymmetry(epochs, 'F4', 'F3', 8, 13)
    
    # Connectivity
    features['coherence'] = compute_coherence(epochs)
    
    return features
```

### fNIRS Features

```python
def extract_fnirs_features(hb_data):
    \"\"\"Extract fNIRS features\"\"\"
    features = {}
    
    # Mean activation
    features['mean_hbo'] = np.mean(hb_data['HbO'], axis=0)
    
    # Peak activation
    features['peak_hbo'] = np.max(hb_data['HbO'], axis=0)
    
    # Time to peak
    features['time_to_peak'] = np.argmax(hb_data['HbO'], axis=0)
    
    # Connectivity
    features['connectivity'] = compute_functional_connectivity(hb_data)
    
    return features
```

## Quality Assurance

### Signal Quality Checks

**EEG**:
- Impedance < 10kΩ
- No flat channels
- No excessive noise
- Successful artifact removal

**fNIRS**:
- Good scalp coupling
- Sufficient signal strength
- No saturation
- Cardiac pulsation visible (quality indicator)

**fMRI**:
- No excessive motion (< 2mm)
- Good signal-to-noise ratio
- No artifacts (susceptibility, motion)
- Successful registration

### Artifact Detection

```python
def detect_eeg_artifacts(epochs):
    \"\"\"Detect and mark artifacted epochs\"\"\"
    artifacts = []
    
    # Amplitude threshold
    if np.max(np.abs(epochs)) > 100:  # microvolts
        artifacts.append('amplitude')
    
    # Flat signal
    if np.std(epochs) < 0.1:
        artifacts.append('flat')
    
    # High frequency noise
    if np.mean(np.abs(np.diff(epochs))) > 10:
        artifacts.append('noise')
    
    return artifacts
```

## Statistical Analysis

### Group Comparisons

```python
from scipy import stats

# Compare conditions
def compare_conditions(condition1, condition2):
    \"\"\"Statistical comparison of neural markers\"\"\"
    # Paired t-test
    t_stat, p_value = stats.ttest_rel(condition1, condition2)
    
    # Effect size
    cohens_d = (condition1.mean() - condition2.mean()) / condition1.std()
    
    return {'t': t_stat, 'p': p_value, 'd': cohens_d}
```

### Brain-Behavior Correlations

```python
def correlate_brain_behavior(neural_data, behavioral_data):
    \"\"\"Correlate neural markers with behavior\"\"\"
    r, p = stats.pearsonr(neural_data, behavioral_data)
    return {'r': r, 'p': p}
```

## Integration with BrainJam

### Real-Time Applications

Brain markers can be extracted in real-time to:
- Adapt music generation to user state
- Provide neurofeedback
- Trigger events based on cognitive states
- Monitor engagement and flow

### Validation Studies

Use brain markers to:
- Validate self-report measures
- Understand mechanisms of interventions
- Identify neural correlates of outcomes
- Predict individual responses

## Ethical Considerations

### Neural Privacy
- Brain data may reveal unintended information
- Secure storage and limited access
- Clear consent about inferences made

### Data Quality
- Don't over-interpret noisy data
- Report preprocessing decisions
- Use appropriate statistics

### Clinical Claims
- Avoid diagnostic language without validation
- Don't promise therapeutic effects
- Clearly distinguish research from clinical use

## Resources

### Software

**EEG**: MNE-Python, EEGLAB, FieldTrip
**fNIRS**: Homer2/3, nirsLAB
**fMRI**: FSL, SPM, AFNI, nilearn

### References

**EEG & Affect**:
- Davidson, R. J. (1992). Anterior cerebral asymmetry and the nature of emotion. Brain and Cognition, 20(1), 125-151.
- Pizzagalli, D. A. (2007). Electroencephalography and high-density electrophysiological source localization. Handbook of Psychophysiology, 3, 56-84.

**fNIRS**:
- Piper, S. K., et al. (2014). A wearable multi-channel fNIRS system for brain imaging in freely moving subjects. NeuroImage, 85, 64-71.

**Creativity Networks**:
- Beaty, R. E., et al. (2016). Robust prediction of individual creative ability from brain functional connectivity. PNAS, 113(4), 1087-1092.
- Benedek, M., & Fink, A. (2019). Toward a neurocognitive framework of creative cognition. Trends in Cognitive Sciences, 23(9), 742-754.

**Predictive Coding**:
- Friston, K. (2005). A theory of cortical responses. Philosophical Transactions of the Royal Society B, 360(1456), 815-836.
- Vuust, P., & Witek, M. A. (2014). Rhythmic complexity and predictive coding: a novel approach to modeling rhythm and meter perception in music. Frontiers in Psychology, 5, 1111.

## Contributing

When adding new markers:
1. Provide clear definition and interpretation
2. Include preprocessing code
3. Specify feature extraction methods
4. Reference validation studies
5. Discuss limitations

## Contact

For questions about neural markers or analysis methods, please open an issue.
