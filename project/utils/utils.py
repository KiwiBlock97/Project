from aiohttp import web, ClientSession, ClientTimeout
from aiohttp_session import get_session
from project.utils.vars import Var

async def user_session(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    user_type = session.get("type", None)
    return email, user_type


async def send_mail(name, email, text, subject):
    async with ClientSession(
        timeout=ClientTimeout(total=10)
    ) as session:
        headers = {
            'accept': 'application/json',
            'api-key': Var.BREVO_API,
            'content-type': 'application/json',
        }
        json_data = {
            'sender': {
                'name': 'Springs Fern',
                'email': 'mail@springsfern.in',
            },
            'to': [
                {
                    'email': email,
                    'name': name,
                },
            ],
            'subject': subject,
            'htmlContent': text,
        }

        async with session.post("https://api.brevo.com/v3/smtp/email", headers=headers, json=json_data) as resp:
            return await resp.json()
