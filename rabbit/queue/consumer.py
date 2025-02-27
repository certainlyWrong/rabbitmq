import pika
import time


def run():
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        time.sleep(body.count(b'.'))
        print(f" [x] Done {body}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    try:
        # host = 'orangepi'
        # host = 'localhost:5672'
        host = 'localhost'
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host)
        )

        channel = connection.channel()

        channel.queue_declare(
            queue='hello',
            durable=True,
            exclusive=False,
            auto_delete=False,
            arguments=None,
        )

        channel.basic_qos(prefetch_count=1, prefetch_size=0, global_qos=False)

        channel.basic_consume(
            queue='hello', on_message_callback=callback, auto_ack=False)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        connection.close()
        print("Exiting...")
