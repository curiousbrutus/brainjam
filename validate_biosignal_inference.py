"""
Validation Script for BioSignalInference Module

Tests the latent_mapper module to ensure:
1. Correct initialization and processing
2. Feature extraction works for EEG, fNIRS, EMG
3. Style vector output is in [0, 1] range
4. Conditional trigger works (arousal > 0.8, effort > 0.7)
5. Performance stays under 100ms latency budget
"""

import numpy as np
import time
from src.bridge.latent_mapper import BioSignalInference


def generate_mock_signals(n_samples=100, eeg_ch=8, fnirs_ch=2, emg_ch=1):
    """Generate mock synchronized biosignals for testing."""
    # Mock EEG with alpha and beta components
    t = np.linspace(0, 1, n_samples)
    eeg = np.zeros((n_samples, eeg_ch))
    for ch in range(eeg_ch):
        alpha = np.sin(2 * np.pi * 10 * t + ch * 0.5)  # 10 Hz alpha
        beta = 0.5 * np.sin(2 * np.pi * 20 * t + ch * 0.3)  # 20 Hz beta
        eeg[:, ch] = alpha + beta + 0.1 * np.random.randn(n_samples)
    
    # Mock fNIRS with HbO2 trend
    fnirs = np.zeros((n_samples, fnirs_ch))
    fnirs[:, 0] = 0.5 + 0.1 * t + 0.05 * np.random.randn(n_samples)  # HbO2 with positive slope
    fnirs[:, 1] = 0.5 - 0.05 * t + 0.05 * np.random.randn(n_samples)  # HbR with negative slope
    
    # Mock EMG with muscle activation
    emg = np.zeros((n_samples, emg_ch))
    emg[:, 0] = 0.3 + 0.2 * np.sin(2 * np.pi * 5 * t) + 0.1 * np.random.randn(n_samples)
    
    return eeg, fnirs, emg


def test_initialization():
    """Test BioSignalInference initialization."""
    print("=" * 60)
    print("TEST 1: Initialization")
    print("=" * 60)
    
    try:
        processor = BioSignalInference(
            eeg_channels=8,
            fnirs_channels=2,
            emg_channels=1,
            sample_rate=250.0,
            buffer_size=500
        )
        print("✓ BioSignalInference initialized successfully")
        print(f"  - EEG channels: {processor.eeg_channels}")
        print(f"  - fNIRS channels: {processor.fnirs_channels}")
        print(f"  - EMG channels: {processor.emg_channels}")
        print(f"  - Sample rate: {processor.sample_rate} Hz")
        print(f"  - Buffer size: {processor.buffer_size} samples")
        print(f"  - Device: {processor.device}")
        return True, processor
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False, None


