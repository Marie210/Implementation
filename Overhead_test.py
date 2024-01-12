from paho.mqtt import client as mqtt_client
import random
import time
import os
from statistics import mean

broker = '192.168.1.51'
port = 1883
topic = "test"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

'''
FIXED_SIZED = 50000
message_text = os.urandom(FIXED_SIZED)

'''

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,message):
     msg_count = 1
     while True:
         time.sleep(1)
         msg = message
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         #if status == 0:
             #print(f"Send `{msg}` to topic `{topic}`")
         #else:
             #print(f"Failed to send message to topic {topic}")
         msg_count += 1
         if msg_count > 1:
             break

def run(message):
    client = connect_mqtt()
    client.loop_start()
    publish(client, message)
    client.loop_stop()

'''
iter = 10
time_list = []
for i in range(iter):
    start = time.time()
    run(message_text)
    end = time.time()
    time_list.append(end - start)
    print(f"Time : {end - start} seconds")
    message_text = os.urandom(FIXED_SIZED)

print(f"Average time : {mean(time_list)}")

'''