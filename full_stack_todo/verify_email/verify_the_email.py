import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

email_for_msg = os.getenv('email_for_msg')
email_pass = os.getenv('email_pass')

def send_html_email():
    # Create an HTML email message
    msg = MIMEMultipart()
    msg['From'] = email_for_msg
    msg['To'] = "recipient@example.com"
    msg['Subject'] = "HTML Email with Link Example"

    # HTML content with a hyperlink
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>This is an HTML Email with a Link</h1>
        <p>Hello, <strong>world</strong>! Click the link below:</p>
        <p><a href="https://www.example.com">Visit Example.com</a></p>
    </body>
    </html>
    """

    # Attach the HTML content to the email message
    msg.attach(MIMEText(html_content, 'html'))

    # Create an SMTP connection and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=email_for_msg, password=email_pass)
        connection.sendmail(email_for_msg, "anythingcpit@gmail.com", msg.as_string())


if __name__=="__main__":
    send_html_email()




# import smtplib
# from dotenv import load_dotenv
# import os
# import socket
# import datetime as dt

# load_dotenv() 
# email_for_msg=os.getenv('email_for_msg')
# email_pass=os.getenv('email_pass')
# # to_email=os.getenv('to_email')

# # gmail : smtp.gmail.com
# # hotmail : smtp.live.com
# # yahoo : smtp.mail.yahoo.com
# def test_email():
# # first create object of the email use with to close the connection after sending the email 
#     with smtplib.SMTP("smtp.gmail.com",587) as connection:
#         # securing the email from the man in the middle by encrypting the email (TLS) Transport Layer Security 
#         connection.starttls()  
#         # the password is from you google account to allow signing in your google account so you can send emails
#         connection.login(user=email_for_msg,password=email_pass)
#         # send email method 1-(first the sender) 2-(then the resevier) 3-(the message)
#         connection.sendmail(
#             from_addr=email_for_msg,
#             to_addrs="anythingcpit@gmail.com",
#             msg="Subject:from python\n\nThis is the body of my email."
#             )
#     # no need for the line before the close() because we are using (with)
#     # connection.close()
