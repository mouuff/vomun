'''Load the config from ~/.vomun/config.json'''

import os
import json
import libs.globals

config = {}

configpath = os.path.expanduser("~/.vomun/config.json")


def open_config():
    try:
        configfile = open(configpath,"r+")
    except IOError:
        defaultConfig = {   
            'vomundir': os.getenv('HOME') + '/.vomun/',
            'gnupgdir': os.getenv('HOME') + '/.vomun/gnupg/',
        }
        configfile = open(configpath,"a")
        configfile.write(json.dumps(defaultConfig,indent = 4))
        configfile.flush()
        configfile.close()
        configfile = open(configpath,"r+")
    return configfile


configfile = open_config()
print configfile
def load_config():

    
    import libs
    dir (libs)
    libs.globals.global_vars["config"] = json.loads(configfile.read())
    configfile.seek(0) # return read/write position to beginning of the file

def save_config():
    configfile.write(json.dumps(libs.globals.global_vars["config"],indent = 4))

load_config()