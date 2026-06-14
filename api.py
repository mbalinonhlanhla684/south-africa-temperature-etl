from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect('weather_etl.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/temperature")
def get_temperature():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT month, Y2000, Y2005, Y2010, Y2015, Y2016, Y2017, Y2018, Y2019
        FROM temperature_changes
        WHERE measure = 'Temperature change'
        AND month IN (
            'January','February','March','April','May','June',
            'July','August','September','October','November','December'
        )
        ORDER BY Y2019 DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

@app.get("/api/yearly-trend")
def get_yearly_trend():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Y2000, Y2005, Y2010, Y2015, Y2016, Y2017, Y2018, Y2019
        FROM temperature_changes
        WHERE measure = 'Temperature change'
        AND month = 'Meteorological year'
    """)
    row = dict(cursor.fetchone())
    conn.close()
    years = [
        {"year": "2000", "change": row["Y2000"]},
        {"year": "2005", "change": row["Y2005"]},
        {"year": "2010", "change": row["Y2010"]},
        {"year": "2015", "change": row["Y2015"]},
        {"year": "2016", "change": row["Y2016"]},
        {"year": "2017", "change": row["Y2017"]},
        {"year": "2018", "change": row["Y2018"]},
        {"year": "2019", "change": row["Y2019"]},
    ]
    return years

@app.get("/api/stats")
def get_stats():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT month, Y2019
        FROM temperature_changes
        WHERE measure = 'Temperature change'
        AND month IN (
            'January','February','March','April','May','June',
            'July','August','September','October','November','December'
        )
        ORDER BY Y2019 DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    hottest = rows[0]
    coldest = rows[-1]
    avg = round(sum(r["Y2019"] for r in rows) / len(rows), 3)
    return {
        "hottest_month": hottest["month"],
        "hottest_value": hottest["Y2019"],
        "coldest_month": coldest["month"],
        "coldest_value": coldest["Y2019"],
        "average_change": avg,
        "country": "South Africa"
    }