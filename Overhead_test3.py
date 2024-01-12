import QUARK
from paho.mqtt import client as mqtt_client
import random
import time
import os
import hashlib
import tate_bilinear_pairing as tbp
from tate_bilinear_pairing import eta
from bitstring import BitArray
import vaulty
from statistics import mean

broker = '192.168.1.51'
port = 1883
topic = "test"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

'''
FIXED_SIZED = 50000
message_text = os.urandom(FIXED_SIZED)
resp = b'\x821\xa5\x1b\x1c-\x19\xb3JPh\xf8B\xe6\x8f;\xea\x97\x07\xedV\x93T\xddQ\x97\xe0\x0b\xcb\xce\x80p\xe8\xa0?\x1e\xb1\x82Z(\x19\xee[\x18\xc6\xbc\x9ej'

tbp.eta.init(151)
eccGenerator = tbp.ecc.gen()
deviceIdPointValue = int.from_bytes(hashlib.sha256("devicei".encode(encoding='UTF-8', errors='strict')).digest(),'big')
deviceIdPoint = tbp.ecc.scalar_mult(deviceIdPointValue, eccGenerator)
userIdPointValue = int.from_bytes(hashlib.sha256("user".encode(encoding='UTF-8', errors='strict')).digest(),'big')
userIdPoint = tbp.ecc.scalar_mult(userIdPointValue, eccGenerator)
'''
def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    object = QUARK.D_Quark()
    output = object.keyed_hash(BitArray(passcode), BitArray(passcode))
    return output.tobytes()

def transformationCoordinateToKey(coord):

    k = 0
    for elem1 in coord:
        for elem2 in elem1:
            for elem3 in elem2:
                for elem4 in elem3:
                    k += elem4
    k = str(k)
    return gen_fernet_key(k.encode('utf-8'))

def cypherMessage( msg, resp, userIdPoint, deviceIdPoint):

    resp = int.from_bytes(resp, 'big')
    a = tbp.ecc.scalar_mult(resp, deviceIdPoint)
    key = tbp.eta.pairing(a[1], a[2], userIdPoint[1], userIdPoint[2])
    key = transformationCoordinateToKey(key)

    v = vaulty.Vaulty()
    encMessage = v.encrypt(msg, key)


    return encMessage


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


def publish(client,message_text,  resp, userIdPoint, deviceIdPoint):
     msg_count = 1
     while True:
         time.sleep(1)
         msg = cypherMessage(message_text, resp, userIdPoint, deviceIdPoint)
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

def run(message_text, resp, userIdPoint, deviceIdPoint):
    client = connect_mqtt()
    client.loop_start()
    publish(client,message_text,  resp, userIdPoint, deviceIdPoint)
    client.loop_stop()



'''
iter = 10
time_list = []
for i in range(iter):
    start = time.time()
    run(message_text, resp, userIdPoint, deviceIdPoint)
    end = time.time()
    time_list.append(end - start)
    print(f"Time : {end - start} seconds")
    message_text = os.urandom(FIXED_SIZED)

print(f"Average time : {mean(time_list)}")

'''