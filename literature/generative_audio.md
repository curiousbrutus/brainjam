# Generative Audio and Music Models

## Large-Scale Audio Generation

### MusicLM: Generating Music from Text
**Agostinelli, A., et al. (2023)** - *MusicLM: Generating Music From Text*
- **Link**: https://arxiv.org/abs/2301.11325
- **Summary**: Hierarchical sequence-to-sequence model generating high-fidelity music from text descriptions. Uses AudioLM with MuLan for text conditioning.
- **Relevance**: State-of-the-art controllable music generation; potential for conditioning on neural features.
- **Key Features**: 24kHz audio, 2+ minute coherent generations, multi-conditional control

### AudioLM: Language Modeling for Audio Generation
**Borsos, Z., et al. (2023)** - *AudioLM: a Language Modeling Approach to Audio Generation*
- **Link**: https://arxiv.org/abs/2209.03143
- **Summary**: Treats audio as language using discrete tokens, enabling long-form coherent audio generation.
- **Relevance**: Demonstrates feasibility of high-quality unconditional audio generation with structure.

### Riffusion: Stable Diffusion for Music
**Forsgren, S., & Martiros, H. (2022)** - *Riffusion - Stable diffusion for real-time music generation*
- **Link**: https://riffusion.com/about
- **Summary**: Fine-tunes Stable Diffusion on spectrograms for music generation; enables interpolation.
- **Relevance**: Real-time capable, supports smooth transitions between styles (useful for brain-state interpolation).

## Music Representation Learning

### Jukebox: Generative Model for Music
**Dhariwal, P., et al. (2020)** - *Jukebox: A Generative Model for Music*
- **Link**: https://arxiv.org/abs/2005.00341
- **Summary**: VQ-VAE architecture generating music with singing in raw audio, conditioned on genre/artist/lyrics.
- **Relevance**: Demonstrates rich latent spaces for music; transfer learning potential.

### MusPy: Toolkit for Symbolic Music
**Dong, H.-W., et al. (2020)** - *MusPy: A Toolkit for Symbolic Music Generation*
- **Link**: https://arxiv.org/abs/2008.01951
- **Summary**: Standardized toolkit for symbolic music data processing and generation.
- **Relevance**: Useful for intermediate symbolic representations before audio synthesis.

## Controllable Generation

### Music Transformer: Generating Long Sequences
**Huang, C.-Z. A., et al. (2018)** - *Music Transformer*
- **Link**: https://arxiv.org/abs/1809.04281
- **Summary**: Self-attention mechanism for generating coherent multi-track symbolic music with long-term structure.
- **Relevance**: Demonstrates importance of temporal coherence in music generation.

### MusicVAE: Latent Space for Musical Sequences
**Roberts, A., et al. (2018)** - *A Hierarchical Latent Vector Model for Learning Long-Term Structure in Music*
- **Link**: https://arxiv.org/abs/1803.05428
- **Summary**: VAE with hierarchical decoder enabling smooth interpolation in music space.
- **Relevance**: Structured latent space ideal for mapping brain states to musical outputs.

## Neural Audio Synthesis

### DDSP: Differentiable Digital Signal Processing
**Engel, J., et al. (2020)** - *DDSP: Differentiable Digital Signal Processing*
- **Link**: https://arxiv.org/abs/2001.04643
- **Summary**: Combines neural networks with DSP for controllable, high-quality audio synthesis.
- **Relevance**: Interpretable controls (pitch, loudness, timbre) suitable for brain-conditioned synthesis.

### WaveNet and Variants
**van den Oord, A., et al. (2016)** - *WaveNet: A Generative Model for Raw Audio*
- **Link**: https://arxiv.org/abs/1609.03499
- **Summary**: Deep generative model for raw audio waveforms using dilated convolutions.
- **Relevance**: Foundation for many modern audio generation systems.

## Music Understanding

### Music Tagging and Representation
**Won, M., et al. (2021)** - *Emotion Embeddings: Learning Representations from Music*
- **Link**: https://arxiv.org/abs/2104.00154
- **Summary**: Self-supervised learning of music representations capturing emotional and semantic content.
- **Relevance**: Provides embeddings for matching brain states to musical characteristics.

### CLAP: Contrastive Language-Audio Pretraining
**Wu, Y., et al. (2023)** - *Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation*
- **Link**: https://arxiv.org/abs/2211.06687
- **Summary**: CLIP-style model for audio-text alignment.
- **Relevance**: Enables semantic control and retrieval for audio generation.

## Real-Time and Interactive Systems

### Magenta Studio
**Magenta Team (2019)** - *Magenta Studio: Music and Art Generation with Machine Intelligence*
- **Link**: https://magenta.tensorflow.org/studio
- **Summary**: Suite of music plugins using ML models (Continue, Generate, Interpolate, Groove).
- **Relevance**: Practical examples of interactive ML-driven music creation tools.

### NSynth: Neural Audio Synthesis
**Engel, J., et al. (2017)** - *Neural Audio Synthesis of Musical Notes with WaveNet Autoencoders*
- **Link**: https://arxiv.org/abs/1704.01279
- **Summary**: Learns timbre representations enabling novel sound synthesis and morphing.
- **Relevance**: Demonstrates potential for creative sound design through latent space exploration.

## Transfer Learning Resources

### Pretrained Models Available
- **OpenAI Jukebox** - Pretrained on 1.2M songs
- **MusicGen (Meta)** - Text-to-music models
- **AudioCraft** - Suite of generative audio models
- **Riffusion** - Diffusion-based music generation
- **Magenta Models** - Various music generation architectures

### Model Hubs
- Hugging Face Audio Models
- Magenta Checkpoints
- GitHub repositories with pretrained weights

## Implementation Considerations

- **Latency**: Real-time requires <100ms; consider efficient architectures
- **Coherence**: Long-term structure challenging; hierarchical models help
- **Control**: Balance between expressiveness and constraint
- **Quality**: Trade-offs between fidelity, diversity, and controllability
