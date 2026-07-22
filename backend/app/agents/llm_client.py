"""
llm_client.py

Job of this file: create ONE shared connection to the Groq LLM that all
three agents (resume, career, interview) reuse.

Why a separate file instead of putting this in each agent?
If we ever change the model name, temperature, or switch providers, we
change it here ONCE instead of in three different files.
"""

import os
from langchain_groq import ChatGroq

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# temperature=0.3 keeps answers mostly factual and consistent, while still
# allowing a little natural variation in phrasing - good for career advice.
llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
)
