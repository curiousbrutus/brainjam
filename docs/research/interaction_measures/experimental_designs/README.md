# Experimental Designs

Templates and methodologies for rigorous psychological research in brain-mediated music studies.

## Overview

This directory provides experimental design templates, power analysis tools, and methodological guidance for conducting well-controlled studies of emotion, agency, creativity, and well-being.

## Design Types

### 1. Within-Subjects Designs

**Description**: Each participant experiences all conditions

**Advantages**:
- Controls for individual differences
- Requires fewer participants
- Higher statistical power
- Direct within-person comparisons

**Disadvantages**:
- Order effects possible
- Carryover effects
- Practice/fatigue effects
- Longer sessions per participant

**Applications**:
- Pre/post intervention comparisons
- Comparing different music generation modes
- Testing multiple neural feedback conditions

**Considerations**:
- Counterbalancing order
- Washout periods between conditions
- Session length and fatigue

**Notebook**: [`within_subjects_template.ipynb`](within_subjects_template.ipynb)

### 2. Between-Subjects Designs

**Description**: Different participants in each condition

**Advantages**:
- No order effects
- No carryover
- Shorter individual sessions
- Can test incompatible conditions

**Disadvantages**:
- Individual differences confound
- Requires more participants
- Lower statistical power
- Need for matching/randomization

**Applications**:
- Control vs. intervention groups
- Different system versions
- One-time manipulations

**Considerations**:
- Random assignment
- Group matching on key variables
- Larger sample sizes needed

**Notebook**: [`between_subjects_template.ipynb`](between_subjects_template.ipynb)

### 3. Mixed Designs

**Description**: Combination of within and between factors

**Example**: 2 (Group: Control vs. Intervention) × 3 (Time: Pre, Post, Follow-up)
- Group is between-subjects
- Time is within-subjects

**Advantages**:
- Flexible and efficient
- Can test interactions
- Combines benefits of both designs

**Disadvantages**:
- Complex analysis
- Requires careful planning
- Assumptions to check

**Applications**:
- Intervention studies with multiple assessments
- Individual differences moderating within-person effects

**Notebook**: [`mixed_design_template.ipynb`](mixed_design_template.ipynb)

### 4. Longitudinal Designs

**Description**: Repeated measurements over extended time periods

**Time Scales**:
- Short-term: Days to weeks
- Medium-term: Weeks to months
- Long-term: Months to years

**Advantages**:
- Track development and change
- Establish temporal precedence
- Individual trajectories
- Test lasting effects

**Disadvantages**:
- Attrition/dropout
- Time and cost intensive
- Practice effects
- History effects (external events)

**Applications**:
- Long-term well-being effects
- Creative skill development
- Sustained intervention effects

**Considerations**:
- Retention strategies
- Missing data handling
- Appropriate time lags
- Developmental changes

**Notebook**: [`longitudinal_template.ipynb`](longitudinal_template.ipynb)

### 5. Single-Case Experimental Designs (N-of-1)

**Description**: Intensive within-person studies

**Phases**:
- A: Baseline (no intervention)
- B: Intervention
- Can include: ABA, ABAB, multiple baselines

**Advantages**:
- Personalized evidence
- Clinical applications
- High internal validity
- Feasible when N is limited

**Disadvantages**:
- Generalization unclear
- Time-intensive
- Requires stability in baseline
- May not suit all research questions

**Applications**:
- Individual intervention testing
- Therapeutic case studies
- Personalized brain-music mapping

**Notebook**: [`single_case_template.ipynb`](single_case_template.ipynb)

## Sample Size and Power Analysis

### Power Analysis Basics

