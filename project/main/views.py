import os
from typing import Dict
import uuid

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from project.utils.cashfree import create_order, fetch_payment
from project.utils.database import MySQLConnection
from project.utils.timeformat import get_readable_time
db=MySQLConnection()
routes = web.RouteTableDef()

@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> Dict[str, str]:
    files = os.listdir("project/templates")
    return {"files": files}

@routes.get("/signup")
async def create_account(request: web.Request):
    return aiohttp_jinja2.render_template("create.html", request, {})

@routes.post("/api/create")
async def create_account2(request: web.Request):
    data=await request.post()
    admission_number=data["admission-number"]
    name=data["name"]
    email=data["email"]
    photo=data["photo"]
    department=data["department"]
    password=data["pass"]
    file_name=admission_number
    status = db.create_user(admission_number, name, email, file_name, department, password)
    if status=="exist":
        return web.Response(body="User Already Exist")
    else:
        with open(f"photo/{admission_number}", "wb") as f:
            f.write(photo.file.read())
        return web.HTTPSeeOther("/login")
    
@routes.route("*", "/login")
async def login(request: web.Request):
    data=await request.post()
    email=data.get("email")
    password=data.get("password")
    if not (email or password):
        return aiohttp_jinja2.render_template("login.html", request, {})
    Resp, Type = db.auth_user(email, password)
    session = await get_session(request)

    if Resp==None:
        return web.Response(body="Invalid Email or Password")
    session["email"]=email
    session["type"]=Type
    if Type=="Admin":
        return web.HTTPSeeOther("/admin")
    elif Type=="Student":
        session["admid"]=Resp
        return web.HTTPSeeOther("/student",)

@routes.get("/photo")
async def login(request: web.Request):
    session = await get_session(request)
    admid=session["admid"]
    if admid:
        return web.FileResponse(f"photo/{admid}")
    return web.HTTPNotFound

