from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(description="Sdsddsd",title="the id ")],
    q: Annotated[str | None, Query(alias="item-query",description="Asdsdads")] = None,
):
    """
    - itemid
        - sd    
    """
    results = {"item_id": item_id}
    more_data={"name":"A","age":23}
    if q:
        results.update(more_data)
    return results

# THE None variables should come last
@app.get("/itemsdss/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    size: Annotated[float |None, Query(gt=0, lt=10.5)]=None,
    q: Annotated[str | None ,Query(alias="D")]=None,
    ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

