"""
Tests for Hybrid Adaptive Agent

Tests cover:
- All behavioral states (calm, active, responsive)
- ML and no-ML execution paths
- Control vector processing
- Buffer management
- EMA calculations
"""

import sys
import os
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from performance_system.agents import HybridAdaptiveAgent


def test_initialization():
    """Test agent initialization."""
    print("Testing initialization...")
    
    agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0)
    
    assert agent.buffer_duration == 10.0
    assert agent.sample_rate == 10.0
    assert len(agent.intensity_buffer) == 0
    assert agent.ema_intensity == 0.5
    assert agent.ema_density == 0.5
    assert agent.state == "responsive"
    
    print("✓ Initialization test passed")


def test_calm_state():
    """Test calm behavioral state (low intensity)."""
    print("\nTesting calm state...")
    
    agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0)
    
    # Feed low-intensity controls to trigger calm state
    for _ in range(20):
        controls = {
            'control_1': 0.1,  # Low intensity
            'control_2': 0.2,
            'control_3': 0.3,
            'control_4': 0.2
        }
        response = agent.respond(controls)
    
    # Check state
    state = agent.get_state()
    assert state['behavioral_state'] == 'calm', f"Expected calm, got {state['behavioral_state']}"
    
    # Check response characteristics for calm state
    # Should have low note density (0.1-0.3)
    assert 0.0 <= response['note_density'] <= 0.4, f"Density {response['note_density']} out of range for calm"
    assert 60 <= response['tempo_suggestion'] <= 140
    assert 0.0 <= response['harmonic_tension'] <= 1.0
    assert 0.0 <= response['fill_probability'] <= 1.0
    
    print(f"  State: {state['behavioral_state']}")
    print(f"  Note density: {response['note_density']:.3f}")
    print(f"  Tempo: {response['tempo_suggestion']} BPM")
    print("✓ Calm state test passed")


def test_active_state():
    """Test active behavioral state (high intensity)."""
    print("\nTesting active state...")
    
    agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0)
    
    # Feed high-intensity controls to trigger active state
    for _ in range(20):
        controls = {
            'control_1': 0.9,  # High intensity
            'control_2': 0.8,
            'control_3': 0.7,
            'control_4': 0.6
        }
        response = agent.respond(controls)
    
    # Check state
    state = agent.get_state()
    assert state['behavioral_state'] == 'active', f"Expected active, got {state['behavioral_state']}"
    
    # Check response characteristics for active state
    # Should have high note density (0.7-0.9)
    assert response['note_density'] >= 0.6, f"Density {response['note_density']} too low for active"
    assert 60 <= response['tempo_suggestion'] <= 140
    assert 0.0 <= response['harmonic_tension'] <= 1.0
    assert 0.0 <= response['fill_probability'] <= 1.0
    
    print(f"  State: {state['behavioral_state']}")
    print(f"  Note density: {response['note_density']:.3f}")
    print(f"  Tempo: {response['tempo_suggestion']} BPM")
    print("✓ Active state test passed")


def test_responsive_state():
    """Test responsive behavioral state (medium intensity)."""
    print("\nTesting responsive state...")
    
    agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0)
    
    # Feed medium-intensity controls to trigger responsive state
    for _ in range(20):
        controls = {
            'control_1': 0.5,  # Medium intensity
            'control_2': 0.5,
            'control_3': 0.5,
            'control_4': 0.5
        }
        response = agent.respond(controls)
    
    # Check state
    state = agent.get_state()
    assert state['behavioral_state'] == 'responsive', f"Expected responsive, got {state['behavioral_state']}"
    
    # Check response is within valid ranges
    assert 0.0 <= response['note_density'] <= 1.0
    assert 60 <= response['tempo_suggestion'] <= 140
    assert 0.0 <= response['harmonic_tension'] <= 1.0
    assert 0.0 <= response['fill_probability'] <= 1.0
    
    print(f"  State: {state['behavioral_state']}")
    print(f"  Note density: {response['note_density']:.3f}")
    print(f"  Tempo: {response['tempo_suggestion']} BPM")
    print("✓ Responsive state test passed")


def test_state_transitions():
    """Test transitions between behavioral states."""
    print("\nTesting state transitions...")
    
    agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0)
    
    # Start calm
    for _ in range(15):
        agent.respond({'control_1': 0.1, 'control_2': 0.2, 'control_3': 0.2, 'control_4': 0.2})
    assert agent.get_state()['behavioral_state'] == 'calm'
    print("  ✓ Started in calm state")
    
    # Transition to active
    for _ in range(15):
        agent.respond({'control_1': 0.9, 'control_2': 0.8, 'control_3': 0.7, 'control_4': 0.6})
    assert agent.get_state()['behavioral_state'] == 'active'
    print("  ✓ Transitioned to active state")
    
    # Transition to responsive
    for _ in range(15):
        agent.respond({'control_1': 0.5, 'control_2': 0.5, 'control_3': 0.5, 'control_4': 0.5})
    assert agent.get_state()['behavioral_state'] == 'responsive'
    print("  ✓ Transitioned to responsive state")
    
    print("✓ State transition test passed")


def test_buffer_management():
    """Test circular buffer management."""
    print("\nTesting buffer management...")
    
    agent = HybridAdaptiveAgent(buffer_duration=1.0, sample_rate=10.0)  # 10 samples max
    
    # Fill buffer
    for i in range(15):
        controls = {
            'control_1': i / 15.0,
            'control_2': 0.5,
            'control_3': 0.5,
            'control_4': 0.5
        }
        agent.respond(controls)
    
    # Buffer should be at max size
    state = agent.get_state()
    assert state['buffer_length'] == 10, f"Expected buffer size 10, got {state['buffer_length']}"
    
    # Check that oldest values were dropped (should have recent values)
    assert len(agent.intensity_buffer) == 10
    
    print(f"  Buffer size: {state['buffer_length']}")
    print("✓ Buffer management test passed")


