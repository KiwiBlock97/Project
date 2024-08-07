import os
import pathlib
from typing import Dict

import aiohttp_jinja2
import markdown2
from aiohttp import web, MultipartReader
from aiohttp_session import get_session
from project.utils.database import MySQLConnection
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
        return web.HTTPTemporaryRedirect("/login")
    
@routes.route("*", "/login")
async def login(request: web.Request):
    data=await request.post()
    email=data.get("email")
    password=data.get("password")
    if not (email or password):
        return aiohttp_jinja2.render_template("login.html", request, {})
    Resp, Type = db.auth_user(email, password)
    session = await get_session(request)
    session["Test"]="Testing"

    if Resp==None:
        return web.Response(body="Invalid Email or Password")
    session["email"]=email
    session["type"]=Type
    if Type=="Admin":
        return web.HTTPTemporaryRedirect("/static/admin_home.html")
    elif Type=="Student":
        session["admid"]=Resp
        return web.HTTPTemporaryRedirect("/student")

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
    print(session)
    email = session.get("email", None)
    user_type = session.get("type", None)
    if (not email) or user_type!="Student":
        return web.HTTPTemporaryRedirect("/login")
    user = db.get_user(email, "Student")
    bus_pass = db.get_pass(user[0])
    if not bus_pass:
        return web.HTTPTemporaryRedirect("/student/apply")
    return aiohttp_jinja2.render_template("student_home.html", request, {
        "name": user[1],
        "department": user[4],
        "admission": user[0],
        "validity": bus_pass[3],
        "from": user[2],
        "ticketid": user[4],
    })
