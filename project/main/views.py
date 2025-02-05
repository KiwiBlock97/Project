import uuid
import aiohttp_jinja2

from datetime import datetime, date, timedelta
from aiohttp import web
from aiohttp_session import get_session
from project.utils.cashfree import create_order, fetch_payment
from project.utils.database import MySQLConnection
from project.utils.utils import send_mail
from project.utils.vars import Var
db=MySQLConnection()
routes = web.RouteTableDef()

@routes.get("/")
async def index(request: web.Request):
    return aiohttp_jinja2.render_template("index.html", request, {})

@routes.get("/signup")
@routes.post("/signup")
async def get_create_account(request: web.Request):
    if request.method == "GET":
        departments=db.get_departments()
        return aiohttp_jinja2.render_template("signup.html", request, {
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

@routes.get("/login")
async def login_get(request: web.Request):
    if request["user_type"]:
        return web.HTTPSeeOther("/"+request["user_type"].lower())
    return aiohttp_jinja2.render_template("login.html", request, {})

@routes.post("/login")
async def login_post(request: web.Request):
    data=await request.post()
    email=data.get("email")
    password=data.get("password")
    if not (email and password):
        return web.HTTPSeeOther("/login")
    Resp, Type = db.auth_user(email, password)
    if not Resp:
        return web.Response(body="Invalid Email or Password")
    if Type in ["Student", "Staff"] and Resp[1]==0:
        code=db.gen_code(email)
        text=f"<html><head></head><body><p>Verify your email address by opening this link<br>{Var.URL}/verify?code={code}</p></body></html>"
        await send_mail(Resp[2], email, text, "Email Verification")
        return web.Response(text="Refresh this page or Login again after verifying your Email by Opening Link sent to Provided Email Address")
    session = await get_session(request)
    session["email"]=email
    session["type"]=Type
    if Type=="Admin":
        return web.HTTPSeeOther("/admin")
    elif Type=="Student":
        return web.HTTPSeeOther("/student")
    elif Type=="Staff":
        return web.HTTPSeeOther("/staff")
    
@routes.get("/logout")
async def logout(request: web.Request):
    session = await get_session(request)
    session.invalidate()
    return web.HTTPSeeOther("/login")

@routes.get("/photo")
async def get_photo(request: web.Request):
    if request["user_type"]=="Admin":
        admid=request.rel_url.query.get("id")
    else:
        email=request["email"]
        user_type=request["user_type"]
        user=db.get_user(email, user_type=user_type)
        admid=user[0]
    if admid:
        return web.FileResponse(f"photo/{admid}")
    return web.HTTPNotFound

@routes.get("/student")
async def student_home(request: web.Request):
    user=request["user"]
    bus_pass = db.get_pass(user[0])
    valid_pass=[ x for x in bus_pass if x[4] >= datetime.now().date()]
    if not valid_pass:
        return web.HTTPSeeOther("/student/apply")
    return aiohttp_jinja2.render_template("student_home.html", request, {
        "name": user[1],
        "department": user[4],
        "admission": user[0],
        "bus_pass": valid_pass,
    })

@routes.get("/student/print")
async def student_home(request: web.Request):
    bus_pass = db.get_pass(key=request.rel_url.query.get("key"))
    user = db.get_user(admid=bus_pass[0])
    return aiohttp_jinja2.render_template("student_print.html", request, {
        "name": user[1],
        "department": user[4],
        "admission": user[0],
        "ticket": bus_pass,
    })

@routes.get("/student/apply")
async def student_apply(request: web.Request):
    user = request["user"]
    place=db.get_place()
    return aiohttp_jinja2.render_template("student_apply.html", request, {
        "name": user[1],
        "department": user[4],
        "adm_no": user[0],
        "place": place,
    })

@routes.get("/student/renew")
async def student_renew(request: web.Request):
    key=request.rel_url.query.get("key")
    if not key:
        return web.HTTPBadRequest()
    elif not (bus_pass:=db.get_pass(key=key)):
        return web.HTTPSeeOther("/student/apply")
    place=db.get_place(bus_pass[1])
    user=request["user"]
    return aiohttp_jinja2.render_template("student_renew.html", request, {
        "name": user[1],
        "department": user[4],
        "place": bus_pass[1],
        "adm_no": user[0],
        "price": place[1],
        "ukey": bus_pass[2],
        "fromdate": bus_pass[4]+timedelta(days=1)
    })

@routes.post("/student/order/confirm")
async def order_confirm(request: web.Request):
    data=await request.post()
    user=request["user"]
    if ukey:=data.get("ukey", None):
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
    phoneno=data.get("phone")

    start_date = datetime.strptime(datefrom, "%Y-%m-%d")
    end_date = datetime.strptime(dateto, "%Y-%m-%d")
    
    no_days = (end_date - start_date).days
    no_sun = (no_days)//7
    if (no_days % 7 + start_date.isoweekday()) >= 7:
        no_sun+=1
    validity = no_days+1-no_sun
    db_place = db.get_place(place=place)
    price = int(db_place[1])
    
    amount = price * validity

    payment_id=await create_order(str(admid), str(phoneno), name, email, str(uuid4), amount, "/student/order/checkout")
    if payment_id:
        db.create_order(str(uuid4), email, place, datefrom, dateto, 1 if ukey else 0, ukey if ukey else None, None, amount)
        return aiohttp_jinja2.render_template("student_order_confirm.html", request, {
            "sessionid": payment_id,
            "name": name,
            "department": user[4],
            "place": place,
            "validity": end_date.strftime("%d-%m-%Y"),
            "adm_no": admid,
            "price": amount,
            "order_id": str(uuid4),
            "renew": "Yes" if bool(ukey) else "No",
        })
    return web.HTTPServerError()

@routes.get("/student/order/checkout")
async def checkout(request: web.Request):
    order_id=request.rel_url.query.get("order_id")
    if not order_id:
        return web.HTTPMethodNotAllowed()
    resp=(await fetch_payment(order_id))[0]
    if resp.get("payment_status")=="SUCCESS":
        order=db.get_order(order_id)
        if order[8] in ["SUCCESS", "PROCESSED"]:
            return aiohttp_jinja2.render_template("student_order_checkout.html", request, {
                "status": resp.get("payment_status"),
                "payment_id": resp.get("cf_payment_id"),
                "order_id": resp.get("order_id")
            })
        db.modify_order(order_id, str(resp.get("payment_status")))
        user=db.get_user(email=order[1], user_type="Student")
        place=db.get_place(place=order[2])
        fromtime: date=order[3]
        totime: date=order[4]
        if order[5]==0:
            db.create_pass(user[0], place[0], order_id, fromtime, totime)
        elif order[5]==1:
            db.extend_pass(totime, order[6])
        db.modify_order(order_id, "PROCESSED")
    elif resp.get("payment_status"):
        db.modify_order(order_id, str(resp.get("payment_status")))
        # [PENDING, USER_DROPPED, FAILED]
    else:
        return web.HTTPBadRequest()
    return aiohttp_jinja2.render_template("student_order_checkout.html", request, {
        "status": resp.get("payment_status"),
        "payment_id": resp.get("cf_payment_id"),
        "order_id": resp.get("order_id")
    })

@routes.get("/admin")
async def admin_home(request: web.Request):
    return aiohttp_jinja2.render_template("admin_home.html", request, {})

@routes.get("/admin/students")
@routes.post("/admin/students")
async def admin_home(request: web.Request):
    if request.method == "GET":
        students=db.get_students()
        staff=db.get_students(1)
        return aiohttp_jinja2.render_template("admin_students.html", request, {
            "students": students,
            "staff": staff
        })
    data=await request.post()
    if (admid:=data.get("admid")):
        db.remove_student(int(admid))
    elif (aadhar:=data.get("aadhar")):
        db.remove_student(int(aadhar), 2)
        return web.HTTPSeeOther("/admin/students")
    return web.HTTPMethodNotAllowed("POST", ["GET"])

@routes.get("/admin/validate")
async def admin_validate(request: web.Request):
    if key:=request.rel_url.query.get("ticket-id", None):
        usertype=0
        if bus_pass:=db.get_pass(key=key):
            usertype="Student"
        elif bus_pass:=db.get_pass(key=key, utype=2):
            usertype="Staff"
        user = db.get_user(admid=bus_pass[0], user_type=usertype) if bus_pass else None
        context={
            "key": key,
            "ticket": bus_pass,
            "user": user,
            "usertype": usertype
        }
    else:
        context = {"key": None}
    return aiohttp_jinja2.render_template("admin_validate.html", request, context)
    
@routes.get("/admin/stops")
@routes.post("/admin/stops")
async def admin_stops_post(request: web.Request):
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

@routes.get("/admin/details")
async def admin_details(request: web.Request):
    user_type=request.rel_url.query.get("type")
    if ticket:=request.rel_url.query.get("pass"):
        db.remove_pass(uuid4=ticket, utype=user_type)
    if not (admid:=request.rel_url.query.get("id")):
        return web.HTTPBadRequest()
    utype=1
    if not (user:=db.get_user(admid=admid)):
        utype=2
        user=db.get_user(admid=admid, user_type="Staff")
    bus_pass = db.get_pass(user[0], utype=utype)
    if utype==1:
        valid_pass=[ x for x in bus_pass if x[4] >= datetime.now().date()]
    else:
        valid_pass=[ x for x in bus_pass if x[3] > len(x[4])]
    return aiohttp_jinja2.render_template("admin_details.html", request, {
        "AdmissionId": user[0],
        "Name": user[1],
        "Email": user[2],
        "Department": user[4],
        "bus_pass": valid_pass,
        "utype": utype
    })
    
@routes.get("/admin/departments")
@routes.post("/admin/departments")
async def admin_departments_post(request: web.Request):
    if request.method == "GET":
        departments=db.get_departments()
        return aiohttp_jinja2.render_template("admin_departments.html", request, {
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

@routes.get("/admin/tickets/purchased")
async def admin_tickets(request: web.Request):
    fromdate=request.rel_url.query.get("fromdate")
    todate=request.rel_url.query.get("todate")
    department=request.rel_url.query.get("department")
    departments=db.get_departments()
    context={"departments": departments}
    if fromdate and todate:
        student, staff=db.get_order(fromdate=fromdate, todate=todate, department=department)
        sum=0
        for x in student:
            sum+=x[4]
        for x in staff:
            sum+=x[3]
        context.update({
            "student": student,
            "staff": staff,
            "sum": sum,
            "departments": departments,
            "count": len(student)+len(staff),
            "fromdate": fromdate,
            "todate": todate
            })
    return aiohttp_jinja2.render_template("admin_tickets_purchased.html", request, context)

@routes.get("/admin/tickets/regular")
async def admin_tickets_regular(request: web.Request):
    fromdate=request.rel_url.query.get("fromdate")
    todate=request.rel_url.query.get("todate")
    params={"fromdate": fromdate, "todate": todate}
    if fromdate and todate:
        passes=db.get_pass(regular=True, fromdate=fromdate, todate=todate)
        params["passes"]=enumerate(passes, 1)
    return aiohttp_jinja2.render_template("admin_tickets_regular.html", request, params)

@routes.post("/admin/tickets/today")
@routes.get("/admin/tickets/today")
async def admin_tickets_today(request: web.Request):
    if request.method == "GET":
        today=datetime.now().date()
        passes=db.get_pass(regular=True, fromdate=today, todate=today)
        staff=db.get_pass(regular=True, utype=2)
        return aiohttp_jinja2.render_template("admin_tickets_today.html", request, {
            "passes": list(enumerate(passes, 1)) if passes else None,
            "staff": enumerate(staff, 1) if staff else None,
            "today": str(today)
        })
    data=await request.post()
    if "student" in data.keys():
        students=data.getall("student")
        for x in students:
            db.update_pass(x, datetime.now().date())
    if "staff" in data.keys():
        staff=data.getall("staff")
        for x in staff:
            db.update_pass(x, datetime.now().date(), utype=2)
    return web.HTTPSeeOther("/admin/tickets/today")

@routes.get("/verify")
async def verify_email(request: web.Request):
    code=request.rel_url.query.get("code")
    resp=db.verify_code(code)
    if resp:
        return web.Response(text="Email Verified successfully. Please Login Again")
    else:
        return web.Response(text="invalid Link or Account already verified")
    
# -------------------------------------------

@routes.get("/staff")
async def student_home(request: web.Request):
    user=request["user"]
    bus_pass = db.get_pass(user[0], utype=2)
    valid_pass=[ x for x in bus_pass if x[3] > len(x[4])]
    if not valid_pass:
        return web.HTTPSeeOther("/staff/apply")
    return aiohttp_jinja2.render_template("staff_home.html", request, {
        "name": user[1],
        "department": user[4],
        "aadhar": user[0],
        "bus_pass": valid_pass,
    })

@routes.get("/staff/print")
async def student_home(request: web.Request):
    bus_pass = db.get_pass(key=request.rel_url.query.get("key"), utype=2)
    user=request["user"]
    return aiohttp_jinja2.render_template("staff_print.html", request, {
        "name": user[1],
        "department": user[4],
        "aadhar": user[0],
        "ticket": bus_pass
    })

@routes.get("/staff/apply")
async def student_apply(request: web.Request):
    user = request["user"]
    place=db.get_place()
    return aiohttp_jinja2.render_template("staff_apply.html", request, {
        "name": user[1],
        "department": user[4],
        "aadhar_no": user[0],
        "place": place
    })

@routes.post("/staff/order/confirm")
async def order_confirm(request: web.Request):
    data=await request.post()
    user=request["user"]

    days=int(data.get("days"))
    place=data.get("from-to")
    uuid4=uuid.uuid4()
    aadhar=user[0]
    name=user[1]
    email=user[2]
    phoneno=data.get("phone")

    db_place = db.get_place(place=place)
    price = int(db_place[1])
    
    amount = price * days

    payment_id=await create_order(str(aadhar), str(phoneno), name, email, str(uuid4), amount, "/staff/order/checkout")
    if payment_id:
        db.create_order(str(uuid4), email, place, price=amount, days=days)
        return aiohttp_jinja2.render_template("staff_order_confirm.html", request, {
            "sessionid": payment_id,
            "name": name,
            "department": user[4],
            "place": place,
            "days": days,
            "aadhar": aadhar,
            "price": amount,
        })
    return web.HTTPServerError()

@routes.get("/staff/order/checkout")
async def checkout(request: web.Request):
    order_id=request.rel_url.query.get("order_id")
    if not order_id:
        return web.HTTPMethodNotAllowed()
    resp=(await fetch_payment(order_id))[0]
    if resp.get("payment_status")=="SUCCESS":
        order=db.get_order(order_id, utype=2)
        if order[5] in ["SUCCESS", "PROCESSED"]:
            return aiohttp_jinja2.render_template("student_order_checkout.html", request, {
                "status": resp.get("payment_status"),
                "payment_id": resp.get("cf_payment_id"),
                "order_id": resp.get("order_id")
            })
        db.modify_order(order_id, str(resp.get("payment_status")), utype=2)
        user=db.get_user(email=order[1], user_type="Staff")
        place=db.get_place(place=order[2])
        days: int=order[3]
        db.create_pass(user[0], place[0], order_id, days=days)
        db.modify_order(order_id, "PROCESSED", utype=2)
    elif resp.get("payment_status"):
        db.modify_order(order_id, str(resp.get("payment_status")), utype=2)
        # [PENDING, USER_DROPPED, FAILED]
    else:
        return web.HTTPBadRequest()
    return aiohttp_jinja2.render_template("student_order_checkout.html", request, {
        "status": resp.get("payment_status"),
        "payment_id": resp.get("cf_payment_id"),
        "order_id": resp.get("order_id")
    })

@routes.get("/forgot")
async def forgot_password(request: web.Request):
    data=request.rel_url.query
    user_type=data.get("user-type")
    email=data.get("email", "")
    otp=data.get("otp", "")
    password=data.get("password", None)
    error=None
    success=False
    if email:
        if otp:
            resp=db.update_password(email, otp, password)
            if resp:
                if password:
                    success=True
            else:
                error="Inavlid OTP"
                otp=""
        else:
            gen_otp=db.gen_otp(email, user_type)
            if gen_otp:
                await send_mail(None, email, "Your otp for changing password is "+gen_otp, "OTP for Password Reset")
            else:
                error="Invalid Email or User type"
                email=""
            
            
    return aiohttp_jinja2.render_template("forgot_password.html", request, {
        "user_type": user_type,
        "email": email,
        "otp": otp,
        "success": success,
        "error": error,
        "btn_name": "Update Password" if otp else "Verify OTP" if email else "Generate OTP"
    })