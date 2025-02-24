import bcrypt
from app.models.user_model import User
from app.repositories.user_repo import (
    get_user_by_username,
    create_user,
    delete_user_by_id,
)

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def check_password(password: str, hashed_password: str) -> bool:
    """Check if password matches stored hash"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def signup(username: str, password: str) -> User | dict:
    """Sign up a user with a hashed password"""
    if get_user_by_username(username):
        return {"error": "Username already exists"}

    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    return create_user(new_user)

def login(username: str, password: str) -> dict:
    """Validate user credentials"""
    user = get_user_by_username(username)

    if not user:
        return {"error": "User not found"}

    if check_password(password, user.password):
        return {"message": "Login successful"}

    return {"error": "Invalid credentials"}

def delete_user(user_id: int) -> dict:
    """Delete a user"""
    return delete_user_by_id(user_id)
