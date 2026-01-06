"""
Demo 2: AI as Co-Performer

Performer triggers events, AI responds with timing + variation.
Brain signal biases AI behavior (not commands it).
"""

import numpy as np
import time
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False

from performance_system.controllers import MockEEGController
from performance_system.sound_engines import SymbolicSynth
from performance_system.agents import HybridAdaptiveAgent


class AICoPerformer:
    """
    AI co-performer that responds to brain signals with musical variations.
    """
    
    def __init__(self, response_delay: float = 0.5, variability: float = 0.3):
        """
        Initialize AI co-performer.
        
        Args:
            response_delay: Time delay for AI responses (seconds)
            variability: Amount of variation in AI responses (0-1)
        """
        self.response_delay = response_delay
        self.variability = variability
        self.last_trigger_time = 0.0
        self.response_history = []
        
    def should_respond(self, current_time: float, brain_signal: dict) -> bool:
        """
        Decide if AI should respond based on time and brain signal.
        
        Args:
            current_time: Current time
            brain_signal: Current brain signal state
            
        Returns:
            True if AI should trigger a response
        """
        time_since_last = current_time - self.last_trigger_time
        
        # Brain signal biases response probability
        arousal = brain_signal.get('control_1', 0.5)
        response_threshold = 0.5 + 0.3 * (1 - arousal)  # Higher arousal = more responsive
        
        # Check if enough time has passed and random trigger
        if time_since_last >= self.response_delay:
            if np.random.rand() < (1.0 - response_threshold):
                self.last_trigger_time = current_time
                return True
        
        return False
    
    def generate_response_params(self, brain_signal: dict) -> dict:
        """
        Generate AI response parameters biased by brain signal.
        
        Args:
            brain_signal: Current brain signal state
            
        Returns:
            Modified control parameters for AI response
        """
        # Base parameters from brain signal
        params = brain_signal.copy()
        
        # AI adds variation
        for key in params:
            # Add controlled randomness
            variation = np.random.randn() * self.variability * 0.1
            params[key] = np.clip(params[key] + variation, 0.0, 1.0)
        
        # AI biases certain parameters
        # Make responses slightly brighter and more varied than input
        if 'control_2' in params:
            params['control_2'] = min(1.0, params['control_2'] * 1.2)
        if 'control_3' in params:
            params['control_3'] = min(1.0, params['control_3'] * 1.1)
        
        return params


