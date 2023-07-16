from fastapi import FastAPI,Depends,Form,status,Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
import psycopg
import os
from pydantic import BaseModel
from typing import Annotated,Union

from db_connection.connection import get_db 

templates=Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")



# load_dotenv() 

# PG_HOST=os.getenv('PG_HOST')
# PG_DB = os.getenv('PG_DB')
# PG_USER= os.getenv('PG_USER')
# PG_PW = os.getenv('PG_PW')
# PG_PORT=os.getenv('PG_PORT')

    
    

# Database connection configuraon
# DATABASE_CONFIG = {
#     "dbname": PG_DB,
#     "user": PG_USER,
#     "password": PG_PW,
#     "host": PG_HOST,
#     "port": PG_PORT,
# }

# # Database connection helper function
# def get_db():
#     conn = psycopg.connect(**DATABASE_CONFIG)
#     try:
#         yield conn
#     finally:
#         conn.close()



@app.get("/cookies")
def get_cookie_html(request: Request, cookie: Annotated[Union[str, None], Cookie()] = None):
    return templates.TemplateResponse("cookie.html",{"request": request,"cookie":cookie})


@app.post("/get-cookie")
async def save_name(name:Annotated[Union[str , None],Form()]=None):
    res=RedirectResponse("/cookies",status_code=status.HTTP_303_SEE_OTHER)
    if name:
        res.set_cookie(key="cookie",value=name)
    else:
        res.delete_cookie(key="cookie")
    return res




@app.get("/")
def main(request:Request,conn=Depends(get_db)):
    cur=conn.cursor()
    todo_table=cur.execute("SELECT all_todos, id FROM todo")
    # # another way to do it
    """
    todos = [( row[0], row[1]) for row in todo_table.fetchall()]
    todos = [{"all_todos": row[0], "id": row[1]} for row in todo_table.fetchall()]
    todos = [[row[0], row[1]] for row in todo_table.fetchall()]

    these three do the same thing
    """
    todos = [[row[0], row[1]] for row in todo_table.fetchall()]

    return templates.TemplateResponse("index.html",{"request":request,"all":todos})

    # todos = []
    # for row in todo_table.fetchall():
    # todo = {"all_todos": row[0], "id": row[1]}
    # todos.append(todo)

    # todos = list(map(lambda row: {"all_todos": row[0], "id": row[1]}, todo_table.fetchall()))



    # cur.execute("SELECT all_todos from todo")
    # # # these two do the same things
    # all_of_todos = [row[0] for row in cur.fetchall()]
    # return templates.TemplateResponse("index.html",{"request":request,"all":all_of_todos})

    # all_of_todos=[]
    # a=cur.fetchall()
    # #[('sdd',), ('sd',)]
    # for row in cur.fetchall():
    # #row will return ('sds',) only last index
    #     for r in row:
    # #r will return sds only the last index
    #         all_of_todos.append(r)

    # # row will return ('sds',)
    # # r will return sds only
    # # these two do the same things
    
    # #[('sdd','ger'), ('sd','hfh')] this is list of tuple 
    # #('sdd','ger') on the left row[0] on the right row[1]
    # # if you want to access the first value use row[0] that means at the first row access the first column

    # # will return list of tuples
    # c=cur.fetchall()
    # # output of the above [('sdd',), ('sd',), ('sds',), ('dlkffopf',), ('sdsd',), ('sds',), ('dksjd',), ('sds',)]


    # # will return only the last value
    # for row in cur.fetchall():
    #     for r in row:
    #         pass
    # # output  sds 

    
    # gettng_todos=[dict(all_of_todos=row[0]) for row in cur.fetchall()]
    


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




@app.post("/update/{todo_id}")
def update(todo_id:str,conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("UPDATE todo SET complete = NOT complete WHERE id = %s", (todo_id,))
    conn.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# <form action="/update/{{ todo.id }}" method="get" style="display: inline;">
# because the todo_id is on the action="/update/{{ todo.id }} so the id will be passed 
# to the endpoint {todo_id}

@app.post("/delete/{todo_id}")
def delete(todo_id:int,conn=Depends(get_db)):
    cur=conn.cursor()
    cur.execute("DELETE FROM todo WHERE id=%s", (todo_id,))
    conn.commit()
    url = app.url_path_for("main")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


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


