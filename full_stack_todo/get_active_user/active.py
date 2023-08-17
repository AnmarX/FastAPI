

from fastapi import Depends,status,Cookie
from pydantic import BaseModel,EmailStr
from db_connection.connection import get_db
from pydantic.fields import Field
from fastapi.exceptions import HTTPException
from hashing import hash_the_password,verify_password
from typing import Annotated
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY=os.getenv("secret_key")
ALGORITHM=os.getenv("ALGORITHM")


ACCESS_TOKEN_EXPIRE_MINUTES = 5


password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


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
   





def get_user(email,cur):
    all=cur.execute("SELECT email,password_,disables,user_id FROM users WHERE email = %s", (email,))
    get_user_info=[{"email":row[0],"password_":row[1],"disables":row[2],"user_id":row[3]}for row in all.fetchall()]
    if get_user_info:
        for user in get_user_info:
            return for_id(**user)

def authenticate_user(cur,email,password):
    user=get_user(email,cur)
    print(user)
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
    current_user: Annotated[for_id, Depends(get_current_user)]
):
    try:
        if not current_user.disables:
            raise HTTPException(status_code=400, detail="Inactive user")
    except AttributeError:
        return False


    return current_user
