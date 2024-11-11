import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from database.auth.user import User, UserInDB  
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from auth.utils import get_password_hash
import os
import jwt

PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = 60

class PasswordResetForm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

class PasswordResetRequest(BaseModel):
    email: str

def create_password_reset_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY", "your_secret_key"), algorithm="HS256")

def verify_password_reset_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "your_secret_key"), algorithms=["HS256"])
        return payload.get("sub")  # Return email (sub) if token is valid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

def send_reset_email(email: str, reset_link: str):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    message = MIMEMultipart()
    message["From"] = smtp_email
    message["To"] = email
    message["Subject"] = "Password Reset Request"
    
    body = f"""
    <p>Hi,</p>
    <p>To reset your password, click the link below:</p>
    <p><a href="{reset_link}">Reset your password</a></p>
    <p>If you did not request a password reset, please ignore this email or contact support.</p>
    <p>Best regards,<br>CardMath Support Team</p>
    """
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, email, message.as_string())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to send email")

async def request_password_recovery(email: str, db: Session):
    # Find user by email
    user = db.query(UserInDB).filter(UserInDB.username == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create password reset token
    token = create_password_reset_token(email)
    reset_link = f"https://cardmath.ai/reset-password?token={token}"
    
    # Send reset email
    send_reset_email(email, reset_link)
    return {"msg": "Password reset link sent to the registered email address"}

async def reset_password(token: str, new_password: str, db: Session):
    # Verify token and retrieve the email
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Fetch the user by email
    user: UserInDB = db.query(UserInDB).filter(UserInDB.username == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update password
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)
    return {"msg": "Password has been reset successfully"}
