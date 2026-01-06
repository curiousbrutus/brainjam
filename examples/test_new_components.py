"""
Test and demonstration script for new sound engines and components.

Tests:
1. DDSP Piano Synth
2. DDSP Guitar Synth
3. Beat Generator
4. Agent Memory (GRU)
5. EEG Mapper
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from performance_system.sound_engines import DDSPPianoSynth, DDSPGuitarSynth, BeatGenerator
from performance_system.agents import AgentMemory
from performance_system.mapping_models import EEGMapper

print("=" * 70)
print("TESTING NEW COMPONENTS")
print("=" * 70)

# Test 1: Piano Synth
print("\n1. Testing DDSP Piano Synth...")
piano = DDSPPianoSynth(sample_rate=44100)
audio = piano.generate(duration=1.0, control_params={
    'midi_note': 60,  # Middle C
    'velocity': 0.8,
    'brightness': 0.7,
    'resonance': 0.3
})
print(f"   ✓ Generated {len(audio)} samples ({len(audio)/44100:.2f}s)")
print(f"   ✓ Audio range: [{np.min(audio):.3f}, {np.max(audio):.3f}]")

# Test 2: Guitar Synth
print("\n2. Testing DDSP Guitar Synth...")
guitar = DDSPGuitarSynth(sample_rate=44100)
audio = guitar.generate(duration=1.0, control_params={
    'midi_note': 55,  # G
    'velocity': 0.7,
    'tone': 0.6,
    'pick_position': 0.5
})
print(f"   ✓ Generated {len(audio)} samples ({len(audio)/44100:.2f}s)")
print(f"   ✓ Audio range: [{np.min(audio):.3f}, {np.max(audio):.3f}]")

# Test polyphonic chord
chord_notes = [55, 59, 62]  # G, B, D (G major chord)
chord_audio = guitar.generate_chord(chord_notes, duration=2.0, velocity=0.7, strum_time=0.02)
print(f"   ✓ Generated chord with {len(chord_notes)} notes")

# Test 3: Beat Generator
print("\n3. Testing Beat Generator...")
beats = BeatGenerator(sample_rate=44100)
audio = beats.generate(duration=4.0, control_params={
    'tempo': 120,
    'pattern_style': 'four_on_floor',
    'intensity': 0.8,
    'fill_prob': 0.2
})
print(f"   ✓ Generated {len(audio)} samples ({len(audio)/44100:.2f}s)")
print(f"   ✓ Available patterns: {list(beats.PATTERNS.keys())}")

# Test 4: Agent Memory
print("\n4. Testing Agent Memory (GRU)...")
memory = AgentMemory(context_length=10)
print(f"   ✓ Memory initialized with context length {memory.context_length}")
print(f"   ✓ Model available: {memory.model_available}")

# Add some context
for i in range(5):
    memory.add_context({
        'control_1': 0.5 + 0.1 * np.sin(i),
        'control_2': 0.6,
        'control_3': 0.4,
        'control_4': 0.5
    })

prediction = memory.predict_response()
if prediction:
    print(f"   ✓ Memory prediction: {prediction}")
else:
    print(f"   ℹ No prediction (model not trained)")

state = memory.get_memory_state()
print(f"   ✓ Memory state: {state}")

# Test 5: EEG Mapper
print("\n5. Testing EEG Mapper...")
eeg_mapper = EEGMapper(n_channels=8, sample_rate=250.0, window_size=0.5)
print(f"   ✓ EEG Mapper initialized")
print(f"   ✓ Model available: {eeg_mapper.model_available}")

# Generate synthetic EEG data
n_samples = int(0.5 * 250)  # 0.5 seconds at 250 Hz
eeg_data = np.random.randn(8, n_samples) * 10  # 8 channels, random EEG-like data

# Map to controls
controls = eeg_mapper.map_eeg_to_controls(eeg_data)
print(f"   ✓ EEG mapped to controls: {controls}")

info = eeg_mapper.get_mapper_info()
print(f"   ✓ Mapper info: {info}")

# Integration test: Use all components together
print("\n" + "=" * 70)
print("INTEGRATION TEST")
print("=" * 70)

print("\nGenerating musical sequence with all components...")

# Use EEG to generate controls
controls = eeg_mapper.map_eeg_to_controls(eeg_data)
print(f"1. EEG controls: {controls}")

# Add to memory
memory.add_context(controls)

# Generate piano note
piano_audio = piano.generate(duration=1.0, control_params=controls)
print(f"2. Piano: {len(piano_audio)} samples")

# Generate guitar note
guitar_audio = guitar.generate(duration=1.0, control_params=controls)
print(f"3. Guitar: {len(guitar_audio)} samples")

# Generate beat
beat_audio = beats.generate(duration=1.0, control_params=controls)
print(f"4. Beats: {len(beat_audio)} samples")

# Mix all together
mixed_audio = (0.4 * piano_audio + 0.4 * guitar_audio + 0.2 * beat_audio)
print(f"5. Mixed: {len(mixed_audio)} samples")

print("\n" + "=" * 70)
print("✓ ALL TESTS PASSED")
print("=" * 70)

print("\nComponent Summary:")
print("  • DDSPPianoSynth: MIDI-controllable piano with realistic envelope")
print("  • DDSPGuitarSynth: Polyphonic guitar with pluck/strum articulations")
print("  • BeatGenerator: Rule-based rhythm patterns (no ML needed)")
print("  • AgentMemory: GRU-based musical dialogue learning")
print("  • EEGMapper: EEGNet-based EEG-to-control mapping")
print("\nAll components are ready for integration!")
