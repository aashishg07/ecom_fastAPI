from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from pydantic import BaseModel, EmailStr
from typing import List
from .models import User
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

email_connection = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL =  False,
    USE_CREDENTIALS = True,
) 


class EmailSchema(BaseModel):
    email: List[EmailStr]


async def send_email(email: EmailSchema, instance: User):

    token_data = {
        "id": instance.id,
        "username": instance.username   
    }

    token = jwt.encode(token_data)


    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Email Verification</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f2f2f2;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
        <h1 style="color: #333333; text-align: center;">Email Verification</h1>
        <p style="color: #666666; line-height: 1.5; margin-bottom: 20px;">Dear User,</p>
        <p style="color: #666666; line-height: 1.5; margin-bottom: 20px;">Thank you for signing up! To verify your email address, please click the button below:</p>
        <a href="http://localhost:8000/verify/?token={token}" style="display: inline-block; background-color: #007bff; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-top: 20px;">Verify Email</a>
    </div>
    </body>
    </html>

    """


    message = MessageSchema(
        subject = "THIS IS THE TEST EMAIL VERIFICATION",
        recipients = email,
        body = template,
        subtype = "html"
    )

    fm = FastMail(email_connection)
    await fm.send_message(message=message)