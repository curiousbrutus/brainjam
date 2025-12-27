"""
Plotting Utilities

Visualization helpers for the Streamlit GUI
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_time_series(time_vec, signal, title="Signal"):
    """
    Create time series plot
    
    Args:
        time_vec: Time array
        signal: Signal array
        title: Plot title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_vec,
        y=signal,
        mode='lines',
        name='Signal',
        line=dict(color='#1f77b4', width=1.5)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time (s)",
        yaxis_title="Amplitude",
        height=300,
        margin=dict(l=50, r=20, t=50, b=50),
        template="plotly_white"
    )
    
    return fig


def plot_band_powers(features):
    """
    Create bar chart of band powers
    
    Args:
        features: Dict with theta_power, alpha_power, beta_power
        
    Returns:
        Plotly figure
    """
    bands = ['Theta (4-8 Hz)', 'Alpha (8-13 Hz)', 'Beta (13-30 Hz)']
    powers = [
        features['theta_power'],
        features['alpha_power'],
        features['beta_power']
    ]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    fig = go.Figure(data=[
        go.Bar(
            x=bands,
            y=powers,
            marker_color=colors,
            text=[f'{p:.1f}' for p in powers],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Band Powers",
        yaxis_title="Power",
        height=300,
        margin=dict(l=50, r=20, t=50, b=50),
        template="plotly_white"
    )
    
    return fig


def plot_control_parameters(controls):
    """
    Create bar chart of control parameters
    
    Args:
        controls: Dict with control_1, control_2, control_3, control_4
        
    Returns:
        Plotly figure
    """
    labels = ['Control 1', 'Control 2', 'Control 3', 'Control 4']
    values = [
        controls['control_1'],
        controls['control_2'],
        controls['control_3'],
        controls['control_4']
    ]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    
    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker_color=colors,
            text=[f'{v:.2f}' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Control Parameters",
        yaxis_title="Value (0-1)",
        yaxis_range=[0, 1],
        height=300,
        margin=dict(l=50, r=20, t=50, b=50),
        template="plotly_white"
    )
    
    return fig


def plot_mapping_curve(input_range, output_values, title="Mapping Curve"):
    """
    Plot input-output mapping curve
    
    Args:
        input_range: Array of input values
        output_values: Array of output values
        title: Plot title
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=input_range,
        y=output_values,
        mode='lines',
        name='Mapping',
        line=dict(color='#e74c3c', width=3)
    ))
    
    # Add diagonal reference line
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Identity',
        line=dict(color='gray', width=1, dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Input Signal",
        yaxis_title="Output Control",
        xaxis_range=[0, 1],
        yaxis_range=[0, 1],
        height=400,
        margin=dict(l=50, r=20, t=50, b=50),
        template="plotly_white"
    )
    
    return fig


def plot_sound_parameters(sound_params):
    """
    Create radar chart for sound parameters
    
    Args:
        sound_params: Dict with tempo_density, harmonic_tension, etc.
        
    Returns:
        Plotly figure
    """
    categories = [
        'Tempo/Density',
        'Harmonic Tension',
        'Spectral Brightness',
        'Noise Balance'
    ]
    
    values = [
        sound_params.get('tempo_density', 0.5),
        sound_params.get('harmonic_tension', 0.5),
        sound_params.get('spectral_brightness', 0.5),
        sound_params.get('noise_balance', 0.5)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Sound Parameters',
        line_color='#e74c3c'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        template="plotly_white"
    )
    
    return fig


def create_system_diagram():
    """
    Create a simple system architecture diagram using plotly
    
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Define boxes
    boxes = [
        {'x': 0.5, 'y': 5, 'text': 'Signal Input<br>(EEG/fNIRS/Mock)', 'color': '#ff6b6b'},
        {'x': 0.5, 'y': 4, 'text': 'Feature Extraction<br>(Band Powers)', 'color': '#4ecdc4'},
        {'x': 0.5, 'y': 3, 'text': 'Mapping Model<br>(Linear/MLP)', 'color': '#45b7d1'},
        {'x': 0.5, 'y': 2, 'text': 'Sound Engine<br>(Parametric Synth)', 'color': '#96ceb4'},
        {'x': 0.5, 'y': 1, 'text': 'Audio Output<br>→ Performer', 'color': '#ffeaa7'},
    ]
    
    # Add boxes
    for box in boxes:
        fig.add_shape(
            type="rect",
            x0=box['x']-0.3, y0=box['y']-0.3,
            x1=box['x']+0.3, y1=box['y']+0.3,
            line=dict(color=box['color'], width=3),
            fillcolor=box['color'],
            opacity=0.3
        )
        fig.add_annotation(
            x=box['x'], y=box['y'],
            text=box['text'],
            showarrow=False,
            font=dict(size=12, color='black'),
            bgcolor='white',
            opacity=0.8
        )
    
    # Add arrows
    for i in range(len(boxes)-1):
        fig.add_annotation(
            x=boxes[i]['x'], y=boxes[i]['y']-0.35,
            ax=boxes[i]['x'], ay=boxes[i+1]['y']+0.35,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='#2d3436'
        )
    
    # Add feedback loop
    fig.add_annotation(
        x=0.8, y=2.5,
        ax=0.8, ay=1.5,
        xref='x', yref='y', axref='x', ayref='y',
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor='#fdcb6e',
        text='Feedback Loop',
        textangle=-90
    )
    
    fig.update_xaxes(range=[0, 1], showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(range=[0, 6], showgrid=False, showticklabels=False, zeroline=False)
    
    fig.update_layout(
        title="BrainJam System Pipeline",
        height=600,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='white',
        showlegend=False
    )
    
    return fig
