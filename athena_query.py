import boto3
import os
import time
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

athena = boto3.client(
    "athena",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

OUTPUT_LOCATION = f"s3://{BUCKET_NAME}/athena-results/"

def run_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": "sa_climate_db"},
        ResultConfiguration={"OutputLocation": OUTPUT_LOCATION}
    )
    query_id = response["QueryExecutionId"]

    # Wait for it to finish
    while True:
        status = athena.get_query_execution(QueryExecutionId=query_id)
        state = status["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(1)

    if state != "SUCCEEDED":
        raise Exception(f"Query {state}")

    # Fetch results
    results = athena.get_query_results(QueryExecutionId=query_id)
    rows = results["ResultSet"]["Rows"]

    # First row = headers
    headers = [col["VarCharValue"] for col in rows[0]["Data"]]
    data = []
    for row in rows[1:]:
        values = [col.get("VarCharValue", "") for col in row["Data"]]
        data.append(dict(zip(headers, values)))

    return data

if __name__ == "__main__":
    result = run_query("SELECT * FROM sa_climate_db.temperature_changes LIMIT 5")
    for row in result:
        print(row)