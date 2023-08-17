from fastapi import APIRouter,Form,Depends,status,Request
from fastapi.responses import RedirectResponse
from typing import Annotated
from db_connection.connection import get_db
from get_active_user.active import for_id,get_current_active_user
from starlette.middleware.sessions import SessionMiddleware

import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY=os.getenv("secret_key")
router = APIRouter()



@router.post("/add-todo")
async def add_todo(
    title:Annotated[str,Form()],
    request:Request,
    token:Annotated[for_id,Depends(get_current_active_user)],
    conn=Depends(get_db)
):
    try:
        user_id=token.user_id
        cur=conn.cursor()
        cur.execute("insert into todo(all_todos,user_id) values(%s,%s)",(title,user_id))
        conn.commit()
        response=RedirectResponse("/todos-page",status_code=status.HTTP_303_SEE_OTHER)
        return response
    except (AttributeError):
        request.session["next_page"] = "/show-todos"
        redirect_url = f"/login-page?mgs=login to access the todo"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
    



@router.post("/delete-todo/{todo_id}")
async def delete_todo(
    todo_id:int,
    token:Annotated[for_id,Depends(get_current_active_user)],
    conn=Depends(get_db)
):  
    user_id=token.user_id
    cur=conn.cursor()
    cur.execute("DELETE FROM todo WHERE user_id=%s AND todo_id=%s", (user_id,todo_id))
    conn.commit()
    response=RedirectResponse("/todos-page",status_code=status.HTTP_303_SEE_OTHER)
    return response

@router.post("/complete-todo")
async def delete_todo():
    pass


if __name__=="__main__":
    pass