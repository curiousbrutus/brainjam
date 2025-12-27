"""
Audio Utilities

Audio generation and playback helpers for the Streamlit GUI
"""

import numpy as np
import io
import base64


def generate_simple_tone(duration, frequency, sample_rate=44100):
    """
    Generate a simple sine tone
    
    Args:
        duration: Duration in seconds
        frequency: Frequency in Hz
        sample_rate: Sample rate in Hz
        
    Returns:
        Audio array (float32)
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = 0.3 * np.sin(2 * np.pi * frequency * t)
    return audio.astype(np.float32)


def audio_to_bytes(audio, sample_rate=44100):
    """
    Convert audio array to WAV bytes
    
    Args:
        audio: Audio array (float32)
        sample_rate: Sample rate in Hz
        
    Returns:
        WAV file bytes
    """
    import wave
    
    # Convert to 16-bit PCM
    audio_int = np.int16(audio * 32767)
    
    # Create WAV file in memory
    byte_io = io.BytesIO()
    with wave.open(byte_io, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int.tobytes())
    
    return byte_io.getvalue()


def create_audio_player_html(audio, sample_rate=44100):
    """
    Create HTML audio player
    
    Args:
        audio: Audio array (float32)
        sample_rate: Sample rate in Hz
        
    Returns:
        HTML string for audio player
    """
    wav_bytes = audio_to_bytes(audio, sample_rate)
    b64 = base64.b64encode(wav_bytes).decode()
    
    html = f'''
        <audio controls>
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
    '''
    
    return html
