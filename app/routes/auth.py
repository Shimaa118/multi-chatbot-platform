from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.utils.auth import hash_password, verify_password, create_access_token

auth_router = APIRouter()

# Dummy in-memory user store (replace with real database in production)
users_db = {}

class User(BaseModel):
    username: str
    email: str
    password: str

@auth_router.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    users_db[user.username] = {"email": user.email, "password": hashed_password}
    return {"message": "User registered successfully"}

@auth_router.post("/login")
def login(username: str, password: str):
    user = users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": username})
    return {"access_token": token}    
