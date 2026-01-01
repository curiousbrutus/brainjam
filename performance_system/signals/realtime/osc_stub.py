"""
OSC Device Stub

⚠️ EXPERIMENTAL / PLACEHOLDER

This is a stub for Open Sound Control (OSC) integration.
OSC is a networking protocol commonly used for real-time musical control.

When implemented, this will:
- Receive OSC messages from various sources (TouchOSC, Max/MSP, etc.)
- Map OSC addresses to performance parameters
- Support flexible routing and scaling

Current status: Simulates the interface but returns mock data.
"""

from typing import Dict
import numpy as np
from .base_device import BaseDevice


class OSCDevice(BaseDevice):
    """
    OSC (Open Sound Control) device interface (STUB).
    
    This is a placeholder showing how OSC controllers would integrate.
    
    Future implementation will use:
    - python-osc library for OSC server
    - Configurable address space mapping
    - Support for TouchOSC, Lemur, Max/MSP, etc.
    
    For now, this returns simulated control signals.
    """
    
    def __init__(self, ip: str = "127.0.0.1", port: int = 8000, 
                 address_mapping: Dict[str, str] = None):
        """
        Initialize OSC device.
        
        Args:
            ip: IP address to listen on
            port: UDP port to listen on
            address_mapping: Dict mapping control names to OSC addresses
                            e.g., {"intensity": "/control/1", "density": "/control/2"}
        """
        super().__init__(device_name=f"OSC ({ip}:{port})")
        self.ip = ip
        self.port = port
        self.address_mapping = address_mapping or {
            "intensity": "/brainjam/intensity",
            "density": "/brainjam/density",
            "variation": "/brainjam/variation",
            "brightness": "/brainjam/brightness"
        }
        self.server = None
        self.values = {name: 0.5 for name in self.address_mapping.keys()}
        self.t = 0.0
        
    def connect(self) -> bool:
        """
        Start OSC server.
        
        Future implementation:
        ```python
        from pythonosc import dispatcher, osc_server
        import threading
        
        # Create dispatcher
        disp = dispatcher.Dispatcher()
        
        # Register handlers for each address
        for name, address in self.address_mapping.items():
            def handler(unused_addr, value, ctrl_name=name):
                # Normalize to 0-1 range (assumes input is 0-1)
                self.values[ctrl_name] = float(value)
            disp.map(address, handler)
        
        # Start server in background thread
        self.server = osc_server.ThreadingOSCUDPServer(
            (self.ip, self.port), disp
        )
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        self.is_connected = True
        return True
        ```
        
        Returns:
            True (stub always succeeds)
        """
        print(f"⚠️  STUB: OSC device at {self.ip}:{self.port} - using mock data")
        print("    Real OSC integration requires: pip install python-osc")
        print(f"    Address mapping: {self.address_mapping}")
        self.is_connected = True
        return True
    
    def disconnect(self) -> bool:
        """
        Stop OSC server.
        
        Returns:
            True (stub always succeeds)
        """
        if self.server:
            self.server = None
        self.is_connected = False
        return True
    
    def get_control_frame(self) -> Dict[str, float]:
        """
        Get control parameters from OSC messages.
        
        Future implementation:
        ```python
        # Values are updated asynchronously by OSC server
        # Just return current state
        return self.values.copy()
        ```
        
        Current behavior: Returns time-varying mock data.
        
        Returns:
            Dictionary of control parameters (0-1 range)
        """
        if not self.is_connected:
            return {name: 0.5 for name in self.address_mapping.keys()}
        
        # Simulate OSC messages arriving
        self.t += 0.05
        
        # Simulate different update rates (OSC can be irregular)
        mock_controls = {
            "intensity": 0.5 + 0.35 * np.sin(self.t * 0.7),
            "density": 0.5 + 0.25 * np.sin(self.t * 0.9),
            "variation": 0.5 + 0.2 * np.sin(self.t * 0.4),
            "brightness": 0.5 + 0.3 * np.sin(self.t * 1.1)
        }
        
        # Clip to valid range
        return {
            name: float(np.clip(value, 0, 1))
            for name, value in mock_controls.items()
        }
