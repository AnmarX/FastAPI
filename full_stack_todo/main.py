from fastapi import FastAPI,Form,Depends,status,Cookie,Query,BackgroundTasks
from pydantic import BaseModel,EmailStr,validator,ValidationError
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from db_connection.connection import get_db
from pydantic.fields import Field
from fastapi.exceptions import HTTPException
from hashing import hash_the_password,verify_password
from fastapi.responses import RedirectResponse,Response,JSONResponse,HTMLResponse
from typing import Annotated
from datetime import datetime, timedelta
from jose import JWTError, jwt,ExpiredSignatureError
from todo_CURD import models
import os
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import time
from typing import List
import secrets

load_dotenv()
SECRET_KEY=os.getenv("secret_key")
ALGORITHM=os.getenv("ALGORITHM")
email_pass=os.getenv("email_pass")
email_for_msg=os.getenv("email_for_msg")

templates=Jinja2Templates(directory="templates")


conf = ConnectionConfig(
    MAIL_USERNAME = email_for_msg,
    MAIL_PASSWORD = email_pass,
    MAIL_FROM = email_for_msg,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
print(email_pass)
print(email_for_msg)


app=FastAPI()
fm = FastMail(conf)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(models.router)

app.mount("/static", StaticFiles(directory="static"), name="static")



ACCESS_TOKEN_EXPIRE_MINUTES = 15


password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


# class EmailSchema(BaseModel):
#     email_verify: List[EmailStr]

class User(BaseModel):
    email:EmailStr
    

class UserPassword(User):
    password_:str = Field(regex=password_regex)
    disables:bool

class for_id(UserPassword):
    user_id:int
# class Dis(UserPassword):
#     disables:bool



    # Pydantic validator to set disables to True if not provided by the user
    # @validator('disables', pre=True, always=True)
    # def set_disables(cls, v):
    #     return v if v is not None else True
   



@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    session = request.cookies.get('session')
    if session:
        response.set_cookie(key='session', value=request.cookies.get('session'), httponly=True,max_age=60)
    return response





def get_user(email,cur):
    all=cur.execute("SELECT email,password_,disables,user_id FROM users WHERE email = %s", (email,))
    get_user_info=[{"email":row[0],"password_":row[1],"disables":row[2],"user_id":row[3]}for row in all.fetchall()]
    if get_user_info:
        for user in get_user_info:
            return for_id(**user)

def authenticate_user(cur,email,password):
    user=get_user(email,cur)
    # print(user)
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
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    

def temp_access_token(data:dict,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=2)
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
    current_user: Annotated[for_id, Depends(get_current_user)]
):
    # NEXT ADD here if the user register and the email valildation expired add
    # a button to send to them again

    try:
        if not current_user.disables:
            raise HTTPException(status_code=400, detail="you need to active your account with the email we sent you")
    except AttributeError:
        return False


    return current_user




async def send_email(
        user_email:list[EmailStr],    
        token:str    
):
    
    template=f"""
    <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        </head>
        <body>
        <a href="http://localhost:9999/verify-email/{token}">
            please verify your account
        </a>
        </body>
        </html>
    """
    message = MessageSchema(
       subject="Fastapi-Mail module",
       recipients=user_email,  # List of recipients, as many as you can pass  
       body=template,
       subtype="html"
       )
    
    await fm.send_message(message)
    print("email sent")



def is_token_expired(token: str):
    try:
        jwt.decode(token,SECRET_KEY,ALGORITHM)
        # expiration_time = datetime.utcfromtimestamp(payload["exp"])
        # print(expiration_time)
        # current_time = datetime.utcnow()
        # return current_time > expiration_time
    except (ExpiredSignatureError,JWTError):
        # Token has expired
        # Token is invalid or cannot be decoded
        print("exp1")
        return True
    


@app.get("/verify-email/{user_token}")
async def verifying(
        # user:Annotated[for_id,Depends(get_current_user)],
        user_token:str,
        conn=Depends(get_db)    
):
    cursor=conn.cursor()
    user_exp=is_token_expired(user_token)
    if user_exp is True:
        # # add here a link to send a new link rather than this return msg
        return {"msg":"the validation link has expired"}
    
    user = await get_current_user(user_token,conn)
    if user is False:
        return {"msg":"token is expired go back to login again"}
    # user=get_user_for_validation(user_token,conn)
    print(user.user_id)
    cursor.execute("UPDATE users SET disables = %s WHERE user_id = %s", (True,user.user_id))
    conn.commit()
    return {"msg":"done"}



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



