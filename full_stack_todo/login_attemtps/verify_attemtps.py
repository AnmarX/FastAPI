from fastapi import FastAPI, Request, HTTPException, Depends,Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from db_connection.connection import get_db





async def check_login_attempts(request:Request,conn=Depends(get_db)):
    cur=conn.cursor()
    # Can just get the email when the user enter it but i need to check first if its on the database or not
    email = request.json().get("email")
    if email:
        cur.execute("SELECT failed_attempts, suspended FROM login_attempts WHERE user_id = (SELECT user_id FROM users WHERE email = %s) FOR UPDATE", (email,))
        result = cur.fetchone()

        if result:
            failed_attempts, suspended = result
            if suspended:
                raise HTTPException(status_code=403, detail="Account is suspended. Try again later.")

            if failed_attempts >= 5:
                # Suspend the account
                cur.execute("UPDATE login_attempts SET suspended = TRUE WHERE user_id = (SELECT user_id FROM users WHERE email = %s)", (email,))
                conn.commit()
                raise HTTPException(status_code=403, detail="Account is suspended. Try again later.")

