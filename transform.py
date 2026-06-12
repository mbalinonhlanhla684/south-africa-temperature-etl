import pandas as pd

def transform(df):
    print("Transforming data...")

    # 1. Filter for South Africa only
    df = df[df['Area'] == 'South Africa']

    # 2. Keep only useful columns
    df = df[['Area', 'Months', 'Element', 'Unit',
             'Y2000', 'Y2005', 'Y2010', 'Y2015', 'Y2016',
             'Y2017', 'Y2018', 'Y2019']]

    # 3. Rename columns to be cleaner
    df = df.rename(columns={'Area': 'country', 'Months': 'month',
                            'Element': 'measure', 'Unit': 'unit'})

    # 4. Fix encoding artifacts in month names (e.g. Mar\x96Apr → Mar-Apr)
    df['month'] = df['month'].str.encode('latin1').str.decode('utf-8', errors='replace')
    df['month'] = df['month'].str.replace('\ufffd', '-', regex=False)

    # 5. Drop rows where all year values are missing
    df = df.dropna(subset=['Y2000', 'Y2010', 'Y2019'], how='all')

    # 6. Reset index
    df = df.reset_index(drop=True)

    print(f"Transformed data: {len(df)} rows")
    print(df.head())
    return df

if __name__ == "__main__":
    raw = pd.read_csv('Environment_Temperature_change_E_All_Data_NOFLAG.csv',
                      encoding='latin1')
    transformed = transform(raw)