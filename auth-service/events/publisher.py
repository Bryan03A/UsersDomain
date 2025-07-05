import pika
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "auth-events")

def publish_event(event_name: str, data: dict):
    event_payload = {
        "event": event_name,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()

        # Declare the queue if it doesn't exist
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

        # Publish the message
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(event_payload),
            properties=pika.BasicProperties(
                delivery_mode=2  # Make the message persistent
            )
        )

        print(f"[Publisher] Event published: {event_name}")
        connection.close()

    except Exception as e:
        print(f"[Publisher Error] {e}")