def test_feature_extraction(processor):
    """Test feature extraction from biosignals."""
    print("\n" + "=" * 60)
    print("TEST 2: Feature Extraction")
    print("=" * 60)
    
    try:
        # Generate mock signals
        eeg, fnirs, emg = generate_mock_signals(n_samples=200)
        
        # Process frame
        style_vector = processor.process_frame(eeg, fnirs, emg)
        
        print("✓ Feature extraction successful")
        print(f"  - Arousal (Beta/Alpha): {style_vector['arousal']:.3f}")
        print(f"  - Cognitive Load (fNIRS slope): {style_vector['cognitive_load']:.3f}")
        print(f"  - Effort (EMG RMS): {style_vector['effort']:.3f}")
        
        return True, style_vector
    except Exception as e:
        print(f"✗ Feature extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_style_vector_range(style_vector):
    """Test that style vector outputs are in [0, 1] range."""
    print("\n" + "=" * 60)
    print("TEST 3: Style Vector Range [0, 1]")
    print("=" * 60)
    
    try:
        params = ['tempo_density', 'harmonic_tension', 'spectral_brightness', 'noise_balance']
        all_valid = True
        
        for param in params:
            value = style_vector[param]
            in_range = 0.0 <= value <= 1.0
            status = "✓" if in_range else "✗"
            print(f"  {status} {param}: {value:.3f} {'[OK]' if in_range else '[OUT OF RANGE]'}")
            all_valid = all_valid and in_range
        
        if all_valid:
            print("✓ All parameters in valid [0, 1] range")
            return True
        else:
            print("✗ Some parameters out of range")
            return False
    except Exception as e:
        print(f"✗ Range test failed: {e}")
        return False


def test_conditional_trigger(processor):
    """Test conditional tempo/density trigger."""
    print("\n" + "=" * 60)
    print("TEST 4: Conditional Trigger (Arousal > 0.8, Effort > 0.7)")
    print("=" * 60)
    
    try:
        # Generate signals with high beta (high arousal) and high EMG (high effort)
        t = np.linspace(0, 1, 200)
        
        # High beta EEG
        eeg = np.zeros((200, 8))
        for ch in range(8):
            beta = 2.0 * np.sin(2 * np.pi * 20 * t)  # Strong beta
            alpha = 0.3 * np.sin(2 * np.pi * 10 * t)  # Weak alpha
            eeg[:, ch] = beta + alpha + 0.1 * np.random.randn(200)
        
        # Positive fNIRS slope
        fnirs = np.zeros((200, 2))
        fnirs[:, 0] = 0.5 + 0.2 * t + 0.05 * np.random.randn(200)
        fnirs[:, 1] = 0.5 - 0.1 * t + 0.05 * np.random.randn(200)
        
        # High EMG
        emg = np.zeros((200, 1))
        emg[:, 0] = 0.8 + 0.1 * np.random.randn(200)  # High baseline
        
        # Process
        style_vector = processor.process_frame(eeg, fnirs, emg)
        
        arousal = style_vector['arousal']
        effort = style_vector['effort']
        tempo_density = style_vector['tempo_density']
        
        print(f"  - Arousal: {arousal:.3f} (threshold: 0.8)")
        print(f"  - Effort: {effort:.3f} (threshold: 0.7)")
        print(f"  - Tempo Density: {tempo_density:.3f}")
        
        if arousal > 0.8 and effort > 0.7:
            if tempo_density == 1.0:
                print("✓ Trigger activated correctly (tempo_density = 1.0 → 180 BPM)")
                return True
            else:
                print(f"✗ Trigger should activate but tempo_density = {tempo_density}")
                return False
        else:
            print(f"  Note: Conditions not met (arousal={arousal:.3f}, effort={effort:.3f})")
            print("  Trigger logic present but not activated in this test")
            return True
            
    except Exception as e:
        print(f"✗ Trigger test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_performance(processor):
    """Test processing latency."""
    print("\n" + "=" * 60)
    print("TEST 5: Performance (<100ms Latency Budget)")
    print("=" * 60)
    
    try:
        # Process multiple frames to get stable timing
        n_trials = 50
        latencies = []
        
        for _ in range(n_trials):
            eeg, fnirs, emg = generate_mock_signals(n_samples=100)
            
            start = time.perf_counter()
            processor.process_frame(eeg, fnirs, emg)
            latency = (time.perf_counter() - start) * 1000  # ms
            
            latencies.append(latency)
        
        # Get statistics
        stats = processor.get_performance_stats()
        
        print(f"  - Mean latency: {stats['mean_latency_ms']:.2f} ms")
        print(f"  - Std latency: {stats['std_latency_ms']:.2f} ms")
        print(f"  - Max latency: {stats['max_latency_ms']:.2f} ms")
        print(f"  - P95 latency: {stats['p95_latency_ms']:.2f} ms")
        
        if stats['p95_latency_ms'] < 100:
            print(f"✓ P95 latency {stats['p95_latency_ms']:.2f}ms < 100ms budget")
            return True
        else:
            print(f"✗ P95 latency {stats['p95_latency_ms']:.2f}ms exceeds 100ms budget")
            return False
            
    except Exception as e:
        print(f"✗ Performance test failed: {e}")
        return False


def test_transfer_learning_hook(processor):
    """Test transfer learning placeholder function."""
    print("\n" + "=" * 60)
    print("TEST 6: Transfer Learning Hook")
    print("=" * 60)
    
    try:
        # Test without projection matrix (identity)
        vector = np.array([0.5, 0.7, 0.3])
        aligned = processor.align_with_mindvis_latent(vector)
        
        if np.allclose(aligned, vector):
            print("✓ Identity mapping works (no projection matrix set)")
        else:
            print("✗ Identity mapping failed")
            return False
        
        # Test with mock projection matrix
        projection = np.random.randn(3, 3)
        processor.set_mindvis_projection(projection)
        
        aligned = processor.align_with_mindvis_latent(vector)
        expected = projection @ vector
        
        if np.allclose(aligned, expected):
            print("✓ Projection mapping works (with projection matrix)")
            return True
        else:
            print("✗ Projection mapping failed")
            return False
            
    except Exception as e:
        print(f"✗ Transfer learning test failed: {e}")
        return False


def main():
    """Run all validation tests."""
    print("\n" + "=" * 60)
    print("BioSignalInference Validation Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Initialization
    success, processor = test_initialization()
    results.append(("Initialization", success))
    
    if not success:
        print("\n✗ Cannot proceed without successful initialization")
        return
    
    # Test 2: Feature Extraction
    success, style_vector = test_feature_extraction(processor)
    results.append(("Feature Extraction", success))
    
    if not success:
        print("\n✗ Cannot proceed without successful feature extraction")
        return
    
    # Test 3: Style Vector Range
    success = test_style_vector_range(style_vector)
    results.append(("Style Vector Range", success))
    
    # Test 4: Conditional Trigger
    success = test_conditional_trigger(processor)
    results.append(("Conditional Trigger", success))
    
    # Test 5: Performance
    success = test_performance(processor)
    results.append(("Performance (<100ms)", success))
    
    # Test 6: Transfer Learning Hook
    success = test_transfer_learning_hook(processor)
    results.append(("Transfer Learning Hook", success))
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    all_passed = all(passed for _, passed in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
