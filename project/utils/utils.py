from aiohttp import ClientSession
from project.utils.vars import Var

session = None

async def send_mail(name, email, text, subject):
    global session
    if not session:
        headers = {
            'accept': 'application/json',
            'api-key': Var.BREVO_API,
            'content-type': 'application/json',
        }
        session = ClientSession("https://api.brevo.com", headers=headers)
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

    async with session.post("/v3/smtp/email", json=json_data) as resp:
        return await resp.json()
