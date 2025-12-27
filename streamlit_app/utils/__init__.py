"""
Utilities package for BrainJam Streamlit GUI
"""

from .signal_utils import MockSignalGenerator, normalize_features
from .plot_utils import (
    plot_time_series, 
    plot_band_powers, 
    plot_control_parameters,
    plot_mapping_curve,
    plot_sound_parameters,
    create_system_diagram
)
from .audio_utils import generate_simple_tone, audio_to_bytes, create_audio_player_html

__all__ = [
    'MockSignalGenerator',
    'normalize_features',
    'plot_time_series',
    'plot_band_powers',
    'plot_control_parameters',
    'plot_mapping_curve',
    'plot_sound_parameters',
    'create_system_diagram',
    'generate_simple_tone',
    'audio_to_bytes',
    'create_audio_player_html',
]
