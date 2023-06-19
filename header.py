from typing import Annotated
from fastapi import FastAPI, Header,Cookie,Response,Request
from fastapi.responses import JSONResponse
import uvicorn



app = FastAPI()

tokenn="anmar"
@app.get("/items/")
async def read_items(
    user_agent: Annotated[str | None, Header()] = None,
    sec_ch_ua_platform:Annotated[str|None,Header()]=None,
    x_cat_dog:Annotated[str|None,Header()]=None
                     ):
    return {"User-Agent": user_agent,"sec-ch-Ua-Platform":sec_ch_ua_platform,"X-Cat-Dog":x_cat_dog}

@app.get("/headers-and-object/")
def get_headers():
    response=JSONResponse({"msg":"done"})
    response.headers["x-cat-dog"] = "alone in the world"
    return response 

@app.get("/headers/")
async def get_headers(request: Request):
    # client_headers = request.headers
    # a=dict(client_headers)
    # return {"headers": a["user-agent"]}
    client_headers = request.headers
    return {"headers": dict(client_headers)}

@app.get("/get-header/")
def get_headers(token:Annotated[str,Header()]):
    if tokenn == token and token:
        return {"msg":"done"}
    else:
        return {"msg":"not valid"}
    

if __name__ == '__main__':
    uvicorn.run('header:app', server_header=False)
    #uvicorn header:app --no-server-header --reload