'''Server routing
'''

from .views import STATIC_DIR, index, load_event, query_events, restart


def setup_routes(app):
    '''Configure routes to resource handlers
    '''
    app.router.add_get('/', index)
    app.router.add_static('/static', path=STATIC_DIR)

    app.router.add_post('/events', load_event)
    app.router.add_get('/events', query_events)

    app.router.add_post('/restart', restart)
