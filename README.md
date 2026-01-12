# UIDAI Hackathon - Aadhaar Data Analysis

## Project Overview
This project analyzes Aadhaar enrolment, demographic update, and biometric update data to uncover meaningful patterns, trends, and actionable insights for UIDAI system improvements.

## Problem Statement
[To be defined based on chosen focus area]

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
1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Analysis
1. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
2. Open notebooks in the `notebooks/` folder sequentially
3. Run cells to reproduce analysis

## Data Description

### Enrolment Data (~1M records)
- New Aadhaar registrations by date, location, and age group
- Fields: date, state, district, pincode, age_0_5, age_5_17, age_18_greater

### Demographic Update Data (~2M records)
- Demographic information updates (address, name, DOB changes)
- Fields: date, state, district, pincode, demo_age_5_17, demo_age_17_

### Biometric Update Data (~1.8M records)
- Biometric data updates (fingerprint, iris, photo)
- Fields: date, state, district, pincode, bio_age_5_17, bio_age_17_

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
[Add your team information]

## License
This project is created for the UIDAI Hackathon 2026.

## Contact
[Add contact information]
