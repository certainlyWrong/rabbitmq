import pika
import time
import random


def run():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('orangepi'))
    channel = connection.channel()

    channel.queue_declare(
        queue='hello',
        durable=True,
        exclusive=False,
        auto_delete=False,
        arguments=None,
    )

    try:
        count = 0
        while True:
            time.sleep(0.5)
            print(f" [x] Sending {count}")
            channel.basic_publish(
                exchange='',
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
                routing_key='hello',
                body=f'Hello | {count} | '
                f'{"." * random.randint(1, 3)}'
            )
            count += 1
    except KeyboardInterrupt:
        connection.close()
        print("Exiting...")
