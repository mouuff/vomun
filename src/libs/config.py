'''Load the config from ~/.vomun/config.json'''

import os
import json
import libs.globals

config = {}

configpath = os.path.expanduser("~/.vomun/config.json")

configfile = None

def load_config():
    try:
        configfile = open(configpath,"r")
    except IOError:
        defaultConfig = {   
            'vomundir': os.getenv('HOME') + '/.vomun/',
            'gnupgdir': os.getenv('HOME') + '/.vomun/gnupg/',
        }
        configfile = open(configpath,"a")
        configfile.write(json.dumps(defaultConfig,indent = 4))
        configfile.flush()

    libs.globals.global_vars["config"] = json.loads(configfile.read())

def save_config():
    configfile.write(json.dumps(libs.globals.global_vars["config"],indent = 4))

load_config()
