
import json
import os

import pika
import pymysql
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "iotuser"
RABBITMQ_PASSWORD = "iotpass123"

QUEUE_NAME = "sensor.data.queue"


def save_sensor_data(message):
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
            sql = """
                INSERT INTO sensor_data (
                    message_id,
                    sensor_id,
                    temperature,
                    humidity,
                    measured_at
                )
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE message_id = message_id
            """

            cursor.execute(
                sql,
                (
                    message["message_id"],
                    message["sensor_id"],
                    message.get("temperature"),
                    message.get("humidity"),
                    message["measured_at"],
                ),
            )

        connection.commit()

    finally:
        connection.close()


def main():
    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD,
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials,
        )
    )

    channel = connection.channel()
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
    )

    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        try:
            message = json.loads(body.decode("utf-8"))

            # DB 저장과 COMMIT이 성공한 다음 ACK 전송
            save_sensor_data(message)

            print(
                f"[DB 저장 성공] "
                f"sensor_id={message['sensor_id']}, "
                f"temperature={message.get('temperature')}, "
                f"humidity={message.get('humidity')}"
            )

            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )

        except Exception as error:
            print(f"[처리 실패] {error}")

            # 메시지를 재전달하도록 요청
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=True,
            )

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
    )

    print(f"'{QUEUE_NAME}' DB Consumer 실행 중...")

    try:
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\nConsumer를 종료합니다.")

    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
