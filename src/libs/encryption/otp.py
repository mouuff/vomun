'''This module handles one-time pad encryption. This encryption method works
great for Anon+ because it allows for data of any size to be transfered without
an attacker being able to know anything about the data other than its length.
However, pad exchanges need to be done via a different encryption methods such
as GPG encryption.'''
import libs.encryption.base
from libs.errors import UsageError

class Encryption(libs.encryption.base.Encryption):
    '''One-time pad encryption class.'''
    ord_range = 255 # Maximum value of the ord function

    def encrypt(self, data):
        '''Encrypt data using a one-time pad.'''
        encrypted = ''
        for character in data:
            num = ord(character) + self.pad[-1]
            num = num % self.ord_range
            encrypted += str(num)
        return encrypted

    def set_pad(self, pad):
        '''Set the pad to given pad object.'''
        if isinstance(pad, Pad):
            self.pad = pad
        else:
            raise UsageError('The pad object must be an instance of Pad')

class Pad(object):
    '''Stores the current pad state and offers methods like pop()'''
    def __init__(self, pad):
        self.pad = pad

    def __len__(self):
        return len(self.pad)
    
    def pop(self):
        '''Remove the last character from the pad and return it.
        Yes, we are reading the pad backwards!
        '''
        last_char = self.pad[-1]
        self.pad = self.pad[0:-1]
        return last_char
            
