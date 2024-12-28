import asyncio
from project.__main__ import create_app

async def app():
    return create_app()

def on_exit(server):
    from project.__main__ import cleanup
    asyncio.run(cleanup())