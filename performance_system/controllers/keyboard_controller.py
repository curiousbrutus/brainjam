"""
Keyboard Controller

Maps keyboard input to continuous control parameters.
Useful for testing and as a baseline comparison for EEG control.
"""

import numpy as np
from typing import Dict, Optional
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class KeyboardController:
    """
    Simple keyboard-based controller for testing the performance system.
    
    This provides manual control over the same parameters that might be
    controlled by EEG, useful for:
    - Testing the sound engine independently
    - Comparing EEG control to manual control
    - Allowing hybrid control modes
    """
    
    def __init__(self):
        """Initialize keyboard controller."""
        self.control_values = {
            'control_1': 0.5,
            'control_2': 0.5,
            'control_3': 0.5,
            'control_4': 0.5,
        }
        self.step_size = 0.05
        
        if PYGAME_AVAILABLE:
            pygame.init()
            self.screen = pygame.display.set_mode((400, 300))
            pygame.display.set_caption("BrainJam Keyboard Controller")
        else:
            self.screen = None
    
    def get_control_vector(self) -> Dict[str, float]:
        """
        Get current control values, updated by keyboard input.
        
        Returns:
            Dictionary of control parameters (0-1 range)
        """
        if PYGAME_AVAILABLE:
            self._process_events()
        
        return self.control_values.copy()
    
    def _process_events(self):
        """Process pygame events to update control values."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        keys = pygame.key.get_pressed()
        
        # Control 1: Q/W keys
        if keys[pygame.K_q]:
            self.control_values['control_1'] = max(0, 
                self.control_values['control_1'] - self.step_size)
        if keys[pygame.K_w]:
            self.control_values['control_1'] = min(1, 
                self.control_values['control_1'] + self.step_size)
        
        # Control 2: A/S keys
        if keys[pygame.K_a]:
            self.control_values['control_2'] = max(0, 
                self.control_values['control_2'] - self.step_size)
        if keys[pygame.K_s]:
            self.control_values['control_2'] = min(1, 
                self.control_values['control_2'] + self.step_size)
        
        # Control 3: Z/X keys
        if keys[pygame.K_z]:
            self.control_values['control_3'] = max(0, 
                self.control_values['control_3'] - self.step_size)
        if keys[pygame.K_x]:
            self.control_values['control_3'] = min(1, 
                self.control_values['control_3'] + self.step_size)
        
        # Control 4: E/R keys
        if keys[pygame.K_e]:
            self.control_values['control_4'] = max(0, 
                self.control_values['control_4'] - self.step_size)
        if keys[pygame.K_r]:
            self.control_values['control_4'] = min(1, 
                self.control_values['control_4'] + self.step_size)
        
        # Reset: Space
        if keys[pygame.K_SPACE]:
            self.control_values = {k: 0.5 for k in self.control_values}
    
    def display_help(self):
        """Print keyboard control help."""
        print("=" * 50)
        print("Keyboard Controller Help")
        print("=" * 50)
        print("Control 1: Q (down) / W (up)")
        print("Control 2: A (down) / S (up)")
        print("Control 3: Z (down) / X (up)")
        print("Control 4: E (down) / R (up)")
        print("Reset all: SPACE")
        print("=" * 50)
    
    def close(self):
        """Clean up resources."""
        if PYGAME_AVAILABLE and self.screen is not None:
            pygame.quit()


class SimpleKeyboardController:
    """
    Simplified keyboard controller that doesn't require pygame.
    Uses simple state machine with manual update calls.
    """
    
    def __init__(self):
        """Initialize simple keyboard controller."""
        self.control_values = {
            'control_1': 0.5,
            'control_2': 0.5,
            'control_3': 0.5,
            'control_4': 0.5,
        }
    
    def set_control(self, control_name: str, value: float):
        """
        Manually set a control value.
        
        Args:
            control_name: Name of control parameter
            value: New value (will be clipped to 0-1)
        """
        if control_name in self.control_values:
            self.control_values[control_name] = np.clip(value, 0, 1)
    
    def adjust_control(self, control_name: str, delta: float):
        """
        Adjust a control value by a delta.
        
        Args:
            control_name: Name of control parameter
            delta: Amount to add (can be negative)
        """
        if control_name in self.control_values:
            new_val = self.control_values[control_name] + delta
            self.control_values[control_name] = np.clip(new_val, 0, 1)
    
    def get_control_vector(self) -> Dict[str, float]:
        """
        Get current control values.
        
        Returns:
            Dictionary of control parameters (0-1 range)
        """
        return self.control_values.copy()
    
    def reset(self):
        """Reset all controls to 0.5."""
        self.control_values = {k: 0.5 for k in self.control_values}
