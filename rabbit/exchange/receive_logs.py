
import pika


def run():
    try:
        # host = 'orangepi'
        # host = 'localhost:5672'
        host = 'localhost'
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='logs', queue=queue_name)

        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(f" [x] {body}")

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
    except KeyboardInterrupt:
        connection.close()
        print("Exiting...")
