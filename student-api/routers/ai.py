 # routers/ai.py

import os

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Literal

from google import genai
from google.genai import types

from dependencies import get_current_user


# ======================================================
# Router
# ======================================================

# IMPORTANT:
# DO NOT ADD prefix="/ai" HERE
# main.py already adds:
# prefix="/api/v1/ai"

router = APIRouter(
    tags=["AI"]
)


# ======================================================
# Gemini Setup
# ======================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing"
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)
MODEL_NAME = "gemini-2.5-flash"
GENERATION_CONFIG = types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=512,
)


# ======================================================
# System Prompt
# ======================================================

SYSTEM_CONTEXT = (
    "You are a helpful Python programming assistant for students. "
    "Answer questions about Python, FastAPI, React, SQLite, and AI. "
    "Keep answers beginner friendly and under 200 words."
)


# ======================================================
# Session Management
# ======================================================

# Stores user chat sessions
chat_sessions = {}


def get_or_create_session(user_id: int):

    if user_id not in chat_sessions:

        chat_sessions[user_id] = client.chats.create(
            model=MODEL_NAME,
            history=[
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": SYSTEM_CONTEXT
                        }
                    ]
                },
                {
                    "role": "model",
                    "parts": [
                        {
                            "text": "Ready to help."
                        }
                    ]
                },
            ]
        )

    return chat_sessions[user_id]


# ======================================================
# Chat Schemas
# ======================================================

class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=1000
    )


class ChatResponse(BaseModel):
    reply: str


# ======================================================
# Chat Endpoint
# ======================================================

@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat_with_ai(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):

    try:

        session = get_or_create_session(
            current_user.id
        )

        response = session.send_message(
            request.message
        )

        return ChatResponse(
            reply=response.text.strip()
        )

    except Exception as e:

        print("FULL GEMINI ERROR:")
        print(repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ======================================================
# Reset Chat Endpoint
# ======================================================

@router.delete(
    "/chat/reset",
    status_code=204
)
def reset_chat(
    current_user=Depends(get_current_user)
):

    chat_sessions.pop(
        current_user.id,
        None
    )

    return Response(
        status_code=204
    )


# ======================================================
# Summarize Schemas
# ======================================================

class SummarizeRequest(BaseModel):
    text: str = Field(
        min_length=20,
        max_length=5000
    )


class SummarizeResponse(BaseModel):
    summary: str


# ======================================================
# Summarize Endpoint
# ======================================================

@router.post(
    "/summarize",
    response_model=SummarizeResponse
)
def summarize_text(
    request: SummarizeRequest,
    current_user=Depends(get_current_user),
):

    prompt = (
        f"Summarize this text:\n\n"
        f"{request.text}"
    )

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=GENERATION_CONFIG,
        )

        return SummarizeResponse(
            summary=response.text.strip()
        )

    except Exception as e:

        print("SUMMARIZE ERROR:")
        print(repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ======================================================
# Explain Schemas
# ======================================================

class ExplainRequest(BaseModel):
    topic: str
    level: Literal[
        "beginner",
        "intermediate",
        "expert"
    ] = "beginner"


class ExplainResponse(BaseModel):
    explanation: str


# ======================================================
# Explain Endpoint
# ======================================================

@router.post(
    "/explain",
    response_model=ExplainResponse
)
def explain_topic(
    request: ExplainRequest,
    current_user=Depends(get_current_user),
):

    prompt = (
        f"Explain {request.topic} "
        f"for a {request.level} programmer. "
        f"Use simple language."
    )

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=GENERATION_CONFIG,
        )

        return ExplainResponse(
            explanation=response.text.strip()
        )

    except Exception as e:

        print("EXPLAIN ERROR:")
        print(repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )