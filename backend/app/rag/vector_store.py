"""
vector_store.py

Job of this file: everything related to the "RAG" (Retrieval-Augmented
Generation) part of the project.

Three responsibilities:
 1. Split resume text into small chunks
 2. Convert those chunks into embeddings (number vectors) and store them
    in ChromaDB
 3. Given a user's question, retrieve the most relevant chunks

Why chunk at all? A resume might be 500-1000 words. If we tried to search
whole-resume matches, we'd always get "the whole resume" as the result,
which isn't precise. Splitting into small chunks lets us fetch just the
"Projects" section when someone asks about projects, for example.
"""

import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ---- Configuration ----
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "data/chroma_db")
COLLECTION_NAME = "resume_collection"

# This model runs locally on CPU, is small (~80MB), and free —
# perfect for a fresher-level project since it needs no API key.
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Loaded once and reused everywhere (loading a model is slow, so we don't
# want to reload it on every single request).
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def get_vector_store() -> Chroma:
    """
    Connects to (or creates) our ChromaDB collection on disk.
    Called every time we need to read or write resume chunks.
    """
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=CHROMA_DB_PATH,
    )


def split_text_into_chunks(text: str) -> list[str]:
    """
    Breaks one long resume string into smaller overlapping pieces.

    chunk_size=500 characters keeps each chunk focused on one section
    (like "Projects" or "Skills").
    chunk_overlap=50 means consecutive chunks share a bit of text, so we
    don't accidentally cut a sentence in half and lose meaning.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    return splitter.split_text(text)


def store_resume_text(resume_text: str) -> int:
    """
    Takes the full resume text, splits it, embeds it, and saves it to
    ChromaDB.

    Returns the number of chunks stored (useful for the API response,
    so the frontend can show "12 sections indexed").
    """
    # Clear out any previous resume first — this project supports
    # ONE active resume at a time, keeping it simple for a fresher project.
    clear_resume_data()

    chunks = split_text_into_chunks(resume_text)

    vector_store = get_vector_store()

    # add_texts() automatically embeds each chunk and stores it in Chroma
    vector_store.add_texts(texts=chunks)

    return len(chunks)


def retrieve_relevant_chunks(question: str, top_k: int = 3) -> list[str]:
    """
    Given a user's question, finds the most relevant resume chunks.

    This is called by every agent (resume/career/interview) before asking
    the LLM to answer, so the AI always grounds its answer in the actual
    resume instead of making things up.
    """
    vector_store = get_vector_store()

    # similarity_search finds the chunks whose embeddings are "closest"
    # in meaning to the question's embedding
    results = vector_store.similarity_search(question, k=top_k)

    return [doc.page_content for doc in results]


def clear_resume_data() -> None:
    """
    Deletes all previously stored resume chunks.
    Called before storing a new resume, so old and new resumes never mix.
    """
    vector_store = get_vector_store()
    existing_ids = vector_store.get()["ids"]
    if existing_ids:
        vector_store.delete(ids=existing_ids)


def has_resume_data() -> bool:
    """
    Quick check used by GET /resume to tell the frontend whether a
    resume has already been uploaded and indexed.
    """
    vector_store = get_vector_store()
    existing_ids = vector_store.get()["ids"]
    return len(existing_ids) > 0
