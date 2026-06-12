# 🌡️ South Africa Temperature ETL Pipeline

An automated ETL pipeline that extracts FAO global temperature 
change data, transforms and filters it for South Africa, 
and loads it into a SQLite database for analysis.

## Pipeline Architecture
Extract (CSV) → Transform (Pandas) → Load (SQLite)

## Tech Stack
- Python 3
- Pandas
- SQLite

## Key Finding
May recorded the highest temperature change in South Africa 
in 2019 at +2.812°C above baseline.

## How to Run
pip install pandas
python pipeline.py

## Data Source
FAO Environment Temperature Change Dataset via Kaggle