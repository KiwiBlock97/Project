from aiohttp import ClientSession, ClientTimeout
from project.utils.vars import Var


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
