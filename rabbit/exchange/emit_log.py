import pika
import time


def run():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('orangepi'))
    channel = connection.channel()

    channel.exchange_declare(
        exchange='logs',
        exchange_type='fanout',
    )

    result = channel.queue_declare(
        queue='',
        durable=True,
        exclusive=True,
        auto_delete=True,
        arguments=None,
    )

    channel.queue_bind(
        exchange='logs',
        queue=result.method.queue,
        routing_key=None,
        arguments=None,
    )

    try:
        count = 0
        while True:
            time.sleep(1)
            print(f" [x] Sending {count}")
            channel.basic_publish(
                exchange='logs',
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
                routing_key='',
                body=f'Hello | {count}'
            )
            count += 1
    except KeyboardInterrupt:
        connection.close()
        print("Exiting...")