@routes.get("/student")
async def login(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    user_type = session.get("type", None)
    if (not email) or user_type!="Student":
        return web.HTTPSeeOther("/login")
    user = db.get_user(email, "Student")
    if not user:
        return web.HTTPSeeOther("/login")
    bus_pass = db.get_pass(user[0])
    if not bus_pass:
        return web.HTTPSeeOther("/student/apply")
    return aiohttp_jinja2.render_template("student_home.html", request, {
        "name": user[1],
        "department": user[4],
        "admission": user[0],
        "validity": get_readable_time(bus_pass[2]),
        "from": bus_pass[1],
        "ticketid": bus_pass[3],
    })

@routes.route("*", "/student/apply")
async def apply_pass(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    data=await request.post()
    if not email:
        return web.HTTPSeeOther("/login")
    user = db.get_user(email, "Student")
    if not user:
        return web.HTTPSeeOther("/signup")
    place=db.get_place()
    return aiohttp_jinja2.render_template("student_apply.html", request, {
        "name": user[1],
        "department": user[4],
        "adm_no": user[0],
        "place": place
    })

@routes.route("*", "/student/renew")
async def apply_pass(request: web.Request):
    session = await get_session(request)
    if not session.get("email", None):
        return web.HTTPSeeOther("/login")
    email = session.get("email", None)
    user=db.get_user(email,"Student")
    if not user:
        return web.HTTPSeeOther("/signup")
    bus_pass=db.get_pass(user[0])
    if not bus_pass:
        return web.HTTPSeeOther("/student/apply")
    place=db.get_place(bus_pass[1])
    return aiohttp_jinja2.render_template("student_renew.html", request, {
        "name": user[1],
        "department": user[4],
        "place": bus_pass[1],
        "adm_no": user[0],
        "price": place[1],
        "ukey": bus_pass[3]
    })

@routes.get("/admin")
async def admin_login(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    user_type = session.get("type", None)
    if (not email) or user_type!="Admin":
        return web.HTTPSeeOther("/login")
    user = db.get_user(email, "Admin")
    if not user:
        return web.HTTPSeeOther("/login")
    students=db.get_students()
    return aiohttp_jinja2.render_template("admin_home.html", request, {
        "students": students
    })

@routes.get("/admin/validate")
async def admin_login(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    user_type = session.get("type", None)
    if (not email) or user_type!="Admin":
        return web.HTTPSeeOther("/login")
    user = db.get_user(email, "Admin")
    if not user:
        return web.HTTPSeeOther("/login")
    key=request.rel_url.query.get("ticket-id", None)
    if not key:
        return aiohttp_jinja2.render_template("admin_validate.html", request, {
            "valid": False,
            "invalid": False
        })
    bus_pass=db.get_pass(key=key)
    if bus_pass:
        status=True
    else:
        status=False
    return aiohttp_jinja2.render_template("admin_validate.html", request, {
        "valid": status,
        "invalid": (not status)
    })

@routes.get("/admin/stops")
async def admin_stops_get(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    user_type = session.get("type", None)
    if (not email) or user_type!="Admin":
        return web.HTTPSeeOther("/login")
    user = db.get_user(email, "Admin")
    if not user:
        return web.HTTPSeeOther("/login")
    stops=db.get_place()
    return aiohttp_jinja2.render_template("admin_stops.html", request, {
        "places": stops
        })
    
@routes.post("/admin/stops")
async def admin_stops_post(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    user_type = session.get("type", None)
    if (not email) or user_type!="Admin":
        return web.HTTPSeeOther("/login")
    user = db.get_user(email, "Admin")
    if not user:
        return web.HTTPSeeOther("/login")
    data=await request.post()
    method=data.get("method", None)
    place=data.get("place")
    price=data.get("price")
    if method=="add" and price.isdigit():
        db.add_place(place, int(price))
        return web.HTTPSeeOther("/admin/stops")
    elif method=="delete":
        db.remove_place(place)
        return web.HTTPSeeOther("/admin/stops")
    else:
        return web.HTTPBadRequest()

@routes.get("/logout")
async def logout(request: web.Request):
    session = await get_session(request)
    session.invalidate()
    return web.HTTPSeeOther("/login")

@routes.post("/order/confirm")
async def apply_pass(request: web.Request):
    session = await get_session(request)
    email = session.get("email", None)
    data=await request.post()
    if not email:
        return web.HTTPSeeOther("/login")
    user = db.get_user(email, "Student")
    if not user:
        return web.HTTPSeeOther("/signup")
    if not (data):
        return web.HTTPSeeOther("/student")
    ukey=data.get("ukey", None)
    if ukey:
        buspass=db.get_pass(key=ukey)
        place=buspass[1]
    else:
        place=data.get("from-to")
    uuid4=uuid.uuid4()
    admid=user[0]
    name=user[1]
    email=user[2]
    validity=int(data.get("validity"))
    db_place=db.get_place(place=place)
    amount=int(db_place[1])*validity
    payment_id=create_order(str(admid), "1234567890", name, email, str(uuid4), amount)
    if payment_id:
        db.create_order(str(uuid4), email, place, validity, 1 if ukey else 0, ukey if ukey else None, None)
        return aiohttp_jinja2.render_template("checkout.html", request, {
            "sessionid": payment_id,
            "name": name,
            "department": user[4],
            "place": place,
            "validity": validity,
            "adm_no": admid,
            "price": amount,
            "order_id": str(uuid4),
            "renew": bool(ukey)
        })
    return web.HTTPServerError()

@routes.get("/order/checkout")
async def checkout(request: web.Request):
    order_id=request.rel_url.query.get("order_id")
    if not order_id:
        return web.HTTPMethodNotAllowed()
    resp=(fetch_payment(order_id))[0]
    if resp.payment_status=="SUCCESS":
        order=db.get_order(order_id)
        if order[7]=="SUCCESS":
            return web.HTTPSeeOther("/student")
        db.modify_order(order_id, str(resp.payment_status))
        user=db.get_user(order[1], "Student")
        place=db.get_place(place=order[2])
        validity=int(order[3])
        valid=validity*86400
        if order[4]==0:
            db.create_pass(user[0], place[0], valid, order_id)
        elif order[4]==1:
            bus_pass=db.get_pass(user[0])
            valid=int(bus_pass[2])+valid
            db.extend_pass(valid, order[5])
        return web.HTTPSeeOther("/student")
    elif resp.payment_status:
        db.modify_order(order_id, str(resp.payment_status))
        return web.HTTPBadRequest(reason=f"payment {resp.payment_status}")
        # [PENDING, USER_DROPPED, FAILED]
    else:
        return web.HTTPBadRequest()