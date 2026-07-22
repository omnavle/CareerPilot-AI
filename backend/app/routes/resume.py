import os
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.parser.pdf_parser import extract_text_from_pdf
from app.rag.vector_store import store_resume_text, has_resume_data
from app.models.schemas import UploadResponse, ResumeStatusResponse

router = APIRouter()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "data/uploads")

# Keep track of the currently uploaded filename in memory.
# This is fine for a simple fresher-level, single-user project.
# (A production app would store this in a real database instead.)
current_resume_filename: str | None = None


@router.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Accepts a PDF file, saves it to disk, extracts its text, and stores
    the text as embeddings in ChromaDB.
    """
    global current_resume_filename

    # Step 1: basic validation - only accept PDFs
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Step 2: save the uploaded file to disk
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    file_bytes = await file.read()
    with open(file_path, "wb") as saved_file:
        saved_file.write(file_bytes)

    # Step 3: extract plain text from the PDF
    resume_text = extract_text_from_pdf(file_path)

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract any text from this PDF. It might be a scanned image.",
        )

    # Step 4: chunk + embed + store in ChromaDB
    chunks_stored = store_resume_text(resume_text)

    current_resume_filename = file.filename

    return UploadResponse(
        message="Resume uploaded and indexed successfully.",
        filename=file.filename,
        chunks_stored=chunks_stored,
    )


@router.get("/resume", response_model=ResumeStatusResponse)
async def get_resume_status():
    """
    Lets the frontend check whether a resume is already uploaded,
    e.g. to decide whether to show the Chat page or redirect to Upload.
    """
    return ResumeStatusResponse(
        resume_uploaded=has_resume_data(),
        filename=current_resume_filename,
    )
