import smtplib, ssl
from email.message import EmailMessage
from email.utils import formataddr
from aiohttp import ClientSession
from project.utils.vars import Var

session = None
server = None
test=None

async def send_mail(name, email, text, subject):
    if Var.BREVO_API:
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
    else:
        global server
        global test
        test=123
        if not server:
            context = ssl.create_default_context()
            server=smtplib.SMTP_SSL(Var.SMTP_HOST, Var.SMTP_PORT, context=context)
            server.login(Var.SMTP_USER, Var.SMTP_PASS)

        msg = EmailMessage()
        msg['From'] = formataddr(('Bus Pass', Var.SMTP_MAIL))
        msg['To'] = formataddr((name, email))
        msg["Subject"] = subject
        msg.set_content(text)
        server.sendmail(Var.SMTP_MAIL, email, msg.as_string())