from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta

from project.utils.vars import Var

Cashfree.XClientId = Var.CF_CLIENTID
Cashfree.XClientSecret = Var.CF_CLIENTSECRET
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = Var.CF_VERSION
def create_order(admid: str, phone: str, name: str, email: str, uuid4: str, amount: int):
    customerDetails = CustomerDetails(customer_id=admid, customer_phone=phone)
    customerDetails.customer_name = name
    customerDetails.customer_email = email
    createOrderRequest = CreateOrderRequest(order_id=uuid4, order_amount=amount, order_currency="INR", customer_details=customerDetails)

    orderMeta = OrderMeta()
    orderMeta.return_url = Var.URL+"/order/checkout?order_id={order_id}"
    orderMeta.payment_methods = "cc,dc,upi"
    createOrderRequest.order_meta = orderMeta

    try:
        api_response = Cashfree().PGCreateOrder(x_api_version, createOrderRequest, None, None)
        return api_response.data.payment_session_id
    except Exception as e:
        print(e)

def fetch_payment(order_id: str):
    try:
        api_response = Cashfree().PGOrderFetchPayments(x_api_version, order_id, None)
        return api_response.data
    except Exception as e:
        print(e)