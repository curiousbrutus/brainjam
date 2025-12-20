# Notebooks for Brain-Mediated Music Research

This directory contains Jupyter notebooks for experiments, analyses, and prototypes.

## Notebook Organization

### 1. Model Loading and Exploration
- `01_load_pretrained_models.ipynb` - Load and test pretrained audio/music models
- `02_explore_latent_spaces.ipynb` - Visualize and navigate model latent spaces

### 2. Neural Signal Processing
- `03_simulated_fmri_features.ipynb` - Simulate and extract fMRI features
- `04_simulated_fnirs_features.ipynb` - Simulate and extract fNIRS features
- `05_simulated_eeg_features.ipynb` - Simulate and extract EEG features

### 3. Brain-Music Mapping
- `06_latent_space_mapping.ipynb` - Map neural features to music latent spaces
- `07_feature_correlation_analysis.ipynb` - Analyze brain-music correlations

### 4. Prototypes and Demos
- `08_real_time_synthesis_demo.ipynb` - Real-time audio synthesis demo
- `09_brain_to_sound_pipeline.ipynb` - End-to-end brain→sound pipeline

## Usage

### Setup
```bash
# Install Jupyter
pip install jupyter ipywidgets

# Launch Jupyter
jupyter notebook
```

### Running Notebooks
1. Start with model loading notebooks to download pretrained weights
2. Explore neural signal simulation notebooks
3. Experiment with mapping strategies
4. Test real-time prototypes

### Data Requirements
- Notebooks use simulated data by default
- For real neural data, update data paths in notebooks
- See individual notebook headers for specific requirements

## Best Practices

- **Run in order**: Earlier notebooks set up models/data for later ones
- **GPU recommended**: For faster model inference
- **Save outputs**: Notebooks save intermediate results to `outputs/`
- **Version control**: Don't commit large model files or data

## Contributing

When adding new notebooks:
- Use clear, descriptive names
- Include docstrings and markdown explanations
- Test with fresh kernel before committing
- Update this README with new notebook descriptions
