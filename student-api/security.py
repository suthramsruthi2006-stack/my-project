from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "my-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()

users_db = []

class UserData(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    username = verify_access_token(token)

    for user in users_db:
        if user["username"] == username:
            return user

    raise HTTPException(status_code=401, detail="User not found")

@app.post("/register", status_code=201)
def register(user: UserData):
    for u in users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already taken")

    new_user = {
        "id": len(users_db) + 1,
        "username": user.username,
        "hashed_password": hash_password(user.password)
    }

    users_db.append(new_user)

    return {"message": "Registered successfully"}

@app.post("/login")
def login(user: UserData):
    found_user = None

    for u in users_db:
        if u["username"] == user.username:
            found_user = u
            break

    if not found_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, found_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "username": current_user["username"]
    }

@app.get("/dashboard")
def dashboard(current_user=Depends(get_current_user)):
    return {
        "message": f"Welcome {current_user['username']}",
        "data": "This is protected data"
    }