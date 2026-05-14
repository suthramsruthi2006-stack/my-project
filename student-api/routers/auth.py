from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from model.user import User   # ✅ FIXED (model, not models)
from utils.hashing import hash_password, verify_password
from utils.jwt import create_access_token

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


# ── REGISTER ─────────────────────────────────────────────────
@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)  # ✅ hashed properly
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"Account created for {user.username}"}


# ── LOGIN ─────────────────────────────────────────────────
@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    found = db.query(User).filter(User.username == user.username).first()

    # ✅ SAFE CHECK (prevents 500 error)
    if not found or not found.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ VERIFY PASSWORD
    if not verify_password(user.password, found.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ GENERATE TOKEN
    access_token = create_access_token(found.username)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }