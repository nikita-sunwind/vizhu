'''Server routing
'''

from .views import STATIC_PATH, index


def setup_routes(app):
    '''Configure routes to resource handlers
    '''
    app.router.add_get('/', index)
    app.router.add_static('/static', path=STATIC_PATH)
