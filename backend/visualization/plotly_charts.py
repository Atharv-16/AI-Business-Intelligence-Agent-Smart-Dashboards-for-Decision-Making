import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Any

def create_time_series_chart(df: pd.DataFrame, metric: str, title: str) -> Dict[str, Any]:
    """
    Create a time series chart for a specific metric.
    
    Args:
        df: DataFrame containing the data
        metric: Name of the metric to plot
        title: Chart title
        
    Returns:
        Dictionary containing the Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df[metric],
        mode='lines+markers',
        name=metric,
        line=dict(color='#1f77b4')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=metric,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig.to_dict()

def create_metric_comparison_chart(df: pd.DataFrame, metrics: list, title: str) -> Dict[str, Any]:
    """
    Create a chart comparing multiple metrics over time.
    
    Args:
        df: DataFrame containing the data
        metrics: List of metrics to compare
        title: Chart title
        
    Returns:
        Dictionary containing the Plotly figure
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    for i, metric in enumerate(metrics):
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df[metric],
                name=metric,
                line=dict(color=colors[i % len(colors)])
            ),
            secondary_y=(i > 0)
        )
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig.to_dict()

def create_metric_distribution_chart(df: pd.DataFrame, metric: str, title: str) -> Dict[str, Any]:
    """
    Create a distribution chart for a specific metric.
    
    Args:
        df: DataFrame containing the data
        metric: Name of the metric to plot
        title: Chart title
        
    Returns:
        Dictionary containing the Plotly figure
    """
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df[metric],
        nbinsx=30,
        name=metric,
        marker_color='#1f77b4'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title=metric,
        yaxis_title='Count',
        template='plotly_white'
    )
    
    return fig.to_dict()

def create_correlation_heatmap(df: pd.DataFrame, metrics: list, title: str) -> Dict[str, Any]:
    """
    Create a correlation heatmap for selected metrics.
    
    Args:
        df: DataFrame containing the data
        metrics: List of metrics to include in correlation
        title: Chart title
        
    Returns:
        Dictionary containing the Plotly figure
    """
    corr_matrix = df[metrics].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=metrics,
        y=metrics,
        colorscale='RdBu',
        zmid=0
    ))
    
    fig.update_layout(
        title=title,
        template='plotly_white'
    )
    
    return fig.to_dict() 