import redis.asyncio as rd
import uvicorn
from fastapi import Depends, FastAPI

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = rd.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)


@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=10))])
async def index():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)