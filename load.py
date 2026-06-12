import sqlite3
import pandas as pd

def load(df, db_name='weather_etl.db'):
    print("Loading data into SQLite...")

    # Connect to SQLite (creates the file if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Load dataframe into a table called 'temperature_changes'
    df.to_sql('temperature_changes', conn, if_exists='replace', index=False)

    # Verify it loaded correctly
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM temperature_changes")
    count = cursor.fetchone()[0]
    print(f"Successfully loaded {count} rows into '{db_name}'")

    conn.close()

if __name__ == "__main__":
    from extract import extract
    from transform import transform

    raw = extract('Environment_Temperature_change_E_All_Data_NOFLAG.csv')
    clean = transform(raw)
    load(clean)