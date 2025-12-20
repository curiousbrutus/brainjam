# Pretrained Audio and Music Models for Transfer Learning

This directory documents pretrained models suitable for brain-mediated music generation research. These models provide learned representations of music and audio that can be fine-tuned or conditioned on neural signals.

## Available Model Categories

1. **Text-to-Music Models** - Generate music from text descriptions
2. **Audio Autoencoders** - Learn compressed latent representations
3. **Music Understanding Models** - Extract semantic and structural features
4. **Audio Synthesis Models** - Generate high-quality audio waveforms
5. **Symbolic Music Models** - Work with MIDI and symbolic representations

## Model Selection Criteria

For brain-mediated music applications, prioritize models with:
- **Interpretable latent spaces** - For meaningful brain-to-music mapping
- **Real-time capability** - Low latency for interactive systems
- **Controllable generation** - Parameters for conditioning on neural features
- **Transfer learning support** - Pretrained weights available
- **Open source** - Accessible for research use

---

## 1. Text-to-Music Models

### MusicGen (Meta AudioCraft)
- **Repository**: https://github.com/facebookresearch/audiocraft
- **Paper**: https://arxiv.org/abs/2306.05284
- **Modality**: Text → Audio
- **Architecture**: Transformer-based with audio tokens
- **Pretrained Models**: 
  - `small` (300M params)
  - `medium` (1.5B params)
  - `large` (3.3B params)
  - `melody` (1.5B params, with melody conditioning)
- **Advantages**: 
  - State-of-the-art quality
  - Multiple conditioning modalities
  - Well-documented API
- **Use Case**: Condition on text descriptions derived from brain states
- **Installation**: `pip install audiocraft`

```python
# Quick start
from audiocraft.models import MusicGen
model = MusicGen.get_pretrained('medium')
```

### MusicLM (Google Research)
- **Paper**: https://arxiv.org/abs/2301.11325
- **Modality**: Text → Audio
- **Architecture**: Hierarchical autoregressive model
- **Status**: Research preview, limited public access
- **Advantages**: Excellent long-form coherence
- **Note**: May require custom implementation or API access

### Riffusion
- **Repository**: https://github.com/riffusion/riffusion
- **Website**: https://www.riffusion.com
- **Modality**: Text → Spectrogram → Audio
- **Architecture**: Stable Diffusion fine-tuned on spectrograms
- **Pretrained Model**: Available on HuggingFace
- **Advantages**: 
  - Real-time generation
  - Smooth interpolation in latent space
  - Easy integration with diffusion tools
- **Use Case**: Interpolate between brain-state-defined musical styles
- **Installation**: `pip install riffusion`

---

## 2. Audio Autoencoders

### EnCodec (Meta)
- **Repository**: https://github.com/facebookresearch/encodec
- **Paper**: https://arxiv.org/abs/2210.13438
- **Modality**: Audio → Tokens → Audio
- **Architecture**: Convolutional autoencoder with residual vector quantization
- **Pretrained Models**: 24kHz music and 48kHz audiogen
- **Advantages**:
  - High compression (48kHz → 1.5 kbps)
  - Excellent reconstruction quality
  - Enables discrete modeling
- **Use Case**: Learn compact representations for neural conditioning
- **Installation**: `pip install encodec`

### DDSP (Google Magenta)
- **Repository**: https://github.com/magenta/ddsp
- **Paper**: https://arxiv.org/abs/2001.04643
- **Modality**: Audio features → Audio
- **Architecture**: Differentiable DSP with neural networks
- **Pretrained Models**: Violin, flute, trumpet, singing voice
- **Advantages**:
  - Interpretable controls (pitch, loudness, timbre)
  - High-quality synthesis
  - Physically grounded parameters
- **Use Case**: Map neural features to interpretable audio parameters
- **Installation**: `pip install ddsp`

### Jukebox (OpenAI)
- **Repository**: https://github.com/openai/jukebox
- **Paper**: https://arxiv.org/abs/2005.00341
- **Modality**: Tokens → Audio (VQ-VAE)
- **Architecture**: Hierarchical VQ-VAE with transformers
- **Pretrained Models**: 5B model trained on 1.2M songs
- **Advantages**: Rich latent space, includes vocals
- **Challenges**: Large model, slow generation
- **Use Case**: Explore learned music representations

---

## 3. Music Understanding Models

### MERT (Music Understanding)
- **Repository**: https://github.com/yizhilll/MERT
- **Paper**: https://arxiv.org/abs/2306.00107
- **Modality**: Audio → Embeddings
- **Architecture**: Transformer-based (like BERT for music)
- **Pretrained Models**: 95M and 330M parameters
- **Advantages**: 
  - Strong music understanding
  - Transfer learning for downstream tasks
  - Acoustic and semantic features
- **Use Case**: Extract music features for matching brain states
- **HuggingFace**: `m-a-p/MERT-v1-330M`

### CLAP (Contrastive Language-Audio Pretraining)
- **Repository**: https://github.com/LAION-AI/CLAP
- **Paper**: https://arxiv.org/abs/2211.06687
- **Modality**: Audio ↔ Text (joint embedding)
- **Architecture**: Dual-encoder (CLIP for audio)
- **Pretrained Models**: Various sizes on AudioSet and music
- **Advantages**:
  - Zero-shot classification
  - Audio-text retrieval
  - Semantic search
