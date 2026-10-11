
import json
import os

import pika
import pymysql
from dotenv import load_dotenv

load_dotenv()

# RabbitMQ 연결
credentials = pika.PlainCredentials(
    os.getenv("RABBITMQ_USER", "iotuser"),
    os.getenv("RABBITMQ_PASSWORD", "iotpass123"),
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        credentials=credentials,
    )
)

channel = connection.channel()

# 기존 큐 사용
channel.queue_declare(
    queue="device.status.queue",
    durable=True,
)

channel.basic_qos(prefetch_count=1)


def save_device_status(data):
    db = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4",
    )

    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO device_status (
                    message_id,
                    sensor_id,
                    device_status,
                    measured_at
                )
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    message_id = message_id
                """,
                (
                    data["message_id"],
                    data["sensor_id"],
                    str(data["device_status"]),
                    data["measured_at"],
                ),
            )

        db.commit()

    finally:
        db.close()


def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))

        save_device_status(data)

        print(
            "[DB 저장 성공] "
            f"sensor_id={data['sensor_id']}, "
            f"device_status={data['device_status']}"
        )

        # DB 저장이 성공한 뒤 메시지 ACK
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[처리 실패] {e}")

        # 즉시 무한 재전달되는 것을 방지하기 위해
        # 이번 단계에서는 실패 메시지를 큐에서 제외한다.
        # 운영 환경에서는 DLQ와 재시도 정책을 별도로 구성한다.
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False,
        )


channel.basic_consume(
    queue="device.status.queue",
    on_message_callback=callback,
)

print("'device.status.queue' Consumer 실행 중...")
print("종료하려면 Ctrl+C를 누르세요.")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
finally:
    connection.close()
