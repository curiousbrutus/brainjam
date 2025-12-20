# Behavioral Tasks

Objective assessments of psychological constructs through task-based measures.

## Overview

Behavioral tasks provide objective, performance-based measures that complement self-report questionnaires. These tasks assess creativity, agency, decision-making, and aesthetic responses through observable behavior.

## Available Tasks

### 1. Divergent Thinking Tasks

**Alternative Uses Test (AUT)**
- **Purpose**: Measure creative thinking ability
- **Task**: Generate as many uses as possible for common objects (e.g., brick, paperclip)
- **Scoring**: Fluency (number of ideas), flexibility (categories), originality (uniqueness)
- **Duration**: 2-3 minutes per object
- **Reference**: Guilford (1967)

**Notebook**: [`divergent_thinking_notebook.ipynb`](divergent_thinking_notebook.ipynb)

### 2. Agency Manipulation Tasks

**Intentional Binding Task**
- **Purpose**: Implicit measure of sense of agency
- **Task**: Judge temporal interval between action and outcome
- **Measure**: Perceived compression of time (binding) indicates agency
- **Duration**: 10-15 minutes
- **Reference**: Haggard, Clark, & Kalogeras (2002)

**Perceptual Matching Task**
- **Purpose**: Measure agency under different control conditions
- **Task**: Match sensory feedback to actions under varying delays/transformations
- **Measure**: Accuracy and confidence in agency judgments
- **Duration**: 15-20 minutes

**Notebook**: [`agency_tasks_notebook.ipynb`](agency_tasks_notebook.ipynb)

### 3. Creative Fluency Tasks

**Musical Pattern Generation**
- **Purpose**: Measure musical creativity
- **Task**: Generate rhythmic or melodic patterns following constraints
- **Scoring**: Number of unique patterns, diversity, complexity
- **Duration**: 5-10 minutes

**Sound Exploration Task**
- **Purpose**: Assess exploratory behavior in sound space
- **Task**: Freely explore generative audio system parameters
- **Measure**: Parameter diversity, exploration breadth, return patterns
- **Duration**: 5-15 minutes

**Notebook**: [`creative_fluency_notebook.ipynb`](creative_fluency_notebook.ipynb)

### 4. Aesthetic Judgment Tasks

**Preference Rating Task**
- **Purpose**: Measure aesthetic preferences
- **Task**: Rate musical excerpts on pleasantness, beauty, interest
- **Scoring**: Rating distributions, consistency, extremity
- **Duration**: 10-20 minutes

**Forced-Choice Aesthetic Task**
- **Purpose**: Assess aesthetic decision-making
- **Task**: Choose between pairs of musical stimuli
- **Measure**: Choice patterns, consistency, reaction time
- **Duration**: 10-15 minutes

**Notebook**: [`aesthetic_judgment_notebook.ipynb`](aesthetic_judgment_notebook.ipynb)

### 5. Decision-Making Tasks

**Musical Choice Task**
- **Purpose**: Examine decision-making in creative contexts
- **Task**: Choose between different generative parameters or outputs
- **Measure**: Choice consistency, risk-taking, exploration vs. exploitation
- **Duration**: 10-15 minutes

**Effort Allocation Task**
- **Purpose**: Measure motivation and engagement
- **Task**: Choose effort levels for rewards
- **Measure**: Effort willingness, task persistence
- **Duration**: 10-15 minutes

**Notebook**: [`decision_making_notebook.ipynb`](decision_making_notebook.ipynb)

### 6. Reaction Time Paradigms

**Go/No-Go Task**
- **Purpose**: Measure cognitive control and impulsivity
- **Task**: Respond to target stimuli, withhold for non-targets
- **Measure**: Accuracy, reaction time, false alarms
- **Duration**: 5-10 minutes

**Affective Priming**
- **Purpose**: Implicit measure of emotional associations
- **Task**: Categorize targets after brief emotional primes
- **Measure**: RT facilitation/interference from primes
- **Duration**: 10-15 minutes

**Notebook**: [`reaction_time_notebook.ipynb`](reaction_time_notebook.ipynb)

## Task Design Principles

### Validity
- **Face validity**: Task appears to measure what it claims
- **Construct validity**: Task measures the intended psychological construct
- **Ecological validity**: Task resembles real-world creative behavior
- **Criterion validity**: Task correlates with related measures

### Reliability
- **Internal consistency**: Multiple trials/items yield consistent results
- **Test-retest reliability**: Performance stable across sessions
- **Inter-rater reliability**: Scoring is objective or agreement is high

### Standardization
- **Instructions**: Clear, consistent, and complete
- **Procedure**: Standardized administration across participants
- **Timing**: Consistent duration and time limits
- **Environment**: Controlled testing conditions

### Participant Considerations
- **Practice trials**: Allow familiarization with task
- **Feedback**: Provide appropriate feedback (or explicitly withhold)
- **Motivation**: Ensure engagement and effort
- **Fatigue**: Keep tasks reasonably brief
- **Accessibility**: Consider diverse abilities and backgrounds

