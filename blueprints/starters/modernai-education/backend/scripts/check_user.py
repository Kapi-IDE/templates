"""
Check if a user exists in the database.
"""
import os
import sys
from sqlalchemy.orm import Session

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User, UserRoles

def check_user(username: str):
    """
    Check if a user exists in the database.
    
    Args:
        username: The username to check
    """
    db = SessionLocal()
    try:
        # Check if the user exists
        user = db.query(User).filter(User.username == username).first()
        
        if user:
            print(f"User '{username}' exists:")
            print(f"  - ID: {user.id}")
            print(f"  - Email: {user.email}")
            print(f"  - Role: {user.role}")
            print(f"  - Is Active: {user.is_active}")
            
            if user.role != UserRoles.admin:
                print("WARNING: This user is not an admin!")
        else:
            print(f"User '{username}' does not exist.")
            
    except Exception as e:
        print(f"Error checking user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check if a user exists")
    parser.add_argument("--username", required=True, help="Username to check")
    
    args = parser.parse_args()
    
    check_user(args.username)