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
    def __init__(self,roomId):
        self.roomId = roomId
        self.Clients = {}

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

class SomeServerProtocol(WebSocketServerProtocol):


    def onConnect(self, request):
        print(request.params)
        if 'roomID' not in request.params :
            raise ConnectionDeny(403, reason=unicode("roomID required"))
        roomID = request.params['roomID'][0]
    
    
        if roomID not in rooms:
            rooms[roomID]= Room(roomID)
            room = rooms[roomID]
            User2Room[request.peer] = roomID
            print(roomID + " room created ")
        else:
			room = rooms[roomID]
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
            rooms[rid].removeUser(client.peer)
            User2Room.pop(client.peer)
            if rooms[rid].numberOfClients <=0:
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



    log.startLogging(sys.stdout)

    # SSL server context: load server key and certificate
    # We use this for both WS and Web!
    contextFactory = ssl.DefaultOpenSSLContextFactory('keys/server.key',
                                                      'keys/server.crt')

    factory = ChatRouletteFactory(u"wss://35.229.213.23:443")
    # by default, allowedOrigins is "*" and will work fine out of the
    # box, but we can do better and be more-explicit about what we
    # allow. We are serving the Web content on 8080, but our WebSocket
    # listener is on 9000 so the Origin sent by the browser will be
    # from port 8080...


    factory.setProtocolOptions(maxFramePayloadSize=1048576,
                                     maxMessagePayloadSize=1048576,
                                     autoFragmentSize=65536,
                                     failByDrop=False,
                                     openHandshakeTimeout=20.5,
                                     closeHandshakeTimeout=10.,
                                     tcpNoDelay=True,
                                     autoPingInterval=10.,
                                     autoPingTimeout=5.,
                                     autoPingSize=4,
                                     # perMessageCompressionOffers=offers,
                                     # perMessageCompressionAccept=accept,
                                     allowedOrigins=[
                                         "https://35.229.213.23:443",
                                        "https://127.0.0.1:8080",
                                        "https://localhost:8080",
        ],)


    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)


    webdir = File(".")
    webdir.putChild(b"ws",resource)
    webdir.contentTypes['.crt'] = 'application/x-x509-ca-cert'
    web = Site(webdir)
    reactor.listenSSL(443, web, contextFactory)

    reactor.run()