## Implementation Guidelines

### Task Programming

Most tasks can be implemented using:
- **PsychoPy**: Full-featured psychology experiment software
- **jsPsych**: Browser-based JavaScript experiments
- **Custom Python**: Using pygame, kivy, or similar
- **Unity/Unreal**: For more complex interactive tasks

### Data Collection

**Essential data**:
- Responses (choices, ratings, generated content)
- Reaction times (when relevant)
- Accuracy (for performance tasks)
- Timestamps and trial information
- Participant ID and condition

**Useful metadata**:
- Trial order and randomization
- Stimulus properties
- Response patterns and strategies
- Errors and corrections

### Quality Control

**Attention checks**:
- Catch trials with obvious correct answers
- Comprehension checks after instructions
- Reaction time outliers

**Exclusion criteria**:
- Below-chance performance
- Extremely fast/slow responding
- Missing data above threshold
- Failed attention checks

## Scoring and Analysis

### Divergent Thinking Scoring

```python
def score_aut(responses):
    \"\"\"
    Score Alternative Uses Test responses
    
    Returns:
    - fluency: total number of responses
    - flexibility: number of different categories
    - originality: statistical infrequency of responses
    \"\"\"
    fluency = len(responses)
    
    # Categorize responses (domain-specific)
    categories = categorize_uses(responses)
    flexibility = len(set(categories))
    
    # Calculate originality (1 - frequency in population)
    originality = calculate_originality(responses, norm_data)
    
    return {
        'fluency': fluency,
        'flexibility': flexibility,
        'originality': originality
    }
```

### Reaction Time Analysis

```python
def analyze_rt(rt_data, accuracy_data):
    \"\"\"
    Analyze reaction time data with accuracy
    \"\"\"
    # Remove error trials
    correct_rts = rt_data[accuracy_data == 1]
    
    # Remove outliers (typically ±3 SD)
    mean_rt = correct_rts.mean()
    sd_rt = correct_rts.std()
    clean_rts = correct_rts[(correct_rts > mean_rt - 3*sd_rt) & 
                            (correct_rts < mean_rt + 3*sd_rt)]
    
    return {
        'mean_rt': clean_rts.mean(),
        'median_rt': np.median(clean_rts),
        'accuracy': accuracy_data.mean()
    }
```

### Agency Scoring

```python
def calculate_intentional_binding(operant_judgments, baseline_judgments):
    \"\"\"
    Calculate intentional binding effect
    
    Negative values indicate temporal compression (binding)
    \"\"\"
    binding = operant_judgments.mean() - baseline_judgments.mean()
    return binding
```

## Integration with BrainJam

### Combining with Neural Measures

**During tasks**:
- Record EEG/fNIRS during task performance
- Time-lock neural analysis to trial events
- Correlate brain states with task performance

**Between measures**:
- Compare behavioral creativity with neural markers
- Validate agency scales with implicit measures
- Triangulate across self-report, behavior, and brain data

### Creative System Evaluation

Use behavioral tasks to:
- Assess creative output from brain-music systems
- Measure user engagement and exploration
- Validate sense of agency in human-AI collaboration
- Evaluate aesthetic quality of generated music

## Ethical Considerations

### Task Difficulty
- Avoid inducing frustration or failure
- Provide breaks for long task batteries
- Allow participants to stop if distressed

### Performance Pressure
- Frame as "no right answers" when appropriate
- Avoid language suggesting evaluation
- Emphasize process over outcome

### Debriefing
- Explain purpose of tasks
- Clarify any deception used
- Provide performance feedback if appropriate
- Answer questions

## Resources

### Software

**PsychoPy**:
- Free, open-source
- Python-based
- Excellent timing precision
- Large user community

**jsPsych**:
- JavaScript library
- Browser-based
- Good for online studies
- Easy deployment

### Databases

- **Open Science Framework**: Pre-registered studies and materials
- **PsyToolkit**: Free online psychological tasks
- **Gorilla**: Online experiment platform

### References

**Creativity Tasks**:
- Guilford, J. P. (1967). The nature of human intelligence. McGraw-Hill.
- Benedek et al. (2013). Assessment of divergent thinking by means of the subjective top-scoring method. Psychology of Aesthetics, Creativity, and the Arts, 7(1), 75-88.

**Agency Tasks**:
- Haggard, P., Clark, S., & Kalogeras, J. (2002). Voluntary action and conscious awareness. Nature Neuroscience, 5(4), 382-385.
- Moore, J. W., & Obhi, S. S. (2012). Intentional binding and the sense of agency. Consciousness and Cognition, 21(1), 546-561.

**Reaction Time**:
- Ratcliff, R., & McKoon, G. (2008). The diffusion decision model: Theory and data for two-choice decision tasks. Neural Computation, 20(4), 873-922.

## Contributing

When adding new tasks:
1. Provide complete implementation code
2. Include practice trials and instructions
3. Specify scoring procedures
4. Document validation studies
5. Consider accessibility
6. Test thoroughly before use

## Contact

For questions about task implementation or scoring, please open an issue.
