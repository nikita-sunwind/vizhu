'''Server logging
'''

import logging.config


def setup_loggers():
    '''Configure debug loggers
    '''
    config = {
        'version': 1,
        'handlers': {
            'default': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler'
            },
        },
        'loggers': {}
    }

    loggers = [
        # 'asyncio',
        'aiohttp.access',
        'aiohttp.client',
        'aiohttp.internal',
        'aiohttp.server',
        'aiohttp.web',
        'aiohttp.websocket',
        'vizhu',
    ]

    for logger in loggers:
        config['loggers'][logger] = {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }

    logging.config.dictConfig(config)