@app.get("/todos-page")
async def signup(
    request: Request,
    token:Annotated[for_id,Depends(get_current_active_user)],
    conn=Depends(get_db)
                 ):
    
    if token:
        cur=conn.cursor()
        user_id=token.user_id
        todo_table=cur.execute("SELECT all_todos,todo_id FROM todo WHERE user_id = %s", (user_id,))
        # todo_table=cur.execute("SELECT all_todos, todo_id FROM todo")
        all=[[row[0],row[1]] for row in todo_table.fetchall()]
        return templates.TemplateResponse("todoList.html", {"request": request,"all":all})
   

    request.session["next_page"] = "/show-todos"
    redirect_url = f"/login-page?msg=not valid token"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    return response

  

    


# 4
@app.get("/show-todos",response_model=User)
def show_todos(
    request:Request,
    get_token:Annotated[for_id,Depends(get_current_active_user)],
    token:Annotated[str,Cookie()]=None
):  
    # if the token is valdid it will take you to the todo app
    if get_token:
        # print(get_token)
        redirect_url = f"/todos-page?token={token}"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
        # return get_token
    else:
        request.session["next_page"] = "/show-todos"
        # for_session.set_cookie(key="next_page",max_age=30)
        redirect_url = f"/login-page?mgs=login to access the todo"
        return RedirectResponse(redirect_url,status_code=status.HTTP_303_SEE_OTHER)
    
    

# # NEED to add here if the user tryied to access this endpoint without token
# # i will send him back to the login page
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
    user=authenticate_user(cur,email.lower(),apass)
    # #modify here
    if not user:
        return credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    next_page = request.session.get("next_page")
    
    redirect_url = f"/logedin-page?token={access_token}"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="token", value=access_token, httponly=True, max_age=900)
    if next_page:
        response= RedirectResponse(url=next_page, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="token", value=access_token, httponly=True, max_age=900)
        return response
    return response
    # response = RedirectResponse("/logedin-page",status_code=status.HTTP_303_SEE_OTHER)
    # response.set_cookie(key="token", value=access_token, httponly=True,max_age=1800)
    # response.headers["Location"] += f"?token={access_token}"
    # return response
   



# 1
@app.post("/register")
async def register(
# request:Request,
# response:Response,
background_tasks: BackgroundTasks,
email:EmailStr=Form(...),
apass:str=Form(...),
conn=Depends(get_db),


):
    try:
        user_in= UserPassword(email=email.lower(),password_=apass,disables=False)
        # validation_for_email=EmailSchema(email_verify=email)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (user_in.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="email already exists")
        
        

        hashed_password = hash_the_password(user_in.password_)

        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
        data={"sub": user_in.email}, expires_delta=access_token_expires
        )        


        temp_token_expires = timedelta(minutes=2)
        temp_token=temp_access_token(
        data={"sub": user_in.email}, expires_delta=temp_token_expires
        )
        background_tasks.add_task(send_email, [user_in.email], temp_token)
        # await send_email([user_in.email],access_token)
        cursor.execute(
            "INSERT INTO users (email, password_,disables)"
            "VALUES (%s, %s,'False') RETURNING email",
            (user_in.email, hashed_password),
        )
        conn.commit()
        user_data = cursor.fetchone()
        
        print(user_data)
        res=RedirectResponse("/",status_code=status.HTTP_303_SEE_OTHER)
        res.set_cookie(key="token", value=access_token, httponly=True, max_age=3600)
        return res
    except ValidationError as e:

        print(e)
        back=RedirectResponse("/missmatch-error",status_code=status.HTTP_303_SEE_OTHER)
        back.set_cookie(key="email_cookie" ,value=email)
        return back
        
    
@app.get("/sign-out")
def sign_out(
):
    res=RedirectResponse("/")
    res.delete_cookie(key="token")
    return res



# #todo # #
# add more project to the home page
# if the user register take him to the loged in page and show them their accout
# add back buttons
# make every endpoint protected even the home page only leave login and register alone
# in the future try to put the register and the login in seperate containers to apply microservice
# add forget password button
# add the profile page