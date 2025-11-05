import os
import secrets
import string
import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, Field, validator

# Use environment variable for secret key in production
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable must be set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180

# Password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    expires_at: Optional[datetime] = None

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

def generate_password(length: int = 12) -> str:
    """Generate a cryptographically secure random password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token with optional custom expiration.
    
    Args:
        data (dict): Payload data to encode in the token
        expires_delta (Optional[timedelta]): Custom token expiration time
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    # Use provided expiration or default
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Add expiration to token payload
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    
    Args:
        token (str): JWT token to decode
    
    Returns:
        Optional[dict]: Decoded token payload or None if invalid
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


# Mailgun configuration
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN', 'modernai.mitrarobot.com')
MAILGUN_FROM_EMAIL = os.getenv('MAILGUN_FROM_EMAIL', 'noreply@modernai.mitrarobot.com')
MAILGUN_FROM_NAME = os.getenv('MAILGUN_FROM_NAME', 'Modern AI Pro')
BASE_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, text_content: str, html_content: Optional[str] = None) -> Dict[str, Any]:
    """
    Send an email using Mailgun API.
    
    Args:
        to_email (str): Recipient email address
        subject (str): Email subject
        text_content (str): Plain text content
        html_content (Optional[str]): HTML content (optional)
        
    Returns:
        Dict[str, Any]: API response
    """
    # For debugging purposes
    logger.info(f"Email configuration: MAILGUN_API_KEY exists: {bool(MAILGUN_API_KEY)}, MAILGUN_DOMAIN: {MAILGUN_DOMAIN}")
    
    if not MAILGUN_API_KEY:
        # Log the email content for development/testing
        logger.info(f"Would send email to: {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Content: {text_content}")
        return {"id": "development-mode", "message": "Email logged to console"}
    
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    auth = ("api", MAILGUN_API_KEY)
    data = {
        "from": f"{MAILGUN_FROM_NAME} <{MAILGUN_FROM_EMAIL}>",
        "to": [to_email],
        "subject": subject,
        "text": text_content
    }
    
    if html_content:
        data["html"] = html_content
    
    try:
        response = requests.post(url, auth=auth, data=data)
        response.raise_for_status()
        logger.info(f"Successfully sent email to {to_email} with subject: {subject}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send email: {str(e)}")
        # Fallback to logging the email for debugging
        logger.info(f"Would send email to: {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Content: {text_content}")
        
        # In development mode, don't throw errors for email failures
        if os.getenv('ENVIRONMENT', 'development') == 'development':
            return {"error": str(e), "message": "Email logged to console (development mode)"}
        else:
            # In production, we might want to raise the error or handle it differently
            return {"error": str(e)}

def send_verification_email(to_email: str, token: str, username: str) -> Dict[str, Any]:
    """
    Send an email verification link.
    
    Args:
        to_email (str): Recipient email address
        token (str): Verification token
        username (str): Username for personalization
        
    Returns:
        Dict[str, Any]: API response
    """
    verification_url = f"{BASE_URL}/login?verify={token}"
    
    subject = "Verify your email address for Modern AI Pro"
    
    text_content = f"""
    Hello {username},
    
    Thank you for registering with Modern AI Pro!
    
    Please verify your email address by clicking the link below:
    
    {verification_url}
    
    This link will expire in 48 hours.
    
    If you did not sign up for Modern AI Pro, please ignore this email.
    
    Best regards,
    The Modern AI Pro Team
    """
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #6b46c1; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .button {{ display: inline-block; background-color: #6b46c1; color: white; padding: 10px 20px; 
                      text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ font-size: 12px; color: #777; margin-top: 30px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Modern AI Pro</h2>
            </div>
            <div class="content">
                <p>Hello {username},</p>
                <p>Thank you for registering with Modern AI Pro!</p>
                <p>Please verify your email address by clicking the button below:</p>
                <p style="text-align: center;">
                    <a href="{verification_url}" class="button">Verify Email Address</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p>{verification_url}</p>
                <p>This link will expire in 48 hours.</p>
                <p>If you did not sign up for Modern AI Pro, please ignore this email.</p>
                <p>Best regards,<br>The Modern AI Pro Team</p>
            </div>
            <div class="footer">
                <p>© {datetime.now().year} Modern AI Pro. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(to_email, subject, text_content, html_content)

def send_password_reset_email(to_email: str, token: str, username: str) -> Dict[str, Any]:
    """
    Send a password reset link.
    
    Args:
        to_email (str): Recipient email address
        token (str): Reset token
        username (str): Username for personalization
        
    Returns:
        Dict[str, Any]: API response
    """
    reset_url = f"{BASE_URL}/login?token={token}"
    
    subject = "Reset your Modern AI Pro password"
    
    text_content = f"""
    Hello {username},
    
    We received a request to reset your password for Modern AI Pro.
    
    Please click the link below to reset your password:
    
    {reset_url}
    
    This link will expire in 24 hours.
    
    If you did not request a password reset, please ignore this email.
    
    Best regards,
    The Modern AI Pro Team
    """
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #6b46c1; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .button {{ display: inline-block; background-color: #6b46c1; color: white; padding: 10px 20px; 
                      text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ font-size: 12px; color: #777; margin-top: 30px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Modern AI Pro</h2>
            </div>
            <div class="content">
                <p>Hello {username},</p>
                <p>We received a request to reset your password for Modern AI Pro.</p>
                <p>Please click the button below to reset your password:</p>
                <p style="text-align: center;">
                    <a href="{reset_url}" class="button">Reset Password</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p>{reset_url}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you did not request a password reset, please ignore this email.</p>
                <p>Best regards,<br>The Modern AI Pro Team</p>
            </div>
            <div class="footer">
                <p>© {datetime.now().year} Modern AI Pro. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(to_email, subject, text_content, html_content)
