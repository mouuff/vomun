'''Handles the encryption and decryption of messages we get and send.
Documentation on the gngpg module: https://code.google.com/p/python-gnupg/
'''
import libs.errors
from api.functions import register_with_api

try:
    import gnupg
except ImportError:
    raise libs.errors.DependancyError(
        'Please install https://code.google.com/p/python-gnupg/')
        
import libs.globals

try:
    gpg = gnupg.GPG(gnupghome = libs.globals.global_vars['config']['gnupgdir'])
except ValueError:
    raise libs.errors.DependancyError('GPG does not appear to be installed.')

def generate_key(key_length = 2048, key_type = 'RSA', name = 'Anonymous'):
    '''Generate a key and return the key ID'''
    # TODO: use the name parameter
    key_data = gpg.gen_key_input(key_type = key_type, key_length = key_length)
    key = gpg.gen_key(key_data)

@register_with_api   
def encrypt_to(keyid, string):
    '''Encrypt a message with public key, `keyid`'''
    # TODO: Eventually we want to switch armor to False (binary data)
    gpg.encrypt(string, recipients = keyid) # TODO: find the right way

@register_with_api     
def sign_with(keyid, string):
    '''Sign string with `keyid`
    This will not be used in P2P data transfer but may be for other messages
    such as chat data.
    '''
    # TODO: make sure that this works
    gpg.sign(string, keyid = keyid)

@register_with_api
def decrypt(string):
    '''Decrypt `string`'''
    # TODO: make sure this actually works!
    return gpg.decrypt(string)

@register_with_api
def verify(string):
    '''Verify the signature on `string` and return the signing key ID'''
    # TODO: make sure this actually works!
    return gpg.verify(string)
