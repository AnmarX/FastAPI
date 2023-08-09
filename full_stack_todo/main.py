from fastapi import FastAPI,Form,Depends,status,Cookie,Query
from pydantic import BaseModel,EmailStr,validator,ValidationError
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from db_connection.connection import get_db
from pydantic.fields import Field
from fastapi.exceptions import HTTPException
from hashing import hash_the_password,verify_password
from fastapi.responses import RedirectResponse,Response,JSONResponse
from typing import Annotated
from datetime import datetime, timedelta
from jose import JWTError, jwt
from todo_CURD import models
import os
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY=os.getenv("secret_key")
ALGORITHM=os.getenv("ALGORITHM")

templates=Jinja2Templates(directory="templates")

app=FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.include_router(models.router, prefix="/todo_CURD")
app.mount("/static", StaticFiles(directory="static"), name="static")



ACCESS_TOKEN_EXPIRE_MINUTES = 5


password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class User(BaseModel):
    email:EmailStr
    

class UserPassword(User):
    password_:str = Field(regex=password_regex)
    disables:bool


# class Dis(UserPassword):
#     disables:bool



    # Pydantic validator to set disables to True if not provided by the user
    # @validator('disables', pre=True, always=True)
    # def set_disables(cls, v):
    #     return v if v is not None else True
   




def get_user(email,cur):
    all=cur.execute("SELECT email,password_,disables FROM users WHERE email = %s", (email,))
    get_user_info=[{"email":row[0],"password_":row[1],"disables":row[2]}for row in all.fetchall()]
    if get_user_info:
        for user in get_user_info:
            return UserPassword(**user)

def authenticate_user(cur,email,password):
    user=get_user(email,cur)
    if not user:
        return False
    if not verify_password(password,user.password_):
        print("password not good")
        return False
    return user


def create_access_token(data:dict,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    




async def get_current_user(token: Annotated[str|None, Cookie()]=None,conn=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,ALGORITHM)
        email:str=payload.get("sub")
        if not email:
            raise credentials_exception
        # token_data=For_token_valid(email=email)
    except (AttributeError,JWTError,TypeError):
        return False
    cursor=conn.cursor()
    user = get_user(email,cursor)
    if user is None:
       return False
    return user



async def get_current_active_user(
    current_user: Annotated[UserPassword, Depends(get_current_user)]
):
    try:
        if not current_user.disables:
            raise HTTPException(status_code=400, detail="Inactive user")
    except AttributeError:
        return False


    return current_user




@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register-page")
async def signup(
    request: Request,
                 ):
    return templates.TemplateResponse("Register.html", {"request": request})

@app.get("/missmatch-error")
async def signup(
    request: Request,
    email_cookie:Annotated[str|None,Cookie()]=None
                 ):
    return templates.TemplateResponse("missmatch_pass.html", {"request": request,"email_cookie":email_cookie})







# @app.get("/login-page")
# async def signup(
#     request: Request,
#     token:Annotated[str,Cookie()]=None,
#                  ):
#     print(token)
#     if token is None:
#         return templates.TemplateResponse("login.html", {"request": request})

#     redirect_url = f"/logedin-page?token={token}"
#     response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
#     return response
    

    
    







@app.get("/todos-page")
async def signup(
    request: Request,
    token=Depends(get_current_active_user)
                 ):
    print(token)
    if token:
        return templates.TemplateResponse("todoList.html", {"request": request})
   
    redirect_url = f"/login-page?msg=not valid token"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response


# 4
@app.get("/show-todos",response_model=User)
def show_todos(
    request:Request,
    get_token:Annotated[UserPassword,Depends(get_current_active_user)],
    token:Annotated[str,Cookie()]=None
):  
    # if the token is valdid it will take you to the todo app
    if get_token:
        redirect_url = f"/todos-page?token={token}"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
        # return get_token
    else:
        request.session["next_page"] = "/show-todos"
        redirect_url = f"/login-page?mgs=login to access the todo"
        return RedirectResponse("/login-page",status_code=status.HTTP_303_SEE_OTHER)
    
    


@app.get("/logedin-page")
async def signup(
    request: Request
                 ):
    # after the user has loged in i will do operation with the database here and sent it to the user page to see
    return templates.TemplateResponse("logged_in.html", {"request": request})

@app.get("/login-page")
async def signup(
    request: Request,
    token_exists:Annotated[str,Depends(get_current_active_user)]=None,
    token:Annotated[str,Cookie()]=None,
                 ):
    if token_exists:
        redirect_url = f"/logedin-page?token={token}"
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        return response
    
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(
    request:Request,
    email:EmailStr=Form(...),
    apass:str=Form(...),
    conn=Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    cur=conn.cursor()
    user=authenticate_user(cur,email,apass)
    if not user:
        return credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    next_page = request.session.get("next_page")
    
    redirect_url = f"/logedin-page?token={access_token}"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="token", value=access_token, httponly=True, max_age=1800)
    if next_page:
        response= RedirectResponse(url=next_page, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="token", value=access_token, httponly=True, max_age=1800)
        return response
    return response
    # response = RedirectResponse("/logedin-page",status_code=status.HTTP_303_SEE_OTHER)
    # response.set_cookie(key="token", value=access_token, httponly=True,max_age=1800)
    # response.headers["Location"] += f"?token={access_token}"
    # return response
   



# 1
@app.post("/register")
def register(
# request:Request,
# response:Response,
email:EmailStr=Form(...),
apass:str=Form(...),
conn=Depends(get_db)

):
    try:
        user_in= UserPassword(email=email,password_=apass,disables=True)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (user_in.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="email already exists")
       
        hashed_password = hash_the_password(user_in.password_)
        
        cursor.execute(
            "INSERT INTO users (email, password_,disables)"
            "VALUES (%s, %s,'True') RETURNING email",
            (user_in.email, hashed_password),
        )
        
        user_data = cursor.fetchone()
        conn.commit()
        print(user_data)

    except ValidationError as e:

        print(e)
        back=RedirectResponse("/missmatch-error",status_code=status.HTTP_303_SEE_OTHER)
        back.set_cookie(key="email_cookie" ,value=email)
        return back
        
    
         

    
    

# 2










