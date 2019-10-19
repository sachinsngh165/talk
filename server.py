import sys


from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor,ssl

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol,listenWS

from autobahn.twisted.resource import WebSocketResource

from autobahn.websocket.types import ConnectionDeny
rooms = {}
User2Room = {}

class Room():
    def __init__(self,roomId,password):
        self.roomId = roomId
        self.Clients = {}
        self.password = password

    def addUser(self,client):
        print(client.peer + " added ")
        self.Clients[client.peer]=client

    def removeUser(self,client):
        try:
            self.Clients.pop(client.peer)
            print(client.peer + " removed from room ")
        except:
            pass

    def isExist(self,clientId):
        if clientId in self.Clients:
            return True
        return False

    def numberOfClients(self):
        return len(self.Clients)

    def getAllClients(self):
        return self.Clients

    def getPassword(self):
        return self.password

class SomeServerProtocol(WebSocketServerProtocol):


    def onConnect(self, request):
        print(request.params)
        if 'roomID' not in request.params :
            raise ConnectionDeny(403, reason=unicode("roomID required"))
        roomID = request.params['roomID'][0]
        if 'password' not in request.params:
            raise ConnectionDeny(403, reason=unicode("password required"))
        password = request.params['password'][0]
        if roomID not in rooms:
            rooms[roomID]= Room(roomID,password)
            room = rooms[roomID]
            User2Room[request.peer] = roomID
            print(roomID + " room created ")
        else:
            room = rooms[roomID]
            if password != room.getPassword():
                raise ConnectionDeny(403, reason=unicode("! incorrect password"))
            User2Room[request.peer] = roomID
        
    def onOpen(self):
        self.factory.register(self)
        print("Connection is opened")

    def connectionLost(self, reason):
        print("Connect is closed")
        self.factory.unregister(self)

    def onMessage(self, payload, isBinary):
        self.factory.communicate(self, payload, isBinary)

class ChatRouletteFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(ChatRouletteFactory, self).__init__(*args, **kwargs)

    def register(self,client):
        rid = User2Room[client.peer]
        room = rooms[rid]
        room.addUser(client)
        print("number of client= "+str(room.numberOfClients()))
        if room.numberOfClients()==1:
        	client.sendMessage("initiator")
    	elif room.numberOfClients()==2:
    		client.sendMessage("not initiator")
    	else:
    		client.sendMessage("only 2 clients can connect")

    def unregister(self, client):
        try:
            rid = User2Room[client.peer]
            rooms[rid].removeUser(client)
            User2Room.pop(client)
            if rooms[rid].numberOfClients() <=0:
                rooms.pop(rid)
        except:
            pass


    def communicate(self, client, payload, isBinary):
    	print(payload)
        rid = User2Room[client.peer]
        room = rooms[rid]
        partners = room.getAllClients()
        if not partners:
            client.sendMessage("Sorry you dont have partner yet, check back in a minute")
        else:
            for partner in partners:
                if client.peer != partner:
                    partners[partner].sendMessage(payload)



if __name__ == "__main__":
    log.startLogging(sys.stdout)
    factory = ChatRouletteFactory("ws://localhost:8080")
    factory.setProtocolOptions(maxFramePayloadSize=1048576,
                                     maxMessagePayloadSize=1048576,
                                     autoFragmentSize=65536,
                                     failByDrop=False,
                                     openHandshakeTimeout=2.5,
                                     closeHandshakeTimeout=1.,
                                     tcpNoDelay=True,
                                     autoPingInterval=1.,
                                     autoPingTimeout=1.,
                                     autoPingSize=4,
                                     allowedOrigins=[
                                    "*",
                                    ],
                                )

    factory.protocol = SomeServerProtocol
    listenWS(factory)
    webdir = File("./client")
    web = Site(webdir)
    reactor.listenTCP(9000, web)
    reactor.run()

