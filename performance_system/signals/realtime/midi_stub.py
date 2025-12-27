"""
MIDI Device Stub

⚠️ EXPERIMENTAL / PLACEHOLDER

This is a stub for MIDI controller integration.
Standard MIDI input for musical control is not yet fully implemented.

When implemented, this will:
- Connect to MIDI controllers (keyboards, pads, breath controllers, etc.)
- Map MIDI CC (continuous controller) messages to performance parameters
- Support standard MIDI devices as alternative/complementary input

Current status: Simulates the interface but returns mock data.
"""

from typing import Dict
import numpy as np
from .base_device import BaseDevice


class MIDIDevice(BaseDevice):
    """
    MIDI controller interface (STUB).
    
    This is a placeholder showing how MIDI controllers would integrate.
    
    Future implementation will use:
    - mido or python-rtmidi for MIDI I/O
    - CC mapping configuration
    - Support for multiple controllers simultaneously
    
    For now, this returns simulated control signals.
    """
    
    def __init__(self, port_name: str = "BrainJam-MIDI", cc_mapping: Dict[str, int] = None):
        """
        Initialize MIDI device.
        
        Args:
            port_name: Name of MIDI port to connect to
            cc_mapping: Dict mapping control names to CC numbers
                       e.g., {"intensity": 1, "density": 7, "brightness": 74}
        """
        super().__init__(device_name=f"MIDI ({port_name})")
        self.port_name = port_name
        self.cc_mapping = cc_mapping or {
            "intensity": 1,      # Modulation wheel
            "density": 7,        # Volume
            "variation": 10,     # Pan
            "brightness": 74     # Filter cutoff (standard)
        }
        self.port = None
        self.cc_values = {name: 64 for name in self.cc_mapping.keys()}  # Start at mid-point
        self.t = 0.0
        
    def connect(self) -> bool:
        """
        Connect to MIDI port.
        
        Future implementation:
        ```python
        import mido
        
        # List available ports
        available_ports = mido.get_input_names()
        
        # Connect to specified port
        if self.port_name in available_ports:
            self.port = mido.open_input(self.port_name)
            self.is_connected = True
            return True
        return False
        ```
        
        Returns:
            True (stub always succeeds)
        """
        print(f"⚠️  STUB: MIDI device '{self.port_name}' - using mock data")
        print("    Real MIDI integration requires: pip install mido python-rtmidi")
        print(f"    CC mapping: {self.cc_mapping}")
        self.is_connected = True
        return True
    
    def disconnect(self) -> bool:
        """
        Disconnect from MIDI port.
        
        Returns:
            True (stub always succeeds)
        """
        if self.port:
            self.port = None
        self.is_connected = False
        return True
    
    def get_control_frame(self) -> Dict[str, float]:
        """
        Get control parameters from MIDI controller.
        
        Future implementation:
        ```python
        # Poll for MIDI messages
        for msg in self.port.iter_pending():
            if msg.type == 'control_change':
                # Find which control this CC belongs to
                for name, cc_num in self.cc_mapping.items():
                    if msg.control == cc_num:
                        # Store normalized value (MIDI is 0-127)
                        self.cc_values[name] = msg.value / 127.0
        
        return self.cc_values
        ```
        
        Current behavior: Returns time-varying mock data.
        
        Returns:
            Dictionary of control parameters (0-1 range)
        """
        if not self.is_connected:
            return {name: 0.5 for name in self.cc_mapping.keys()}
        
        # Simulate MIDI controller movements
        self.t += 0.05
        
        # Simulate slow controller movements
        mock_controls = {
            "intensity": 0.5 + 0.3 * np.sin(self.t * 0.4),
            "density": 0.5 + 0.2 * np.sin(self.t * 0.6),
            "variation": 0.5 + 0.25 * np.sin(self.t * 0.35),
            "brightness": 0.5 + 0.2 * np.sin(self.t * 0.8)
        }
        
        # Clip to valid range
        return {
            name: float(np.clip(value, 0, 1))
            for name, value in mock_controls.items()
        }
