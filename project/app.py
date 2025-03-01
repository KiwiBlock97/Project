from pathlib import Path

import aiohttp_jinja2
import jinja2

# from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, SimpleCookieStorage, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from project.routes import init_routes
from project.main.views import db


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

@web.middleware
async def middleware(request: web.Request, handler):
    request["session"] = await get_session(request)
    request["email"] = request["session"].get("email", None)
    request["user_type"] = request["session"].get("type", None)

    path=request.path
    if path.startswith(("/student", "/staff")):
        if request["user_type"] not in ["Student", "Staff"]:
            return web.HTTPSeeOther("/login")
        request["user"] = db.get_user(email=request["email"], user_type=request["user_type"])
        if not request["user"]:
            return web.HTTPSeeOther("/login")
    elif path.startswith("/admin"):
        if request["user_type"]!="Admin":
            return web.HTTPSeeOther("/login")
    return await handler(request)

def init_app() -> web.Application:
    app = web.Application(client_max_size=10485760)

    init_jinja2(app)
    init_session(app)
    init_routes(app)
    app.middlewares.append(middleware)

    return app
