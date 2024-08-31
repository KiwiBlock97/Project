from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta

Cashfree.XClientId = "TEST10244234e9fe257518c2ddd5090843244201"
Cashfree.XClientSecret = "cfsk_ma_test_735c83fb1b89df45df8c8b8b757ef3b8_420df7eb"
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = "2023-08-01"
def create_order(admid: str, phone: str, name: str, email: str, uuid4: str, amount: int):
    customerDetails = CustomerDetails(customer_id=admid, customer_phone=phone)
    customerDetails.customer_name = name
    customerDetails.customer_email = email
    createOrderRequest = CreateOrderRequest(order_id=uuid4, order_amount=amount, order_currency="INR", customer_details=customerDetails)

    orderMeta = OrderMeta()
    orderMeta.return_url = "http://localhost:8000/order/checkout?order_id={order_id}"
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
