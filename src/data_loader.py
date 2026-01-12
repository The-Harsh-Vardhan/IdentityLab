"""
Data Loader Module for UIDAI Hackathon

This module provides functions to load and combine Aadhaar data from multiple CSV files.
"""

import pandas as pd
import glob
import os
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AadhaarDataLoader:
    """Class to handle loading of Aadhaar datasets"""
    
    def __init__(self, base_path: str):
        """
        Initialize the data loader
        
        Args:
            base_path: Base directory containing Dataset folder
        """
        self.base_path = Path(base_path)
        self.dataset_path = self.base_path / "Dataset"
        
        if not self.dataset_path.exists():
            raise ValueError(f"Dataset path not found: {self.dataset_path}")
    
    def load_enrolment_data(self, use_dask: bool = False) -> pd.DataFrame:
        """
        Load all enrolment CSV files and combine them
        
        Args:
            use_dask: If True, use Dask for large file handling
            
        Returns:
            Combined DataFrame with all enrolment data
        """
        logger.info("Loading enrolment data...")
        enrolment_path = self.dataset_path / "api_data_aadhar_enrolment"
        csv_files = glob.glob(str(enrolment_path / "*.csv"))
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {enrolment_path}")
        
        logger.info(f"Found {len(csv_files)} enrolment files")
        
        if use_dask:
            import dask.dataframe as dd
            df = dd.read_csv(csv_files)
            df = df.compute()
        else:
            dfs = []
            for file in csv_files:
                logger.info(f"Reading {os.path.basename(file)}")
                dfs.append(pd.read_csv(file))
            df = pd.concat(dfs, ignore_index=True)
        
        logger.info(f"Loaded {len(df):,} enrolment records")
        return df
    
    def load_demographic_data(self, use_dask: bool = False) -> pd.DataFrame:
        """
        Load all demographic update CSV files and combine them
        
        Args:
            use_dask: If True, use Dask for large file handling
            
        Returns:
            Combined DataFrame with all demographic update data
        """
        logger.info("Loading demographic update data...")
        demographic_path = self.dataset_path / "api_data_aadhar_demographic"
        csv_files = glob.glob(str(demographic_path / "*.csv"))
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {demographic_path}")
        
        logger.info(f"Found {len(csv_files)} demographic files")
        
        if use_dask:
            import dask.dataframe as dd
            df = dd.read_csv(csv_files)
            df = df.compute()
        else:
            dfs = []
            for file in csv_files:
                logger.info(f"Reading {os.path.basename(file)}")
                dfs.append(pd.read_csv(file))
            df = pd.concat(dfs, ignore_index=True)
        
        logger.info(f"Loaded {len(df):,} demographic update records")
        return df
    
    def load_biometric_data(self, use_dask: bool = False) -> pd.DataFrame:
        """
        Load all biometric update CSV files and combine them
        
        Args:
            use_dask: If True, use Dask for large file handling
            
        Returns:
            Combined DataFrame with all biometric update data
        """
        logger.info("Loading biometric update data...")
        biometric_path = self.dataset_path / "api_data_aadhar_biometric"
        csv_files = glob.glob(str(biometric_path / "*.csv"))
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {biometric_path}")
        
        logger.info(f"Found {len(csv_files)} biometric files")
        
        if use_dask:
            import dask.dataframe as dd
            df = dd.read_csv(csv_files)
            df = df.compute()
        else:
            dfs = []
            for file in csv_files:
                logger.info(f"Reading {os.path.basename(file)}")
                dfs.append(pd.read_csv(file))
            df = pd.concat(dfs, ignore_index=True)
        
        logger.info(f"Loaded {len(df):,} biometric update records")
        return df
    
    def load_all_data(self, use_dask: bool = False) -> Dict[str, pd.DataFrame]:
        """
        Load all three datasets
        
        Args:
            use_dask: If True, use Dask for large file handling
            
        Returns:
            Dictionary with keys 'enrolment', 'demographic', 'biometric'
        """
        logger.info("Loading all datasets...")
        
        data = {
            'enrolment': self.load_enrolment_data(use_dask),
            'demographic': self.load_demographic_data(use_dask),
            'biometric': self.load_biometric_data(use_dask)
        }
        
        logger.info("All datasets loaded successfully")
        return data
    
    def get_data_summary(self, df: pd.DataFrame, name: str) -> None:
        """
        Print summary statistics for a dataset
        
        Args:
            df: DataFrame to summarize
            name: Name of the dataset
        """
        print(f"\n{'='*60}")
        print(f"Summary for {name.upper()} Dataset")
        print(f"{'='*60}")
        print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nData Types:\n{df.dtypes}")
        print(f"\nMemory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"\nMissing Values:\n{df.isnull().sum()}")
        print(f"\nSample Data:")
        print(df.head())


def quick_load(base_path: str, dataset_type: str = 'all', use_dask: bool = False):
    """
    Quick function to load datasets
    
    Args:
        base_path: Base directory containing Dataset folder
        dataset_type: 'enrolment', 'demographic', 'biometric', or 'all'
        use_dask: If True, use Dask for large file handling
        
    Returns:
        DataFrame or dictionary of DataFrames
    """
    loader = AadhaarDataLoader(base_path)
    
    if dataset_type == 'enrolment':
        return loader.load_enrolment_data(use_dask)
    elif dataset_type == 'demographic':
        return loader.load_demographic_data(use_dask)
    elif dataset_type == 'biometric':
        return loader.load_biometric_data(use_dask)
    elif dataset_type == 'all':
        return loader.load_all_data(use_dask)
    else:
        raise ValueError(f"Invalid dataset_type: {dataset_type}")


if __name__ == "__main__":
    # Example usage
    base_path = r"c:\Users\harsh\OneDrive - Indian Institute of Information Technology, Nagpur\IIIT Nagpur\6th Semester\Projects\UIDAI Hackathon"
    
    loader = AadhaarDataLoader(base_path)
    
    # Load one dataset as example
    enrolment_df = loader.load_enrolment_data()
    loader.get_data_summary(enrolment_df, "Enrolment")
