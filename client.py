import asyncio
import websockets
import hashlib
import tate_bilinear_pairing as tbp
from tate_bilinear_pairing import eta
from cryptography.fernet import Fernet
import base64
from json import loads

def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def transformationCoordinateToKey(coord):

    k = 0
    for elem1 in coord:
        for elem2 in elem1:
            for elem3 in elem2:
                for elem4 in elem3:
                    k += elem4
    k = str(k)
    return gen_fernet_key(k.encode('utf-8'))


class client:

    def __init__(self, name):
        self.name = name
        self.prefixList = ["Pref"]
        self.psswrd = "Chaton"

        tbp.eta.init(151)
        self.eccGenerator = tbp.ecc.gen()
        deviceIdPointValue = int.from_bytes(hashlib.sha256("devicei".encode(encoding='UTF-8', errors='strict')).digest(),'big')
        self.deviceIdPoint = tbp.ecc.scalar_mult(deviceIdPointValue, self.eccGenerator)

        userIdPointValue = int.from_bytes(hashlib.sha256("user".encode(encoding='UTF-8', errors='strict')).digest(),'big')
        self.userIdPoint = tbp.ecc.scalar_mult(userIdPointValue, self.eccGenerator)


    def decypherMsg(self, msg, respPoint):

        print(f"Device ID Point: {self.deviceIdPoint}")

        keyPoint = tbp.eta.pairing(self.deviceIdPoint[1], self.deviceIdPoint[2], respPoint[0], respPoint[1])
        print(f"Pairing result: {keyPoint}")
        key = transformationCoordinateToKey(keyPoint)
        print(f"Key: {key}")
        fernet = Fernet(key)

        decr_data = fernet.decrypt(bytes(msg[2:len(msg)-1], 'utf-8') ).decode('utf-8')

        return decr_data


    def connectMsg(self):
        return f"1 {self.name}"

    def subscribeMsg(self, topic):
        return f"8 {topic} {self.name}"


    async def communicateBroker(self, message):
        uri = "ws://localhost:8765"
        responseList = []
        toplist = []
        async with websockets.connect(uri) as websocket:
            print(f"Client sends message: {message}")
            await websocket.send(message)

            response = await websocket.recv()
            num = response[0]
            if num == "0":
                print(f"Client received response: {response[1:]}")
            else:
                for i in range(int(num)):
                    response = await websocket.recv()
                    print(f"Received message :{response} ")
                    responseList.append(response)
                    await websocket.send("received")
                    response = await websocket.recv()
                    print(f"From topic : Pref/{response} ")
                    toplist.append(response)
                    await websocket.send("received")

        return responseList, toplist


    def messageExchangeBroker(self, message):
        responseList, toplist = asyncio.get_event_loop().run_until_complete(self.communicateBroker(message))
        return responseList, toplist


    async def communicateAdmin(self, topic):
        uri = "ws://localhost:8766"
        token = 0

        async with websockets.connect(uri) as websocket:
            print(f"Client wants to connect to admin")
            await websocket.send(f"{self.name} {self.psswrd}")
            response = await websocket.recv()
            print(f"Admin responded: {response}")
            await websocket.send(topic)
            print(f"Client asks for permission to access topic {topic}")
            token = await websocket.recv()

            subjectName = token[token.find("###") + 3:]
            a = token[token.find(" ")+1:token.find('###')-2]
            b = a[:a.find(']]')+2]
            c = a[a.find('[[', 2):]
            token = [loads(b), loads(c)]
            print(f"Admin gave the token: {token} \n and the topic is linked to the subject {subjectName}")

        return token, subjectName



    def messageExchangeAdmin(self, topName):
        token, subjectName = asyncio.get_event_loop().run_until_complete(self.communicateAdmin(topName))
        return token, subjectName



cli = client("Sophie")

responseList, toplist = cli.messageExchangeBroker(cli.connectMsg())

'''

tokenList = []
subjectList = []
for elem in toplist:
    token, subjectName = cli.messageExchangeAdmin(elem)
    tokenList.append(token)
    subjectList.append(subjectName)

for i in range(len(responseList)):
    decypheredMsg = cli.decypherMsg(responseList[i], tokenList[i])
    print(f"The decyphered message is '{decypheredMsg}' on topic {subjectList[i]}")
'''



resp = cli.messageExchangeBroker(cli.subscribeMsg("Pref/#"))






'''
top = b'\xf4\xf2v\xb4\xdb\xde\xd4\xa8\x12\x12\xc3\x84YJ\x19|\xcc\x15o\x89'
token = cli.messageExchangeAdmin(top)

'''
'''

cli.messageExchangeBroker(cli.connectMsg())
cli.messageExchangeBroker(cli.subscribeMsg("test/#"))
'''