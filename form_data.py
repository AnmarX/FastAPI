from typing import Annotated

from fastapi import FastAPI, Form,Request
from fastapi.templating import Jinja2Templates
from pydantic import Field

app = FastAPI()

templates=Jinja2Templates(directory="templates")

@app.get("/")
async def locate(request:Request):
    return templates.TemplateResponse("for_form_data.html",{"request":request})


@app.post("/login/")
async def login(user_name: Annotated[str, Form(...,alias="user-name")]):
    return {"username": user_name}
