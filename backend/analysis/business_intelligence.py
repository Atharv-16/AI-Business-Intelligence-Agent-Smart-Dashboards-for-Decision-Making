import pandas as pd
from typing import Dict, List, Any
from datetime import datetime, timedelta
from ..visualization.plotly_charts import (
    create_time_series_chart,
    create_metric_comparison_chart,
    create_metric_distribution_chart,
    create_correlation_heatmap
)

class BusinessIntelligenceAnalyzer:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the analyzer with a DataFrame containing business metrics.
        
        Args:
            df: DataFrame containing business metrics with a 'date' column
        """
        self.df = df.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
        
    def analyze_trends(self, metric: str, window: int = 7) -> Dict[str, Any]:
        """
        Analyze trends for a specific metric using moving averages.
        
        Args:
            metric: Name of the metric to analyze
            window: Window size for moving average calculation
            
        Returns:
            Dictionary containing analysis results and visualizations
        """
        # Calculate moving average
        self.df[f'{metric}_ma'] = self.df[metric].rolling(window=window).mean()
        
        # Calculate trend direction
        latest_value = self.df[metric].iloc[-1]
        previous_value = self.df[metric].iloc[-window]
        trend_direction = "increasing" if latest_value > previous_value else "decreasing"
        
        # Create visualization
        fig = create_time_series_chart(
            self.df,
            metric,
            f"{metric} Trend Analysis"
        )
        
        return {
            "trend_direction": trend_direction,
            "latest_value": latest_value,
            "previous_value": previous_value,
            "percentage_change": ((latest_value - previous_value) / previous_value) * 100,
            "visualization": fig
        }
    
    def compare_metrics(self, metrics: List[str]) -> Dict[str, Any]:
        """
        Compare multiple metrics and their relationships.
        
        Args:
            metrics: List of metrics to compare
            
        Returns:
            Dictionary containing analysis results and visualizations
        """
        # Calculate correlations
        correlations = self.df[metrics].corr()
        
        # Create visualizations
        comparison_chart = create_metric_comparison_chart(
            self.df,
            metrics,
            "Metric Comparison"
        )
        
        correlation_heatmap = create_correlation_heatmap(
            self.df,
            metrics,
            "Metric Correlations"
        )
        
        return {
            "correlations": correlations.to_dict(),
            "comparison_chart": comparison_chart,
            "correlation_heatmap": correlation_heatmap
        }
    
    def analyze_distribution(self, metric: str) -> Dict[str, Any]:
        """
        Analyze the distribution of a metric.
        
        Args:
            metric: Name of the metric to analyze
            
        Returns:
            Dictionary containing analysis results and visualizations
        """
        # Calculate distribution statistics
        stats = {
            "mean": self.df[metric].mean(),
            "median": self.df[metric].median(),
            "std": self.df[metric].std(),
            "min": self.df[metric].min(),
            "max": self.df[metric].max()
        }
        
        # Create visualization
        distribution_chart = create_metric_distribution_chart(
            self.df,
            metric,
            f"{metric} Distribution"
        )
        
        return {
            "statistics": stats,
            "visualization": distribution_chart
        }
    
    def detect_anomalies(self, metric: str, threshold: float = 2.0) -> Dict[str, Any]:
        """
        Detect anomalies in a metric using z-score method.
        
        Args:
            metric: Name of the metric to analyze
            threshold: Z-score threshold for anomaly detection
            
        Returns:
            Dictionary containing analysis results and visualizations
        """
        # Calculate z-scores
        mean = self.df[metric].mean()
        std = self.df[metric].std()
        self.df[f'{metric}_zscore'] = (self.df[metric] - mean) / std
        
        # Identify anomalies
        anomalies = self.df[self.df[f'{metric}_zscore'].abs() > threshold]
        
        # Create visualization
        fig = create_time_series_chart(
            self.df,
            metric,
            f"{metric} with Anomalies"
        )
        
        return {
            "anomaly_count": len(anomalies),
            "anomaly_dates": anomalies['date'].dt.strftime('%Y-%m-%d').tolist(),
            "anomaly_values": anomalies[metric].tolist(),
            "visualization": fig
        }
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive business intelligence report.
        
        Returns:
            Dictionary containing the complete analysis report
        """
        metrics = ['revenue', 'users', 'conversion_rate', 'average_order_value']
        
        report = {
            "trend_analysis": {},
            "metric_comparison": self.compare_metrics(metrics),
            "distributions": {},
            "anomalies": {}
        }
        
        # Analyze trends for each metric
        for metric in metrics:
            report["trend_analysis"][metric] = self.analyze_trends(metric)
            report["distributions"][metric] = self.analyze_distribution(metric)
            report["anomalies"][metric] = self.detect_anomalies(metric)
        
        return report 