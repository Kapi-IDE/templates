"""
Verify a user's password.
"""
import os
import sys
from sqlalchemy.orm import Session

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User
from app.auth_utils import verify_password

def check_password(username: str, password: str):
    """
    Check if a user's password is correct.
    
    Args:
        username: The username to check
        password: The password to verify
    """
    db = SessionLocal()
    try:
        # Check if the user exists
        user = db.query(User).filter(User.username == username).first()
        
        if user:
            print(f"User '{username}' exists.")
            is_valid = verify_password(password, user.hashed_password)
            print(f"Password verification result: {is_valid}")
            print(f"Hashed password in DB: {user.hashed_password}")
        else:
            print(f"User '{username}' does not exist.")
            
    except Exception as e:
        print(f"Error verifying password: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Verify a user's password")
    parser.add_argument("--username", required=True, help="Username to check")
    parser.add_argument("--password", required=True, help="Password to verify")
    
    args = parser.parse_args()
    
    check_password(args.username, args.password)