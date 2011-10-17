'''Run a server on 127.0.0.1:3451 for the localhost API. Parse the packets
with api.packets when we get them.
'''

import socket
import libs.threadmanager

class Server(libs.threadmanager.Thread):
    '''Threaded server class'''
    def __init__(self):
        super(Server, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('127.0.0.1', 3451))
        self.sock.setblocking(False)
        
    def run(self):
        if not self._stop.isSet():
            try:
                packet = self.sock.recvfrom(4096)
                ip = packet[1][0]
                data = packet[0]
                
                
            except socket.error, error:
                if error.errno == 11: # No new messages
                    time.sleep(1)
                else:
                    raise error
            