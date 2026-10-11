import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    charset="utf8mb4",
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        print("MariaDB version:", cursor.fetchone()[0])

        cursor.execute("SHOW TABLES")
        print("Tables:", cursor.fetchall())
finally:
    connection.close()