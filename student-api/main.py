import os

from dotenv import load_dotenv

# ✅ LOAD .env FIRST
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# Import routers AFTER loading .env
from routers import auth, students, ai

import model.user
from model.students import Student


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI app
app = FastAPI(
    title="Student Management API",
    version="1.0.0",
    description="API for managing students and authentication"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    students.router,
    prefix="/api/v1/students",
    tags=["Students"]
)

app.include_router(
    ai.router,
    prefix="/api/v1/ai",
    tags=["AI"]
)


# Root endpoint
@app.get("/")
def root():
    return {"message": "Student API is running"}


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Startup event
@app.on_event("startup")
def startup_event():
    print("🚀 Server started successfully")

    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key:
        print("✅ GEMINI_API_KEY loaded")
    else:
        print("❌ GEMINI_API_KEY missing")