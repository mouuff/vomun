#! /usr/bin/env python
print('''
=== Anon+ Setup ===
== Project Vomun ==
''')
import os
import libs.errors

# Import gnupg
try:
    import gnupg
except ImportError:
    raise libs.errors.DependancyError(
                'Please install https://code.google.com/p/python-gnupg/')
                                      

# Create ~/.vomun/
print('[*] Making ~/.vomun/')

## Key setup
print('[*] Setting up encryption keys')
# Create ~/.vomun/keys/
print(' [*] Making ~/.vomun/keys/')

# Create ~/.vomun/keys/private/
print(' [*] Making ~/.vomun/keys/private/')

# Generate 2048 bit node key
print(' [*] Generating a 2048 bit node key')
print('     this could take a while...')

# Generate 2048 bit identity key
print(' [*] Generating a 2048 bit identity key')
print('     this could take a while...')
