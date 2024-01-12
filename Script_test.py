#from Overhead_test import run as run1

import Overhead_test
import Overhead_test2
import Overhead_test3
import Overhead_test4
import os
from random import randint
import time
from statistics import mean
import tate_bilinear_pairing as tbp
from tate_bilinear_pairing import eta
import hashlib

broker = '192.168.1.51'
port = 1883
topic = "test"
client_id = f'python-mqtt-{randint(0, 1000)}'
FIXED_SIZE_LIST = [5, 50, 500, 5000, 50000]
meanTimeDic1 = {}
meanTimeDic2 = {}
meanTimeDic3 = {}
meanTimeDic4 = {}

def testScript1(iter, FIXED_SIZE):

    time_list = []
    for i in range(iter):
        message_text = os.urandom(FIXED_SIZE)
        start = time.time()
        Overhead_test.run(message_text)
        end = time.time()
        time_list.append(end - start)
        #print(f"Time : {end - start} seconds")
    m = mean(time_list)
    print(f"Average time : {m}")
    return m

def testScript2(iter, FIXED_SIZE, resp, userIdPoint, deviceIdPoint):

    time_list = []
    for i in range(iter):
        message_text = os.urandom(FIXED_SIZE)
        start = time.time()
        Overhead_test2.run(message_text, resp, userIdPoint, deviceIdPoint)
        end = time.time()
        time_list.append(end - start)
        #print(f"Time : {end - start} seconds")

    m = mean(time_list)
    print(f"Average time : {m}")
    return m

def testScript3(iter, FIXED_SIZE, resp, userIdPoint, deviceIdPoint):

    time_list = []
    for i in range(iter):
        message_text = os.urandom(FIXED_SIZE)
        start = time.time()
        Overhead_test3.run(message_text, resp, userIdPoint, deviceIdPoint)
        end = time.time()
        time_list.append(end - start)
        #print(f"Time : {end - start} seconds")

    m = mean(time_list)
    print(f"Average time : {m}")
    return m

def testScript4(iter, FIXED_SIZE, resp, userIdPoint, deviceIdPoint):

    time_list = []
    for i in range(iter):
        message_text = os.urandom(FIXED_SIZE)
        start = time.time()
        Overhead_test4.run(message_text, resp, userIdPoint, deviceIdPoint)
        end = time.time()
        time_list.append(end - start)
        #print(f"Time : {end - start} seconds")

    m = mean(time_list)
    print(f"Average time : {m}")
    return m


def globalTesting(FIXED_SIZE_LIST):
    iter = 30
    resp = b'\x821\xa5\x1b\x1c-\x19\xb3JPh\xf8B\xe6\x8f;\xea\x97\x07\xedV\x93T\xddQ\x97\xe0\x0b\xcb\xce\x80p\xe8\xa0?\x1e\xb1\x82Z(\x19\xee[\x18\xc6\xbc\x9ej'
    tbp.eta.init(151)
    eccGenerator = tbp.ecc.gen()
    deviceIdPointValue = int.from_bytes(hashlib.sha256("devicei".encode(encoding='UTF-8', errors='strict')).digest(),
                                        'big')
    deviceIdPoint = tbp.ecc.scalar_mult(deviceIdPointValue, eccGenerator)
    userIdPointValue = int.from_bytes(hashlib.sha256("user".encode(encoding='UTF-8', errors='strict')).digest(), 'big')
    userIdPoint = tbp.ecc.scalar_mult(userIdPointValue, eccGenerator)

    for j in FIXED_SIZE_LIST:
        print(j)
        m1 = testScript1(iter, j)
        m2 =testScript2(iter, j, resp, userIdPoint, deviceIdPoint)
        m3 =testScript3(iter, j, resp, userIdPoint, deviceIdPoint)
        m4 =testScript4(iter, j, resp, userIdPoint, deviceIdPoint)
        meanTimeDic1[j] = m1
        meanTimeDic2[j] = m2
        meanTimeDic3[j] = m3
        meanTimeDic4[j] = m4

    print(f"Script1 : {meanTimeDic1}")
    print(f"Script2 : {meanTimeDic2}")
    print(f"Script3 : {meanTimeDic3}")
    print(f"Script4 : {meanTimeDic4}")

globalTesting(FIXED_SIZE_LIST)