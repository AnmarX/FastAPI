
from dotenv import load_dotenv
import psycopg
import os

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
