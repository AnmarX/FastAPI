from fastapi import FastAPI,Form,Depends,status,Cookie
from pydantic import BaseModel,EmailStr,validator,ValidationError
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from db_connection.connection import get_db
from pydantic.fields import Field
from fastapi.exceptions import HTTPException
from hashing import hash_the_password,verify_password
from fastapi.responses import RedirectResponse,Response
from typing import Annotated


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

class Dis(UserPassword):
    disables:bool
    
    # Pydantic validator to set disables to True if not provided by the user
    # @validator('disables', pre=True, always=True)
    # def set_disables(cls, v):
    #     return v if v is not None else True
   


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

@app.get("/logged")
async def signup(
    request: Request
                 ):
    return templates.TemplateResponse("logged_in.html", {"request": request})


@app.get("/log-in")
async def signup(
    request: Request
                 ):
    return templates.TemplateResponse("login.html", {"request": request})



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
        user_in= UserPassword(email=email,password_=apass)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (user_in.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="email already exists")
        
        # cursor.execute("SELECT * FROM users WHERE email = %s", (user_in.email,))
        # if cursor.fetchone():
        #     raise HTTPException(status_code=400, detail="Email already exists")
        
        hashed_password = hash_the_password(user_in.password_)
        # cur.execute("INSERT INTO users (hashed_password,username,email,disables) VALUES (%s,%s,%s,'True')",
        #         (hashed_password,username,email))

        cursor.execute(
            "INSERT INTO users (email, password_,disables)"
            "VALUES (%s, %s,'True') RETURNING email",
            (user_in.email, hashed_password),
        )
        
        user_data = cursor.fetchone()
        conn.commit()
        print(user_data)

    except ValidationError:
       
        back=RedirectResponse("/missmatch-error",status_code=status.HTTP_303_SEE_OTHER)
        back.set_cookie(key="email_cookie" ,value=email)
        return back
        
    
         

    
    

# 2
@app.post("/login")
def login():
    pass

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





