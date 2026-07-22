"""
resume_agent.py

Job of this file: answer questions ABOUT the resume itself.
Examples: "Summarize my resume", "Improve my resume", "What skills do I have?",
"Explain my projects".

Every agent in this project follows the SAME pattern:
  1. Retrieve relevant resume chunks from ChromaDB (RAG step)
  2. Build a prompt that includes those chunks + the user's question
  3. Ask the LLM to answer, using ONLY the given resume context
  4. Return the answer text + the source chunks used
"""

from app.rag.vector_store import retrieve_relevant_chunks
from app.agents.llm_client import llm

RESUME_AGENT_SYSTEM_PROMPT = """You are a professional resume reviewer helping a
fresher (entry-level job seeker) improve their resume.

Rules:
- Only use the resume content given below. Do not invent experience or skills
  that aren't there.
- Be specific and practical. Fresher resumes are usually short, so give
  concrete, actionable suggestions.
- If the resume context doesn't contain enough information to answer,
  say so honestly instead of guessing.
"""


def run_resume_agent(question: str) -> dict:
    """
    Handles resume-related questions.

    Returns a dict with 'answer' and 'sources' so the graph/route layer
    can build the final ChatResponse.
    """
    # Step 1: RAG retrieval - get the resume chunks most related to the question
    relevant_chunks = retrieve_relevant_chunks(question, top_k=4)
    resume_context = "\n---\n".join(relevant_chunks)

    # Step 2: build the full prompt for the LLM
    user_prompt = f"""Resume context:
{resume_context}

Question: {question}

Answer the question using only the resume context above."""

    # Step 3: call the LLM
    response = llm.invoke([
        ("system", RESUME_AGENT_SYSTEM_PROMPT),
        ("human", user_prompt),
    ])

    return {
        "answer": response.content,
        "sources": relevant_chunks,
    }
    
def stream_resume_agent(question: str):
    """
    Same as run_resume_agent(), but STREAMS the answer token-by-token
    instead of waiting for the full response.
    """
    relevant_chunks = retrieve_relevant_chunks(question, top_k=4)
    resume_context = "\n---\n".join(relevant_chunks)

    user_prompt = f"""Resume context:
{resume_context}

Question: {question}

Answer the question using only the resume context above."""

    for chunk in llm.stream([
        ("system", RESUME_AGENT_SYSTEM_PROMPT),
        ("human", user_prompt),
    ]):
        if chunk.content:
            yield {"type": "chunk", "text": chunk.content}

    yield {"type": "sources", "sources": relevant_chunks}
