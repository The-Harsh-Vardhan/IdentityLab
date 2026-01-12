# GitHub Copilot Instructions for IdentityLab

## Project Overview
IdentityLab is a research-grade analytics platform for analyzing UIDAI Aadhaar enrollment, demographic, and biometric datasets (~5M records). Built for the UIDAI Hackathon 2026, it provides a complete data pipeline from loading through visualization.

## Architecture & Data Flow

### Core Pipeline (Sequential Execution)
1. **Data Loading** ([src/data_loader.py](../src/data_loader.py)): Combine multiple CSVs from `Dataset/` subdirectories
2. **Preprocessing** ([src/preprocessing.py](../src/preprocessing.py)): Clean, validate, and engineer features
3. **Analysis** ([src/analysis.py](../src/analysis.py)): Statistical, temporal, and geographical aggregation
4. **Visualization** ([src/visualization.py](../src/visualization.py)): Generate interactive plots to `outputs/`

### Class-Based Module Structure
- `AadhaarDataLoader`: Load enrolment/demographic/biometric CSVs with optional Dask support
- `AadhaarDataPreprocessor`: Date normalization, outlier detection (IQR/Z-score), feature engineering
- `AadhaarAnalyzer`: Univariate/bivariate analysis, temporal/geo aggregation, seasonality detection
- `AadhaarVisualizer`: Plotly/Seaborn/Folium visualizations with consistent `plotly_white` template

## Code Conventions & Patterns

### Naming Standards
- **Column names**: Lowercase with underscores (e.g., `total_enrolments`, `bio_age_5_17`)
- **Method names**: Verb-first descriptive names (`clean_enrolment_data`, `detect_seasonality`)
- **Feature columns**: Pattern `{metric}_{aggregation}` (e.g., `total_enrolments_sum`, `total_enrolments_mean`)

### Date Handling (Critical Pattern)
```python
# Always use this format - data files use dd-mm-yyyy
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')

# Temporal features (standard across all datasets)
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['week_of_year'] = df['date'].dt.isocalendar().week
```

### Data Cleaning Pipeline (Consistent Across Datasets)
1. Convert dates with `pd.to_datetime(..., format='%d-%m-%Y', errors='coerce')`
2. Strip and title-case string columns (`state`, `district`)
3. Normalize pincodes to 6-digit zero-padded strings
4. Convert numeric columns with `pd.to_numeric(..., errors='coerce')`, fill NaN with 0, clip negative values
5. Calculate totals across age group columns
6. Remove zero-count rows
7. Add temporal features

### Age Group Column Patterns
- **Enrolment**: `age_0_5`, `age_5_17`, `age_18_greater` → `total_enrolments`
- **Demographic**: `demo_age_5_17`, `demo_age_17_` (incomplete in data) → `total_demo_updates`
- **Biometric**: `bio_age_5_17`, `bio_age_17_` (incomplete in data) → `total_bio_updates`

### Aggregation Keys (Standard Groupings)
Common dimensions: `['date', 'state', 'district', 'pincode']`
```python
# Temporal: Use pd.Grouper with freq='D'/'W'/'M'
df.groupby(pd.Grouper(key='date', freq='M')).agg({...})

# Geographical: Direct groupby with value aggregations
df.groupby('state').agg({value_col: ['sum', 'mean', 'count']})
```

### Outlier Detection Methods
```python
# IQR method (default threshold=3.0)
detect_outliers(df, 'total_enrolments', method='iqr', threshold=3.0)

# Z-score method (default threshold=3.0)
detect_outliers(df, 'total_enrolments', method='zscore', threshold=3.0)
```

### Visualization Standards
- Use Plotly for interactive charts (template: `'plotly_white'`)
- Save all outputs to `outputs/` directory with descriptive filenames
- Include `hovermode='x unified'` for time series plots
- Use `make_subplots` for multi-panel figures
- Geospatial maps use Folium with state/district-level GeoJSON

## Development Workflow

