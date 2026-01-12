"""
Analysis Module for UIDAI Hackathon

This module provides functions for statistical analysis, time-series analysis,
and pattern detection in Aadhaar data.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AadhaarAnalyzer:
    """Class to perform various analyses on Aadhaar data"""
    
    def __init__(self):
        """Initialize the analyzer"""
        self.analysis_results = {}
    
    def univariate_analysis(self, df: pd.DataFrame, column: str) -> Dict:
        """
        Perform univariate analysis on a column
        
        Args:
            df: DataFrame
            column: Column name to analyze
            
        Returns:
            Dictionary with statistical measures
        """
        logger.info(f"Performing univariate analysis on {column}")
        
        results = {
            'count': df[column].count(),
            'mean': df[column].mean(),
            'median': df[column].median(),
            'std': df[column].std(),
            'min': df[column].min(),
            'max': df[column].max(),
            'q25': df[column].quantile(0.25),
            'q75': df[column].quantile(0.75),
            'skewness': df[column].skew(),
            'kurtosis': df[column].kurtosis()
        }
        
        return results
    
    def bivariate_analysis(self, df: pd.DataFrame, col1: str, col2: str) -> Dict:
        """
        Perform bivariate analysis between two columns
        
        Args:
            df: DataFrame
            col1: First column name
            col2: Second column name
            
        Returns:
            Dictionary with correlation and statistical tests
        """
        logger.info(f"Performing bivariate analysis: {col1} vs {col2}")
        
        # Pearson correlation
        pearson_corr, pearson_pval = stats.pearsonr(df[col1].dropna(), df[col2].dropna())
        
        # Spearman correlation
        spearman_corr, spearman_pval = stats.spearmanr(df[col1].dropna(), df[col2].dropna())
        
        results = {
            'pearson_correlation': pearson_corr,
            'pearson_pvalue': pearson_pval,
            'spearman_correlation': spearman_corr,
            'spearman_pvalue': spearman_pval,
            'significant': pearson_pval < 0.05
        }
        
        return results
    
    def temporal_aggregation(self, df: pd.DataFrame, value_col: str, 
                            freq: str = 'D') -> pd.DataFrame:
        """
        Aggregate data by time period
        
        Args:
            df: DataFrame with 'date' column
            value_col: Column to aggregate
            freq: Frequency ('D'=daily, 'W'=weekly, 'M'=monthly)
            
        Returns:
            Aggregated DataFrame
        """
        logger.info(f"Aggregating {value_col} by {freq}")
        
        df_agg = df.groupby(pd.Grouper(key='date', freq=freq)).agg({
            value_col: ['sum', 'mean', 'count']
        }).reset_index()
        
        df_agg.columns = ['date', f'{value_col}_sum', f'{value_col}_mean', 'count']
        
        return df_agg
    
    def geographical_aggregation(self, df: pd.DataFrame, level: str, 
                                 value_col: str) -> pd.DataFrame:
        """
        Aggregate data by geographical level
        
        Args:
            df: DataFrame
            level: 'state', 'district', or 'pincode'
            value_col: Column to aggregate
            
        Returns:
            Aggregated DataFrame
        """
        logger.info(f"Aggregating {value_col} by {level}")
        
        df_agg = df.groupby(level).agg({
            value_col: ['sum', 'mean', 'count']
        }).reset_index()
        
        df_agg.columns = [level, f'{value_col}_sum', f'{value_col}_mean', 'count']
        df_agg = df_agg.sort_values(f'{value_col}_sum', ascending=False)
        
        return df_agg
    
    def calculate_growth_rate(self, df: pd.DataFrame, value_col: str, 
                             periods: int = 1) -> pd.DataFrame:
        """
        Calculate period-over-period growth rate
        
        Args:
            df: DataFrame with time series data
            value_col: Column to calculate growth for
            periods: Number of periods to shift
            
        Returns:
            DataFrame with growth rate column added
        """
        df_copy = df.copy()
        df_copy[f'{value_col}_growth'] = df_copy[value_col].pct_change(periods=periods) * 100
        
        return df_copy
    
    def detect_seasonality(self, df: pd.DataFrame, value_col: str) -> Dict:
        """
        Detect seasonal patterns in time series data
        
        Args:
            df: DataFrame with 'date' and value column
            value_col: Column to analyze for seasonality
            
        Returns:
            Dictionary with seasonality statistics
        """
        logger.info(f"Detecting seasonality in {value_col}")
        
        # Aggregate by month
        df['month'] = df['date'].dt.month
        monthly_avg = df.groupby('month')[value_col].mean()
        
        # Calculate coefficient of variation
        cv = (monthly_avg.std() / monthly_avg.mean()) * 100
        
        results = {
            'monthly_averages': monthly_avg.to_dict(),
            'peak_month': monthly_avg.idxmax(),
            'low_month': monthly_avg.idxmin(),
            'coefficient_of_variation': cv,
            'has_strong_seasonality': cv > 20  # Arbitrary threshold
        }
        
        return results
    
    def top_n_analysis(self, df: pd.DataFrame, group_col: str, 
                      value_col: str, n: int = 10) -> pd.DataFrame:
        """
        Get top N groups by a value column
        
        Args:
            df: DataFrame
            group_col: Column to group by
            value_col: Column to rank by
            n: Number of top groups to return
            
        Returns:
            DataFrame with top N groups
        """
        top_n = df.groupby(group_col)[value_col].sum().nlargest(n).reset_index()
        top_n.columns = [group_col, f'total_{value_col}']
        
        return top_n
    
    def calculate_update_ratio(self, enrolment_df: pd.DataFrame, 
                               update_df: pd.DataFrame,
                               geo_level: str = 'state') -> pd.DataFrame:
        """
        Calculate the ratio of updates to enrolments by geography
        
        Args:
            enrolment_df: Enrolment DataFrame
            update_df: Update DataFrame (demographic or biometric)
            geo_level: Geographical level to aggregate
            
        Returns:
            DataFrame with update ratios
        """
        logger.info(f"Calculating update ratio at {geo_level} level")
        
        # Aggregate enrolments
        enrol_agg = enrolment_df.groupby(geo_level)['total_enrolments'].sum()
        
        # Determine update column
        update_col = 'total_demo_updates' if 'total_demo_updates' in update_df.columns else 'total_bio_updates'
        
        # Aggregate updates
        update_agg = update_df.groupby(geo_level)[update_col].sum()
        
        # Combine and calculate ratio
        ratio_df = pd.DataFrame({
            'enrolments': enrol_agg,
            'updates': update_agg
        }).fillna(0)
        
        ratio_df['update_ratio'] = (ratio_df['updates'] / ratio_df['enrolments'] * 100).round(2)
        ratio_df = ratio_df.sort_values('update_ratio', ascending=False).reset_index()
        
        return ratio_df


def perform_chi_square_test(df: pd.DataFrame, cat_col1: str, cat_col2: str) -> Dict:
    """
    Perform chi-square test for independence between two categorical variables
    
    Args:
        df: DataFrame
        cat_col1: First categorical column
        cat_col2: Second categorical column
        
    Returns:
        Dictionary with test results
    """
    contingency_table = pd.crosstab(df[cat_col1], df[cat_col2])
    chi2, pvalue, dof, expected = stats.chi2_contingency(contingency_table)
    
    return {
        'chi2_statistic': chi2,
        'p_value': pvalue,
        'degrees_of_freedom': dof,
        'significant': pvalue < 0.05
    }


def calculate_concentration_index(df: pd.DataFrame, value_col: str) -> float:
    """
    Calculate Gini coefficient to measure concentration/inequality
    
    Args:
        df: DataFrame
        value_col: Column to calculate concentration for
        
    Returns:
        Gini coefficient (0 = perfect equality, 1 = perfect inequality)
    """
    values = df[value_col].sort_values().values
    n = len(values)
    cumsum = np.cumsum(values)
    
    gini = (2 * np.sum((np.arange(1, n+1) * values))) / (n * cumsum[-1]) - (n + 1) / n
    
    return gini


if __name__ == "__main__":
    print("Analysis module loaded successfully")
