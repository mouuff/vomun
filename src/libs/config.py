'''Load the config from ~/.vomun/config.json'''

import os
import json
import libs.globals
from api.functions import register_with_api

config = {}

configpath = os.path.expanduser("~/.vomun/config.json")


def open_config():
    try:
        configfile = open(configpath,"r+")
    except IOError:
        defaultConfig = {   
            'vomundir': os.getenv('HOME') + '/.vomun/',
            'gnupgdir': os.getenv('HOME') + '/.vomun/gnupg/',
            'nodekey': ''
        }
        configfile = open(configpath,"a")
        configfile.write(json.dumps(defaultConfig,indent = 4))
        configfile.flush()
        configfile.close()
        configfile = open(configpath,"r+")
    return configfile


configfile = open_config()

@register_with_api
def load_config():
    '''Load the configuration file'''
    import libs
    libs.globals.global_vars['config'] = json.loads(configfile.read())
    configfile.seek(0) # return read/write position to beginning of the file

@register_with_api
def get_config():
    '''Return the contents of the configuration file'''
    return config

@register_with_api
def save_config():
    '''Write the configuration file to the hard disk'''
    configfile.write(json.dumps(libs.globals.global_vars["config"],indent = 4))

load_config()
