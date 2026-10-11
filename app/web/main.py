
import os
from fastapi.responses import FileResponse
from pathlib import Path
import pymysql
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI(title="IoT Monitoring API")

BASE_DIR = Path(__file__).resolve().parent


@app.get("/dashboard")
def dashboard():
    return FileResponse(BASE_DIR / "static" / "index.html")

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


@app.get("/")
def home():
    return {
        "message": "IoT Monitoring API is running!"
    }


@app.get("/api/sensor-data")
def get_sensor_data():
    connection = None

    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    sensor_id,
                    temperature,
                    humidity,
                    measured_at,
                    received_at
                FROM sensor_data
                ORDER BY id DESC
                LIMIT 100
            """)
            rows = cursor.fetchall()

        # MariaDB의 Decimal, datetime을 JSON 호환 형식으로 변환
        for row in rows:
            for key, value in row.items():
                if value is not None and hasattr(value, "isoformat"):
                    row[key] = value.isoformat()
                elif key in ("temperature", "humidity") and value is not None:
                    row[key] = float(value)

        return {
            "count": len(rows),
            "data": rows,
        }

    except Exception as e:
        print(f"DB 조회 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="센서 데이터 조회에 실패했습니다.",
        ) from e

    finally:
        if connection:
            connection.close()



@app.get("/api/device-status")
def get_device_status():
    connection = None

    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    sensor_id,
                    device_status,
                    measured_at,
                    received_at
                FROM device_status
                ORDER BY id DESC
                LIMIT 100
            """)
            rows = cursor.fetchall()

        for row in rows:
            for key, value in row.items():
                if value is not None and hasattr(value, "isoformat"):
                    row[key] = value.isoformat()

        return {
            "count": len(rows),
            "data": rows
        }

    except Exception as e:
        print(f"장치 상태 조회 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="장치 상태 조회에 실패했습니다."
        ) from e

    finally:
        if connection:
            connection.close()
