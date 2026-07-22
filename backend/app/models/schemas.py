"""
schemas.py

This file defines the "shape" of data that flows in and out of our API.
Pydantic automatically validates incoming JSON and rejects bad requests
with a clear error message, so we don't have to write manual checks like
"if 'question' not in data: raise error".
"""

from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    """
    What the frontend sends when the user asks a question in the chat box.

    Example JSON body:
    {
        "question": "What skills should I learn?"
    }
    """
    question: str


class ChatResponse(BaseModel):
    """
    What our backend sends back after the AI answers.

    'agent' tells the frontend which agent handled the question
    (resume / career / interview) so the UI can show a small badge/label.

    'sources' is a list of resume text chunks that were used to answer
    the question. This is useful for showing "AI used this part of your
    resume" in the UI, and it's a common RAG best-practice for transparency.
    """
    agent: str
    answer: str
    sources: List[str] = []


class UploadResponse(BaseModel):
    """
    What our backend sends back after a resume PDF is uploaded and processed.
    """
    message: str
    filename: str
    chunks_stored: int


class ResumeStatusResponse(BaseModel):
    """
    What our backend sends back when the frontend asks
    "has a resume already been uploaded?" (GET /resume).
    """
    resume_uploaded: bool
    filename: str | None = None
