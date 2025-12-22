# Neural Decoding and Mind-Vis Literature

## Visual and Conceptual Decoding

### Mind-Vis: Seeing Beyond the Brain
**Tang, J., et al. (2023)** - *Mind-Vis: Conditional Diffusion Models for Decoding Visual Stimuli from fMRI*
- **Link**: https://mind-vis.github.io/
- **Summary**: Proposes using conditional diffusion models to reconstruct visual stimuli from fMRI signals. Uses contrastive learning to align brain representations with CLIP embeddings.
- **Relevance**: Demonstrates feasibility of decoding complex perceptual content from fMRI; techniques adaptable to music/audio perception.
- **Key Methods**: 
  - CLIP-based brain encoder
  - Latent diffusion models conditioned on fMRI
  - Subject-specific fine-tuning

### Reconstructing Perceived Images from Brain Activity
**Horikawa, T., & Kamitani, Y. (2017)** - *Generic decoding of seen and imagined objects using hierarchical visual features*
- **Link**: https://doi.org/10.1038/ncomms15037
- **Summary**: Pioneering work showing that both seen and imagined visual content can be decoded from fMRI using hierarchical CNNs.
- **Relevance**: Establishes that internal mental representations (imagination) are decodable, crucial for creativity research.

## Auditory Decoding

### Neural Decoding of Music from Brain Signals
**Di Liberto, G. M., et al. (2020)** - *Cortical encoding of melodic expectations in human temporal cortex*
- **Link**: https://doi.org/10.7554/eLife.51784
- **Summary**: Shows how predictive coding in auditory cortex encodes musical structure and expectations.
- **Relevance**: Understanding how brain represents musical expectations is key for generative music conditioning.

### Reconstructing Speech from fMRI
**Anumanchipalli, G. K., et al. (2019)** - *Speech synthesis from neural decoding of spoken sentences*
- **Link**: https://doi.org/10.1038/s41586-019-1119-1
- **Summary**: Demonstrates reconstruction of intelligible speech from brain activity during speaking.
- **Relevance**: Proof-of-concept that acoustic information can be decoded from neural signals.

## EEG-Based Decoding

### Deep Learning for EEG Decoding
**Schirrmeister, R. T., et al. (2017)** - *Deep learning with convolutional neural networks for EEG decoding and visualization*
- **Link**: https://doi.org/10.1002/hbm.23730
- **Summary**: Comprehensive evaluation of CNN architectures for EEG signal decoding.
- **Relevance**: Practical methods for real-time EEG feature extraction applicable to music interfaces.

### EEG Correlates of Musical Emotion
**Daly, I., et al. (2019)** - *Neural correlates of emotional responses to music: An EEG study*
- **Link**: https://doi.org/10.1016/j.neuroimage.2019.116214
- **Summary**: Maps EEG patterns associated with emotional responses to music across frequency bands.
- **Relevance**: Provides basis for emotion-aware brain-music interfaces.

## Cross-Modal Decoding

### Shared Representations Across Modalities
**Huth, A. G., et al. (2016)** - *Natural speech reveals the semantic maps that tile human cerebral cortex*
- **Link**: https://doi.org/10.1038/nature17637
- **Summary**: Creates semantic maps showing how concepts are organized across cortical surface.
- **Relevance**: Suggests that abstract creative concepts may have consistent neural representations.

## Challenges and Limitations

### Individual Differences in Neural Representations
**Finn, E. S., et al. (2015)** - *Functional connectome fingerprinting: identifying individuals using patterns of brain connectivity*
- **Link**: https://doi.org/10.1038/nn.4135
- **Summary**: Demonstrates high individual variability in brain connectivity patterns.
- **Relevance**: Highlights need for personalized models and calibration in brain decoding systems.

## Notes

- Most neural decoding work uses supervised learning with known stimuli
- Decoding internal states (imagination, creativity) remains challenging
- Temporal resolution trade-offs: fMRI (spatial) vs EEG (temporal)
- Real-time decoding requires careful optimization and dimensionality reduction
