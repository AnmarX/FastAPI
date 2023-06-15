from fastapi import FastAPI,Body
from pydantic import BaseModel,HttpUrl
from typing import Annotated

app = FastAPI()

# with list
class Item(BaseModel):
    name: str|None=None
    description: str | None = None
    price: float|None=None
    tax: float | None = None
    # if i want to only use a specific data type i will use it like this : tags: list[str] = []
    tags: list[int] = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item:Annotated[Item,Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results




# with set
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results




# nested models
class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results







#advance nested models 
class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer
