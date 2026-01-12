"""
Data Preprocessing Module for UIDAI Hackathon

This module provides functions to clean, transform, and prepare Aadhaar data for analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AadhaarDataPreprocessor:
    """Class to handle preprocessing of Aadhaar datasets"""
    
    def __init__(self):
        """Initialize the preprocessor"""
        self.cleaning_report = {}
    
    def clean_enrolment_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess enrolment data
        
        Args:
            df: Raw enrolment DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning enrolment data...")
        df_clean = df.copy()
        
        # Store initial shape
        initial_rows = len(df_clean)
        
        # Convert date column to datetime
        df_clean['date'] = pd.to_datetime(df_clean['date'], format='%d-%m-%Y', errors='coerce')
        
        # Remove rows with invalid dates
        invalid_dates = df_clean['date'].isnull().sum()
        df_clean = df_clean.dropna(subset=['date'])
        
        # Clean string columns
        string_cols = ['state', 'district']
        for col in string_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].str.strip().str.title()
        
        # Convert pincode to string and ensure 6 digits
        if 'pincode' in df_clean.columns:
            df_clean['pincode'] = df_clean['pincode'].astype(str).str.zfill(6)
            # Remove invalid pincodes (not 6 digits)
            df_clean = df_clean[df_clean['pincode'].str.len() == 6]
        
        # Ensure age columns are numeric and non-negative
        age_cols = ['age_0_5', 'age_5_17', 'age_18_greater']
        for col in age_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].fillna(0).clip(lower=0)
        
        # Add total enrolment column
        if all(col in df_clean.columns for col in age_cols):
            df_clean['total_enrolments'] = df_clean[age_cols].sum(axis=1)
        
        # Remove rows with zero total enrolments
        zero_enrolments = (df_clean['total_enrolments'] == 0).sum()
        df_clean = df_clean[df_clean['total_enrolments'] > 0]
        
        # Add temporal features
        df_clean['year'] = df_clean['date'].dt.year
        df_clean['month'] = df_clean['date'].dt.month
        df_clean['day_of_week'] = df_clean['date'].dt.dayofweek
        df_clean['week_of_year'] = df_clean['date'].dt.isocalendar().week
        
        # Store cleaning report
        self.cleaning_report['enrolment'] = {
            'initial_rows': initial_rows,
            'final_rows': len(df_clean),
            'rows_removed': initial_rows - len(df_clean),
            'invalid_dates': invalid_dates,
            'zero_enrolments': zero_enrolments
        }
        
        logger.info(f"Enrolment data cleaned: {initial_rows:,} -> {len(df_clean):,} rows")
        return df_clean
    
    def clean_demographic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess demographic update data
        
        Args:
            df: Raw demographic DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning demographic update data...")
        df_clean = df.copy()
        
        initial_rows = len(df_clean)
        
        # Convert date column to datetime
        df_clean['date'] = pd.to_datetime(df_clean['date'], format='%d-%m-%Y', errors='coerce')
        
        # Remove rows with invalid dates
        invalid_dates = df_clean['date'].isnull().sum()
        df_clean = df_clean.dropna(subset=['date'])
        
        # Clean string columns
        string_cols = ['state', 'district']
        for col in string_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].str.strip().str.title()
        
        # Convert pincode to string and ensure 6 digits
        if 'pincode' in df_clean.columns:
            df_clean['pincode'] = df_clean['pincode'].astype(str).str.zfill(6)
            df_clean = df_clean[df_clean['pincode'].str.len() == 6]
        
        # Ensure demographic columns are numeric and non-negative
        demo_cols = ['demo_age_5_17', 'demo_age_17_']
        for col in demo_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].fillna(0).clip(lower=0)
        
        # Add total updates column
        if all(col in df_clean.columns for col in demo_cols):
            df_clean['total_demo_updates'] = df_clean[demo_cols].sum(axis=1)
        
        # Remove rows with zero total updates
        zero_updates = (df_clean['total_demo_updates'] == 0).sum()
        df_clean = df_clean[df_clean['total_demo_updates'] > 0]
        
        # Add temporal features
        df_clean['year'] = df_clean['date'].dt.year
        df_clean['month'] = df_clean['date'].dt.month
        df_clean['day_of_week'] = df_clean['date'].dt.dayofweek
        df_clean['week_of_year'] = df_clean['date'].dt.isocalendar().week
        
        # Store cleaning report
        self.cleaning_report['demographic'] = {
            'initial_rows': initial_rows,
            'final_rows': len(df_clean),
            'rows_removed': initial_rows - len(df_clean),
            'invalid_dates': invalid_dates,
            'zero_updates': zero_updates
        }
        
        logger.info(f"Demographic data cleaned: {initial_rows:,} -> {len(df_clean):,} rows")
        return df_clean
    
    def clean_biometric_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess biometric update data
        
        Args:
            df: Raw biometric DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning biometric update data...")
        df_clean = df.copy()
        
        initial_rows = len(df_clean)
        
        # Convert date column to datetime
        df_clean['date'] = pd.to_datetime(df_clean['date'], format='%d-%m-%Y', errors='coerce')
        
        # Remove rows with invalid dates
        invalid_dates = df_clean['date'].isnull().sum()
        df_clean = df_clean.dropna(subset=['date'])
        
        # Clean string columns
        string_cols = ['state', 'district']
        for col in string_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].str.strip().str.title()
        
        # Convert pincode to string and ensure 6 digits
        if 'pincode' in df_clean.columns:
            df_clean['pincode'] = df_clean['pincode'].astype(str).str.zfill(6)
            df_clean = df_clean[df_clean['pincode'].str.len() == 6]
        
        # Ensure biometric columns are numeric and non-negative
        bio_cols = ['bio_age_5_17', 'bio_age_17_']
        for col in bio_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].fillna(0).clip(lower=0)
        
        # Add total updates column
        if all(col in df_clean.columns for col in bio_cols):
            df_clean['total_bio_updates'] = df_clean[bio_cols].sum(axis=1)
        
        # Remove rows with zero total updates
        zero_updates = (df_clean['total_bio_updates'] == 0).sum()
        df_clean = df_clean[df_clean['total_bio_updates'] > 0]
        
        # Add temporal features
        df_clean['year'] = df_clean['date'].dt.year
        df_clean['month'] = df_clean['date'].dt.month
        df_clean['day_of_week'] = df_clean['date'].dt.dayofweek
        df_clean['week_of_year'] = df_clean['date'].dt.isocalendar().week
        
        # Store cleaning report
        self.cleaning_report['biometric'] = {
            'initial_rows': initial_rows,
            'final_rows': len(df_clean),
            'rows_removed': initial_rows - len(df_clean),
            'invalid_dates': invalid_dates,
            'zero_updates': zero_updates
        }
        
        logger.info(f"Biometric data cleaned: {initial_rows:,} -> {len(df_clean):,} rows")
        return df_clean
    
    def get_cleaning_report(self) -> Dict:
        """
        Get the cleaning report
        
        Returns:
            Dictionary with cleaning statistics
        """
        return self.cleaning_report
    
    def print_cleaning_report(self) -> None:
        """Print a formatted cleaning report"""
        print("\n" + "="*60)
        print("DATA CLEANING REPORT")
        print("="*60)
        
        for dataset_name, stats in self.cleaning_report.items():
            print(f"\n{dataset_name.upper()} Dataset:")
            print(f"  Initial rows: {stats['initial_rows']:,}")
            print(f"  Final rows: {stats['final_rows']:,}")
            print(f"  Rows removed: {stats['rows_removed']:,} ({stats['rows_removed']/stats['initial_rows']*100:.2f}%)")
            print(f"  Invalid dates: {stats.get('invalid_dates', 0):,}")
            print(f"  Zero counts: {stats.get('zero_enrolments', stats.get('zero_updates', 0)):,}")


def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr', threshold: float = 3.0) -> pd.Series:
    """
    Detect outliers in a numeric column
    
    Args:
        df: DataFrame
        column: Column name to check for outliers
        method: 'iqr' or 'zscore'
        threshold: IQR multiplier or Z-score threshold
        
    Returns:
        Boolean Series indicating outliers
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return (df[column] < lower_bound) | (df[column] > upper_bound)
    
    elif method == 'zscore':
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        return z_scores > threshold
    
    else:
        raise ValueError(f"Invalid method: {method}")


if __name__ == "__main__":
    # Example usage
    print("Preprocessing module loaded successfully")
