from datetime import datetime, timedelta
from typing import Annotated
import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status,Form,Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel,EmailStr
import psycopg
from typing import Dict
from fastapi.responses import JSONResponse

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    


class UserInDB(User):
    hashed_password: str
    disables: bool | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# # get the username if its excting or not
def get_user(cursor, username: str):
    all=cursor.execute("SELECT hashed_password,username,email,disables FROM users WHERE username = %s", (username,))
    todos = [{"hashed_password": row[0], "username": row[1],"email":row[2],"disables":row[3]} for row in all.fetchall()]
    if todos:
        for todo in todos: 
            return UserInDB(**todo)
        
# check if the username and password match on the database or not
def authenticate_user(cursor, username: str, password: str):
    user = get_user(cursor, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWTError,TypeError,AttributeError):
        raise credentials_exception
    cursor=conn.cursor()
    user = get_user(cursor, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Assuming you have a function to get the database connection 'conn'
# def update_user_status(username: str, is_disabled: bool, conn):
#     cur = conn.cursor()
#     cur.execute("UPDATE users SET disables = %s WHERE username = %s", (is_disabled, username))
#     conn.commit()
#     cur.close()


# #no need to use User model here its only for hiting
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.disables:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/insert")
def insert(
    password:str,
    username:str,
    email:EmailStr,
    conn=Depends(get_db)
    ):
    hashed_password=get_password_hash(password)
    cur=conn.cursor()
    cur.execute("INSERT INTO users (hashed_password,username,email,disables) VALUES (%s,%s,%s,'True')",
                (hashed_password,username,email))
    conn.commit()
    return {"msg":"done"}

    

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    conn=Depends(get_db)
):
    cursor=conn.cursor()
    user = authenticate_user(cursor ,form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="token", value=access_token, httponly=True,max_age=1800)
    return response


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
