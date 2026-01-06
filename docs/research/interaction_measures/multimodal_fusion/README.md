# Multimodal Data Fusion

Integrating questionnaires, behavioral tasks, and brain measures for comprehensive assessment.

## Overview

Multimodal data fusion combines information from multiple sources (self-report, behavior, neural data) to provide richer, more reliable insights into psychological states and processes.

## Why Multimodal?

### Complementary Information

**Self-report**:
- Direct access to subjective experience
- Quick and practical
- But subject to bias, limited awareness

**Behavioral**:
- Objective performance measures
- Less influenced by self-presentation
- But indirect inference about internal states

**Neural**:
- Direct measure of brain activity
- Not subject to conscious control
- But requires inference about psychological meaning

### Triangulation

Using multiple methods to:
- **Converge**: Multiple measures pointing to same conclusion
- **Diverge**: Different measures revealing different aspects
- **Validate**: Cross-check findings across modalities

### Enhanced Prediction

Combining modalities often provides better prediction than any single source:
- Capture complementary variance
- Reduce measurement error
- Model complex relationships

## Fusion Approaches

### 1. Simple Concatenation

**Method**: Combine features from all modalities into one vector

**Advantages**:
- Simple to implement
- No assumptions about relationships
- Works with standard ML algorithms

**Disadvantages**:
- Ignores modality structure
- May give equal weight to unequal information
- Can suffer from curse of dimensionality

```python
import numpy as np

def concatenate_features(questionnaire_data, behavioral_data, neural_data):
    \"\"\"Simple feature concatenation\"\"\"
    # Normalize each modality
    q_norm = (questionnaire_data - questionnaire_data.mean()) / questionnaire_data.std()
    b_norm = (behavioral_data - behavioral_data.mean()) / behavioral_data.std()
    n_norm = (neural_data - neural_data.mean()) / neural_data.std()
    
    # Concatenate
    combined = np.hstack([q_norm, b_norm, n_norm])
    return combined
```

**Notebook**: [`concatenation_fusion.ipynb`](concatenation_fusion.ipynb)

### 2. Weighted Combination

**Method**: Combine modalities with learned or fixed weights

**Advantages**:
- Can emphasize more reliable modalities
- Flexible weighting schemes
- Easy to interpret

**Disadvantages**:
- Requires choosing/learning weights
- Linear combination may be too simple

```python
from sklearn.linear_model import Ridge

def weighted_fusion(modalities, target, alpha=1.0):
    \"\"\"
    Learn optimal weights for combining modalities
    
    modalities: list of numpy arrays, one per modality
    target: target variable to predict
    \"\"\"
    # Fit ridge regression to learn weights
    X = np.hstack(modalities)
    model = Ridge(alpha=alpha)
    model.fit(X, target)
    
    # Extract weights for each modality
    n_features = [m.shape[1] for m in modalities]
    weights = []
    start = 0
    for n in n_features:
        modality_weights = model.coef_[start:start+n]
        weights.append(modality_weights.mean())  # Average weight for modality
        start += n
    
    return weights, model
```

**Notebook**: [`weighted_fusion.ipynb`](weighted_fusion.ipynb)

### 3. Ensemble Methods

**Method**: Train separate models on each modality, combine predictions

**Types**:
- **Voting**: Majority vote or average prediction
- **Stacking**: Meta-model learns to combine base models
- **Boosting**: Sequential models correct previous errors

**Advantages**:
- Each modality modeled optimally
- Robust to modality-specific noise
- Often better performance

**Disadvantages**:
- More complex
- Requires more data
- Less interpretable

```python
from sklearn.ensemble import VotingClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def ensemble_fusion(modalities, target):
    \"\"\"
    Ensemble approach: separate classifier per modality
    \"\"\"
    # Create base classifiers
    classifiers = []
    for i, modality in enumerate(modalities):
        clf = ('modality_{}'.format(i), SVC(probability=True))
        classifiers.append(clf)
    
    # Voting ensemble
    ensemble = VotingClassifier(estimators=classifiers, voting='soft')
    
    # This is conceptual - in practice, need to handle modalities separately
    # then combine at decision level
    return ensemble
```

**Notebook**: [`ensemble_fusion.ipynb`](ensemble_fusion.ipynb)

### 4. Multi-View Learning

**Method**: Explicitly model relationships between modalities

**Approaches**:
- **Canonical Correlation Analysis (CCA)**: Find maximally correlated projections
- **Multi-view dimensionality reduction**: Shared latent space
- **Multi-view deep learning**: Neural networks with modality-specific pathways

**Advantages**:
- Models inter-modality relationships
- Can handle missing modalities
- Discovers shared representations

**Disadvantages**:
- More complex algorithms
- Requires sufficient data
- Hyperparameter tuning

