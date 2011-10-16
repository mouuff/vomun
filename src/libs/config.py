'''Manage the configuration file. Load/save/modify it.'''
import os

def load_config():
    '''Load the configuration file from ~/.vomun/config.*
    TODO: Decide on using a JSON file for a human readable config or if we
          should use the ConfigParser module.
    '''

    # Temporary until we load from a file or similar
    return {
        'gnupgdir': os.path.expanduser("~/.vomun/friends.json") # unused
    }
    
def save_config():
    '''Save the configuration file to ~/.vomun/config.*'''
    pass

load_config()