**Key Parameters**:
- **α (alpha)**: Type I error rate (typically 0.05)
- **β (beta)**: Type II error rate (typically 0.20)
- **Power**: 1 - β (typically 0.80 or 80%)
- **Effect size**: Magnitude of difference (Cohen's d, r, etc.)

**Required Information**:
- Expected effect size (from literature or pilot data)
- Desired power level
- Significance level
- Design type (within, between, etc.)

### Effect Size Guidelines (Cohen, 1988)

**Cohen's d** (mean differences):
- Small: d = 0.2
- Medium: d = 0.5
- Large: d = 0.8

**Correlation (r)**:
- Small: r = 0.1
- Medium: r = 0.3
- Large: r = 0.5

**Partial η²** (ANOVA):
- Small: η² = 0.01
- Medium: η² = 0.06
- Large: η² = 0.14

### Sample Size Calculations

```python
from scipy import stats
import numpy as np

def power_analysis_ttest(effect_size, alpha=0.05, power=0.80):
    \"\"\"
    Calculate required sample size for t-test
    
    effect_size: Cohen's d
    alpha: significance level
    power: desired statistical power
    \"\"\"
    # This is a simplified approximation
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    
    n = 2 * ((z_alpha + z_beta) / effect_size)**2
    return int(np.ceil(n))

# Example: Medium effect size
n_required = power_analysis_ttest(effect_size=0.5)
print(f\"Required N per group: {n_required}\")
```

**Notebook**: [`power_analysis.ipynb`](power_analysis.ipynb)

## Counterbalancing

### Order Counterbalancing

**Complete Counterbalancing**: All possible orders
- 2 conditions: 2 orders (AB, BA)
- 3 conditions: 6 orders (ABC, ACB, BAC, BCA, CAB, CBA)
- 4 conditions: 24 orders (grows factorially!)

**Latin Square**: Each condition appears in each position once
- Efficient for many conditions
- Incomplete counterbalancing
- Good compromise

**Random Order**: Each participant gets random order
- Simplest approach
- Works with enough participants
- Doesn't guarantee balance

### Example Implementation

```python
import itertools
import random

def generate_counterbalanced_orders(conditions, method='complete'):
    \"\"\"Generate counterbalanced condition orders\"\"\"
    if method == 'complete':
        # All possible permutations
        orders = list(itertools.permutations(conditions))
    elif method == 'latin_square':
        # Latin square (simplified)
        n = len(conditions)
        orders = []
        for i in range(n):
            order = [conditions[(i + j) % n] for j in range(n)]
            orders.append(tuple(order))
    elif method == 'random':
        # Just provide one random order (would generate per participant)
        order = list(conditions)
        random.shuffle(order)
        orders = [tuple(order)]
    
    return orders
```

## Randomization

### Random Assignment

**Simple Randomization**: Flip coin for each participant
- Easy but may result in unequal groups
- Fine for large samples

**Block Randomization**: Randomize within blocks
- Ensures equal/near-equal group sizes
- Better for small to moderate samples

**Stratified Randomization**: Balance on key variables
- Match groups on demographics, baseline scores
- Reduces confounding

### Example Implementation

```python
import random

def block_randomize(n_participants, block_size=4, conditions=['A', 'B']):
    \"\"\"
    Block randomization for equal group assignment
    \"\"\"
    n_blocks = n_participants // block_size
    assignments = []
    
    for _ in range(n_blocks):
        block = conditions * (block_size // len(conditions))
        random.shuffle(block)
        assignments.extend(block)
    
    # Handle remaining participants
    remaining = n_participants % block_size
    if remaining:
        extra = conditions * (remaining // len(conditions) + 1)
        random.shuffle(extra)
        assignments.extend(extra[:remaining])
    
    return assignments
```

## Blinding

### Types of Blinding

**Single-blind**: Participants don't know condition
- Reduces placebo effects
- Reduces demand characteristics
- Not always possible in music studies

**Double-blind**: Neither participants nor experimenter knows
- Gold standard when feasible
- Reduces experimenter bias
- Difficult with interactive systems

**Triple-blind**: Data analysts also blinded
- Prevents analysis bias
- Possible with coded data

### Implementing Blinding

- Use automated systems when possible
- Code conditions for experimenters
- Use confederates for assessment
- Separate data collection from analysis

## Control Conditions

### Types of Controls

**No-treatment control**: No intervention
- Establishes intervention effect
- But doesn't control for attention/expectation

**Placebo control**: Inactive intervention
- Controls for non-specific effects
- Important for psychological interventions

**Active control**: Different active intervention
- Tests specificity of intervention
- Controls for time, attention, engagement

**Waitlist control**: Delayed intervention
- Ethical way to include control
- All participants eventually receive intervention

### Choosing Controls

Consider what you want to control for:
- Passage of time
- Attention from experimenter
- Expectation of benefit
- Practice effects
- Technological interaction

## Blinding Checks and Manipulation Checks

### Manipulation Checks

**Purpose**: Verify manipulation worked as intended

**Examples**:
- Did agency manipulation affect perceived control?
- Did emotional music induce intended emotion?
- Did participants notice the feedback delay?

**Implementation**:
```python
def check_manipulation(perceived, intended):
    \"\"\"
    Check if manipulation was perceived as intended
    \"\"\"
    # Compare perceived to intended condition
    accuracy = (perceived == intended).mean()
    print(f\"Manipulation check accuracy: {accuracy:.2%}\")
    
    # Statistical test
    from scipy.stats import chi2_contingency
    contingency = pd.crosstab(perceived, intended)
    chi2, p, dof, expected = chi2_contingency(contingency)
    print(f\"χ²({dof}) = {chi2:.2f}, p = {p:.4f}\")
```

### Blinding Checks

**Purpose**: Verify participants couldn't guess condition

**Assessment**: Ask participants to guess their condition

**Analysis**: If guessing is at chance, blinding worked

## Data Collection Planning

### Timeline Planning

**Pre-session** (1-2 weeks before):
- Screening questionnaires
- Informed consent
- Baseline measures (if needed)

**Session** (1-3 hours):
- Setup and calibration (15-30 min)
- Instructions and practice (10-15 min)
- Baseline measures (10-15 min)
- Main task/intervention (30-90 min)
- Post measures (10-20 min)
- Debriefing (10-15 min)

**Follow-up** (optional):
- 1 week, 1 month, 3 months
- Assess lasting effects
- Gather feedback

### Pilot Testing

**Goals**:
- Test procedures
- Estimate effect sizes
- Identify problems
- Refine measures
- Check timing

**Sample**: 5-10 participants

**Iteration**: Modify and retest

## Common Pitfalls

❌ **Too many conditions**: Complexity without sufficient power
❌ **Inadequate sample size**: Underpowered studies
❌ **No counterbalancing**: Confounding of order with condition
❌ **Unclear hypotheses**: Can't design appropriate test
❌ **No pilot data**: Surprises during main study
❌ **Ignoring individual differences**: Large unexplained variance
❌ **No manipulation checks**: Don't know if manipulation worked
❌ **Inappropriate controls**: Can't isolate mechanism

## Best Practices

✅ Pre-register hypotheses and analysis plan
✅ Power analysis before data collection
✅ Pilot test procedures thoroughly
✅ Use validated measures when available
✅ Include manipulation checks
✅ Counterbalance order effects
✅ Use appropriate controls
✅ Plan for missing data
✅ Document all procedures
✅ Share materials openly

## Resources

### Statistical Software
- R: Free, powerful, large community
- Python (statsmodels, pingouin): Flexible, integrates with analysis
- JASP/jamovi: User-friendly GUI, open source
- G*Power: Free power analysis tool

### Online Tools
- **OSF**: Pre-registration, materials sharing
- **AsPredicted**: Simple pre-registration
- **Power calculators**: Various online tools

### References

**Experimental Design**:
- Maxwell, S. E., Delaney, H. D., & Kelley, K. (2017). Designing experiments and analyzing data: A model comparison perspective (3rd ed.). Routledge.
- Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002). Experimental and quasi-experimental designs for generalized causal inference. Houghton Mifflin.

**Power Analysis**:
- Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2nd ed.). Routledge.
- Faul, F., Erdfelder, E., Lang, A. G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program. Behavior Research Methods, 39(2), 175-191.

**Single-Case Designs**:
- Kratochwill, T. R., et al. (2013). Single-case intervention research design standards. Remedial and Special Education, 34(1), 26-38.

## Contributing

When adding new design templates:
1. Provide clear description and use cases
2. Include power analysis guidance
3. Discuss assumptions and limitations
4. Provide example code
5. Reference validation studies

## Contact

For questions about study design or statistical analysis, please open an issue.
