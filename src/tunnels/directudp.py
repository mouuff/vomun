import time
import socket
import threading
import libs.threadmanager
import tunnels.base
import libs.events
from libs.packets import make_packet
from libs.construct import *
connections = {}

class Tunnel(tunnels.base.Tunnel):
    '''Make a direct UDP connection to a peer'''
    pass
    
class Connection(tunnels.base.Connection):
    '''UDP "connection" to a peer'''
    def __init__(self, node): # TODO switch to a global node class
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((node.ip, node.port))
    
        self.data = ""
        self.packages = {}
        
        self.beginHandshake()
        #self.send('{"type":"connect_request"}')
        
    def beginHandshake(self):
        connectionRequest = libs.packets.packets[0]
        ip = "192.168.1.104"
        key="5416435343454"
        packet = make_packet("ConnectionRequest", encryptionmethod="aes",ip=ip, iplength = len(ip), key = key, keylength = len(key))
        self.send(packet)
        
        #handshake is ended in friends.handle_packets
    def send(self, Message):
        self.sock.send(Message)

    
    
class Listener(libs.threadmanager.Thread):
    '''Listen for UDP connections on our port'''
    def __init__(self, port = 1337):
        super(Listener, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.sock.bind(('0.0.0.0', port)) # TODO: bind other addresses
        self.sock.setblocking(False)
        
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        
    def run(self):
        leftover = ""
        while not self._stop.isSet():
            try:
                data = self.sock.recvfrom(4096)
                ip = data[1][0]
                friend = libs.friends.getFriendWithIP(ip)
                friend.connection = self.sock
                friend.data += data[0]
                friend.parse_packets()
                friend.connection = self.sock
            except socket.error, error:
                if error.errno == 11: # No messages
                    time.sleep(1)       
        
        
def start():
    listener = Listener()
    listener.start()
    libs.threadmanager.register(listener)
    
