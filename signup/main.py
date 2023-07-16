# from fastapi import FastAPI
# from pydantic import BaseModel, EmailStr
# from register import hash_the_password
# app = FastAPI()


# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None


# class UserIn(UserBase):
#     password: str


# class UserOut(UserBase):
#     pass


# # class UserInDB(UserBase):
# #     hashed_password: str


# # def fake_password_hasher(raw_password: str):
# #     return "supersecret" + raw_password


# # def fake_save_user(user_in: UserIn):
# #     hashed_password = fake_password_hasher(user_in.password)
# #     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
# #     print("User saved! ..not really")
# #     return user_in_db


# @app.post("/register/")
# async def create_user(user_in: UserIn) -> UserBase:
#     hased=hash_the_password(user_in.password)
#     print(hased)
#     return user_in





import psycopg
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException,Depends,Body,Request,Form,status,Response,Cookie
from fastapi.responses import HTMLResponse,RedirectResponse,JSONResponse
from pydantic import BaseModel, EmailStr,constr
from passlib.hash import bcrypt
from hashing import hash_the_password
from hashing import verify_password
from dotenv import load_dotenv
import os
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import re
from pydantic import ValidationError,Field
from typing import Annotated

templates=Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


# using pydantic if you want to create an api without the any pages (htmls)
class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserIn(UserBase):
    password: str = Field(..., regex=password_regex)
    # @classmethod
    # def as_form(
    #     cls,
    #     password: str = Form(...),
    #     username: str = Form(...),
    #     email:EmailStr=Form(...)
    # ):
    #     return cls(password=password,username=username,email=email)


class UserOut(UserBase):
    pass


class For_login(BaseModel):
    username:str
    password:str
   

load_dotenv() 

PG_HOST=os.getenv('PG_HOST')
PG_DB = os.getenv('PG_DB')
PG_USER= os.getenv('PG_USER')
PG_PW = os.getenv('PG_PW')
PG_PORT=os.getenv('PG_PORT')

    
    

# Database connection configuration
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

# ... Rest of the code ...

# Endpoints
@app.get("/")
def main(request:Request):
    return templates.TemplateResponse("sign_up.html",{"request":request})



# user_in: UserIn, 
@app.post("/register", response_model=UserOut)
async def register(
    request:Request,
    conn = Depends(get_db),
    username:str=Form(...),
    password:str=Form(...),
    email:str=Form(...)
    ) -> UserOut:
    try:
        user_in=UserIn(username=username,email=email,password=password)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (user_in.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = hash_the_password(jsonable_encoder(user_in.password))
        
        cursor.execute(
            "INSERT INTO users (username, password_, email)"
            "VALUES (%s, %s, %s) RETURNING username, email",
            (user_in.username, hashed_password, user_in.email),
        )
        
        user_data = cursor.fetchone()
        conn.commit()
        print(user_data)
        
        
        return {
            "username":user_data[0],
            "email":user_data[1]
        }
            # cursor.execute("INSERT INTO student (name) VALUES (%s) RETURNING student_id", (student,))
    except ValidationError:
        error_msg="wrong"
        # return templates.TemplateResponse("error.html", {"request": request, "error_message": error_msg,"name":user_in.username}, status_code=status.HTTP_303_SEE_OTHER)
        response = RedirectResponse("/error", status_code=status.HTTP_303_SEE_OTHER)

        if user_in.username:
            response.set_cookie(key="saved_name", value=user_in.username)
        else:
            response.delete_cookie(key="saved_name")
            
        return response
    
@app.get("/error",response_class=HTMLResponse)
async def read_items(request: Request,saved_name:Annotated[str|None,Cookie()]=None):
    error_msg="wrong"
    return templates.TemplateResponse("error.html", {"request": request,"saved_name":saved_name,"error_message": error_msg})

    # return UserOut(
        #     username=user_data[0],
        #     email=user_data[1],
        # )

@app.post("/login")
async def login(
    conn = Depends(get_db),
    username:str=Form(...),
    password:str=Form(...)
                ):
    for_login=For_login(username=username,password=password)
    cursor = conn.cursor()
    
    # Retrieve user from the database based on the provided username
    cursor.execute("SELECT password_ FROM users WHERE username = %s", (for_login.username,))
    user_data = cursor.fetchone()
    
    if user_data:
        stored_hashed_password = user_data[0]
        
        if verify_password(for_login.password, stored_hashed_password):
            return {"message": "Login successful"}
    
    return {"msg":"error"}
