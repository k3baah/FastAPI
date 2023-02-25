import psycopg2

conn = psycopg2.connect(
    host="containers-us-west-96.railway.app",
    database="railway",
    user="postgres",
    password="7Q694nOaUlDIPSqorW0M"
)

cursor = conn.cursor()
