import pika, random, time
from app import queue_conn

def getRandom():
    return random.randint(0,6)

def queue():
    channel = queue_conn()
    channel.queue_declare(queue='status_queue', durable=True)
    while True:
        queue_data = {
            'status': getRandom(),
            'current_timestamp': time.time()
        }
        channel.basic_publish(exchange='',routing_key='status_queue',body=queue_data
                              ,properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        ))
        print('message sent :', queue_data)
        time.sleep(2)