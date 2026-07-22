from app.rag.vector_store import retrieve_relevant_chunks
from app.agents.llm_client import llm

CAREER_AGENT_SYSTEM_PROMPT = """You are a career coach helping a fresher
(entry-level job seeker) plan their career based on their resume.

Rules:
- Base your advice on the resume context given below - look at their
  current skills and projects before suggesting what to learn next.
- Keep suggestions realistic for a fresher (don't assume years of experience).
- When giving a roadmap, structure it clearly (e.g. by week or by topic).
- If the resume context doesn't contain enough information to answer,
  say so honestly instead of guessing.
"""


def run_career_agent(question: str) -> dict:
    """
    Handles career-guidance questions.
    Returns a dict with 'answer' and 'sources'.
    """
    relevant_chunks = retrieve_relevant_chunks(question, top_k=4)
    resume_context = "\n---\n".join(relevant_chunks)

    user_prompt = f"""Resume context:
{resume_context}

Question: {question}

Give career advice based on the resume context above."""

    response = llm.invoke([
        ("system", CAREER_AGENT_SYSTEM_PROMPT),
        ("human", user_prompt),
    ])

    return {
        "answer": response.content,
        "sources": relevant_chunks,
    }

def stream_career_agent(question: str):
    """
    Streaming version of run_career_agent().
    """
    relevant_chunks = retrieve_relevant_chunks(question, top_k=4)
    resume_context = "\n---\n".join(relevant_chunks)

    user_prompt = f"""Resume context:
{resume_context}

Question: {question}

Give career advice based on the resume context above."""

    for chunk in llm.stream([
        ("system", CAREER_AGENT_SYSTEM_PROMPT),
        ("human", user_prompt),
    ]):
        if chunk.content:
            yield {"type": "chunk", "text": chunk.content}

    yield {"type": "sources", "sources": relevant_chunks}