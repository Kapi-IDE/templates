
from app.database import SessionLocal
from sqlalchemy.orm import Session
import string
import secrets
import os
import sys
from passlib.context import CryptContext
from app.models.user import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_random_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_user(first_name: str, last_name: str, email: str, role: str, db: Session = SessionLocal()):
    # Check if role is in Enum("student", "teacher", "admin", "bd")
    if role not in ["student", "teacher", "admin", "bd"]:
        print("Role must be one of: student, teacher, admin, bd")
        return

    # Check if first_name and last_name are not empty
    if not first_name or not last_name:
        print("First name and last name must not be empty.")
        return

    # Check if email is valid, do a regex check
    if not email or not "@" in email:
        print("Email must not be empty.")
        return

    # Check if user already exists
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        print("An account with this email already exists.")
        return

    username = f"{first_name}.{last_name}".lower()
    password = generate_random_password()
    hashed_password = pwd_context.hash(password)

    new_admin = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        hashed_password=hashed_password,
        role=role
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    print(f"""Account created:\nUsername: {
          username}\nPassword: {password}""")


if __name__ == "__main__":
    print("Creating user...")
    if len(sys.argv) != 5:
        print("Usage: create_user.py <first_name> <last_name> <email> <role>")
        sys.exit(1)

    first_name, last_name, email, role = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    create_user(first_name, last_name, email, role)
