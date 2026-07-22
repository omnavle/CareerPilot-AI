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
