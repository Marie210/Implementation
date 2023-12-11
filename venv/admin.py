import asyncio
import websockets
import py_ecc
#from py_ecc.bls import G2ProofOfPossession as bls_pop
#import random as rd
#import os
import hashlib
import tate_bilinear_pairing as tbp
from tate_bilinear_pairing import eta


T_SIZE = 10
M_size = 20
C_size = 8

class admin:

    def __init__(self):
        self.deviceChallengeList = [[b'\xb9ih\nIC\xd3\xe0\xdd(\xecG8\x7f\x13\x15\x04\xca\x16x', b'I\xca\xdfSl\xca\xce\xf2/\xf0\xf8\xe7|\xfa\x8a\x0c\x9d$\xc2\x99', b'kR\xa2\xa5k\x9ff\x05O]\xd7)\xfe\xac\x85\x90?|D\xc2', b'@?!B\xdc\xa2+\xa5\xd0\xf18\xc9\xc2s\xc6\xa4\x9af\xb5V', b'\xee\xc4dBY\xa3\xfe\xa3`0._\xb0b\xda\xf8\xe16\xb4\xd1', b'\x15\xbc\xf2G2\xa0\xb2\xf6\x15\xb5\xd7\r\x1eau\xb9\xa6`\xb7P', b'N\x8b\xda\xb6P\x95\xa0U\x99N\x8eL=\xc5\xa3\xae\x12Y\x0b\x9a', b'\xd0\xa3\xb3+@\x00L\x15D@\x86RP\x0b\x83\x94[!\xe2\x82', b'\xf4\xf2v\xb4\xdb\xde\xd4\xa8\x12\x12\xc3\x84YJ\x19|\xcc\x15o\x89', b';c\xfc\xe7\xe5\xf6$\xae\x13Y\xd7\xb2\xda\xe0\x192u\x05\x92B'], [b'-\xb7\x98o\xed\x1a$\xd6\xd6\xe9\x0bC5\x9br\xf2g)\x82\xa2', b'\xcb\x81\x9e\xbc\xd1\xe3\xa0\x80X4k7\x96\xac8\xe6>\x8d\xdc\xeb', b'nW\xd7\xde\xd5S\xba^\t{\x83@\x17\xaa;\xb2^!1\x03', b'\x10\x19dh\x89L\x00\x8bV.\xf8\xbcq\xd4D\x88\x91\n.\x9a', b'\xe6\xb9\xa8\xcd@\xc9q\xdc\x18\xe5\x01\xf6\xce\x03\xf9*(a\xf5e', b'&\xac\xae`\x0fs\x97J\x8bH\x89RQM\xa8\x91\xed\xe8\x8ds', b'\x13\x99LL*\xc7\xab\xb8\xfdf\x06\xad\xb6\x13\xac\xba\xa7\x7f\x8a\x1e', b'\x15b\xb9\xa4W\xa9hWWW,\xb8v\xf3\x9d3\x1f{_\xc5', b'\xafk\xd1*\xf4\xbb\xe2\xad<\xe9\x02\xab\xcd\x17\xcc\r|\xa8O\x87', b'k\x05\xc1\x06\x93\xaf\r\xc2P\xec+\xc3\xc3OB\x11\x1eG\x85`'], [b'\n\x90b\xa9\xcbQ\x99]\xea\x9f\xad\x8dP\xa6Q\xddu\xa2&\xf9', b"m\xb2\x99\x1e\x86r\x86\xdaZ\xff\t'p\x13\x10\x02\xab\xe1\x15\x8d", b"\xf1\x11'\x1e\x94\xfa\x90\xce\x03\x86\x0e\xac\xb2*\xa9-q\x80\x0cm", b'\x80A\x14\xe1\x80?&\xbfO\xba\xb2bS\xac\x07\xac\x08\xf35\xeb', b'\xb6r\x1d\x13\x18@6b\x9b\xd1\xcaA6\xef\xec\xdc*i\x173', b'k/e\xfa\xd9\x99\x1a\x850\xeb\xe7\xb6(&v\xdf\xef\x8er\xa5', b'\x98e\x1cn&\xc7\xd3\xe6g\x86\xa8s\xed\x84\xb1_\xf9\xad\xebC', b'\x8c\x16\xee(b\x12\x9a\x98b\xe4toDa\xabT\xcf\xb7\x17\xb0', b'\x08\x90\xaf\x89$\xe0\xef\x7f5H>=~\x15-J\xa1\xdbE\xce', b'\xd3\x1b\xb9\x1d\x8f\xd0n"Z\xbf\xda\x9axc9\xd1Y\xa1P\xd4']]
        self.deviceResponseList = [[b'I\xca\xdfSl\xca\xce\xf2/\xf0\xf8\xe7|\xfa\x8a\x0c\x9d$\xc2\x99', b'kR\xa2\xa5k\x9ff\x05O]\xd7)\xfe\xac\x85\x90?|D\xc2', b'@?!B\xdc\xa2+\xa5\xd0\xf18\xc9\xc2s\xc6\xa4\x9af\xb5V', b'\xee\xc4dBY\xa3\xfe\xa3`0._\xb0b\xda\xf8\xe16\xb4\xd1', b'\x15\xbc\xf2G2\xa0\xb2\xf6\x15\xb5\xd7\r\x1eau\xb9\xa6`\xb7P', b'N\x8b\xda\xb6P\x95\xa0U\x99N\x8eL=\xc5\xa3\xae\x12Y\x0b\x9a', b'\xd0\xa3\xb3+@\x00L\x15D@\x86RP\x0b\x83\x94[!\xe2\x82', b'\xf4\xf2v\xb4\xdb\xde\xd4\xa8\x12\x12\xc3\x84YJ\x19|\xcc\x15o\x89', b';c\xfc\xe7\xe5\xf6$\xae\x13Y\xd7\xb2\xda\xe0\x192u\x05\x92B', b'\xd2\xf8\xfd\xc6yu\xd8\x95k\x88Du\x80G\xbc\xa1\xb7|^\x1d'], [b'\xcb\x81\x9e\xbc\xd1\xe3\xa0\x80X4k7\x96\xac8\xe6>\x8d\xdc\xeb', b'nW\xd7\xde\xd5S\xba^\t{\x83@\x17\xaa;\xb2^!1\x03', b'\x10\x19dh\x89L\x00\x8bV.\xf8\xbcq\xd4D\x88\x91\n.\x9a', b'\xe6\xb9\xa8\xcd@\xc9q\xdc\x18\xe5\x01\xf6\xce\x03\xf9*(a\xf5e', b'&\xac\xae`\x0fs\x97J\x8bH\x89RQM\xa8\x91\xed\xe8\x8ds', b'\x13\x99LL*\xc7\xab\xb8\xfdf\x06\xad\xb6\x13\xac\xba\xa7\x7f\x8a\x1e', b'\x15b\xb9\xa4W\xa9hWWW,\xb8v\xf3\x9d3\x1f{_\xc5', b'\xafk\xd1*\xf4\xbb\xe2\xad<\xe9\x02\xab\xcd\x17\xcc\r|\xa8O\x87', b'k\x05\xc1\x06\x93\xaf\r\xc2P\xec+\xc3\xc3OB\x11\x1eG\x85`', b'==|B8\x1fz)\xa8\x15\x00N\xfe\xb3@\x04\x90M\x07\xb9'], [b"m\xb2\x99\x1e\x86r\x86\xdaZ\xff\t'p\x13\x10\x02\xab\xe1\x15\x8d", b"\xf1\x11'\x1e\x94\xfa\x90\xce\x03\x86\x0e\xac\xb2*\xa9-q\x80\x0cm", b'\x80A\x14\xe1\x80?&\xbfO\xba\xb2bS\xac\x07\xac\x08\xf35\xeb', b'\xb6r\x1d\x13\x18@6b\x9b\xd1\xcaA6\xef\xec\xdc*i\x173', b'k/e\xfa\xd9\x99\x1a\x850\xeb\xe7\xb6(&v\xdf\xef\x8er\xa5', b'\x98e\x1cn&\xc7\xd3\xe6g\x86\xa8s\xed\x84\xb1_\xf9\xad\xebC', b'\x8c\x16\xee(b\x12\x9a\x98b\xe4toDa\xabT\xcf\xb7\x17\xb0', b'\x08\x90\xaf\x89$\xe0\xef\x7f5H>=~\x15-J\xa1\xdbE\xce', b'\xd3\x1b\xb9\x1d\x8f\xd0n"Z\xbf\xda\x9axc9\xd1Y\xa1P\xd4', b'\xa6.\xe9\x8a\x05\x19\xb2q\xacv\x18\x92t\xdcC\r\x0cNo\x81']]
        self.deviceSubjectList = ["Alert", "StateOfCharge", "Temperature"]
        self.deviceIPrefix = "Pref"
        self.usersPSWRD = {"Sophie":  b'\x1fq,]x\x84s\x94\xc1\x84\xaa\xe3\x95\xc37\xf2J\x9a\x0eQ\x92*n\x0b\xea\t\xf0\xf4\x85H\x01\x94'}
        self.userAuthorization = {"Sophie":["Alert","StateOfCharge"]}

        tbp.eta.init(151)
        self.eccGenerator = tbp.ecc.gen()

        '''
        self.authenticationTokensForI = []

        for i in range(len(self.deviceResponseList)):
            for j in range(len(self.deviceResponseList[0])):
                private_key = int.from_bytes(self.deviceResponseList[i][j], 'big')
                public_key = tbp.ecc.scalar_mult(private_key, self.eccGenerator)
                self.authenticationTokensForI.append(public_key)
        '''
        '''
        rd.seed(34)
        private_key = rd.randint(0, (2**150))  #int.from_bytes(os.urandom(31), 'big')
        self.brokerPublic_key = bls_pop.SkToPk(private_key)
        '''

        userIdPointValue = int.from_bytes(hashlib.sha256("user".encode(encoding='UTF-8', errors='strict')).digest(),
                                          'big')
        self.userIdPoint = tbp.ecc.scalar_mult(userIdPointValue, self.eccGenerator)

    def generateToken(self, topName, i, j):
        print(f"resp in bytes : {self.deviceResponseList[i][j]}")
        resp = int.from_bytes(self.deviceResponseList[i][j], 'big')
        print(f"resp: {resp}")
        token = tbp.ecc.scalar_mult(resp, self.userIdPoint)
        print(token)
        return token

    def verifyPSSWRD(self, psswrd, user):
        if self.usersPSWRD[user] == hashlib.sha256(psswrd.encode(encoding='UTF-8', errors='strict')).digest():
            return True
        else:
            return False

    def verifyIfUserAuthorized(self, user, topic):

        i, j = 0, 0
        print(type(topic))
        for elem in self.deviceChallengeList:
            if topic in elem:
                i = self.deviceChallengeList.index(elem)
                print(i)
                j = elem.index(topic)

        if self.deviceSubjectList[i] in self.userAuthorization[user]:
            token = self.generateToken(topic, i, j)
            print(token)
            return (True, token, self.deviceSubjectList[i])
        else:
            return (False, 0, "Not authorized")





    async def handler(self, websocket, path):
        async for message in websocket:
            user = message[:message.find(' ')]
            psswrd = message[message.find(' ')+1:]
            print(f"Broker demand of connection from {user}")
            if self.verifyPSSWRD(psswrd, user) == True:
                print(f"Password accepted, authentication succeeded")
                await websocket.send(f"Password accepted, authentication succeeded")
            else:
                print("Wrong password")
                await websocket.send(f"Wrong password, authentication denied")
                exit
            topic = await websocket.recv()
            autho, token, topName =self.verifyIfUserAuthorized(user, topic)

            if autho ==True:
                await websocket.send(f"{token} ###{topName}")
                print (f"Secret token sent")
            else:
                await websocket.send(f"Authorization denied")

    def listen(self):
        server_port = 8766  # Choose a port for the server
        server_uri = f"ws://localhost:{server_port}"

        start_server = websockets.serve(self.handler, "localhost", server_port)

        print(f"The Admin WebSocket server listening on {server_uri}")

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

ad = admin()

ad.listen()
