from pathlib import Path

import aiohttp_jinja2
import jinja2

# from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import SimpleCookieStorage

from project.routes import init_routes


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    '''
    Initialize jinja2 template for application.
    '''
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )

def init_session(app: web.Application) -> None:
    # fernet_key = fernet.Fernet.generate_key()
    # f = fernet.Fernet(fernet_key)
    setup(app, SimpleCookieStorage())


def init_app() -> web.Application:
    app = web.Application(client_max_size=10485760)

    init_jinja2(app)
    init_session(app)
    init_routes(app)

    return app
