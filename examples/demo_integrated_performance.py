"""
Demo: Integrated Performance with All New Components

Demonstrates all 5 new components working together:
1. EEG Mapper - Maps simulated EEG to control parameters
2. Agent Memory - Learns and predicts musical patterns
3. Piano Synth - Generates melodic content
4. Guitar Synth - Adds harmonic accompaniment
5. Beat Generator - Provides rhythmic foundation

This creates a complete AI-assisted performance system.
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False
    print("Note: soundfile not available, audio will not be saved to file")

from performance_system.sound_engines import DDSPPianoSynth, DDSPGuitarSynth, BeatGenerator
from performance_system.agents import HybridAdaptiveAgent, AgentMemory
from performance_system.mapping_models import EEGMapper
from performance_system.controllers import MockEEGController

print("=" * 80)
print("INTEGRATED PERFORMANCE DEMO")
print("All 5 New Components + Hybrid Adaptive Agent")
print("=" * 80)

# Initialize all components
print("\nInitializing components...")

# EEG source
eeg_controller = MockEEGController(fs=250)
print("  ✓ Mock EEG Controller")

# EEG Mapper
eeg_mapper = EEGMapper(n_channels=8, sample_rate=250.0, window_size=0.5)
print(f"  ✓ EEG Mapper (model available: {eeg_mapper.model_available})")

# Agent with memory
agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0)
memory = AgentMemory(context_length=10)
print(f"  ✓ Hybrid Adaptive Agent")
print(f"  ✓ Agent Memory (model available: {memory.model_available})")

# Sound engines
piano = DDSPPianoSynth(sample_rate=44100)
guitar = DDSPGuitarSynth(sample_rate=44100)
beats = BeatGenerator(sample_rate=44100)
print("  ✓ Piano Synth")
print("  ✓ Guitar Synth")
print("  ✓ Beat Generator")

# Performance parameters
duration = 20.0  # Total duration in seconds
chunk_duration = 0.5  # Process in 0.5s chunks
n_chunks = int(duration / chunk_duration)

print(f"\nGenerating {duration}s performance in {n_chunks} chunks...")
print("=" * 80)

# Storage for audio chunks
all_audio_chunks = []
chunk_info = []

# Generate performance
for i in range(n_chunks):
    # 1. Generate mock EEG data
    n_samples = int(0.5 * 250)
    eeg_data = np.random.randn(8, n_samples) * 10
    
    # 2. Map EEG to controls
    eeg_controls = eeg_mapper.map_eeg_to_controls(eeg_data)
    
    # 3. Pass through hybrid adaptive agent
    agent_response = agent.respond(eeg_controls)
    agent_state = agent.get_state()
    
    # 4. Add to memory and get prediction
    memory.add_context(eeg_controls)
    memory_prediction = memory.predict_response()
    
    # 5. Blend agent response with memory if available
    if memory_prediction:
        # Blend 80% agent, 20% memory
        final_controls = {
            'control_1': 0.8 * agent_response['note_density'] + 0.2 * memory_prediction['control_1'],
            'control_2': 0.8 * agent_response['harmonic_tension'] + 0.2 * memory_prediction['control_2'],
            'control_3': agent_response['note_density'],
            'control_4': agent_response['fill_probability']
        }
    else:
        final_controls = {
            'control_1': agent_response['note_density'],
            'control_2': agent_response['harmonic_tension'],
            'control_3': agent_response['note_density'],
            'control_4': agent_response['fill_probability']
        }
    
    # Map controls to musical parameters
    # Piano: melodic voice (higher register)
    piano_note = 60 + int(final_controls['control_1'] * 24)  # C4 to C6
    piano_params = {
        'midi_note': piano_note,
        'velocity': final_controls['control_2'],
        'brightness': final_controls['control_3'],
        'resonance': 0.3
    }
    
    # Guitar: harmonic accompaniment (lower register)
    guitar_note = 48 + int(final_controls['control_1'] * 12)  # C3 to C4
    guitar_params = {
        'midi_note': guitar_note,
        'velocity': final_controls['control_2'] * 0.8,
        'tone': final_controls['control_3'],
        'pick_position': 0.5
    }
    
    # Beats: rhythmic foundation
    tempo = agent_response['tempo_suggestion']
    beat_params = {
        'tempo': tempo,
        'pattern_style': 'four_on_floor' if agent_state['behavioral_state'] == 'active' else 'minimal',
        'intensity': final_controls['control_3'],
        'fill_prob': final_controls['control_4']
    }
    
    # 6. Generate audio for each component
    piano_audio = piano.generate(chunk_duration, piano_params)
    guitar_audio = guitar.generate(chunk_duration, guitar_params)
    beat_audio = beats.generate(chunk_duration, beat_params)
    
    # 7. Mix all components
    # Balance: 35% piano, 35% guitar, 30% beats
    chunk_audio = (
        0.35 * piano_audio +
        0.35 * guitar_audio +
        0.30 * beat_audio
    )
    
    # Normalize chunk
    if np.max(np.abs(chunk_audio)) > 0:
        chunk_audio = chunk_audio * 0.8 / np.max(np.abs(chunk_audio))
    
    all_audio_chunks.append(chunk_audio)
    
    # Store info
    chunk_info.append({
        'chunk': i,
        'state': agent_state['behavioral_state'],
        'tempo': tempo,
        'piano_note': piano_note,
        'guitar_note': guitar_note,
        'intensity': final_controls['control_3']
    })
    
    # Progress update every 10 chunks
    if (i + 1) % 10 == 0:
        progress = (i + 1) / n_chunks * 100
        print(f"  Progress: {progress:.0f}% | "
              f"State: {agent_state['behavioral_state']:12s} | "
              f"Tempo: {tempo:3d} BPM | "
              f"Piano: {piano_note:2d} | "
              f"Guitar: {guitar_note:2d}")

# Concatenate all chunks
print("\nConcatenating audio chunks...")
final_audio = np.concatenate(all_audio_chunks)

# Final normalization
if np.max(np.abs(final_audio)) > 0:
    final_audio = final_audio * 0.9 / np.max(np.abs(final_audio))

print(f"✓ Generated {len(final_audio)} samples ({len(final_audio)/44100:.2f}s)")

# Save to file if possible
if SOUNDFILE_AVAILABLE:
    output_file = "integrated_performance.wav"
    sf.write(output_file, final_audio, 44100)
    print(f"✓ Audio saved to: {output_file}")

# Performance statistics
print("\n" + "=" * 80)
print("PERFORMANCE STATISTICS")
print("=" * 80)

states_count = {}
for info in chunk_info:
    state = info['state']
    states_count[state] = states_count.get(state, 0) + 1

print(f"\nBehavioral States:")
for state, count in states_count.items():
    percentage = (count / len(chunk_info)) * 100
    print(f"  {state:12s}: {count:3d} chunks ({percentage:5.1f}%)")

tempos = [info['tempo'] for info in chunk_info]
print(f"\nTempo:")
print(f"  Min: {min(tempos)} BPM")
print(f"  Max: {max(tempos)} BPM")
print(f"  Avg: {np.mean(tempos):.1f} BPM")

piano_notes = [info['piano_note'] for info in chunk_info]
print(f"\nPiano Range:")
print(f"  Min: MIDI {min(piano_notes)}")
print(f"  Max: MIDI {max(piano_notes)}")

print("\n" + "=" * 80)
print("DEMO COMPLETE!")
print("=" * 80)

print("\nThis demo showcased:")
print("  1. EEG Mapper - Converted simulated brain signals to controls")
print("  2. Agent Memory - Learned patterns from control history")
print("  3. Hybrid Agent - Adapted behavior (calm/active/responsive)")
print("  4. Piano Synth - Generated melodic content")
print("  5. Guitar Synth - Added harmonic accompaniment")
print("  6. Beat Generator - Provided rhythmic foundation")
print("\nAll 5 components + Hybrid Adaptive Agent working in harmony!")
