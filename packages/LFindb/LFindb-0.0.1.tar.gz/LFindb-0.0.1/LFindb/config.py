# -*- coding:utf-8 -*- 


CONFIG = {
    'USER': None,
    'PASSWORD': None,
    'HOST': None,
    'DATABASE': None
}

def get_config(config):
    CONFIG['USER'] = config['user']
    CONFIG['PASSWORD'] = config['password']
    CONFIG['DATABASE'] = config['database']
    CONFIG['HOST'] = config['host']