from aiohttp import web
from aiohttp_session import get_session
async def user_session(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    user_type = session.get("type", None)
    return email, user_type