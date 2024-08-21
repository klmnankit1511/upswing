import subprocess
import time
import os
import pika
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

def queue_conn():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', 5672))
    channel = connection.channel()
    return channel

def start_rabbitmq():
    print("Starting RabbitMQ...")
    os.system('brew services restart rabbitmq')
    
    is_running = False
    for _ in range(10):
        status = os.system('rabbitmqctl status > /dev/null 2>&1')
        if status == 0:
            is_running = True
            print("RabbitMQ is started")
            break
        else:
            print("Waiting for RabbitMQ...")
            time.sleep(1)
    
    if not is_running:
        print("Failed to start RabbitMQ")
        return False
    
    return True

def connect_db():
    print('Connecting to DB')
    
    load_dotenv()
    mongodb_password = os.getenv("MONGODB_PWD")
    mongodb_id = os.getenv("MONGODB_ID")
    
    uri = f"mongodb+srv://{mongodb_id}:{mongodb_password}@mqtt.vozwt.mongodb.net/?retryWrites=true&w=majority&appName=mqtt"

    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None

def start_server():
    if start_rabbitmq() and connect_db():
        print("Starting the Server...")
        try:
            subprocess.Popen(["python3", "server.py"])
            return True
        except:
            return False
    return False

def start_client():
    print("Starting the Client...")
    subprocess.Popen(["python3", "main.py"])

if __name__ == '__main__':
    if start_server():
        time.sleep(5)
        start_client()
