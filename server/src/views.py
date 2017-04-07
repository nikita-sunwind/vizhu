'''Server view handlers
'''

from pathlib import Path
from aiohttp import web


STATIC_PATH = Path.cwd().parent / 'client' / 'dist'


async def index(_):
    '''Serve index route: return static file index.html
    '''
    return web.FileResponse(STATIC_PATH / 'index.html')
