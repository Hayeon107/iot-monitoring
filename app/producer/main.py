
import json
import time
import uuid
from datetime import datetime, timezone

import pika


RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "iotuser"
RABBITMQ_PASSWORD = "iotpass123"

EXCHANGE_NAME = "iot.topic"
SENSOR_QUEUE = "sensor.data.queue"
STATUS_QUEUE = "device.status.queue"

SENSOR_ID = "sensor-001"


def main():
    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
    )

    channel = connection.channel()

    # Exchange와 Queue가 없으면 생성하고,
    # 이미 존재하면 기존 설정을 사용한다.
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="topic",
        durable=True
    )

    channel.queue_declare(
        queue=SENSOR_QUEUE,
        durable=True
    )

    channel.queue_declare(
        queue=STATUS_QUEUE,
        durable=True
    )

    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=SENSOR_QUEUE,
        routing_key="sensor.data.*"
    )

    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=STATUS_QUEUE,
        routing_key="device.status.*"
    )

    print("RabbitMQ 연결 성공!")
    print("센서 데이터 발행을 시작합니다. Ctrl+C로 종료하세요.")

    try:
        while True:
#            temperature =32.5
            temperature = round(20 + time.time() % 10, 2)
            humidity = round(40 + time.time() % 20, 2)
            measured_at = datetime.now(timezone.utc).isoformat()


            messages = [
                (
                    f"sensor.data.{SENSOR_ID}",
                    {
                        "message_id": str(uuid.uuid4()),
                        "sensor_id": SENSOR_ID,
                        "temperature": temperature,
                        "humidity": humidity,
                        "device_status": None,
                        "measured_at": measured_at
                    }
                ),
                (
                    f"device.status.{SENSOR_ID}",
                    {
                        "message_id": str(uuid.uuid4()),
                        "sensor_id": SENSOR_ID,
                        "temperature": temperature,
                        "humidity": humidity,
                        "device_status": "online",
                        "measured_at": measured_at
                    }
                )
            ]


            for routing_key, message in messages:
                channel.basic_publish(
                    exchange=EXCHANGE_NAME,
                    routing_key=routing_key,
                    body=json.dumps(message).encode("utf-8"),
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        content_type="application/json"
                    )
                )

                print(
                    f"[발행 성공] {routing_key} -> "
                    f"{json.dumps(message, ensure_ascii=False)}"
                )

            time.sleep(5)

    except KeyboardInterrupt:
        print("\n센서 데이터 발행을 종료합니다.")

    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
