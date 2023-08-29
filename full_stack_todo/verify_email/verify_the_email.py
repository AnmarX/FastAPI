import smtplib
from dotenv import load_dotenv
import os
import socket
import datetime as dt

load_dotenv() 
email_for_msg=os.getenv('email_for_msg')
email_pass=os.getenv('email_pass')
# to_email=os.getenv('to_email')

# gmail : smtp.gmail.com
# hotmail : smtp.live.com
# yahoo : smtp.mail.yahoo.com

# first create object of the email use with to close the connection after sending the email 
with smtplib.SMTP("smtp.gmail.com",587) as connection:
    # securing the email from the man in the middle by encrypting the email (TLS) Transport Layer Security 
    connection.starttls()  
    # the password is from you google account to allow signing in your google account so you can send emails
    connection.login(user=email_for_msg,password=email_pass)
    # send email method 1-(first the sender) 2-(then the resevier) 3-(the message)
    connection.sendmail(
        from_addr=email_for_msg,
        to_addrs="vibofag923@stypedia.com",
        msg="Subject:from python\n\nThis is the body of my email."
        )
    # no need for the line before the close() because we are using (with)
    # connection.close()
