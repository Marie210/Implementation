import asyncio
import websockets
import hashlib
#from speck import SpeckCipher
import tate_bilinear_pairing as tbp
from tate_bilinear_pairing import eta
from cryptography.fernet import Fernet
import base64

T_SIZE = 10
M_size = 20
C_size = 8

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



class device:

    def __init__(self, name):
        self.name = "device" + name
        self.prefix = "Pref/"
        self.subjectsList = ["Alert", "StateOfCharge", "Temperature"]
        #self.initialTopicList = [rd.randint(1,(2^C_size)+1), rd.randint(1,(2^C_size)+1), rd.randint(1,(2^C_size)+1)]
        self.currentTopicList = self.subjectsList.copy()
        self.topicsList = [[],[],[]]
        for i in range(T_SIZE):
            for j in range(len(self.subjectsList)):
                if type(self.currentTopicList[j]) == bytes:
                    a = hashlib.sha1(self.currentTopicList[j]).digest()
                else:
                    a = hashlib.sha1(self.currentTopicList[j].encode(encoding='UTF-8', errors='strict')).digest()
                self.topicsList[j].append(a)
                self.currentTopicList[j] = a

        self.responseList = [[],[],[]]
        for i in range(T_SIZE):
            for j in range(len(self.subjectsList)):
                if type(self.topicsList[j][i]) == bytes:
                    self.responseList[j].append(hashlib.sha1(self.topicsList[j][i]).digest())
                else:
                    self.responseList[j].append(hashlib.sha1(self.topicsList[j][i].encode(encoding = 'UTF-8', errors = 'strict')).digest())
        self.brokerPublicKey = b'\xb4@\xc0(\xe0\xa8\x1a\xa7\x1d]r\xf2\xb9N+\x1a\xc8\x06\xb2\xaa\xbe\xc9\xb5T\xb0\xad\xe4]\xc3\x00N\xc6\x19\xf9\xf6\xb1O\xb4\xdd\x06\x05Uy\x84\xb7\x99\xcd\x05'

        tbp.eta.init(151)
        self.eccGenerator = tbp.ecc.gen()
        idPointValue = int.from_bytes(hashlib.sha256(self.name.encode(encoding = 'UTF-8', errors = 'strict')).digest(),'big')
        #self.idPoint = multiply(G2, idPointValue)
        self.idPoint  = tbp.ecc.scalar_mult(idPointValue, self.eccGenerator)
        userIdPointValue = int.from_bytes(hashlib.sha256("user".encode(encoding='UTF-8', errors='strict')).digest(),'big')
        #self.userIdPoint = multiply(G1, userIdPointValue)
        self.userIdPoint  = tbp.ecc.scalar_mult(userIdPointValue, self.eccGenerator)


    def chooseRightTopic(self, subject):

        i = self.subjectsList.index(subject)
        topic = self.currentTopicList[i]
        j = self.topicsList[i].index(topic)
        if j>0:
            self.currentTopicList[i] = self.topicsList[i][j-1]
        else:
            self.currentTopicList[i] = self.topicsList[i][len(self.topicsList[i])]

        return topic

    def cypherMessage(self, msg, topName):

        i,j = 0,0
        for elem in self.topicsList:
            if topName in elem:
                i = self.topicsList.index(elem)
                j = elem.index(topName)

        resp = int.from_bytes(self.responseList[i][j], 'big')
        a = tbp.ecc.scalar_mult(resp, self.idPoint)
        print(f"resp: {resp}")
        print(f"idPoint: {self.idPoint}")
        print(f"userIdPoint: {self.userIdPoint}")
        key = tbp.eta.pairing(a[1], a[2], self.userIdPoint[1], self.userIdPoint[2])
        print(f"keyPoint: {key}")

        key = transformationCoordinateToKey(key)

        print(f"key: {key}")
        fernet = Fernet(key)
        encMessage = fernet.encrypt(msg.encode())
        decrMessag = fernet.decrypt(encMessage)
        print(decrMessag)


        return encMessage


    async def communicate(self, message):
        uri = "ws://localhost:8765"

        async with websockets.connect(uri) as websocket:
            print(f"Device sends message: {message}")
            await websocket.send(message)

            response = await websocket.recv()
            print(f"Device received response: {response}")


    def publishMessage(self, subject, content):

        topic = self.chooseRightTopic(subject)
        cypheredText = self.cypherMessage(content, topic)
        message = '3 ' + self.prefix+ str(topic)[2:len(str(topic))-1] + ' ' + str(cypheredText)    #message structure : Flag Topic Content
        asyncio.get_event_loop().run_until_complete(self.communicate(message))

    def connectMessage(self):
        message = f"1 {self.name}"
        asyncio.get_event_loop().run_until_complete(self.communicate(message))


dev = device("i")

dev.publishMessage( "Alert", "coucou")

'''
topName = b'\xb9ih\nIC\xd3\xe0\xdd(\xecG8\x7f\x13\x15\x04\xca\x16x'
msg = "coucou"
print(dev.cypherMessage(msg, topName))
'''

'''
dev.connectMessage()
dev.publishMessage("test/1", "Bonjour")
dev.publishMessage("test/2", "Bonjour2")
dev.publishMessage("test/3", "Bonjour3")
'''