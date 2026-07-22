"""
interview_agent.py

Job of this file: generate INTERVIEW QUESTIONS based on the resume.
Examples: "Generate interview questions", "Ask me technical questions",
"What HR questions might I get?", "Ask me about my projects".

Same pattern as the other two agents: retrieve resume context -> prompt -> LLM.
"""

from app.rag.vector_store import retrieve_relevant_chunks
from app.agents.llm_client import llm

INTERVIEW_AGENT_SYSTEM_PROMPT = """You are an interviewer preparing a fresher
(entry-level job seeker) for job interviews, based on their resume.

Rules:
- Generate questions based on the actual skills and projects in the resume
  context below - don't ask about technologies that aren't mentioned.
- Cover a mix of question types when relevant: technical questions,
  HR/behavioral questions, and project-specific questions.
- Organize your answer under clear headings so it's easy to read.
- If the resume context doesn't contain enough information to answer,
  say so honestly instead of guessing.
"""


def run_interview_agent(question: str) -> dict:
    """
    Handles interview-question-generation requests.
    Returns a dict with 'answer' and 'sources'.
    """
    relevant_chunks = retrieve_relevant_chunks(question, top_k=4)
    resume_context = "\n---\n".join(relevant_chunks)

    user_prompt = f"""Resume context:
{resume_context}

Request: {question}

Generate interview questions based on the resume context above."""

    response = llm.invoke([
        ("system", INTERVIEW_AGENT_SYSTEM_PROMPT),
        ("human", user_prompt),
    ])

    return {
        "answer": response.content,
        "sources": relevant_chunks,
    }

def stream_interview_agent(question: str):
    """
    Streaming version of run_interview_agent().
    """
    relevant_chunks = retrieve_relevant_chunks(question, top_k=4)
    resume_context = "\n---\n".join(relevant_chunks)

    user_prompt = f"""Resume context:
{resume_context}

Request: {question}

Generate interview questions based on the resume context above."""

    for chunk in llm.stream([
        ("system", INTERVIEW_AGENT_SYSTEM_PROMPT),
        ("human", user_prompt),
    ]):
        if chunk.content:
            yield {"type": "chunk", "text": chunk.content}

    yield {"type": "sources", "sources": relevant_chunks}