"""
Base Device Interface

All signal sources (mock, real-time EEG, MIDI, OSC) expose this interface
for consistent integration with the BrainJam performance system.

This is NOT about decoding brain states - it's about extracting
continuous control parameters from any input modality.
"""

from abc import ABC, abstractmethod
from typing import Dict


class BaseDevice(ABC):
    """
    Abstract base class for all signal input devices.
    
    All devices must implement get_control_frame() to return
    a dictionary of normalized control parameters (0-1 range).
    
    This interface treats all inputs as continuous control signals,
    comparable to gesture sensors, MIDI controllers, or breath sensors.
    """
    
    def __init__(self, device_name: str = "BaseDevice"):
        """
        Initialize device.
        
        Args:
            device_name: Human-readable name for this device
        """
        self.device_name = device_name
        self.is_connected = False
        
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the device.
        
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close connection to the device.
        
        Returns:
            True if disconnection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_control_frame(self) -> Dict[str, float]:
        """
        Get current control parameters from device.
        
        This is the core method all devices must implement.
        Returns a dictionary of normalized control values (0-1 range).
        
        Example return values:
        {
            "intensity": 0.7,      # Overall activation/energy
            "density": 0.4,        # Event rate/texture
            "variation": 0.6,      # Temporal variability
            "brightness": 0.8,     # Spectral quality
            "tension": 0.3         # Harmonic character
        }
        
        Returns:
            Dictionary mapping control parameter names to float values (0-1)
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """
        Get device information.
        
        Returns:
            Dictionary with device metadata
        """
        return {
            "name": self.device_name,
            "connected": str(self.is_connected),
            "type": self.__class__.__name__
        }
