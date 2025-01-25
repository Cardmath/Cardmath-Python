import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
from database.auth.user import User, UserInDB, Subscription
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone
from auth.utils import get_password_hash
import os
import jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES = 60

def create_email_verification_token(email: str):
    logger.info("Creating email verification token for email: %s", email)
    payload = {
        "sub": email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY", "your_secret_key"), algorithm="HS256")

def verify_email_verification_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "your_secret_key"), algorithms=["HS256"])
        logger.info("Email verification token verified for email: %s", payload.get("sub"))
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired for email verification.")
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        logger.error("Invalid token for email verification.")
        raise HTTPException(status_code=400, detail="Invalid token")

def send_verification_email_link(email: str, verification_link: str):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    message = MIMEMultipart()
    message["From"] = smtp_email
    message["To"] = email
    message["Subject"] = "Cardmath - Email Verification Required"
    
    body = f"""
    <p>Hi,</p>
    <p>Thank you for registering with Cardmath! Please verify your email and set a password by clicking the link below:</p>
    <p><a href="{verification_link}">Verify your email and set a password</a></p>
    <p>If you did not register for this account, please ignore this email or contact support by replying to this email.</p>
    <p>Best regards,<br>The Cardmath Team</p>
    """
    message.attach(MIMEText(body, "html"))

    try:
        logger.info("Attempting to send verification email to %s", email)
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, email, message.as_string())
        logger.info("Verification email sent successfully to %s", email)
    except Exception as e:
        logger.error("Failed to send verification email to %s: %s", email, str(e))
        raise HTTPException(status_code=500, detail="Failed to send email")
    
def send_verification(email: str):
    token = create_email_verification_token(email)
    BASE_URL = "cardmath.ai" if os.getenv("ENVIRONMENT", "prod") == "prod" else "localhost:3000"
    verification_link = f"https://{BASE_URL}/registration-steps?token={token}"
    send_verification_email_link(email, verification_link)

async def handle_verification_link_clicked(token: str, db: Session):
    email = verify_email_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(UserInDB).filter(UserInDB.email == email).first()
    if not user:
        logger.warning("User not found for email: %s", email)
        raise HTTPException(status_code=404, detail="User not found")

    subscription = db.query(Subscription).filter(Subscription.user_id == user.id).first()
    if not subscription:
        logger.warning("Subscription not found for user ID: %s", user.id)
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription.status = 'verified-unpaid'
    db.commit()
    logger.info("Email verification completed for user: %s", email)
    return {"msg": "Email verified successfully"}

PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = 60

class PasswordResetForm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

class PasswordResetRequest(BaseModel):
    email: str

def create_password_reset_token(email: str):
    logger.info("Creating password reset token for email: %s", email)
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, os.getenv("SECRET_KEY", "your_secret_key"), algorithm="HS256")

def verify_password_reset_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "your_secret_key"), algorithms=["HS256"])
        logger.info("Password reset token verified for email: %s", payload.get("sub"))
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired for password reset.")
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        logger.error("Invalid token for password reset.")
        raise HTTPException(status_code=400, detail="Invalid token")

def send_reset_email(email: str, reset_link: str):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    message = MIMEMultipart()
    message["From"] = smtp_email
    message["To"] = email
    message["Subject"] = "Cardmath - Set Your Password!"
    
    body = f"""
    <p>Hi,</p>
    <p>Thank you for using Cardmath! To set your password, click the link below:</p>
    <p><a href="{reset_link}">Reset your password</a></p>
    <p>If you did not request a password reset, please ignore this email or contact support by relying to this email.</p>
    <p>Best regards,<br>Cardmath Support</p>
    """
    message.attach(MIMEText(body, "html"))

    try:
        logger.info("Attempting to send password reset email to %s", email)
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, email, message.as_string())
        logger.info("Password reset email sent successfully to %s", email)
    except Exception as e:
        logger.error("Failed to send password reset email to %s: %s", email, str(e))
        raise HTTPException(status_code=500, detail="Failed to send email")

def request_password_recovery(email: str, db: Session):
    user = db.query(UserInDB).filter(UserInDB.email == email).first()
    if not user:
        logger.warning("User not found for password recovery email: %s", email)
        raise HTTPException(status_code=404, detail="User not found")

    token = create_password_reset_token(email)
    reset_link = f"https://cardmath.ai/reset-password?token={token}"
    
    send_reset_email(email, reset_link)
    logger.info("Password reset link sent to %s", email)
    return {"msg": "Password reset link sent to the registered email address"}

async def reset_password(token: str, new_password: str, db: Session):
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user: UserInDB = db.query(UserInDB).filter(UserInDB.username == email).first()
    if not user:
        logger.warning("User not found for email: %s during password reset", email)
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)
    logger.info("Password reset successfully for email: %s", email)
    return {"msg": "Password has been reset successfully"}
