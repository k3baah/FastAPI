from fastapi import FastAPI
from pydantic import BaseModel
import requests
import psycopg2

app = FastAPI()

class Msg(BaseModel):
    msg: str


# define database connection parameters
db_params = {
    host:"containers-us-west-96.railway.app",
    database:"railway",
    user:"postgres",
    password:"7Q694nOaUlDIPSqorW0M"
}

# define SQL query to insert job posting into database
insert_query = """
    INSERT INTO test (position, company, description, role, type, location, skill) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# define a new route that fetches job postings from the API and inserts them into the database
@app.post("/populate_database")
async def populate_database():
    # establish database connection
    conn = psycopg2.connect(**db_params)

    # fetch job postings from API
    api_url = "https://api.browse.ai/v2/robots/b1834629-308e-449a-90aa-8093c4e97e1f/tasks"
    access_token = "934df2e5-0ccc-412f-9e37-5ec4518e4e89:f080c116-24c8-4967-8537-a6841418c7ee"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    job_postings = response.json()["capturedLists"]["jobs"]

    # insert job postings into database
    cursor = conn.cursor()
    for job in job_postings:
        job_values = (
            job["Position"],
            job["company"],
            job["description"],
            job["role"],
            job["type"],
            job["location"],
            job["skill"]
        )
        cursor.execute(insert_query, job_values)
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"Inserted {len(job_postings)} job postings into database."}