def test_ema_calculation():
    """Test exponential moving average calculation."""
    print("\nTesting EMA calculation...")
    
    agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0, ema_alpha=0.5)
    
    # Feed constant high intensity
    for _ in range(20):
        agent.respond({'control_1': 1.0, 'control_2': 1.0, 'control_3': 0.5, 'control_4': 0.5})
    
    state = agent.get_state()
    # EMA should approach 1.0
    assert state['ema_intensity'] > 0.8, f"EMA intensity {state['ema_intensity']} did not converge"
    assert state['ema_density'] > 0.8, f"EMA density {state['ema_density']} did not converge"
    
    print(f"  EMA intensity: {state['ema_intensity']:.3f}")
    print(f"  EMA density: {state['ema_density']:.3f}")
    print("✓ EMA calculation test passed")


def test_no_ml_fallback():
    """Test operation without ML model (rules only)."""
    print("\nTesting no-ML fallback...")
    
    # Create agent with non-existent model path
    agent = HybridAdaptiveAgent(model_path="/nonexistent/path/model.pth")
    
    assert not agent.ml_available, "ML should not be available"
    assert agent.ml_model is None, "ML model should be None"
    
    # Should still work with rules only
    controls = {'control_1': 0.5, 'control_2': 0.5, 'control_3': 0.5, 'control_4': 0.5}
    response = agent.respond(controls)
    
    assert 'note_density' in response
    assert 'harmonic_tension' in response
    assert 'tempo_suggestion' in response
    assert 'fill_probability' in response
    
    print("  ✓ Agent works without ML model")
    print("✓ No-ML fallback test passed")


def test_response_output_format():
    """Test that response always returns correct format."""
    print("\nTesting response output format...")
    
    agent = HybridAdaptiveAgent()
    
    controls = {'control_1': 0.7, 'control_2': 0.6, 'control_3': 0.4, 'control_4': 0.3}
    response = agent.respond(controls)
    
    # Check all required keys
    required_keys = ['note_density', 'harmonic_tension', 'tempo_suggestion', 'fill_probability']
    for key in required_keys:
        assert key in response, f"Missing key: {key}"
    
    # Check types
    assert isinstance(response['note_density'], float)
    assert isinstance(response['harmonic_tension'], float)
    assert isinstance(response['tempo_suggestion'], int)
    assert isinstance(response['fill_probability'], float)
    
    # Check ranges
    assert 0.0 <= response['note_density'] <= 1.0
    assert 0.0 <= response['harmonic_tension'] <= 1.0
    assert 60 <= response['tempo_suggestion'] <= 140
    assert 0.0 <= response['fill_probability'] <= 1.0
    
    print(f"  Note density: {response['note_density']:.3f}")
    print(f"  Harmonic tension: {response['harmonic_tension']:.3f}")
    print(f"  Tempo: {response['tempo_suggestion']} BPM")
    print(f"  Fill probability: {response['fill_probability']:.3f}")
    print("✓ Response format test passed")


def test_reset():
    """Test agent reset functionality."""
    print("\nTesting reset...")
    
    agent = HybridAdaptiveAgent(buffer_duration=10.0, sample_rate=10.0)
    
    # Fill with data
    for _ in range(20):
        agent.respond({'control_1': 0.9, 'control_2': 0.8, 'control_3': 0.7, 'control_4': 0.6})
    
    state_before = agent.get_state()
    assert state_before['buffer_length'] > 0
    
    # Reset
    agent.reset()
    
    state_after = agent.get_state()
    assert state_after['buffer_length'] == 0
    assert state_after['ema_intensity'] == 0.5
    assert state_after['ema_density'] == 0.5
    assert state_after['behavioral_state'] == 'responsive'
    
    print("  ✓ Agent state reset successfully")
    print("✓ Reset test passed")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\nTesting edge cases...")
    
    agent = HybridAdaptiveAgent()
    
    # Test with missing controls
    response = agent.respond({})
    assert 'note_density' in response
    print("  ✓ Handles missing controls")
    
    # Test with extreme values
    response = agent.respond({'control_1': 0.0, 'control_2': 0.0, 'control_3': 0.0, 'control_4': 0.0})
    assert 0.0 <= response['note_density'] <= 1.0
    print("  ✓ Handles zero controls")
    
    response = agent.respond({'control_1': 1.0, 'control_2': 1.0, 'control_3': 1.0, 'control_4': 1.0})
    assert 0.0 <= response['note_density'] <= 1.0
    print("  ✓ Handles maximum controls")
    
    # Test with extra keys
    response = agent.respond({
        'control_1': 0.5, 'control_2': 0.5, 'control_3': 0.5, 'control_4': 0.5,
        'extra_key': 999
    })
    assert 'note_density' in response
    print("  ✓ Ignores extra keys")
    
    print("✓ Edge cases test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("Running Hybrid Adaptive Agent Tests")
    print("=" * 70)
    
    test_initialization()
    test_calm_state()
    test_active_state()
    test_responsive_state()
    test_state_transitions()
    test_buffer_management()
    test_ema_calculation()
    test_no_ml_fallback()
    test_response_output_format()
    test_reset()
    test_edge_cases()
    
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
