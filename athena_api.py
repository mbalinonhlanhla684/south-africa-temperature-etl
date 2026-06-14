from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from athena_query import run_query

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stats")
def get_stats():
    data = run_query("""
        SELECT month, y2019
        FROM sa_climate_db.temperature_changes
        WHERE measure = 'Temperature change'
        AND month IN ('January','February','March','April','May','June',
                       'July','August','September','October','November','December')
        ORDER BY CAST(y2019 AS DOUBLE) DESC
    """)
    hottest = data[0]
    coldest = data[-1]
    avg = sum(float(r["y2019"]) for r in data) / len(data)
    return {
        "hottest_month": hottest["month"],
        "hottest_value": round(float(hottest["y2019"]), 3),
        "coldest_month": coldest["month"],
        "coldest_value": round(float(coldest["y2019"]), 3),
        "average_change": round(avg, 3),
        "country": "South Africa"
    }

@app.get("/api/temperature")
def get_temperature():
    return run_query("""
        SELECT month, y2000, y2010, y2015, y2017, y2018, y2019
        FROM sa_climate_db.temperature_changes
        WHERE measure = 'Temperature change'
        AND month IN ('January','February','March','April','May','June',
                       'July','August','September','October','November','December')
        ORDER BY CAST(y2019 AS DOUBLE) DESC
    """)

@app.get("/api/yearly-trend")
def get_yearly_trend():
    data = run_query("""
        SELECT y2000, y2005, y2010, y2015, y2016, y2017, y2018, y2019
        FROM sa_climate_db.temperature_changes
        WHERE measure = 'Temperature change'
        AND month = 'Meteorological year'
    """)
    row = data[0]
    return [
        {"year": "2000", "change": float(row["y2000"])},
        {"year": "2005", "change": float(row["y2005"])},
        {"year": "2010", "change": float(row["y2010"])},
        {"year": "2015", "change": float(row["y2015"])},
        {"year": "2016", "change": float(row["y2016"])},
        {"year": "2017", "change": float(row["y2017"])},
        {"year": "2018", "change": float(row["y2018"])},
        {"year": "2019", "change": float(row["y2019"])},
    ]