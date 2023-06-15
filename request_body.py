from fastapi import FastAPI,Query
from pydantic import BaseModel
from typing import Annotated


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
 


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item,q:Annotated[str|None,Query(regex="^fixedquery$")]=None):
    d=item.dict()
    if q :
        d.update({"q":q})
    if item.name != "n".strip().lower():
        return{"mge":"error"}
    return d