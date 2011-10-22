'''This module loads a list of friends out of ~/.vomun/friends.json'''
import json
import os.path


import tunnels.directudp as directudp
from tunnels.base import ConnectionError
from libs.globals import global_vars
import libs.encryption
from packets import parse_packets,packets_by_id,make_packet
from api.functions import register_with_api

global_vars["friends"] = {}
friendlistpath = os.path.expanduser("~/.vomun/friends.json")
friendlistr = open(friendlistpath,"r")

def load_friends():
    '''Load the List of friends'''
    friendsjson = json.loads(friendlistr.read())
    for friend in friendsjson:
        try:
            port = friend["port"]
            keyid = friend["keyid"]
            name = friend["name"]
            ip = friend["lastip"]
            friendo = Friend(keyid, ip, port, name)

            print friendo
            global_vars["friends"][keyid] = friendo

        except Exception as ex: 
            print ex, friend

@register_with_api
def save_friends():
    '''Write ~/.vomun/friends.json'''
    friendlistw = open(friendlistpath,"w+")
    json = """[
%s
]"""
    friendsjson = ",".join([friend._json() for friend in global_vars["friends"].values()])

    friendlistw.write(json % friendsjson)

@register_with_api
def add_friend(keyid,ip, port = 1337, name = "unknown"):
    '''Add a friend to our friends list'''
    friend_obj = Friend(keyid, ip, port, name)
    global_vars["friends"][keyid] = friend_obj

@register_with_api
def del_friend(keyid):
    '''Delete a friend'''
    try:
        del global_vars["friends"][keyid]
    except:
        global_vars["logger"].info("could not delete friend %s: Friend not found" % keyid)


        
class Friend:
    def __init__(self, keyid, ip, port=1337, name = "unknown",):
        '''Defines a friend, can be used to send a message'''
        self.ip = ip
        self.port = port
        self.name = name
        self.keyid = keyid
        self.connected = False
        self.rconnection = None
        self.wconnection = None
        self.data = ""

    def parse_packets(self):
        print "parsing packets of %s" % self.name
        packets,leftovers =  parse_packets(self.data)
        self.data = leftovers
        print "leftovers:", leftovers
        for packet in packets:
            self.handle_packets(packet[0],packet[1])

    def handle_packets(self, packetId, packet):
        if packetId in packets_by_id:
            packetId = packets_by_id[packetId]

        else:
            reason = "Invalid packetId: %i" % packetId
            disc = make_packet("Disconnect",reasonType="Custom",reason=reason,reasonlength=len(reason))
            self.send(disc)
            return
        if packetId == "ConnectionRequest":
            print "sending acceptConnection"
            #self.connected = True
            accept_connection = make_packet("AcceptConnection",int=1)
            self.send(accept_connection,1)
            print "acceptConnection sent"

        elif packetId == "AcceptConnection":
            print "got acceptConnection"
            self.connected = True
        else:
            print packetId,packet

    def rename(self, newname):
        '''Rename the Friend'''
        self.name = name

    def connect(self):
        '''Connect to the friend'''
        self.wconnection = directudp.Connection(self)
        #self.connected = True

    def send(self, Message,system=0):
        '''Send a message to the friend. Will try to establish a connection, if not yet connected'''
        if self.wconnection == None:
            self.connect()
            #if not self.connected:
            #    raise ConnectionError("Could not reach %s" % self.ip)
        if not self.connected and not system:
            print "not connected: Message discarded. Message was: %s" % Message
            return
        self.wconnection.send(Message)

    def _json(self):
        '''Returns the json representation of a friend, used to save the friendlist'''
        return """
    {
        "name": "%s",
        "keyid": "%s",
        "lastip": "%s",
        "port": %i    
    }""" % (self.name,self.keyid,self.ip,self.port)

    def _rpc(self):
        '''Returns the dict representation of the friend, used by the rpc server'''
        return {
            "name" : self.name,
            "keyid": self.keyid,
            "lastip" : self.ip,
            "port" : self.port
        }
    def __str__(self):
        return "<friend %s on %s:%i with id %s>" % (
                self.name, self.ip, self.port, self.keyid)

#api section

@register_with_api
def getFriendWithIP(ip):
    for friend in global_vars["friends"].values():
        if friend.ip == ip:
            return friend

@register_with_api
def getFriendWithName(Name):
    for friend in global_vars["friends"].values():
        if friend.name == Name:
            return friend

@register_with_api
def getFriendWithKey(keyid):
    for friend in global_vars["friends"].values():
        if friend.keyid == keyid:
            return friend

@register_with_api
def friend_send(friendname, message):
    return getFriendWithName(friendname).send(message)


@register_with_api
def friend_connect(friendname):
    return getFriendWithName(friendname).connect()


@register_with_api
def friend_rename(friendname, newname):
    return getFriendWithName(friendname).rename(newname)

@register_with_api
def friend_list():

    friendslist = [friend._rpc() for friend in global_vars["friends"].values()]
    return friendslist