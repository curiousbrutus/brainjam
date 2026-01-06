# Questionnaires

Self-report measures for assessing emotion, agency, creativity, and well-being in brain-mediated music research.

## Overview

This directory contains validated psychological questionnaires and scales for measuring subjective experiences during creative music-making and listening.

## Available Questionnaires

### 1. PANAS (Positive and Negative Affect Schedule)

**Purpose**: Measure positive and negative affective states

**Items**: 20 items (10 positive, 10 negative)

**Scales**: 
- Positive Affect (PA): enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud, attentive
- Negative Affect (NA): distressed, upset, guilty, scared, hostile, irritable, ashamed, nervous, jittery, afraid

**Scoring**: 5-point Likert scale (1 = very slightly or not at all, 5 = extremely)

**Time**: ~2-3 minutes

**Reference**: Watson, D., Clark, L. A., & Tellegen, A. (1988). Development and validation of brief measures of positive and negative affect: The PANAS scales. Journal of Personality and Social Psychology, 54(6), 1063-1070.

**Notebook**: [`panas_notebook.ipynb`](panas_notebook.ipynb)

### 2. SAM (Self-Assessment Manikin)

**Purpose**: Non-verbal assessment of emotional valence, arousal, and dominance

**Dimensions**:
- Valence: unhappy → happy
- Arousal: calm → excited
- Dominance: controlled → in control

**Scoring**: 9-point pictorial scale

**Time**: ~30 seconds

**Advantages**: Language-independent, quick, suitable for repeated measures

**Reference**: Bradley, M. M., & Lang, P. J. (1994). Measuring emotion: The Self-Assessment Manikin and the semantic differential. Journal of Behavior Therapy and Experimental Psychiatry, 25(1), 49-59.

**Notebook**: [`sam_notebook.ipynb`](sam_notebook.ipynb)

### 3. Flow State Scale

**Purpose**: Measure experience of flow during creative activities

**Dimensions**:
- Challenge-skill balance
- Action-awareness merging
- Clear goals
- Unambiguous feedback
- Concentration on task
- Sense of control
- Loss of self-consciousness
- Time transformation
- Autotelic experience

**Items**: 36 items (long form) or 9 items (short form)

**Scoring**: 5-point Likert scale (1 = strongly disagree, 5 = strongly agree)

**Time**: 5-10 minutes (long), 2-3 minutes (short)

**Reference**: Jackson, S. A., & Eklund, R. C. (2002). Assessing flow in physical activity: The Flow State Scale-2 and Dispositional Flow Scale-2. Journal of Sport and Exercise Psychology, 24(2), 133-150.

**Notebook**: [`flow_state_notebook.ipynb`](flow_state_notebook.ipynb)

### 4. Agency and Ownership Scales

**Purpose**: Measure sense of agency (feeling of control) and sense of ownership (feeling of authorship)

**Dimensions**:
- **Sense of Agency**: Degree of control over actions and outcomes
- **Sense of Ownership**: Feeling that creative output is "mine"

**Items**: 10-15 items adapted for creative contexts

**Example items**:
- "I felt in control of the music creation process"
- "The music felt like my own creation"
- "I could predict how my actions would affect the sound"
- "I felt like I was the author of the musical output"

**Scoring**: 7-point Likert scale (1 = strongly disagree, 7 = strongly agree)

**Time**: 3-5 minutes

**References**: 
- Gallagher, S. (2000). Philosophical conceptions of the self: Implications for cognitive science. Trends in Cognitive Sciences, 4(1), 14-21.
- Limerick, H., Coyle, D., & Moore, J. W. (2014). The experience of agency in human-computer interactions: A review. Frontiers in Human Neuroscience, 8, 643.

**Notebook**: [`agency_ownership_notebook.ipynb`](agency_ownership_notebook.ipynb)

### 5. Aesthetic Emotions Scale (AESTHEMOS)

**Purpose**: Measure emotions specific to aesthetic experiences

**Emotion Categories**:
- **Epistemic emotions**: Interest, surprise, intellectual challenge
- **Prototypical aesthetic emotions**: Beauty, fascination, enchantment, transcendence
- **Negative emotions**: Confusion, boredom, uneasiness
- **Nostalgia/relaxation**: Nostalgia, peacefulness, relaxation

**Items**: 42 items covering diverse aesthetic emotions

**Scoring**: 5-point Likert scale (1 = not at all, 5 = very much)

**Time**: 5-7 minutes

**Reference**: Schindler, I., Hosoya, G., Menninghaus, W., Beermann, U., Wagner, V., Eid, M., & Scherer, K. R. (2017). Measuring aesthetic emotions: A review of the literature and a new assessment tool. PLoS ONE, 12(6), e0178899.

**Notebook**: [`aesthetic_emotions_notebook.ipynb`](aesthetic_emotions_notebook.ipynb)

### 6. Well-Being Measures

**Purpose**: Assess psychological well-being and life satisfaction

**Included Scales**:
- **SWLS** (Satisfaction With Life Scale): 5 items, overall life satisfaction
- **WHO-5** (Well-Being Index): 5 items, subjective well-being
- **PERMA-Profiler**: Positive emotion, Engagement, Relationships, Meaning, Accomplishment

**Time**: 5-10 minutes combined

**References**:
- Diener, E., Emmons, R. A., Larsen, R. J., & Griffin, S. (1985). The Satisfaction With Life Scale. Journal of Personality Assessment, 49(1), 71-75.
- Butler, J., & Kern, M. L. (2016). The PERMA-Profiler: A brief multidimensional measure of flourishing. International Journal of Wellbeing, 6(3), 1-48.

**Notebook**: [`wellbeing_notebook.ipynb`](wellbeing_notebook.ipynb)

## Usage Guidelines

### When to Administer

**Pre-session**: Baseline measures (trait versions, general well-being)

**During session**: SAM for quick repeated measures

**Post-session**: State measures (PANAS, Flow, Agency), aesthetic emotions

**Follow-up**: Well-being measures for longitudinal assessment

### Administration Modes

1. **Paper-based**: Traditional questionnaire format
2. **Digital**: Online forms, tablet applications
3. **Integrated**: Built into experimental software
4. **Ecological momentary assessment**: Smartphone apps for in-the-moment responses

### Best Practices

**Instructions**:
- Provide clear, standardized instructions
- Specify time frame (right now, past week, in general)
- Include examples when needed

**Response Format**:
- Ensure scales are clearly labeled
- Use consistent formatting across measures
- Consider reverse-scored items for attention checks

**Data Quality**:
- Include attention check items
- Monitor for response patterns (e.g., all same answer)
- Check for missing data
- Calculate reliability (Cronbach's alpha)

**Cultural Considerations**:
- Validate translations if using non-English versions
- Consider cultural differences in emotional expression
- Adapt examples to be culturally relevant

## Data Analysis

### Scoring

Each notebook includes automated scoring functions:

```python
# Example: PANAS scoring
def score_panas(responses):
    """
    responses: dict with item numbers as keys, ratings as values
    returns: dict with 'positive_affect' and 'negative_affect' scores
    """
    positive_items = [1, 3, 5, 9, 10, 12, 14, 16, 17, 19]
    negative_items = [2, 4, 6, 7, 8, 11, 13, 15, 18, 20]
    
    pa_score = sum(responses[i] for i in positive_items)
    na_score = sum(responses[i] for i in negative_items)
    
    return {'positive_affect': pa_score, 'negative_affect': na_score}
```

### Reliability

Calculate internal consistency:

```python
from pingouin import cronbach_alpha

# Calculate Cronbach's alpha
alpha, ci = cronbach_alpha(data=item_responses)
print(f"Cronbach's alpha: {alpha:.3f}, 95% CI: [{ci[0]:.3f}, {ci[1]:.3f}]")
```

### Validity

Check construct validity through:
- Correlations with related measures
- Known-groups comparisons
- Convergent and discriminant validity

## Ethical Considerations

### Privacy
- Store responses securely with encryption
- De-identify data as soon as possible
- Limit access to authorized researchers

### Participant Welfare
- Brief participants on purpose of measures
- Provide option to skip sensitive questions
- Have support resources available if measures induce distress
- Debrief after session

### Data Use
- Use only for stated research purposes
- Obtain consent for any secondary analyses
- Report results aggregated when possible

## Integration with BrainJam

Questionnaires complement other BrainJam measures:

**With Neural Data**:
- Correlate self-reported flow with EEG markers
- Compare agency ratings with neural signatures
- Validate emotion recognition from brain signals

**With Behavioral Tasks**:
- Triangulate creativity across measures
- Cross-validate agency assessments
- Combine objective and subjective indicators

**For Validation**:
- Verify intervention effectiveness
- Monitor psychological safety
- Assess user experience

## Notebooks

All notebooks include:
- Questionnaire display/administration code
- Automated scoring functions
- Data validation checks
- Descriptive statistics
- Visualization templates
- Example analyses
- Interpretation guidelines

## References

### Key Papers

**Emotion Measurement**
- Russell, J. A. (1980). A circumplex model of affect. Journal of Personality and Social Psychology, 39(6), 1161-1178.
- Mauss, I. B., & Robinson, M. D. (2009). Measures of emotion: A review. Cognition and Emotion, 23(2), 209-237.

**Agency and Control**
- Haggard, P., & Chambon, V. (2012). Sense of agency. Current Biology, 22(10), R390-R392.
- Moore, J. W. (2016). What is the sense of agency and why does it matter? Frontiers in Psychology, 7, 1272.

**Creativity Assessment**
- Kaufman, J. C., Plucker, J. A., & Baer, J. (2008). Essentials of creativity assessment. Wiley.
- Silvia, P. J. (2012). Mirrors, masks, and motivation: Implicit and explicit self-focused attention influence effort-related cardiovascular reactivity. Biological Psychology, 90(3), 192-201.

**Psychometrics**
- Streiner, D. L., Norman, G. R., & Cairney, J. (2015). Health measurement scales: A practical guide to their development and use (5th ed.). Oxford University Press.

## Contributing

To add a new questionnaire:

1. Create a new notebook with questionnaire implementation
2. Include psychometric information (reliability, validity)
3. Provide scoring algorithm
4. Add usage examples
5. Update this README

## Contact

For questions about specific questionnaires or psychometric properties, please open an issue.