def generate_coperformance(duration: float = 40.0,
                           output_file: str = "demo2_ai_coperformer.wav",
                           use_hybrid_agent: bool = True):
    """
    Generate musical dialogue between performer (brain) and AI.
    
    Args:
        duration: Total duration in seconds
        output_file: Output audio file path
        use_hybrid_agent: Whether to use the hybrid adaptive agent (default: True)
    """
    print("=" * 70)
    print("Demo 2: AI as Co-Performer")
    print("=" * 70)
    print("\nGenerating AI co-performance...")
    print(f"Duration: {duration}s")
    
    if use_hybrid_agent:
        print("\nUsing Hybrid Adaptive Agent:")
        print("  • Symbolic logic for reliable real-time response")
        print("  • Adaptive behavioral states (calm/active/responsive)")
        print("  • Short-term memory of performer patterns")
        print("  • Optional ML personalization (if model available)")
    else:
        print("\nUsing Simple AI Co-Performer:")
        print("  • Performer (brain) triggers musical events")
        print("  • AI responds with timing variations")
        print("  • Brain signal biases AI behavior (not commands)")
        print("  • Call-and-response musical dialogue")
    print()
    
    # Initialize components
    controller = MockEEGController(fs=250)
    synth = SymbolicSynth(sample_rate=44100)
    
    if use_hybrid_agent:
        # Use new hybrid adaptive agent
        ai_agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0)
    else:
        # Use original simple co-performer
        ai_partner = AICoPerformer(response_delay=0.8, variability=0.4)
    
    # Generate audio
    chunk_duration = 0.1
    n_chunks = int(duration / chunk_duration)
    audio_chunks = []
    
    current_time = 0.0
    performer_events = 0
    ai_responses = 0
    
    print("Generating co-performance...")
    start_time = time.time()
    
    for i in range(n_chunks):
        # Get performer (brain) signal
        brain_signal = controller.get_control_vector(duration=0.5)
        
        if use_hybrid_agent:
            # Use hybrid adaptive agent - it continuously responds
            ai_response = ai_agent.respond(brain_signal)
            
            # Map agent response to synth controls
            # Note: agent provides specialized parameters, we blend them with brain signal
            ai_params = brain_signal.copy()
            ai_params['control_2'] = ai_response['note_density']
            ai_params['control_3'] = ai_response['harmonic_tension']
            
            audio_chunk = synth.generate(chunk_duration, ai_params)
            ai_responses += 1
        else:
            # Use original simple co-performer logic
            # Check if AI should respond
            if ai_partner.should_respond(current_time, brain_signal):
                # AI generates a response biased by brain signal
                ai_params = ai_partner.generate_response_params(brain_signal)
                audio_chunk = synth.generate(chunk_duration, ai_params)
                ai_responses += 1
            else:
                # Direct brain control (performer)
                audio_chunk = synth.generate(chunk_duration, brain_signal)
                performer_events += 1
        
        audio_chunks.append(audio_chunk)
        current_time += chunk_duration
        
        # Progress
        if (i + 1) % 50 == 0:
            progress = (i + 1) / n_chunks * 100
            elapsed = time.time() - start_time
            if use_hybrid_agent:
                agent_state = ai_agent.get_state()
                print(f"  Progress: {progress:.1f}% - State: {agent_state['behavioral_state']}, "
                      f"EMA Intensity: {agent_state['ema_intensity']:.2f}")
            else:
                print(f"  Progress: {progress:.1f}% - "
                      f"Performer: {performer_events} | AI: {ai_responses}")
    
    # Concatenate
    audio = np.concatenate(audio_chunks)
    
    elapsed = time.time() - start_time
    print(f"\nGeneration complete in {elapsed:.2f}s")
    
    # Save
    if SOUNDFILE_AVAILABLE:
        sf.write(output_file, audio, 44100)
        print(f"Audio saved to: {output_file}")
    
    # Statistics
    print("\n" + "=" * 70)
    print("Co-Performance Statistics:")
    print("=" * 70)
    
    if use_hybrid_agent:
        agent_state = ai_agent.get_state()
        print(f"  Total chunks: {n_chunks}")
        print(f"  AI responses: {ai_responses}")
        print(f"  Final behavioral state: {agent_state['behavioral_state']}")
        print(f"  Final EMA intensity: {agent_state['ema_intensity']:.3f}")
        print(f"  Final EMA density: {agent_state['ema_density']:.3f}")
        print(f"  ML personalization: {'Active' if agent_state['ml_available'] else 'Not available'}")
    else:
        print(f"  Total events: {performer_events + ai_responses}")
        print(f"  Performer events: {performer_events}")
        print(f"  AI responses: {ai_responses}")
        print(f"  AI response ratio: {ai_responses/(performer_events+ai_responses)*100:.1f}%")
    
    print("=" * 70)
    
    print("\n✓ Demo 2 complete!")
    
    if use_hybrid_agent:
        print("\nThis demonstrates:")
        print("  → Hybrid adaptive agent with symbolic logic + optional ML")
        print("  → Real-time behavioral state adaptation (calm/active/responsive)")
        print("  → Short-term memory of performer control patterns")
        print("  → AI responds continuously but never generates autonomously")
        print("  → Performer maintains full agency over musical output")
    else:
        print("\nThis demonstrates:")
        print("  → AI as responsive partner (not autonomous)")
        print("  → Brain signal biases AI behavior")
        print("  → Musical dialogue emerges from interaction")
        print("  → Performer maintains agency")
    
    return audio


if __name__ == "__main__":
    print("\nRunning Demo 2: AI as Co-Performer\n")
    audio = generate_coperformance(duration=40.0)
    print("\nDemo completed successfully!")
