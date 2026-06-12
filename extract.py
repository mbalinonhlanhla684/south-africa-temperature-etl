import pandas as pd

def extract(filepath):
    print("Extracting data...")
    df = pd.read_csv(filepath, encoding='latin1')
    print(f"Extracted {len(df)} rows and {len(df.columns)} columns")
    return df

if __name__ == "__main__":
    df = extract('Environment_Temperature_change_E_All_Data_NOFLAG.csv')
    print(df.head())