#!/usr/bin/env python3
"""
BrainJam System Validation Script

Tests the core components added in the device-aware MVP update:
- Device abstraction layer
- Generative sound engine adapters
- Backward compatibility
- Import paths
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_device_stubs():
    """Test all device stubs work correctly."""
    print("=" * 60)
    print("Testing Device Abstraction Layer")
    print("=" * 60)
    
    from performance_system.signals.realtime import EEGLSLDevice, MIDIDevice, OSCDevice
    
    devices = [
        ("EEG LSL", EEGLSLDevice()),
        ("MIDI", MIDIDevice()),
        ("OSC", OSCDevice())
    ]
    
    for name, device in devices:
        print(f"\n{name} Device:")
        device.connect()
        controls = device.get_control_frame()
        info = device.get_info()
        
        # Verify control frame has expected keys
        assert 'intensity' in controls, f"{name}: Missing 'intensity' in controls"
        assert 'density' in controls, f"{name}: Missing 'density' in controls"
        assert 'variation' in controls, f"{name}: Missing 'variation' in controls"
        assert 'brightness' in controls, f"{name}: Missing 'brightness' in controls"
        
        # Verify values are in 0-1 range
        for key, value in controls.items():
            assert 0 <= value <= 1, f"{name}: {key}={value} out of range [0,1]"
        
        print(f"  ✅ {name} device working")
        print(f"     Type: {info['type']}")
        print(f"     Connected: {info['connected']}")
        device.disconnect()
    
    print("\n✅ All device stubs working correctly!\n")


def test_generative_engines():
    """Test generative sound engine adapters."""
    print("=" * 60)
    print("Testing Generative Sound Engine Adapters")
    print("=" * 60)
    
    from performance_system.sound_engines.generative import SunoLikeAdapter
    
    print("\nSuno-Like Adapter:")
    suno = SunoLikeAdapter()
    info = suno.get_info()
    params = suno.get_control_parameters()
    
    print(f"  Type: {info['type']}")
    print(f"  Status: {info['status']}")
    print(f"  Latency: {info['latency']}")
    
    # Generate audio
    controls = {
        'intensity': 0.7,
        'density': 0.5,
        'variation_rate': 0.3,
        'structure_change': 0.0
    }
    
    audio = suno.generate(
        duration=0.5,
        control_params=controls,
        prompt="test audio"
    )
    
    assert audio.shape[0] == 44100 * 0.5, "Audio length incorrect"
    assert audio.dtype.name == 'float32', "Audio dtype incorrect"
    
    print("  ✅ Suno-like adapter working")
    print("\n✅ All generative engines working correctly!\n")


def test_backward_compatibility():
    """Test backward compatibility with old import paths."""
    print("=" * 60)
    print("Testing Backward Compatibility")
    print("=" * 60)
    
    # Old import path
    from performance_system.controllers import MockEEGController
    mock_old = MockEEGController()
    controls_old = mock_old.get_control_vector()
    
    print("\n  Old import path (controllers):")
    print(f"    from performance_system.controllers import MockEEGController")
    print(f"    ✅ Import successful")
    print(f"    ✅ get_control_vector() works")
    
    # New import path
    from performance_system.signals.mock import MockEEGController as MockEEGNew
    mock_new = MockEEGNew()
    controls_new = mock_new.get_control_vector()
    frame = mock_new.get_control_frame()
    
    print("\n  New import path (signals.mock):")
    print(f"    from performance_system.signals.mock import MockEEGController")
    print(f"    ✅ Import successful")
    print(f"    ✅ get_control_vector() works")
    print(f"    ✅ get_control_frame() works (new method)")
    
    # Verify structure
    assert 'control_1' in controls_old, "Missing control_1 in old method"
    assert 'intensity' in frame, "Missing intensity in new method"
    
    print("\n✅ Backward compatibility maintained!\n")


def test_base_device_interface():
    """Test BaseDevice interface."""
    print("=" * 60)
    print("Testing BaseDevice Interface")
    print("=" * 60)
    
    from performance_system.signals.realtime import BaseDevice
    
    # Verify abstract methods exist
    abstract_methods = ['connect', 'disconnect', 'get_control_frame']
    
    for method in abstract_methods:
        assert hasattr(BaseDevice, method), f"Missing abstract method: {method}"
    
    print("\n  ✅ BaseDevice interface properly defined")
    print(f"     Abstract methods: {', '.join(abstract_methods)}")
    print("\n✅ Interface validation passed!\n")


def test_streamlit_pages():
    """Verify Streamlit pages have valid syntax."""
    print("=" * 60)
    print("Testing Streamlit Pages")
    print("=" * 60)
    
    import ast
    
    pages = [
        'streamlit_app/pages/2_Signals.py',
        'streamlit_app/pages/5_Live_Performance.py'
    ]
    
    print()
    for page in pages:
        with open(page, 'r') as f:
            code = f.read()
        try:
            ast.parse(code)
            print(f"  ✅ {page}: Valid syntax")
        except SyntaxError as e:
            print(f"  ❌ {page}: Syntax error - {e}")
            raise
    
    print("\n✅ All Streamlit pages have valid syntax!\n")


def test_documentation():
    """Verify documentation files exist."""
    print("=" * 60)
    print("Testing Documentation")
    print("=" * 60)
    
    docs = [
        'models/PRETRAINED_EEG_MODELS.md',
        'models/README.md',
        'README.md'
    ]
    
    print()
    for doc in docs:
        assert os.path.exists(doc), f"Missing documentation: {doc}"
        print(f"  ✅ {doc}: Exists")
    
    # Verify README has Real-Time & Future Work section
    with open('README.md', 'r') as f:
        readme = f.read()
    
    assert 'Real-Time Devices & Future Integration' in readme, \
        "Missing 'Real-Time Devices & Future Integration' section in README"
    assert 'Miranda' in readme, "Missing Miranda citation in README"
    assert 'Lab Streaming Layer' in readme, "Missing LSL mention in README"
    
    print(f"  ✅ README.md: Contains Real-Time & Future Work section")
    print("\n✅ Documentation complete!\n")


def main():
    """Run all validation tests."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "BrainJam System Validation" + " " * 22 + "║")
    print("║" + " " * 10 + "Device-Aware MVP Update" + " " * 24 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    try:
        test_base_device_interface()
        test_device_stubs()
        test_generative_engines()
        test_backward_compatibility()
        test_streamlit_pages()
        test_documentation()
        
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 18 + "ALL TESTS PASSED" + " " * 24 + "║")
        print("╚" + "═" * 58 + "╝")
        print()
        print("✅ BrainJam device-aware MVP update validated successfully!")
        print()
        return 0
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ VALIDATION FAILED")
        print("=" * 60)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
