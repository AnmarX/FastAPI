from typing import Annotated

from fastapi import Cookie, FastAPI,Response

app = FastAPI()
# writing the cookies 
@app.get('/set')
async def setting(response: Response):
    response.set_cookie(key='refresh_token', value='helloworld', httponly=True)
    return True

# reading the cookies
@app.get("/items/")
async def read_items(refresh_token: Annotated[str | None, Cookie()] = None):
    return {"refresh_token": refresh_token}