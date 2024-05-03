import pika
import time
import random


def run():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='orangepi'))
        channel = connection.channel()

        channel.exchange_declare(
            exchange='direct_logs', exchange_type='direct')

        severity = ['info', 'warning', 'error', 'debug']

        while True:
            time.sleep(1)
            random_severity = random.choice(severity)
            message = f"Hello World! {random_severity}"
            channel.basic_publish(
                exchange='direct_logs',
                routing_key=random_severity,
                body=message
            )
            print(f" [x] Sent '{random_severity}':'{message}'")

    except KeyboardInterrupt:
        connection.close()
        print(" [x] Connection closed")
