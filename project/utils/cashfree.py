import aiohttp
from project.utils.vars import Var

session: aiohttp.ClientSession = None

async def init_session():
    global session
    headers = {
        'x-client-id': Var.CF_CLIENTID,
        'x-client-secret': Var.CF_CLIENTSECRET,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-version': Var.CF_VERSION
    }
    session = aiohttp.ClientSession(
        "https://sandbox.cashfree.com", headers=headers)

async def create_order(admid: str, phone: str, name: str, email: str, uuid4: str, amount: int, return_path: str):
    global session
    if not session:
        await init_session()
    data = {
        "order_amount": amount,
        "order_currency": "INR",
        "order_id": uuid4,
        "customer_details": {
            "customer_id": admid,
            "customer_phone": phone,
            "customer_name": name,
            "customer_email": email
        },
        "order_meta": {
            "return_url": Var.URL+return_path+"?order_id={order_id}",
            "payment_methods": "cc,dc,upi"
        }
    }

    async with session.post('/pg/orders', json=data) as resp:
        resp_data=await resp.json()
        return resp_data.get("payment_session_id")

async def fetch_payment(order_id: str):
    global session
    if not session:
        await init_session()
    async with session.get(f'/pg/orders/{order_id}/payments') as resp:
        resp_data=await resp.json()
        return resp_data
