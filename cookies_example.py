from fastapi import FastAPI, Request, Form,Cookie,Response,status
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# set cookie 
# @app.post("/cookie-and-object/")
# def create_cookie(response: Response):
#     response.set_cookie(key="ads_id", value="fake-cookie-session-value")
#     return {"message": "Come to the dark side, we have cookies"}


# # read cookie
# @app.get("/itemsttttt/")
# async def read_items(ads: Annotated[str | None, Cookie()] = None):
#     return {"ads_id": ads}



@app.get("/",response_class=HTMLResponse)
async def read_items(request: Request,saved_name: Annotated[str |None , Cookie()]=None):
    return templates.TemplateResponse("index.html", {"request": request,"saved_name":saved_name})


# the name here has to be the same on html name="name"
@app.post("/save_name")
async def save_name(name:Annotated[str|None,Form()]=None):
    response = RedirectResponse("/return", status_code=status.HTTP_303_SEE_OTHER)

    if name:
        response.set_cookie(key="saved_name", value=name)
    else:
        response.delete_cookie(key="saved_name")
        
    return response
    
   
@app.get("/return",response_class=HTMLResponse)
async def read_items(request: Request,saved_name: Annotated[str |None , Cookie()]=None):
    return templates.TemplateResponse("for_cookie.html", {"request": request,"saved_name":saved_name})



@app.get("/delete_cookie")
async def delete_cookie():
    response = RedirectResponse("/")
    response.delete_cookie("saved_name")
    return response




# # setting and getting the cookie 
# @app.post("/cookie/")
# def create_cookie(s:str):
#     content = {"message": "Come to the dark side, we have cookies"}
#     response = JSONResponse(content=content)
#     response.set_cookie(key="fakesession", value=s)
#     return response


# @app.get("/return/")
# async def read_items(fakesession: Annotated[str | None, Cookie()] = None):
#     return {"ads_id": fakesession}