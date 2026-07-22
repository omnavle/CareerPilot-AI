"""
main.py

Job of this file: the entrypoint of the backend. This is the file you run
to start the server (`uvicorn app.main:app --reload`).

It does three things:
  1. Loads environment variables from .env
  2. Creates the FastAPI app and enables CORS (so the React frontend,
     running on a different port, is allowed to call this API)
  3. Registers our two route files (resume, chat) under the app
"""

from dotenv import load_dotenv
load_dotenv()  # must run before other modules read os.getenv(), so do it first

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import resume, chat

app = FastAPI(
    title="CareerPilot AI",
    description="An AI-powered resume and career coach.",
    version="1.0.0",
)

# Allow the React frontend (Vite dev server, usually on localhost:5173)
# to make requests to this API. Without this, the browser blocks the
# requests due to CORS security rules.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register our route files. Each router already defines its own paths
# (/upload, /resume, /chat), so we don't add a prefix here.
app.include_router(resume.router, tags=["Resume"])
app.include_router(chat.router, tags=["Chat"])


@app.get("/")
async def root():
    """Simple health-check endpoint to confirm the server is running."""
    return {"status": "CareerPilot AI backend is running"}
