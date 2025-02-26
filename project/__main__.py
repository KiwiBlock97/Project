
import asyncio
from aiohttp import web

from project.utils.vars import Var
from project.main.views import db
from project.utils.cashfree import session as cf_session
from project.utils import utils

from .app import init_app


def create_app() -> web.Application:
    import aiohttp_debugtoolbar

    app = init_app()
    aiohttp_debugtoolbar.setup(app, check_host=False, intercept_redirects=False)

    return app

async def cleanup():
    if cf_session and not cf_session.closed:
        print("Closing Cashfree Session")
        await cf_session.close()
    if utils.session and not utils.session.closed:
        print("Closing Brevo API Session")
        await utils.session.close()
    if utils.server:
        print("Closing SMTP Server")
        utils.server.close()
    db.close_connection()
    print("Closing Connections")


def main() -> None:
    app = init_app()
    print("Started server on", Var.URL)
    web.run_app(
        app,
        host=Var.HOST,
        port=Var.PORT,
    )


if __name__ == '__main__':
    try:
        main()
    finally:
        asyncio.run(cleanup())
