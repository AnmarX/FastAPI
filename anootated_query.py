from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

# annotated provide more metadata or additional constraints
# here it sperated with , 
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=10,min_length=10)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



# without annotated it all in one line the validation and the constraints
# here is not sperated
@app.get("/itemssss/")
async def read_items(q: str | None = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/itemssdsd/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items