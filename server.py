import pika
import json
from fastapi import FastAPI
from app import connect_db, queue_conn

app = FastAPI()

client = connect_db()
db = client['mqtt_db']
collection = db['mqtt_collections']

def callback(ch, method, properties, body):
    message = json.loads(body)
    collection.insert_one(message)
    print(f"Received and stored: {message}")

def start_consumer():
    channel = queue_conn()

    channel.queue_declare(queue='status_queue')
    channel.basic_consume(queue='status_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages...')
    channel.start_consuming()

@app.get("/status_count")
def status_count(start_time: float, end_time: float):
    

    pipeline = [
        {"$match": {"timestamp": {'$gte': start_time, '$lte': end_time}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    
    result = collection.aggregate(pipeline)
    status_counts = {item['_id']: item['count'] for item in result}

    return status_counts

if __name__ == '__main__':
    import threading
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()

    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)

    except (Exception) as e:
        raise e

