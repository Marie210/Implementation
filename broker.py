import asyncio
import websockets



class MqttMsg():
    def __init__(self, content, remainingRecipientNumber):
        self.content = content
        self.remainingRecipientNumber = remainingRecipientNumber


class topic:

    def __init__(self, name):
        self.name = name
        self.bytesName = b'0'
        self.subscribersList = []
        self.messageList = []

    def addSubscriber(self, sub):
        self.subscribersList.append(sub)

    def newMessage(self, msg):
        self.messageList.append(msg)

class broker:

    def __init__(self):

        self.deviceAuthenticationTokens = [b'\x821\xa5\x1b\x1c-\x19\xb3JPh\xf8B\xe6\x8f;\xea\x97\x07\xedV\x93T\xddQ\x97\xe0\x0b\xcb\xce\x80p\xe8\xa0?\x1e\xb1\x82Z(\x19\xee[\x18\xc6\xbc\x9ej', b'\xa2`\x1a\xc4^\xdcr\x13}\x97\x8b\xf4\xd9\xc1\x07\x9e\xbe"H\x84E\x8e\xbe\x90$8\x16\x04k5Zv\xbc\x17o-\xc1J\x7f\xad\xd9\xf9SX\xa0\xa2c\xa3', b'\xa0\xfdiHe\xc1\x8c\x81\xd1\xd8M\x1f\xaaF\xae\xd2\xc1\xc3#4\xa6\xefE\x81\x95\xb9\xe8!\xf2SRO\xee\x9aIr\xaa\x07\xe0K\xfacA\xed!\xbe\x12\x1f', b'\x83\xa5\xd8\x1b,\xa5kG\xd5p\xbd\x85DE\xb0X[\xec\xe3)\x1f<e3W7^\xb3\xde2\xcf\x95\x92\xd9\x0e\xe0\xed\x01\xba{\xfa\xde\x9e\xf5\xfdp:\xf7', b'\xac\xf0\xbb\xd1\xffR\x94\xd4\xd6m\x06\x9aBlJ\xec\xe8=\x1c)\x11R\xfa\x88;\x1d\'\x88b\x85\x1c\xfbt\n\xfa\xd5(\x97\xf0%Z"\x1a \xa4\x8c\xe4+', b'\x8d\x1a&[)BT(V\x84Fg%\xd2\x1f \x8b\xaa\xd4q\x0c\x99\xe5f\xed#\x07\x94*,`?\x99\x16\x9eo\x80\x14D^\xf6f\x0f=\xa6\xf2\xa4\x1a', b'\xa1\xf8\x8d\xf3I\xc3l\xac\xce\xbb\xc0\x08\xd4\xa8\xfd\x05\x85\x9f\x03x\xe9\x1b\xb6\x1aj\x84\x13\xd4\x08\x88\x9e\xb9\xd1a\x1c\xfbC\xf7\x92\x17\xd2"BK)\\\x1a\x82', b'\xa9\x9e\xeb>\xba\xc2\x7f\x03\xff\xe7\x05\xdd\xd7\x90\xfc\x16I\x05\xf2\xe6\xbc\xf31\xc4\xebe \xd5\xe6\xbb~9\xbey\x8f\xc4\xeb\xbb2\xb3\xd2\x9b\xee\xe2ygg?', b'\xa3/EH\xe4v\x8b\xe2\x9d\x9c_I\x9d\x01k\xab\xa4\xfc\x1c\xcc\xf3}\xa14jA\xdc\xd8mP\x18],\xcb\x96y`z\x02eK?\x11\xaf\x9b]\x85\xc5', b"\xa3\x10(\x1eT'n\xb2w\xfeO\x0e\x9cjz\x1d`\x92\xe0\xaa\x00\x9cR\xce\x18z\x92\xa6\x8eJ\xb7\xa7%\xf5\xa5\x93\xd4\x94W\x9b\x04\x02\xbb\x1e\xeb\x91\xcfm", b'\x81@~E\xca\x1c\x86\xd6\xa0\xf5\xd9\xdc}1~`\xa3\x08\n\xe4S\xf50\xb4#\xc3U\xc2\xc2\x90\x93\xe7\xb2_\xa6j~\xf5b\xe2\xe7O\xde\xe8I\x82\xe2;', b"\xb6,\xa2u#\x1b_j\xe0=\xec\xd3.\x98\rT\xa7\x915N\x07l\x14\xff:|\x98\xc4\xcb\xf47\xd3\x06\xdb\x18u\xc0\x93\t'\x12\xfc\xf1\x05I\xb5#\xfa", b'\x8b\xe1\x8e,\x14Gr2>.\xc9\r\x83\x93-mO\xb8Y\x1a\xb2\x9b#\x92\x96\xb55\xaf\xc5\xc9\xda=\x0c\xd7\x91\xd7\xe6\x93z\x08"y\n]\xef\r\x92\xc4', b"\xaa'\xcd\xd3\x17\x06\x1cS\x80v<\x92\xcad}e\xfbG\xda\xb57\xe1\x0c\xad\x9b\xa9po\xd3\x9aKRg!B\x02\x8cO\x917e\x0blg\xf8\x8dV\xea", b'\xa0_a\x14\x03\xfb\x06iKO\xe3k\xb3\x9a\xd5\xf3\xc3Z\xbf\x0f\xaa\x9e\x9c\xc7:\x8f\xcfz}\xd5\xbf\x91bD\x831\x9e\xad\xc3bl\x002\xf1\x1ec\xeb\xa9', b"\xa7{\xe2\x8c\x19\xcb\xb2\xd4\xe2'\xab\xdaHk\x8c\xf2@@\x9c\xe6<Hx\xae#\xa9&Z\xd2\xe5\x1a\x7f\xaa_R\xbe\x87\x03:\xa4[\x0b\xccb>\x8bU\xd4", b"\xb8t<5\xb1\x91\x97%#\x9c\xdd\xe6'p\xf9\\\xf3\x19U\xe8\xd0\xc0\xae\x96i\xf3V\x8cH3z\xd6d=\xe6\x17\x05=\x885X\x93\xee~3\xdc\xc6\x9c", b'\xb7r\x9f\xb2IcM\xce$.\xfe\xcf\xbc\xc6\xbe\x0c\x91\x17\xe4\xd6\xec\x0ccSW\x87l\xa27\x11\t\xf8\xb7G\xbf\x06"\xb7\xad\xfd\x07\xe6\n\xd7\xaf\xf4\xca\xd4', b'\xa1\xf0\x91\xe5p\xfe6\xa82Y\xf8{\xf2\xb2\xa0\xad(\xb5H!b\xacGY&\xf2\x1bH\xd8\x16\xfd\x13\xa5\x9d/I(\xb9y2\x97\xe0\xde\x9f\xe7\xbaW\xc3', b'\x87R\x95\xfe\xcb@\x95\'\xb0\xfc[\xcf\x1b\x92\x9a:o\x85\x00\x97O\x8c"W!\xa6=\x8e]L,q\xa3}\x94w(4^\x1e\x17\x8bG\xaf\xd0m@\x9a', b'\xa4\x06+\xca\xbdo\x13-\xf6\xf2\t\xf6B\xf3\x87\xedi\xa2k/\xa1\xcc.\xa2]\x98\xb5\xf6U*\xeb\xa6zR\x19\xa5\xea\x10\xb5\xd5\xe9\xb5H\xe6d&1\x84', b'\x8aCIH\xe1\xa5Ro\xc8g}\xb7n]\x96\x87\xbf\xed=\x85\x9aA\x03\xd4\xf8R\xbd_!j\x0c!\xae\xe2\xdf4)\x1c#\x93!2M\x9ep\xe2\xf2\xc5', b'\x81\xd3\xc6v\xa1\xbd\xc2\xc1\xc9Y;>\xd49^\x80@\x84X\xd3\x07+\x8f\xff\xb0Dih\xe5g\xea\xef\xf7\xda\xc18>o"\xe9$\x1dC_<j\x83\xf7', b'\x92\xfeuP9sY`\x0f\xddx\xcb]N\xf2\xcc\xca\x93l\x1b\x12\xfcSd\xf0\xbf\xf8|U\xba^\x99e\x07\xab\x01v\x14\x90\x81\xcb\x00\x1a;\xdc\xb1\xd1:', b'\x85\x81\xa7\x8e:m\x9aiZV\xf74L\x17\n\xf2\x0c\x9c\xd0\xd8\xf3\xc9\xbf5A$\xc4 \xaaE_SJ\x15\xbe%\xdbKUoe\xcb[\xfd\x14Ur\xd9', b'\x82\xea\xac]\xb9\x8c\xe80\xfc\xa6$\x08\xe4"CE\x95J&g\xbd\xa2\xf34F\x04\xe5Sh\xed\xc4\x05\xe8%\x9b\x02\x16\xb2\x7f-B\xd5U\x93\xbb\xe1\xefx', b'\x80Z\xf9h{.\xcfv=\x8d\xb4\xa0\xc8\x1fQ\xbc\xb8\xa8\xe9\xba\xe3\xa1\xce\xe6\x00\x9b:$.\xd6}\xfe\xdd\xf6\x90G\xdf\xdb\x99\xd3\xb0\x10O\x01R\xf7\xc9I', b'\xb1\xa0\x8d\x9a\xea\\\x9a09\xc8GX\x17\x18p\x1cc\n\xe8\x83\xa6\xa5\x8a\x8a\xc1M)\x0b\xc1\xd1\xe1\xbd@U\x7f#\x03\x9b%\xf0R\x1br8\xa3\xd2\xa4\x87', b'\x85x\xe9\xf6\xd1\xc6*\x065\x19\x17\xaf7-\n~\xcf\xe8\x98\x0c\x0bg\xe6\x1d\xff;qH\xa6\x12\xc3ij=\xfe\x89\xec\xe1\xb4\xdal\x02t<%V\x19\xf9', b'\x94Y|\xd8\x08s\x04\x12\x1eg\x14\xaf+\xf2\x8f\xe9\x04\xba\t\xf2\x80\'\xf3fT\xb1\xfb\xc2_\xf5\x9f\xca\xbd\xc0\x9b\xc8\xb1\x97\x13x\x04\x92"\x9a\xf58u\xe9']
        self.messageToTransmit = []
        self.listOfTopicsNameBytes = [b'\xb9ih\nIC\xd3\xe0\xdd(\xecG8\x7f\x13\x15\x04\xca\x16x',
                                 b'I\xca\xdfSl\xca\xce\xf2/\xf0\xf8\xe7|\xfa\x8a\x0c\x9d$\xc2\x99',
                                 b'kR\xa2\xa5k\x9ff\x05O]\xd7)\xfe\xac\x85\x90?|D\xc2',
                                 b'@?!B\xdc\xa2+\xa5\xd0\xf18\xc9\xc2s\xc6\xa4\x9af\xb5V',
                                 b'\xee\xc4dBY\xa3\xfe\xa3`0._\xb0b\xda\xf8\xe16\xb4\xd1',
                                 b'\x15\xbc\xf2G2\xa0\xb2\xf6\x15\xb5\xd7\r\x1eau\xb9\xa6`\xb7P',
                                 b'N\x8b\xda\xb6P\x95\xa0U\x99N\x8eL=\xc5\xa3\xae\x12Y\x0b\x9a',
                                 b'\xd0\xa3\xb3+@\x00L\x15D@\x86RP\x0b\x83\x94[!\xe2\x82',
                                 b'\xf4\xf2v\xb4\xdb\xde\xd4\xa8\x12\x12\xc3\x84YJ\x19|\xcc\x15o\x89',
                                 b';c\xfc\xe7\xe5\xf6$\xae\x13Y\xd7\xb2\xda\xe0\x192u\x05\x92B',
                                 b'-\xb7\x98o\xed\x1a$\xd6\xd6\xe9\x0bC5\x9br\xf2g)\x82\xa2',
                                  b'\xcb\x81\x9e\xbc\xd1\xe3\xa0\x80X4k7\x96\xac8\xe6>\x8d\xdc\xeb',
                                  b'nW\xd7\xde\xd5S\xba^\t{\x83@\x17\xaa;\xb2^!1\x03',
                                  b'\x10\x19dh\x89L\x00\x8bV.\xf8\xbcq\xd4D\x88\x91\n.\x9a',
                                 b'\xe6\xb9\xa8\xcd@\xc9q\xdc\x18\xe5\x01\xf6\xce\x03\xf9*(a\xf5e',
                                 b'&\xac\xae`\x0fs\x97J\x8bH\x89RQM\xa8\x91\xed\xe8\x8ds',
                                 b'\x13\x99LL*\xc7\xab\xb8\xfdf\x06\xad\xb6\x13\xac\xba\xa7\x7f\x8a\x1e',
                                 b'\x15b\xb9\xa4W\xa9hWWW,\xb8v\xf3\x9d3\x1f{_\xc5',
                                 b'\xafk\xd1*\xf4\xbb\xe2\xad<\xe9\x02\xab\xcd\x17\xcc\r|\xa8O\x87',
                                 b'k\x05\xc1\x06\x93\xaf\r\xc2P\xec+\xc3\xc3OB\x11\x1eG\x85`',
                                 b'\n\x90b\xa9\xcbQ\x99]\xea\x9f\xad\x8dP\xa6Q\xddu\xa2&\xf9',
                                 b"m\xb2\x99\x1e\x86r\x86\xdaZ\xff\t'p\x13\x10\x02\xab\xe1\x15\x8d",
                                 b"\xf1\x11'\x1e\x94\xfa\x90\xce\x03\x86\x0e\xac\xb2*\xa9-q\x80\x0cm",
                                 b'\x80A\x14\xe1\x80?&\xbfO\xba\xb2bS\xac\x07\xac\x08\xf35\xeb',
                                 b'\xb6r\x1d\x13\x18@6b\x9b\xd1\xcaA6\xef\xec\xdc*i\x173',
                                 b'k/e\xfa\xd9\x99\x1a\x850\xeb\xe7\xb6(&v\xdf\xef\x8er\xa5',
                                 b'\x98e\x1cn&\xc7\xd3\xe6g\x86\xa8s\xed\x84\xb1_\xf9\xad\xebC',
                                 b'\x8c\x16\xee(b\x12\x9a\x98b\xe4toDa\xabT\xcf\xb7\x17\xb0',
                                 b'\x08\x90\xaf\x89$\xe0\xef\x7f5H>=~\x15-J\xa1\xdbE\xce',
                                 b'\xd3\x1b\xb9\x1d\x8f\xd0n"Z\xbf\xda\x9axc9\xd1Y\xa1P\xd4']

        self.listOfTopicsName = []

        for i in range(len(self.listOfTopicsNameBytes)):
            self.listOfTopicsName.append("Pref/" + str(self.listOfTopicsNameBytes[i])[2:len(str(self.listOfTopicsNameBytes[i])) - 1])

        self.listOfTopics = []
        for elem in self.listOfTopicsName:
            top = topic(elem)
            top.bytesName = self.listOfTopicsNameBytes[self.listOfTopicsName.index(elem)]
            self.listOfTopics.append(top)
        self.usersSubscriptions = {}


    def newTopic(self, name):
        print(f"new topic {name}")
        top = topic(name)
        self.listOfTopics.append(top)
        self.listOfTopicsName.append(name)

    def testFct(self):
        self.newTopic("test/testTopic")
        self.newTopic("test/testTopic2")

    def testFct2(self):
        top = "test/testTopic"
        content = "coucou la team"
        for i in range(len(self.listOfTopicsName)):
            if top == self.listOfTopicsName[i]:
                mes = MqttMsg(content, len(self.listOfTopics[i].subscribersList))
                self.listOfTopics[i].messageList.append(mes)
                print(f"{mes.content} PUBLISHED ON {self.listOfTopicsName[i]}")

    def connect(self, msg):

        if msg[0:6] == "device":
            print(f"{msg} connected")
            txt = "Connection succeeded"
        else:
            mesList = []
            topList = []
            txt = [mesList, topList]
            if msg in self.usersSubscriptions:
                for elem in self.usersSubscriptions[msg]:
                    for mes in elem.messageList:
                        mesList.append(mes.content)
                        topList.append(elem.bytesName)
                        #txt +=(f"MESSAGE: {mes.content} FROM TOPIC:{elem.name} \n")
                        mes.remainingRecipientNumber -=1
                        if mes.remainingRecipientNumber <1:
                            elem.messageList.remove(mes)
            else:
                txt = "Connection succeeded"
            print(f"{msg} connected")
        return txt

    def publish(self, msg):
        a = 0
        top = msg[0: msg.find(' ')]
        content = msg[msg.find(' ')+1:]
        for i in range(len(self.listOfTopicsName)):
            if top == self.listOfTopicsName[i]:
                a = 1
                mes = MqttMsg(content, len(self.listOfTopics[i].subscribersList))
                self.listOfTopics[i].messageList.append(mes)
                print(f"{mes.content} PUBLISHED ON {self.listOfTopicsName[i]}")

        if a == 0:
            self.newTopic(top)
            mes = MqttMsg(content, 0)
            self.listOfTopics[len(self.listOfTopics)-1].messageList.append(mes)
            print(f"{mes.content} PUBLISHED ON {self.listOfTopicsName[len(self.listOfTopics)-1]}")

        return "Successful publish"


    def subscribe(self, topName, userName):

        i = 0
        if topName[len(topName)-1] != "#":                    #subscribe to only one topic
            if topName in self.listOfTopicsName:
                i = self.listOfTopicsName.index(topName)
                if userName not in self.listOfTopics[i].subscribersList:
                    self.listOfTopics[i].subscribersList.append(userName)
            else:
                self.newTopic(topName)
                i = len(self.listOfTopicsName) -1
                self.listOfTopics[i].subscribersList.append(userName)

            if userName in self.usersSubscriptions:
                self.usersSubscriptions[userName].append(self.listOfTopics[i])
            else:
                self.usersSubscriptions[userName] = [self.listOfTopics[i]]

            print(f"{userName} subscribed to {topName}")

        else:                                   #subscribe to a set op topics
            prefix = topName[: len(topName) - 1]
            for elem in self.listOfTopicsName:
                if prefix in elem:
                    i = self.listOfTopicsName.index(elem)
                    if userName not in self.listOfTopics[i].subscribersList:
                        self.listOfTopics[i].subscribersList.append(userName)
                    if userName in self.usersSubscriptions:
                        self.usersSubscriptions[userName].append(self.listOfTopics[i])
                    else:
                        self.usersSubscriptions[userName] = [self.listOfTopics[i]]

            print(f"{userName} subscribed to all topic begining with {prefix}")

        return "Subscription completed"



    def receivedMsg(self, msg):
        resp= 0
        flag = int(msg[0])
        if flag == 1:
            resp = self.connect(msg[2:])
        elif flag ==3:
            resp = self.publish(msg[2:])
        elif flag == 8:
            resp = self.subscribe(msg[2:msg.find(" ",2)], msg[msg.find(" ", 2)+1 :])
        else:
            print("???")
        return resp


    async def handler(self, websocket):
        async for message in websocket:
            print(f"Admin received message: {message}")
            resp = self.receivedMsg(message)
            if len(resp) == 2:
                await websocket.send(f"{len(resp[0])}")
                for i in range(len(resp[0])):
                    await websocket.send(f"{resp[0][i]}")
                    print(await websocket.recv())
                    await websocket.send(resp[1][i])
                    print(await websocket.recv())
            else:
                await websocket.send(f"0{resp}")


    def listen(self):
        server_port = 8765  # Choose a port for the server
        server_uri = f"ws://localhost:{server_port}"

        start_server = websockets.serve(self.handler, "localhost", server_port)

        print(f"WebSocket server, alias the broker, listening on {server_uri}")

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

