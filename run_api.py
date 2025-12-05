import random
import sqlite3

from datetime import datetime, timedelta

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from api.time_serie import TimeSerie
from resources.config import db_name

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def info():
    print("----")
    return {"info" : "This exposes data ... eventually."}


@app.get("/search_events", response_class=PlainTextResponse)
def search_events():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM search_events")

    results = cursor.fetchall()
    output = ""
    for row in results:
        if len(output) == 0:
            output += ",".join(row.keys()) + "\n"
        output += (f"{row["se_id"]},{row["search_terms"]},{row["km_radius"]},"
                   f"{row["postal_code"]},{row["number_of_results"]},"
                   f"{row["at_time"]}\n")
    return output


@app.get("/test_csv", response_class=PlainTextResponse)
def test_csv():
    """
    https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/time-series/
    :return:
    """
    now = datetime.now()
    next_time = now - timedelta(minutes=20)
    output = '"A-series", "time"\n'
    for i in range(0, 100):
        v = random.randint(0, 3000)
        output += f"{v},{next_time}\n"
        next_time = next_time + timedelta(minutes=random.randint(10, 100))

    return output



@app.get("/search_events/python")
def search_events_python():
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM search_events
        WHERE search_terms = 'Python' 
        """)
        result = cursor.fetchall()

        datapoints = []
        for row in result:
            n = row["number_of_results"]
            t = row["at_time"]
            datapoint = [n, t]
            datapoints.append(datapoint)

        time_serie = TimeSerie("number.ads", datapoints, {"terms": "Python"}, "n")
        return time_serie


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)