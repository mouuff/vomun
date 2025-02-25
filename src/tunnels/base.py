
class Tunnel(object):
    '''Base Tunnel class. Should be subclassed by other tunnels for
    compatibility reasons as well as ease of use.
    '''
    def connect(self, address, port):
        '''Use this tunnel to connect to `address`:`port`'''
        pass

    def disconnect(self, nodeid):
        '''Disconnect from a node at `nodeid`'''
        pass

class Connection(object):
    '''A class to store a connection to a peer'''
    pass
    
class Message(object):
    '''An object to store a message'''
    def __init__(self, from_ip, from_port, message):
        self.src = from_ip
        self.src_port = from_port
        self.msg = message