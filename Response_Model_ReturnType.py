from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Any

app = FastAPI()


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]




# #the arrow indicate what will be returned 
@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user



# # the second method 


# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: str | None = None


# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn) -> Any:
#     return user