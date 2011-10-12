import gnupg
try:
    gpg = gnupg.GPG(gnupghome = '') # TODO: read path from config
except ValueError:
    print('[*] ERROR: GPG does not appear to be installed.')

def generate_key(keylength = 2048):
    '''Generate a key and return the key ID'''
    pass
    
def encrypt_to(keyid, string):
    '''Encrypt a message with public key, `keyid`'''
    pass
    
def sign_with(keyid, string):
    '''Sign string with `keyid`'''
    pass
    
def decrypt(string):
    '''Decrypt `string`'''
    pass
    
def verify(string):
    '''Verify the signature on `string` and return the signing key ID'''
    pass
