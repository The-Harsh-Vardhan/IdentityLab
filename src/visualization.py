"""
Visualization Module for UIDAI Hackathon

This module provides functions to create professional visualizations
for Aadhaar data analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional
import logging

# Configure plotting
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AadhaarVisualizer:
    """Class to create visualizations for Aadhaar data"""
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize the visualizer
        
        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = output_dir
        import os
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_time_series(self, df: pd.DataFrame, date_col: str, value_col: str,
                        title: str, save_path: Optional[str] = None) -> go.Figure:
        """
        Create an interactive time series plot
        
        Args:
            df: DataFrame with time series data
            date_col: Date column name
            value_col: Value column name
            title: Plot title
            save_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        logger.info(f"Creating time series plot for {value_col}")
        
        fig = px.line(df, x=date_col, y=value_col,
                     title=title,
                     labels={value_col: value_col.replace('_', ' ').title(),
                            date_col: 'Date'})
        
        fig.update_layout(
            hovermode='x unified',
            showlegend=True,
            template='plotly_white'
        )
        
        if save_path:
            fig.write_html(f"{self.output_dir}/{save_path}")
        
        return fig
    
    def plot_distribution(self, df: pd.DataFrame, column: str, 
                         title: str, save_path: Optional[str] = None) -> go.Figure:
        """
        Create a distribution plot (histogram + box plot)
        
        Args:
            df: DataFrame
            column: Column to plot
            title: Plot title
            save_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        logger.info(f"Creating distribution plot for {column}")
        
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.7, 0.3],
            subplot_titles=('Distribution', 'Box Plot'),
            vertical_spacing=0.1
        )
        
        # Histogram
        fig.add_trace(
            go.Histogram(x=df[column], name='Frequency', nbinsx=50),
            row=1, col=1
        )
        
        # Box plot
        fig.add_trace(
            go.Box(x=df[column], name='Box Plot', boxmean='sd'),
            row=2, col=1
        )
        
        fig.update_layout(
            title_text=title,
            showlegend=False,
            template='plotly_white'
        )
        
        if save_path:
            fig.write_html(f"{self.output_dir}/{save_path}")
        
        return fig
    
    def plot_top_n_bar(self, df: pd.DataFrame, category_col: str, 
                      value_col: str, n: int = 15, 
                      title: str = None, save_path: Optional[str] = None) -> go.Figure:
        """
        Create a bar chart for top N categories
        
        Args:
            df: DataFrame
            category_col: Category column
            value_col: Value column
            n: Number of top categories
            title: Plot title
            save_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        logger.info(f"Creating top {n} bar chart")
        
        # Get top N
        top_n = df.nlargest(n, value_col)
        
        fig = px.bar(top_n, x=value_col, y=category_col,
                    orientation='h',
                    title=title or f'Top {n} {category_col.title()}',
                    labels={value_col: value_col.replace('_', ' ').title(),
                           category_col: category_col.replace('_', ' ').title()})
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            template='plotly_white',
            height=max(400, n * 30)
        )
        
        if save_path:
            fig.write_html(f"{self.output_dir}/{save_path}")
        
        return fig
    
    def plot_heatmap(self, df: pd.DataFrame, columns: List[str],
                    title: str, save_path: Optional[str] = None) -> go.Figure:
        """
        Create a correlation heatmap
        
        Args:
            df: DataFrame
            columns: List of columns to include
            title: Plot title
            save_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        logger.info("Creating correlation heatmap")
        
        corr_matrix = df[columns].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title=title,
            template='plotly_white',
            width=800,
            height=700
        )
        
        if save_path:
            fig.write_html(f"{self.output_dir}/{save_path}")
        
        return fig
    
    def plot_geographical_map(self, df: pd.DataFrame, geo_col: str,
                             value_col: str, title: str,
                             save_path: Optional[str] = None) -> go.Figure:
        """
        Create a choropleth map for Indian states
        
        Args:
            df: DataFrame with state-level data
            geo_col: Geography column (should be 'state')
            value_col: Value column to visualize
            title: Plot title
            save_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        logger.info(f"Creating geographical map for {value_col}")
        
        # Note: For full implementation, you would need India GeoJSON data
        # This creates a basic choropleth
        fig = px.choropleth(
            df,
            locations=geo_col,
            locationmode='country names',
            color=value_col,
            hover_name=geo_col,
            hover_data=[value_col],
            title=title,
            color_continuous_scale='Viridis'
        )
        
        fig.update_geos(
            scope='asia',
            center=dict(lat=20.5937, lon=78.9629),
            projection_scale=4
        )
        
        fig.update_layout(
            template='plotly_white',
            height=600
        )
        
        if save_path:
            fig.write_html(f"{self.output_dir}/{save_path}")
        
        return fig
    
    def plot_seasonal_pattern(self, df: pd.DataFrame, value_col: str,
                            title: str, save_path: Optional[str] = None) -> go.Figure:
        """
        Create a seasonal pattern visualization
        
        Args:
            df: DataFrame with 'month' and value column
            value_col: Value column
            title: Plot title
            save_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        logger.info(f"Creating seasonal pattern plot for {value_col}")
        
        monthly_avg = df.groupby('month')[value_col].mean().reset_index()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_avg['month_name'] = monthly_avg['month'].apply(lambda x: month_names[x-1])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_avg['month_name'],
            y=monthly_avg[value_col],
            mode='lines+markers',
            name='Average',
            line=dict(width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Month',
            yaxis_title=value_col.replace('_', ' ').title(),
            template='plotly_white',
            hovermode='x unified'
        )
        
        if save_path:
            fig.write_html(f"{self.output_dir}/{save_path}")
        
        return fig
    
    def plot_comparison(self, df: pd.DataFrame, category_col: str,
                       value_cols: List[str], title: str,
                       save_path: Optional[str] = None) -> go.Figure:
        """
        Create a grouped bar chart for comparing multiple values
        
        Args:
            df: DataFrame
            category_col: Category column
            value_cols: List of value columns to compare
            title: Plot title
            save_path: Optional path to save HTML
            
        Returns:
            Plotly figure
        """
        logger.info(f"Creating comparison plot")
        
        fig = go.Figure()
        
        for col in value_cols:
            fig.add_trace(go.Bar(
                name=col.replace('_', ' ').title(),
                x=df[category_col],
                y=df[col]
            ))
        
        fig.update_layout(
            title=title,
            barmode='group',
            template='plotly_white',
            xaxis_title=category_col.replace('_', ' ').title(),
            yaxis_title='Count',
            legend_title='Category'
        )
        
        if save_path:
            fig.write_html(f"{self.output_dir}/{save_path}")
        
        return fig


def create_summary_dashboard(data_dict: Dict[str, pd.DataFrame], 
                             output_path: str = "outputs/dashboard.html"):
    """
    Create a comprehensive dashboard with multiple plots
    
    Args:
        data_dict: Dictionary with 'enrolment', 'demographic', 'biometric' DataFrames
        output_path: Path to save the dashboard HTML
    """
    logger.info("Creating summary dashboard")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Enrolments Over Time', 'Demographic Updates Over Time',
                       'Biometric Updates Over Time', 'State-wise Comparison'),
        specs=[[{"type": "scatter"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # Add traces for each dataset
    # This is a template - you'll need to customize based on your cleaned data
    
    fig.update_layout(
        title_text="Aadhaar Data Analysis Dashboard",
        showlegend=True,
        height=800,
        template='plotly_white'
    )
    
    fig.write_html(output_path)
    logger.info(f"Dashboard saved to {output_path}")


if __name__ == "__main__":
    print("Visualization module loaded successfully")