```python
from sklearn.cross_decomposition import CCA

def cca_fusion(modality1, modality2, n_components=5):
    \"\"\"
    Canonical Correlation Analysis for two modalities
    \"\"\"
    cca = CCA(n_components=n_components)
    cca.fit(modality1, modality2)
    
    # Transform both modalities to shared space
    m1_transformed, m2_transformed = cca.transform(modality1, modality2)
    
    return m1_transformed, m2_transformed, cca
```

**Notebook**: [`multiview_learning.ipynb`](multiview_learning.ipynb)

### 5. Hierarchical Fusion

**Method**: Combine modalities at multiple levels

**Example**:
1. **Early fusion**: Combine raw features from all modalities
2. **Intermediate fusion**: Combine learned representations
3. **Late fusion**: Combine final predictions

**Advantages**:
- Captures information at multiple scales
- Flexible architecture
- Can combine strengths of different approaches

**Notebook**: [`hierarchical_fusion.ipynb`](hierarchical_fusion.ipynb)

## Temporal Alignment

### Synchronization Challenges

Different modalities have different temporal properties:
- **Self-report**: Discrete time points (pre/post session)
- **Behavioral**: Trial-by-trial or continuous
- **EEG**: Millisecond resolution
- **fNIRS**: ~1 Hz sampling
- **fMRI**: 0.5-2 Hz sampling

### Alignment Strategies

**Time-locking**:
- Align to common events (stimulus onset, response)
- Use event markers in all recordings

**Resampling**:
- Downsample high-resolution data
- Upsample low-resolution data (with care)

**Windowing**:
- Aggregate over time windows
- Match temporal resolution across modalities

```python
import pandas as pd

def align_temporal_data(high_res_data, low_res_timestamps, window_sec=2):
    \"\"\"
    Align high temporal resolution data to lower resolution timestamps
    
    high_res_data: DataFrame with high sampling rate
    low_res_timestamps: Timestamps for low resolution modality
    window_sec: Window size for aggregation
    \"\"\"
    aligned_data = []
    
    for ts in low_res_timestamps:
        # Find data within window around timestamp
        window_start = ts - window_sec/2
        window_end = ts + window_sec/2
        
        # Extract and aggregate
        window_data = high_res_data[
            (high_res_data['timestamp'] >= window_start) &
            (high_res_data['timestamp'] <= window_end)
        ]
        
        # Compute summary statistics
        aligned_data.append({
            'timestamp': ts,
            'mean': window_data.values.mean(),
            'std': window_data.values.std(),
            'max': window_data.values.max()
        })
    
    return pd.DataFrame(aligned_data)
```

**Notebook**: [`temporal_alignment.ipynb`](temporal_alignment.ipynb)

## Feature-Level vs. Decision-Level Fusion

### Feature-Level Fusion

**When**: Combine features before model training

**Pros**:
- Model learns cross-modality interactions
- Single model, simpler pipeline

**Cons**:
- Assumes features are commensurable
- Sensitive to feature scaling

### Decision-Level Fusion

**When**: Train separate models, combine predictions

**Pros**:
- Each modality processed optimally
- Robust to missing modalities
- Interpretable (contribution of each modality)

**Cons**:
- May miss cross-modality interactions
- More complex pipeline

## Handling Missing Data

### Types of Missingness

**MCAR** (Missing Completely At Random): Missingness unrelated to any variables

**MAR** (Missing At Random): Missingness related to observed variables

**MNAR** (Missing Not At Random): Missingness related to unobserved variables

### Missing Modality Strategies

**Complete case analysis**: Only use participants with all modalities
- Simple but loses data and power

**Imputation**: Fill in missing values
- Mean/median imputation
- Model-based imputation
- Multiple imputation

**Modality-specific models**: Adapt to available modalities
- Train models for all modality combinations
- Use only available modalities at test time

```python
def handle_missing_modalities(modalities, target):
    \"\"\"
    Strategy: Train models for all possible modality combinations
    \"\"\"
    from itertools import combinations
    
    models = {}
    n_modalities = len(modalities)
    
    # Train model for each possible combination
    for r in range(1, n_modalities + 1):
        for combo in combinations(range(n_modalities), r):
            # Create dataset with this combination
            X = np.hstack([modalities[i] for i in combo])
            
            # Train model
            model = RandomForestClassifier()
            model.fit(X[~np.isnan(X).any(axis=1)], target[~np.isnan(X).any(axis=1)])
            
            models[combo] = model
    
    return models
```

## Validation Strategies

### Cross-Validation

Standard k-fold cross-validation:
- Same splits across modalities
- Ensures fair comparison

```python
from sklearn.model_selection import cross_val_score

def cross_validate_fusion(modalities, target, model, cv=5):
    \"\"\"Cross-validate multimodal model\"\"\"
    X = np.hstack(modalities)
    scores = cross_val_score(model, X, target, cv=cv)
    return scores.mean(), scores.std()
```