- **Use Case**: Bridge neural states to semantic music concepts
- **HuggingFace**: `laion/clap-htsat-fused`

### MULE (Music Understanding)
- **Repository**: https://github.com/facebookresearch/audiocraft
- **Architecture**: Contrastive learning for music-text alignment
- **Use Case**: Part of AudioCraft ecosystem
- **Advantages**: Integrated with generation models

---

## 4. Audio Synthesis Models

### AudioLDM
- **Repository**: https://github.com/haoheliu/AudioLDM
- **Paper**: https://arxiv.org/abs/2301.12503
- **Modality**: Text/Audio → Audio
- **Architecture**: Latent diffusion for audio
- **Pretrained Models**: AudioLDM-S, M, L
- **Advantages**: Fast diffusion-based generation
- **Use Case**: Condition audio generation on neural features

### WaveNet (DeepMind)
- **Paper**: https://arxiv.org/abs/1609.03499
- **Modality**: Conditional → Audio
- **Architecture**: Dilated causal convolutions
- **Status**: Foundational; many derivative works
- **Use Case**: Historical reference; modern alternatives preferred

---

## 5. Symbolic Music Models

### Music Transformer
- **Repository**: https://github.com/jason9693/MusicTransformer-pytorch
- **Paper**: https://arxiv.org/abs/1809.04281
- **Modality**: MIDI → MIDI
- **Architecture**: Transformer with relative attention
- **Use Case**: Generate symbolic music with long-term structure

### MusicVAE (Magenta)
- **Repository**: https://github.com/magenta/magenta/tree/main/magenta/models/music_vae
- **Paper**: https://arxiv.org/abs/1803.05428
- **Modality**: MIDI → Latent → MIDI
- **Architecture**: Hierarchical VAE
- **Pretrained Models**: Various (melody, drums, trio, etc.)
- **Advantages**: 
  - Smooth latent interpolation
  - Well-structured representations
  - Interactive demos available
- **Use Case**: Map brain states to musical sequences
- **Installation**: `pip install magenta`

### MuseNet (OpenAI)
- **Architecture**: Large-scale transformer for music
- **Status**: API-based access
- **Advantages**: Multi-instrument, style transfer
- **Note**: Limited for research use

---

## Model Comparison Table

| Model | Type | Real-time | Latent Space | Conditioning | License |
|-------|------|-----------|--------------|--------------|---------|
| MusicGen | Text-to-Music | ✓ | Discrete | Text, melody | Research |
| Riffusion | Diffusion | ✓✓ | Continuous | Text, image | MIT |
| DDSP | Synthesis | ✓✓✓ | Interpretable | Audio features | Apache 2.0 |
| MusicVAE | Symbolic | ✓✓✓ | Continuous | None | Apache 2.0 |
| CLAP | Embedding | ✓✓✓ | Joint | Text | MIT |
| MERT | Embedding | ✓✓ | Contextual | None | CC-BY-NC-SA 4.0 |

---

## Transfer Learning Strategies

### 1. Feature Extraction
Use pretrained models to extract music features:
```python
# Example: CLAP embeddings
import laion_clap
model = laion_clap.CLAP_Module(enable_fusion=True)
audio_embed = model.get_audio_embedding_from_data(audio)
```

### 2. Fine-tuning
Adapt pretrained models to brain-conditioned generation:
- Freeze early layers, train conditioning mechanism
- Use brain features as additional input
- Multi-task learning with reconstruction + generation

### 3. Latent Space Mapping
Learn mapping from brain features to model latent space:
```python
# Conceptual: Brain → MusicVAE latent
brain_features → [Neural Network] → musicvae_z → MIDI
```

### 4. Guided Generation
Use brain states to guide sampling/decoding:
- Temperature/top-k adjustment from arousal
- Style conditioning from mood
- Structural control from attention

---

## Hugging Face Model Hub

Search for models on https://huggingface.co/models:
- `task:text-to-audio`
- `task:audio-classification`
- `library:audiocraft`
- `library:diffusers` (for audio diffusion)

---

## Installation Notes

### Recommended Environment
```bash
# Create conda environment
conda create -n brainjam python=3.10
conda activate brainjam

# Install PyTorch (check CUDA version)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install audio libraries
pip install audiocraft transformers librosa soundfile

# Install Magenta for symbolic models
pip install magenta
```

### Storage Requirements
- Small models (~300M params): ~1-2 GB
- Medium models (~1.5B params): ~5-10 GB
- Large models (~3B+ params): ~15+ GB

Plan for ~50-100 GB storage for model collection.

---

## Best Practices

1. **Start Simple**: Begin with smaller models (MusicVAE, DDSP)
2. **Profile Performance**: Measure latency for real-time requirements
3. **Version Control**: Track model versions and checkpoints
4. **Documentation**: Record hyperparameters and training details
5. **Ethical Use**: Respect model licenses and training data sources

---

## Additional Resources

- **Magenta Blog**: https://magenta.tensorflow.org/
- **AudioCraft Documentation**: https://facebookresearch.github.io/audiocraft/
- **HuggingFace Audio Course**: https://huggingface.co/learn/audio-course/
- **Awesome Deep Learning Music**: https://github.com/ybayle/awesome-deep-learning-music
