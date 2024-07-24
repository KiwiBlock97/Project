import pathlib

from aiohttp import web

from project.main.views import index, routes

PROJECT_PATH = pathlib.Path(__file__).parent

def init_routes(app: web.Application) -> None:
    add_route = app.router.add_route

    add_route('*', '/', index, name='index')

    # added static dir
    app.router.add_static(
        '/static/',
        path=(PROJECT_PATH / 'templates'),
        name='static',
    )
    app.add_routes(routes)