
from aiohttp import web

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
        host="0.0.0.0",
        port=8080,
    )


if __name__ == '__main__':
    main()
