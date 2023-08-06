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



templates=Jinja2Templates(directory="templates")

app=FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

SECRET_KEY="0083d357bca59b41161f2016ab18fbb059fad45fdfd4673a6da25ac63c4a152f531f811efb47208ebc3ffeb6e7d5980c5a11444822e1127eeb1760b2527d794c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5


password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class User(BaseModel):
    email:EmailStr
    

class UserPassword(User):
    password_:str = Field(regex=password_regex)
    disables:bool
# class Dis(UserPassword):
#     disables:bool


class For_token_valid(BaseModel):
    email:EmailStr
    
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
        token_data=For_token_valid(email=payload)
    except (AttributeError,JWTError,TypeError):
        raise credentials_exception
    cursor=conn.cursor()
    user = get_user(cursor, email=token_data)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserPassword, Depends(get_current_user)]
):
    if not current_user.disables:
        raise HTTPException(status_code=400, detail="Inactive user")
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


@app.get("/login-page")
async def signup(
    request: Request
                 ):
    
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/logedin-page")
async def signup(
    request: Request,
    token:str=Cookie(None)
                 ):
    
    return templates.TemplateResponse("logged_in.html", {"request": request,"token":token})




# 4
@app.get("show-todos")
def show_todos():
    pass



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
    print(user)
    if not user:
        return credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # response = RedirectResponse("/logedin-page",status_code=status.HTTP_303_SEE_OTHER)
    # response.set_cookie(key="token", value=access_token, httponly=True,max_age=1800)
    # response.headers["Location"] += f"?token={access_token}"
    # return response

    redirect_url = f"/logedin-page?token={access_token}"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="token", value=access_token, httponly=True, max_age=1800)
    return response



# 3
@app.get("token")
def token():
    pass


# 5
@app.post("add-todo")
def add_todo():
    pass


# 6
@app.post("delete-todo")
def delete_todo():
    pass





