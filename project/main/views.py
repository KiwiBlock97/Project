import os
import pathlib
from typing import Dict

import aiohttp_jinja2
import markdown2
from aiohttp import web


@aiohttp_jinja2.template('index.html')
async def index(request: web.Request) -> Dict[str, str]:
    files = os.listdir("project/template")
    return {"files": files}
