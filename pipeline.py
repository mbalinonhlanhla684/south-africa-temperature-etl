from extract import extract
from transform import transform
from load import load

def run_pipeline():
    print("=" * 40)
    print("   WEATHER ETL PIPELINE STARTING")
    print("=" * 40)

    # Step 1 - Extract
    raw = extract('Environment_Temperature_change_E_All_Data_NOFLAG.csv')

    # Step 2 - Transform
    clean = transform(raw)

    # Step 3 - Load
    load(clean)

    print("=" * 40)
    print("   PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 40)

if __name__ == "__main__":
    run_pipeline()