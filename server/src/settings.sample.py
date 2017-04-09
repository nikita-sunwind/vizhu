'''Settings of vizhu application
'''

from pathlib import Path


SERVER_PORT = 8888
STATIC_DIR = Path.cwd().parent / 'client' / 'dist'
DATA_DIR = Path.cwd() / 'data'
