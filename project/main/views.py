import os
import pathlib
from typing import Dict

import aiohttp_jinja2
import markdown2
from aiohttp import web, MultipartReader
from project.utils.database import MySQLConnection
db=MySQLConnection()
routes = web.RouteTableDef()

@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> Dict[str, str]:
    files = os.listdir("project/templates")
    return {"files": files}

@routes.post("/api/create")
async def create_account(request: web.Request):
    print("Hi")
    data=await request.post()
    admission_number=data["admission-number"]
    name=data["name"]
    photo=data["photo"]
    department=data["department"]
    password=data["pass"]
    file_name=photo.filename
    status = db.create_user(admission_number, name, file_name, department, password)
    if status=="exist":
        return web.Response(body="User Already Exist")
    else:
        with open(f"photo/{file_name}", "wb") as f:
            f.write(photo.file.read())
        return web.HTTPTemporaryRedirect("/static/login.html")