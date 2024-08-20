import pika
import json
import random
import time

def send_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
    channel = connection.channel()

    # Declare the queue where messages will be sent
    channel.queue_declare(queue='mqtt_queue')

    while True:
        message = {
            'status': random.randint(0, 6),
            'timestamp': time.time()
        }
        channel.basic_publish(exchange='',
                              routing_key='mqtt_queue',
                              body=json.dumps(message))
        print(f"Sent: {message}")
        time.sleep(1)

if __name__ == '__main__':
    send_message()
