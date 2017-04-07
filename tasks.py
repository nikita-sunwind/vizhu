'''Development automation tasks
'''

import os
from invoke import task


@task
def checks(ctx):
    '''Run code checks: flake8 and pylint
    '''
    sources = 'src test tasks.py'

    ctx.run(
        'flake8 {}'.format(sources),
        echo=True,
        in_stream=open('/dev/tty'))

    ctx.run(
        'pylint --rcfile="./pylintrc.ini" --output-format colorized {}'
        .format(sources),
        echo=True,
        in_stream=open('/dev/tty'))


@task
def tests(ctx):
    '''Run imperative test suit: pytest
    '''
    ctx.run(
        'py.test -vv --color=yes test',
        echo=True,
        in_stream=open('/dev/tty'))


@task
def start_server(ctx, debug=False):
    '''Start API server in development mode
    '''
    if debug:
        os.environ['PYTHONASYNCIODEBUG'] = '1'
        os.environ['DEBUG'] = '1'
        debug_args = '-Wdefault'
    else:
        debug_args = ''

    ctx.run(
        'python {} -m src.server'.format(debug_args),
        echo=True,
        pty=True)


@task
def kill_server(ctx):
    '''Kill API server process
    '''
    ctx.run(
        'pkill -f "python -m src.server"',
        echo=True)