### Modality Ablation

Test contribution of each modality:
- Train with all modalities
- Train with all-but-one
- Compare performance

```python
def ablation_study(modalities, target):
    \"\"\"Test contribution of each modality\"\"\"
    results = {}
    
    # Full model
    X_full = np.hstack(modalities)
    model_full = RandomForestClassifier()
    score_full = cross_val_score(model_full, X_full, target, cv=5).mean()
    results['all'] = score_full
    
    # Leave-one-out
    for i in range(len(modalities)):
        modalities_loo = [m for j, m in enumerate(modalities) if j != i]
        X_loo = np.hstack(modalities_loo)
        model_loo = RandomForestClassifier()
        score_loo = cross_val_score(model_loo, X_loo, target, cv=5).mean()
        results[f'without_{i}'] = score_loo
    
    return results
```

**Notebook**: [`ablation_studies.ipynb`](ablation_studies.ipynb)

## Example Applications

### 1. Affect State Classification

**Modalities**:
- Self-report: PANAS scores
- Behavioral: Facial expressions, voice features
- Neural: EEG frontal asymmetry, heart rate variability

**Fusion**: Ensemble of modality-specific SVMs

**Outcome**: Classify emotional state (positive, negative, neutral)

### 2. Flow State Detection

**Modalities**:
- Self-report: Flow State Scale
- Behavioral: Performance metrics, engagement time
- Neural: EEG alpha/theta, fNIRS prefrontal activation

**Fusion**: Deep learning with modality-specific encoders

**Outcome**: Real-time flow detection

### 3. Agency Quantification

**Modalities**:
- Self-report: Agency questionnaire
- Behavioral: Intentional binding, confidence ratings
- Neural: ERP (error-related negativity), frontal theta

**Fusion**: CCA followed by regression

**Outcome**: Continuous agency score

### 4. Creative Output Quality

**Modalities**:
- Self-report: Creativity self-assessment
- Behavioral: Divergent thinking scores, expert ratings
- Neural: Default mode network connectivity

**Fusion**: Stacked ensemble

**Outcome**: Predict creative quality

**Notebook**: [`example_applications.ipynb`](example_applications.ipynb)

## Interpretation and Visualization

### Feature Importance

```python
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

def plot_feature_importance(model, feature_names, modality_labels):
    \"\"\"Visualize feature importance by modality\"\"\"
    importances = model.feature_importances_
    
    # Group by modality
    modality_importance = []
    start = 0
    for label, n_features in zip(modality_labels, feature_counts):
        modality_importance.append(importances[start:start+n_features].sum())
        start += n_features
    
    # Plot
    plt.bar(modality_labels, modality_importance)
    plt.xlabel('Modality')
    plt.ylabel('Importance')
    plt.title('Feature Importance by Modality')
    plt.show()
```

### Fusion Weights Visualization

```python
def visualize_fusion_weights(weights, modality_names):
    \"\"\"Visualize learned fusion weights\"\"\"
    plt.figure(figsize=(8, 5))
    plt.bar(modality_names, weights)
    plt.xlabel('Modality')
    plt.ylabel('Weight')
    plt.title('Fusion Weights')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.show()
```

## Best Practices

✅ **Normalize features** within each modality before fusion

✅ **Use cross-validation** to prevent overfitting

✅ **Test individual modalities** before fusion

✅ **Perform ablation studies** to understand contributions

✅ **Align temporal resolution** appropriately

✅ **Handle missing data** thoughtfully

✅ **Visualize** fusion results and contributions

✅ **Validate** on independent test set

❌ Don't assume all modalities are equally informative

❌ Don't ignore temporal relationships

❌ Don't forget to check assumptions

## Resources

### Software

**Python**:
- scikit-learn: General ML, fusion basics
- TensorFlow/PyTorch: Deep learning fusion
- mvlearn: Multi-view learning library

**R**:
- mixOmics: Multi-omics integration
- PMA: Penalized multivariate analysis

### References

**Multimodal Fusion**:
- Baltrušaitis, T., Ahuja, C., & Morency, L. P. (2018). Multimodal machine learning: A survey and taxonomy. IEEE Transactions on Pattern Analysis and Machine Intelligence, 41(2), 423-443.

**Multi-View Learning**:
- Sun, S. (2013). A survey of multi-view machine learning. Neural Computing and Applications, 23(7-8), 2031-2038.

**Brain-Behavior Integration**:
- Sui, J., et al. (2012). A review of multivariate methods for multimodal fusion of brain imaging data. Journal of Neuroscience Methods, 204(1), 68-81.

## Contributing

When adding fusion methods:
1. Explain theoretical motivation
2. Provide implementation code
3. Include validation strategy
4. Discuss when to use this approach
5. Reference relevant papers

## Contact

For questions about multimodal fusion, please open an issue.
