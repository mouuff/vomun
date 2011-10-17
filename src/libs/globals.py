'''global storage'''
import os


global_vars = {
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