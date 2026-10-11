
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                message_id VARCHAR(36) NOT NULL UNIQUE,
                sensor_id VARCHAR(100) NOT NULL,
                temperature DECIMAL(6, 2),
                humidity DECIMAL(6, 2),
                measured_at VARCHAR(40) NOT NULL,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    connection.commit()
    print("sensor_data 테이블 생성 완료!")

    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        print("Tables:", cursor.fetchall())

finally:
    connection.close()
