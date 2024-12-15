import uuid
import aiohttp_jinja2

from datetime import datetime, date, timedelta
from aiohttp import web
from aiohttp_session import get_session
from project.utils.cashfree import create_order, fetch_payment
from project.utils.database import MySQLConnection
from project.utils.utils import user_session
db=MySQLConnection()
routes = web.RouteTableDef()

@routes.get("/", name="index")
async def index(request: web.Request):
    return aiohttp_jinja2.render_template("index.html", request, {})

@routes.get("/signup", name="signup")
@routes.post("/signup", name="signup")
async def get_create_account(request: web.Request):
    if request.method == "GET":
        departments=db.get_departments()
        return aiohttp_jinja2.render_template("create.html", request, {
            "departments": departments
        })
    # If method is POST
    data=await request.post()
    photo=data["photo"]
    file_name=data["admission-number"]
    status = db.create_user(data["admission-number"], data["name"], data["email"], file_name, data["department"], data["pass"], data['user-type'])
    if status=="exist":
        return web.Response(body="User Already Exist")
    else:
        with open(f"photo/{data['admission-number']}", "wb") as f:
            f.write(photo.file.read())
    return web.HTTPSeeOther("/login")

@routes.get("/login", name="login")
async def login_get(request: web.Request):
    return aiohttp_jinja2.render_template("login.html", request, {})

@routes.post("/login", name="login_post")
async def login_post(request: web.Request):
    data=await request.post()
    email=data.get("email")
    password=data.get("password")
    if not (email and password):
        return web.HTTPSeeOther("/login")
    Resp, Type = db.auth_user(email, password)
    if Resp==None:
        return web.Response(body="Invalid Email or Password")
    session = await get_session(request)
    session["email"]=email
    session["type"]=Type
    if Type=="Admin":
        return web.HTTPSeeOther("/admin")
    elif Type=="Student":
        session["admid"]=Resp
        return web.HTTPSeeOther("/student",)

@routes.get("/photo", name="photo")
async def get_photo(request: web.Request):
    session = await get_session(request)
    user_type = session.get("type", None)
    admid=session.get("admid")
    if user_type=="Admin":
        admid=request.rel_url.query.get("id")
    if admid:
        return web.FileResponse(f"photo/{admid}")
    return web.HTTPNotFound

@routes.get("/student", name="student_home")
async def student_home(request: web.Request):
    email, user_type = await user_session(request)
    if user_type!="Student":
        return web.HTTPSeeOther("/login")
    user = db.get_user(email=email, user_type="Student")
    if not user:
        return web.HTTPSeeOther("/login")
    bus_pass = db.get_pass(user[0])
    valid_pass=[ x for x in bus_pass if x[4] >= datetime.now().date()]
    if not valid_pass:
        return web.HTTPSeeOther("/student/apply")
    return aiohttp_jinja2.render_template("student_home.html", request, {
        "name": user[1],
        "department": user[4],
        "admission": user[0],
        "bus_pass": valid_pass,
        "usertype": user[6],
    })

@routes.get("/student/apply", name="student_apply")
async def student_apply(request: web.Request):
    email, user_type = await user_session(request)
    user = db.get_user(email=email, user_type="Student")
    if not user:
        return web.HTTPSeeOther("/signup")
    place=db.get_place()
    return aiohttp_jinja2.render_template("student_apply.html", request, {
        "name": user[1],
        "department": user[4],
        "adm_no": user[0],
        "place": place,
        "usertype": user[6]
    })

@routes.get("/student/renew", name="student_renew")
async def student_renew(request: web.Request):
    email, user_type = await user_session(request)
    key=request.rel_url.query.get("key")
    if not key:
        return web.HTTPBadRequest()
    elif not (user:=db.get_user(email=email, user_type="Student")):
        return web.HTTPSeeOther("/signup")
    elif not (bus_pass:=db.get_pass(key=key)):
        return web.HTTPSeeOther("/student/apply")
    place=db.get_place(bus_pass[1])
    return aiohttp_jinja2.render_template("student_renew.html", request, {
        "name": user[1],
        "department": user[4],
        "place": bus_pass[1],
        "adm_no": user[0],
        "price": place[1],
        "ukey": bus_pass[2],
        "fromdate": bus_pass[4]+timedelta(days=1)
    })

@routes.get("/admin", name="admin_home")
async def admin_home(request: web.Request):
    email, user_type = await user_session(request)
    if user_type!="Admin":
        return web.HTTPSeeOther("/login")
    students=db.get_students()
    return aiohttp_jinja2.render_template("admin_home.html", request, {
        "students": students
    })

@routes.get("/admin/validate", name="admin_validate")
async def admin_validate(request: web.Request):
    email, user_type = await user_session(request)
    if user_type!="Admin":
        return web.HTTPSeeOther("/login")
    if key:=request.rel_url.query.get("ticket-id", None):
        bus_pass=db.get_pass(key=key)
        user = db.get_user(admid=bus_pass[0]) if bus_pass else None
        context={
            "key": key,
            "ticket": bus_pass,
            "user": user,
            "validity": bus_pass[4] if bus_pass else 0,
        }
    else:
        context = {"key": None}
    return aiohttp_jinja2.render_template("admin_validate.html", request, context)
    
@routes.get("/admin/stops", name="admin_stops")
@routes.post("/admin/stops", name="admin_stops_post")
async def admin_stops_post(request: web.Request):
    email, user_type = await user_session(request)
    if user_type!="Admin":
        return web.HTTPSeeOther("/login")
    if request.method == "GET":
        stops=db.get_place()
        return aiohttp_jinja2.render_template("admin_stops.html", request, {
            "places": stops
            })
    # If Post Request
    data=await request.post()
    method=data.get("method", None)
    if method=="add":
        db.add_place(data.get("place"), int(data.get("price")))
    elif method=="delete":
        db.remove_place(data.get("place"))
    else:
        return web.HTTPBadRequest()
    return web.HTTPSeeOther("/admin/stops")

@routes.get("/logout", name="logout")
async def logout(request: web.Request):
    session = await get_session(request)
    session.invalidate()
    return web.HTTPSeeOther("/login")

@routes.post("/order/confirm", name="order_confirm")
async def order_confirm(request: web.Request):
    email, user_type = await user_session(request)
    if not (data:=await request.post()):
        return web.HTTPSeeOther("/student")
    elif not (user:=db.get_user(email=email, user_type="Student")):
        return web.HTTPSeeOther("/signup")
    elif ukey:=data.get("ukey", None):
        buspass=db.get_pass(key=ukey)
        datefrom: date=str(buspass[4]+timedelta(days=1))
        place=buspass[1]
    else:
        datefrom=data.get("datefrom")
        place=data.get("from-to")
    uuid4=uuid.uuid4()
    admid=user[0]
    name=user[1]
    email=user[2]
    dateto=data.get("dateto")

    start_date = datetime.strptime(datefrom, "%Y-%m-%d")
    end_date = datetime.strptime(dateto, "%Y-%m-%d")
    
    validity = (end_date - start_date).days + 1
    db_place = db.get_place(place=place)
    price = int(db_place[1])
    
    amount = price * validity

    payment_id=create_order(str(admid), "1234567890", name, email, str(uuid4), amount)
    if payment_id:
        db.create_order(str(uuid4), email, place, datefrom, dateto, 1 if ukey else 0, ukey if ukey else None, None)
        return aiohttp_jinja2.render_template("checkout.html", request, {
            "sessionid": payment_id,
            "name": name,
            "department": user[4],
            "place": place,
            "validity": end_date.strftime("%d-%m-%Y"),
            "adm_no": admid,
            "price": amount,
            "order_id": str(uuid4),
            "renew": "Yes" if bool(ukey) else "No"
        })
    return web.HTTPServerError()

@routes.get("/order/checkout", name="checkout")
async def checkout(request: web.Request):
    order_id=request.rel_url.query.get("order_id")
    if not order_id:
        return web.HTTPMethodNotAllowed()
    resp=(fetch_payment(order_id))[0]
    if resp.payment_status=="SUCCESS":
        order=db.get_order(order_id)
        if order[8] in ["SUCCESS", "PROCESSED"]:
            return aiohttp_jinja2.render_template("status.html", request, {
                "status": resp.payment_status,
                "payment_id": resp.cf_payment_id,
                "order_id": resp.order_id
            })
        db.modify_order(order_id, str(resp.payment_status))
        user=db.get_user(email=order[1], user_type="Student")
        place=db.get_place(place=order[2])
        fromtime: date=order[3]
        totime: date=order[4]
        if order[5]==0:
            db.create_pass(user[0], place[0], order_id, fromtime, totime)
        elif order[5]==1:
            db.extend_pass(totime, order[6])
        db.modify_order(order_id, "PROCESSED")
    elif resp.payment_status:
        db.modify_order(order_id, str(resp.payment_status))
        # [PENDING, USER_DROPPED, FAILED]
    else:
        return web.HTTPBadRequest()
    return aiohttp_jinja2.render_template("status.html", request, {
        "status": resp.payment_status,
        "payment_id": resp.cf_payment_id,
        "order_id": resp.order_id
    })
    
@routes.post("/admin/remove")
async def admin_remove(request: web.Request):
    email, user_type = await user_session(request)
    if user_type!="Admin":
        return web.HTTPSeeOther("/login")
    data=await request.post()
    if (admid:=data.get("admid")):
        db.remove_student(int(admid))
        return web.HTTPSeeOther("/admin")
    return web.HTTPMethodNotAllowed()

@routes.get("/admin/details")
async def admin_details(request: web.Request):
    email, user_type = await user_session(request)
    if user_type!="Admin":
        return web.HTTPSeeOther("/login")
    if ticket:=request.rel_url.query.get("pass"):
        db.remove_pass(uuid4=ticket)
    if not (admid:=request.rel_url.query.get("id")):
        return web.HTTPBadRequest()
    user=db.get_user(admid=admid)
    bus_pass = db.get_pass(user[0])
    valid_pass=[ x for x in bus_pass if x[4] >= datetime.now().date()]
    print(valid_pass)

    return aiohttp_jinja2.render_template("admin_student.html", request, {
        "AdmissionId": user[0],
        "Name": user[1],
        "Email": user[2],
        "Department": user[4],
        "bus_pass": valid_pass,
    })
    
@routes.get("/admin/departments", name="admin_departments")
@routes.post("/admin/departments", name="admin_departments_post")
async def admin_departments_post(request: web.Request):
    email, user_type = await user_session(request)
    if user_type!="Admin":
        return web.HTTPSeeOther("/login")
    if request.method == "GET":
        departments=db.get_departments()
        return aiohttp_jinja2.render_template("admin_department.html", request, {
            "departments": departments
        })
    # if POST Method
    data=await request.post()
    method=data.get("method", None)
    department=data.get("department", None)
    if method=="add" and department:
        db.add_department(department)
    elif method=="delete":
        db.remove_department(department)
    else:
        return web.HTTPBadRequest()
    return web.HTTPSeeOther("/admin/departments")