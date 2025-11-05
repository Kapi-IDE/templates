"""
Create an admin user for the ModernAI Pro platform.

This script creates a new admin user or updates an existing user to have admin role.
"""
import os
import sys
from sqlalchemy.orm import Session

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User, UserRoles, SubscriptionTier
from app.auth_utils import get_password_hash

def create_admin_user(
    username: str, 
    email: str, 
    password: str, 
    first_name: str = "Admin", 
    last_name: str = "User"
):
    """
    Create a new admin user or update an existing user to admin role.
    
    Args:
        username: The username for the admin
        email: The email for the admin
        password: The password for the admin
        first_name: The first name for the admin
        last_name: The last name for the admin
    """
    db = SessionLocal()
    try:
        # Check if the user already exists
        user = db.query(User).filter(User.username == username).first()
        
        if user:
            print(f"User '{username}' already exists. Updating to admin role.")
            user.role = UserRoles.admin
            user.hashed_password = get_password_hash(password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = True
        else:
            print(f"Creating new admin user '{username}'.")
            user = User(
                username=username,
                email=email,
                hashed_password=get_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                role=UserRoles.admin,
                subscription_tier=SubscriptionTier.premium,
                is_active=True
            )
            db.add(user)
        
        db.commit()
        print(f"Admin user '{username}' successfully created/updated.")
        
    except Exception as e:
        db.rollback()
        print(f"Error creating/updating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create or update an admin user")
    parser.add_argument("--username", default="admin", help="Admin username")
    parser.add_argument("--password", required=True, help="Admin password")
    parser.add_argument("--email", required=True, help="Admin email")
    parser.add_argument("--first-name", default="Admin", help="Admin first name")
    parser.add_argument("--last-name", default="User", help="Admin last name")
    
    args = parser.parse_args()
    
    create_admin_user(
        username=args.username,
        email=args.email,
        password=args.password,
        first_name=args.first_name,
        last_name=args.last_name
    )