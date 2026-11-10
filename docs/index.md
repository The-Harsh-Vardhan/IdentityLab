# IdentityLab

A Python data analysis pipeline for the UIDAI Aadhaar enrolment, demographic-update and biometric-update datasets (~5 million raw records), built for the UIDAI Hackathon 2026.

The datasets are aggregate counts per date, state, district and pincode. No personal records are included in the data or in this site.

## What it does
- Loads and combines multiple CSV files per dataset
- Cleans, validates and feature-engineers the data
- Runs statistical, temporal, seasonal and geographic analysis
- Produces interactive Plotly charts (22 HTML files in the reference run)

## Key results (from the project notebooks)
- ~4.35 million records after cleaning; 591,180 duplicates removed (11.9% of raw)
- Date range March 2025 - December 2025, 50+ states/UTs, 950+ districts
- Update-to-enrolment ratio of about 20:1
- Geographic concentration Gini of 0.74-0.77

## Pages
- [Architecture](architecture.md)
- [Source repository and full README](https://github.com/The-Harsh-Vardhan/IdentityLab)