### Environment Setup (Windows-specific)
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m ipykernel install --user --name=identity-lab
```

### Notebook Execution Order
Work sequentially through notebooks (each builds on previous):
1. [notebooks/01_data_exploration.ipynb](../notebooks/01_data_exploration.ipynb)
2. [notebooks/02_data_cleaning.ipynb](../notebooks/02_data_cleaning.ipynb)
3. [notebooks/03_analysis.ipynb](../notebooks/03_analysis.ipynb)
4. [notebooks/04_visualization.ipynb](../notebooks/04_visualization.ipynb)

### Typical Usage Pattern
```python
# Step 1: Load
loader = AadhaarDataLoader('.')
df_enrolment = loader.load_enrolment_data()

# Step 2: Clean
preprocessor = AadhaarDataPreprocessor()
df_clean = preprocessor.clean_enrolment_data(df_enrolment)
preprocessor.print_cleaning_report()  # Always log cleaning stats

# Step 3: Analyze
analyzer = AadhaarAnalyzer()
stats = analyzer.univariate_analysis(df_clean, 'total_enrolments')

# Step 4: Visualize
viz = AadhaarVisualizer(output_dir="outputs")
fig = viz.plot_time_series(df_clean, 'date', 'total_enrolments', 'Title')
```

## Dataset Structure

### Three Main Datasets
- **Enrolment** (~1M records): New registrations by date/location/age
- **Demographic** (~2M records): Demographic updates by date/location/age
- **Biometric** (~1.8M records): Biometric captures by date/location/age

### Expected Columns
All datasets share: `date`, `state`, `district`, `pincode` + age group columns

### File Organization
```
Dataset/
├── api_data_aadhar_enrolment/       # Multiple CSV chunks (0-500K, 500K-1M, etc.)
├── api_data_aadhar_demographic/     # Multiple CSV chunks
└── api_data_aadhar_biometric/       # Multiple CSV chunks
```

## Common Tasks

### Adding New Analysis Methods
1. Add method to `AadhaarAnalyzer` class in [src/analysis.py](../src/analysis.py)
2. Use naming pattern: `analyze_[metric]()` or `aggregate_by_[dimension]()`
3. Return pandas DataFrame/Series with descriptive multi-level columns
4. Log progress with `logger.info()`

### Creating New Visualizations
1. Add method to `AadhaarVisualizer` in [src/visualization.py](../src/visualization.py)
2. Use pattern: `plot_[chart_type](df, x_col, y_col, title, save_path=None)`
3. Auto-save using `fig.write_html(f"{self.output_dir}/{save_path}")`
4. Return the figure object for interactive display

### Feature Engineering
Always create these derived features:
- **Temporal**: year, month, day_of_week, week_of_year, quarter
- **Totals**: Sum across age group columns
- **Ratios**: Updates/enrolments by geography
- **Growth**: Period-over-period percentage change

## Key Dependencies & Tools
- **Data Processing**: pandas, numpy, dask (optional for large datasets)
- **Statistics**: scipy, statsmodels, scikit-learn
- **Time Series**: prophet (for forecasting)
- **Visualization**: plotly (primary), seaborn, matplotlib, folium
- **Geospatial**: geopandas
- **Profiling**: pandas-profiling, ydata-profiling
- **Anomaly Detection**: pyod

## Logging & Reporting
- Use standard logging module with INFO level
- Always print cleaning reports: `preprocessor.print_cleaning_report()`
- Log dataset summaries: `loader.get_data_summary(df, 'Dataset Name')`
- Track rows before/after operations in cleaning_report dict

## Important Notes
- **Windows environment**: Use Windows-style paths and `.\.venv\Scripts\activate`
- **Memory management**: Use Dask (`use_dask=True`) for full 5M record processing
- **Hackathon context**: Prioritize rapid prototyping and visual insights over production code
- **Data format**: Dates are dd-mm-yyyy (not standard yyyy-mm-dd)
- **Pincode validation**: Must be exactly 6 digits (zero-padded)
