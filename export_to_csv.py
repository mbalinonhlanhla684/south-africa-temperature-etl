import sqlite3
import pandas as pd

conn = sqlite3.connect('weather_etl.db')
df = pd.read_sql("SELECT * FROM temperature_changes", conn)
conn.close()

df.to_csv('temperature_changes.csv', index=False)
print(f"✅ Exported {len(df)} rows to temperature_changes.csv")