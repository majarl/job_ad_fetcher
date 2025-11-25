import sqlite3

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

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
    conn = sqlite3.connect("searches.db")
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
    print(output)
    return output


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)