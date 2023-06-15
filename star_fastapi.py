from fastapi import FastAPI

app = FastAPI()



"""
When calling the /items/ endpoint:

http://localhost:8000/items/?q=test will work, passing the value test to the q parameter.
http://localhost:8000/items/test will also work, treating test as a positional argument and assigning it to the q parameter.
When calling the /users/ endpoint:

http://localhost:8000/users/?q=test will work, passing the value test to the q parameter.
http://localhost:8000/users/test will result in an error, as test is treated as a positional argument but there are no parameters before q to receive it.
So, using * enforces the use of keyword arguments for the parameters that follow it, while not using * allows both positional and keyword arguments for those parameters.
"""

@app.get("/items/")
async def read_items(q: str = None):
    return {"q": q}


@app.get("/users/")
async def read_users(*, q: str = None):
    return {"q": q}