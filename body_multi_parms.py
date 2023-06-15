from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: int
    tax: int | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
  
    try:        
        if item:
            if  item.name=="string" or not item.price:
                raise ValueError()
            results.update({"item": item})
        
    except: 
       return {"resullts":results,"notify_msg":"if you use the body make sure to use required fields, else ignore this msg"}

    return results