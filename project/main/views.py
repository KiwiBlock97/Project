import os
import pathlib
from typing import Dict
import uuid

import aiohttp_jinja2
import markdown2
from aiohttp import web, MultipartReader
from aiohttp_session import get_session
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
    file_name=admission_number#photo.filename
    status = db.create_user(admission_number, name, email, file_name, department, password)
    if status=="exist":
        return web.Response(body="User Already Exist")
    else:
        with open(f"photo/{admission_number}", "wb") as f:
            f.write(photo.file.read())
        return web.HTTPFound("/login")
    
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
        return web.HTTPFound("/static/admin_home.html")
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
        return web.HTTPTemporaryRedirect("/login")
    user = db.get_user(email, "Student")
    if not user:
        return web.HTTPFound("/login")
    bus_pass = db.get_pass(user[0])
    if not bus_pass:
        return web.HTTPTemporaryRedirect("/student/apply")
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
    print(data)
    if not email:
        return web.HTTPTemporaryRedirect("/login")
    user = db.get_user(email, "Student")
    if not user:
        return web.HTTPTemporaryRedirect("/signup")
    if not (data):
        return aiohttp_jinja2.render_template("student_apply.html", request, {
            "name": user[1],
            "department": user[4],
            "adm_no": user[0],
        })
    uuid4 = uuid.uuid4()
    admid=int(user[0])
    place=data.get("from-to")
    validity=int(data.get("validity"))
    valid=validity*86400
    db.create_pass(admid, place, valid, str(uuid4))
    return web.HTTPFound("/student")

@routes.route("*", "/student/renew")
async def apply_pass(request: web.Request):
    session = await get_session(request)
    if not session.get("email", None):
        return web.HTTPFound("/login")
    email = session.get("email", None)
    user=db.get_user(email,"Student")
    if not user:
        return web.HTTPFound("/signup")
    bus_pass=db.get_pass(user[0])
    if not bus_pass:
        return web.HTTPFound("/student/apply")
    data=await request.post()
    validity=data.get("validity", None)
    if not validity:
        return aiohttp_jinja2.render_template("student_renew.html", request, {
            "name": user[1],
            "department": user[4],
            "place": bus_pass[1],
            "adm_no": user[0] 
        })
    valid=int(bus_pass[2])+(int(validity)*86400)
    db.extend_pass(valid, bus_pass[3])
    return web.HTTPSeeOther("/student")