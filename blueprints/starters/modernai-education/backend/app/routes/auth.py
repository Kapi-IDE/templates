import os
import secrets
from fastapi import Request, HTTPException, Security, status, Depends, APIRouter, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, Dict
import logging

from app.database import get_db
from app.models.user import User as DBUser, UserRoles, SubscriptionTier
from app.auth_utils import (
    SECRET_KEY, 
    ALGORITHM, 
    get_password_hash, 
    verify_password,
    send_verification_email,
    send_password_reset_email
)
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory token storage (would use Redis or database in production)
reset_tokens: Dict[str, Dict] = {}

# Get the welcome code from environment variable
WELCOME_CODE = os.getenv("WELCOME_CODE", "MODERN-AI-PRO-BETA")

# Pydantic models for validation
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    welcome_code: str = Field(...)
    
    @validator('username')
    def username_must_be_valid(cls, v):
        if not v.isalnum():
            raise ValueError('Username must contain only alphanumeric characters')
        return v
        
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
    
class EmailVerificationRequest(BaseModel):
    token: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

@router.get("/test")
async def test_auth():
    return {"message": "Auth route works"}

# Email sending functions have been moved to auth_utils.py

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Register a new user with welcome code validation and email verification
    """
    # Check if welcome code is valid
    if user_data.welcome_code != WELCOME_CODE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid welcome code",
            headers={"X-Error": "invalid_welcome_code"},
        )
    
    # Check if username already exists
    if db.query(DBUser).filter(DBUser.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if db.query(DBUser).filter(DBUser.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    # Generate verification token
    verification_token = secrets.token_urlsafe(32)
    
    new_user = DBUser(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password,
        role=UserRoles.student,
        subscription_tier=SubscriptionTier.free,
        subscription_start_date=datetime.utcnow(),
        is_active=True,
        last_active_date=datetime.utcnow(),
        # Email verification fields
        email_verified=False,
        email_verification_token=verification_token,
        email_verification_sent_at=datetime.utcnow()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send verification email asynchronously
    background_tasks.add_task(
        send_verification_email, 
        new_user.email, 
        verification_token,
        new_user.username
    )
    
    return {
        "message": "User registered successfully. Please verify your email to activate your account.",
        "username": new_user.username,
        "email": new_user.email,
        "user_id": new_user.id,
        "email_verified": False
    }

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Initiates password reset process by generating a token and sending an email
    """
    # Find user by email
    user = db.query(DBUser).filter(DBUser.email == request.email).first()
    
    # Always return success even if email not found (security best practice)
    if not user:
        logger.info(f"Password reset requested for non-existent email: {request.email}")
        return {"message": "If your email is registered, you will receive a password reset link"}
    
    # Generate a secure token
    reset_token = secrets.token_urlsafe(32)
    
    # Store token with user info and expiration (24 hours)
    reset_tokens[reset_token] = {
        "user_id": user.id,
        "email": user.email,
        "expires": datetime.utcnow() + timedelta(hours=24)
    }
    
    # Send email asynchronously
    background_tasks.add_task(
        send_password_reset_email, 
        user.email, 
        reset_token,
        user.username
    )
    
    return {"message": "If your email is registered, you will receive a password reset link"}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Resets user password using a valid token
    """
    # Validate token
    token_data = reset_tokens.get(request.token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )
    
    # Check token expiration
    if datetime.utcnow() > token_data["expires"]:
        # Remove expired token
        reset_tokens.pop(request.token, None)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired"
        )
    
    # Get user
    user = db.query(DBUser).filter(DBUser.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    # Update password
    user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    
    # Remove used token
    reset_tokens.pop(request.token, None)
    
    return {"message": "Password has been reset successfully"}

@router.post("/verify-email")
async def verify_email(request: EmailVerificationRequest, db: Session = Depends(get_db)):
    """
    Verifies a user's email using the token sent during registration
    """
    # Find user with the verification token
    user = db.query(DBUser).filter(
        DBUser.email_verification_token == request.token
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )
    
    # Check if already verified
    if user.email_verified:
        return {"message": "Email already verified", "email": user.email}
    
    # Check token age (48 hours validity)
    token_age = datetime.utcnow() - user.email_verification_sent_at
    if token_age.total_seconds() > 48 * 3600:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired. Please request a new one."
        )
    
    # Mark email as verified
    user.email_verified = True
    user.email_verification_token = None  # Clear token after use
    db.commit()
    
    return {
        "message": "Email verified successfully",
        "email": user.email,
        "username": user.username
    }

@router.post("/resend-verification")
async def resend_verification(
    request: ForgotPasswordRequest, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    """
    Resends the email verification link
    """
    # Find user by email
    user = db.query(DBUser).filter(DBUser.email == request.email).first()
    
    # Check if user exists and email not verified yet
    if not user:
        # Don't reveal if email exists or not
        return {"message": "If your email is registered, a verification link will be sent."}
    
    if user.email_verified:
        return {"message": "Your email is already verified."}
    
    # Generate new verification token
    verification_token = secrets.token_urlsafe(32)
    user.email_verification_token = verification_token
    user.email_verification_sent_at = datetime.utcnow()
    
    db.commit()
    
    # Send verification email asynchronously
    background_tasks.add_task(
        send_verification_email, 
        user.email, 
        verification_token,
        user.username
    )
    
    return {"message": "If your email is registered, a verification link will be sent."}


def check_authentication(token: str = Security(oauth2_scheme)):
    """
    Validates JWT token from Authorization header.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
