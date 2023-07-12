from fastapi import FastAPI,Depends,Form,status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
import psycopg
import os
from pydantic import BaseModel




templates=Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")



load_dotenv() 

PG_HOST=os.getenv('PG_HOST')
PG_DB = os.getenv('PG_DB')
PG_USER= os.getenv('PG_USER')
PG_PW = os.getenv('PG_PW')
PG_PORT=os.getenv('PG_PORT')

    
    

# Database connection configuraon
DATABASE_CONFIG = {
    "dbname": PG_DB,
    "user": PG_USER,
    "password": PG_PW,
    "host": PG_HOST,
    "port": PG_PORT,
}

# Database connection helper function
def get_db():
    conn = psycopg.connect(**DATABASE_CONFIG)
    try:
        yield conn
    finally:
        conn.close()



@app.get("/")
def main(request:Request,conn=Depends(get_db)):
    cur=conn.cursor()
    cur.execute("SELECT all_todos from todo")
    all_of_todos=[]
    for row in cur.fetchall():
        for r in row:
            all_of_todos.append(r)
    # gettng_todos=[dict(all_of_todos=row[0]) for row in cur.fetchall()]
    
    return templates.TemplateResponse("index.html",{"request":request,"all":all_of_todos})


@app.post("/add")
def insert_to_do(
    title:str=Form(...),
    conn=Depends(get_db)
    ):
    cur=conn.cursor()
    cur.execute("INSERT INTO todo(all_todos) VALUES(%s)", (title,))
    conn.commit()
    url = app.url_path_for("main")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    # return RedirectResponse("/",status_code=status.HTTP_303_SEE_OTHER)




@app.put("/update")
def update():
    pass

@app.delete("/delete")
def delete():
    pass



# from fastapi import FastAPI, Depends, Request, Form, status
# from starlette.responses import RedirectResponse
# from starlette.templating import Jinja2Templates
# import psycopg
# # from psycopg2.extras import DictCursor

# from dotenv import load_dotenv
# import os

# load_dotenv() 

# PG_HOST=os.getenv('PG_HOST')
# PG_DB = os.getenv('PG_DB')
# PG_USER= os.getenv('PG_USER')
# PG_PW = os.getenv('PG_PW')
# PG_PORT=os.getenv('PG_PORT')

# DATABASE_CONFIG = {
#     "dbname": PG_DB,
#     "user": PG_USER,
#     "password": PG_PW,
#     "host": PG_HOST,
#     "port": PG_PORT,
# }


# templates = Jinja2Templates(directory="templates")

# app = FastAPI()

# # Dependency
# def get_db():
#     conn = psycopg.connect(**DATABASE_CONFIG)
#     try:
#         yield conn
#     finally:
#         conn.close()

# @app.get("/")
# def home(request: Request, conn=Depends(get_db)):
#     cur = conn.cursor()
#     cur.execute("SELECT all_todos FROM todo")
#     todos = cur.fetchall()
#     return templates.TemplateResponse("index.html", {"request": request, "todo_list": todos})

# @app.post("/add")
# def add(request: Request, title: str = Form(...), conn=Depends(get_db)):
#     cur = conn.cursor()
#     cur.execute("INSERT INTO todo (all_todos) VALUES (%s)", (title,))
#     conn.commit()
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# @app.get("/update/{todo_id}")
# def update(request: Request, todo_id: int, conn=Depends(get_db)):
#     cur = conn.cursor()
#     cur.execute("UPDATE todo SET complete = NOT complete WHERE id = %s", (todo_id,))
#     conn.commit()
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# @app.get("/delete/{todo_id}")
# def delete(request: Request, todo_id: int, conn=Depends(get_db)):
#     cur = conn.cursor()
#     cur.execute("DELETE FROM todo WHERE id = %s", (todo_id,))
#     conn.commit()
#     url = app.url_path_for("home")
#     return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


