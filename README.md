# IdentityLab

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Hackathon](https://img.shields.io/badge/UIDAI-Hackathon%202026-orange.svg)](https://uidai.gov.in/)

> *Research-grade analytics for India's digital identity ecosystem*

## Overview
IdentityLab is a comprehensive data analysis platform for UIDAI Aadhaar enrollment, demographic, and biometric data. Built to uncover actionable insights in identity access and adoption patterns, this platform analyzes ~5 million records to identify trends, detect anomalies, and support evidence-based policy decisions.

## Features
- 🔄 **Automated Data Loading**: Seamlessly load and combine multiple CSV files
- 🧹 **Data Preprocessing**: Clean, validate, and transform raw data with built-in quality checks
- 📊 **Statistical Analysis**: Univariate, bivariate, and multivariate analysis tools
- 📈 **Advanced Visualizations**: Interactive charts with Plotly, Seaborn, and Matplotlib
- 🗺️ **Geospatial Analysis**: District and state-level mapping capabilities
- ⏱️ **Time Series Analysis**: Temporal pattern detection and forecasting

## Project Structure
```
├── Dataset/                          # Raw CSV data files
│   ├── api_data_aadhar_biometric/
│   ├── api_data_aadhar_demographic/
│   └── api_data_aadhar_enrolment/
├── notebooks/                        # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_analysis.ipynb
│   └── 04_visualization.ipynb
├── src/                              # Source code modules
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── analysis.py
│   └── visualization.py
├── outputs/                          # Generated visualizations and reports
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/Rakshit-2005/IdentityLab.git
cd IdentityLab

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Register Jupyter kernel (optional)
python -m ipykernel install --user --name=identity-lab --display-name "IdentityLab"
```

### Quick Start

```python
# Load data
from src.data_loader import AadhaarDataLoader

loader = AadhaarDataLoader('.')
df_enrolment = loader.load_enrolment_data()
df_demographic = loader.load_demographic_data()
df_biometric = loader.load_biometric_data()

# Preprocess
from src.preprocessing import AadhaarDataPreprocessor

preprocessor = AadhaarDataPreprocessor()
df_clean = preprocessor.clean_enrolment_data(df_enrolment)

# Analyze
from src.analysis import AadhaarAnalyzer

analyzer = AadhaarAnalyzer()
stats = analyzer.univariate_analysis(df_clean, 'total_enrolments')
staModules

### `data_loader.py`
- Load and combine multiple CSV files
- Automatic data type detection
- Memory-efficient loading with optional Dask support

### `preprocessing.py`
- Data cleaning and validation
- Date normalization
- Outlier detection (IQR and Z-score methods)
- Feature engineering (temporal features, totals, ratios)

### `analysis.py`
- Univariate statistics (mean, median, skewness, kurtosis)
- Bivariate analysis (correlation, statistical tests)
- Temporal aggregation (daily, weekly, monthly)
- Geographical aggregation (state, district, pincode)
- Seasonality detection
- Growth rate calculation

### `visualization.py`
- Interactive time series plots
- Distribution analysis (histograms, box plots)
- Top N bar charts
- Correlation heatmaps
- Geospatial choropleth maps
- Seasonal pattern visualization
viz = AadhaarVisualizer(output_dir="outputs")
fig = viz.plot_time_series(df_clean, 'date', 'total_enrolments', 'Enrolments Over Time')
```

### Running Notebooks
```bash
# Start Jupyter
jupyter notebook

# Open notebooks in sequence:
# 1. notebooks/01_data_exploration.ipynb
# 2. notebooks/02_data_cleaning.ipynb
# 3. notebooks/03_analysis.ipynb
# 4. notebooks/04_visualization.ipynb
```

## Data Description

### Enrolment Data (~1M records)
- New Aadhaar registrations by date, location, and age group
- FContributing
Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author
**Rakshit Modanwal**
- GitHub: [@Rakshit-2005](https://github.com/Rakshit-2005)

## Acknowledgments
- UIDAI for providing the hackathon opportunity and datasets
- Open-source community for the amazing data science tools

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This project was developed for the UIDAI Hackathon 2026. The datasets used are for educational and analytical purposes.strict, pincode, bio_age_5_17, bio_age_17_

## Key Findings
[To be populated after analysis]

## Methodology
[To be documented]

## Technologies Used
- **Data Processing**: Pandas, NumPy, Dask
- **Statistical Analysis**: SciPy, Statsmodels, Scikit-learn
- **Time Series**: Prophet
- **Visualization**: Plotly, Seaborn, Matplotlib, Folium
- **Geospatial**: GeoPandas

## Team Members
Rakshit Modanwal
Github : https://github.com/Rakshit-2005

## License
This project is created for the UIDAI Hackathon 2026.

## Contact
[Add contact information]
