
import pika
import sys


def run():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='orangepi'))
        channel = connection.channel()

        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

        routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
        message = ' '.join(sys.argv[2:]) or 'Hello World!'
        channel.basic_publish(
            exchange='topic_logs', routing_key=routing_key, body=message)
        print(f" [x] Sent {routing_key}:{message}")

    except KeyboardInterrupt:
        connection.close()
        print(" [x] Connection closed")
