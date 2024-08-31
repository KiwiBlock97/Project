
from aiohttp import web

from project.utils.vars import Var

from .app import init_app


def create_app() -> web.Application:
    import aiohttp_debugtoolbar

    app = init_app()
    aiohttp_debugtoolbar.setup(app, check_host=False)

    return app


def main() -> None:
    app = init_app()
    web.run_app(
        app,
        host=Var.HOST,
        port=Var.PORT,
    )


if __name__ == '__main__':
    main()
