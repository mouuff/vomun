'''global storage'''
import os

global_vars = { # TODO load some of this from ~/.vomun/config.cfg
    'vomundir': os.getenv('HOME') + '/.vomun/',
    'gnupgdir': os.getenv('HOME') + '/.vomun/gnupg/',
    'running': True,
    'anon+': {
        'VERSION': 'v0.0.0b0pre',
        'BUILD': 0,
    }
}

global_vars['anon+']['banner'] = '''
======================
= Anon+ %s
= Build: %s
======================
'''