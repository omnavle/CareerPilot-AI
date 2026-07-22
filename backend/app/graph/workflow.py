"""
workflow.py

Job of this file: wire together our 4 nodes into a LangGraph graph.

Graph shape (exactly as specified in the project spec):

    User Question
         |
         v
    Router Node  ---> classifies the question
         |
         v
  -------------------------
  |          |            |
  v          v            v
Resume     Career      Interview
Agent      Agent       Agent
  |          |            |
  -------------------------
         |
         v
    Final Answer

We use LangGraph's "conditional edge" feature: the Router node doesn't
generate an answer itself, it just decides which agent node runs next.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

from app.agents.resume_agent import run_resume_agent
from app.agents.career_agent import run_career_agent
from app.agents.interview_agent import run_interview_agent
from app.agents.llm_client import llm


class GraphState(TypedDict):
    """
    This is the "shared notebook" that gets passed between nodes.
    Each node reads from it and writes back into it.

    question -> the user's original question (set at the start)
    agent    -> which agent the router picked ("resume"/"career"/"interview")
    answer   -> the final text answer (set by whichever agent runs)
    sources  -> resume chunks used to generate the answer
    """
    question: str
    agent: str
    answer: str
    sources: list[str]


ROUTER_SYSTEM_PROMPT = """You are a router that classifies a user's question
into exactly ONE category. Reply with ONLY one word, nothing else.

Categories:
- "resume"    -> questions about the resume itself: summarizing it, improving
                 it, extracting skills, explaining projects listed on it.
- "career"    -> questions about career guidance: skill gaps, what to learn,
                 project recommendations, learning roadmaps, career advice.
- "interview" -> questions asking to generate or practice interview questions
                 (technical, HR, or project-specific).

Reply with only one of: resume, career, interview
"""


def classify_question(question: str) -> str:
    """
    Shared classification logic used by BOTH:
      - router_node() below (for the normal, non-streaming /chat endpoint)
      - routes/chat.py's streaming endpoint (/chat/stream)
    """
    response = llm.invoke([
        ("system", ROUTER_SYSTEM_PROMPT),
        ("human", question),
    ])

    category = response.content.strip().lower()
    if category not in ("resume", "career", "interview"):
        category = "career"

    return category


def router_node(state: GraphState) -> GraphState:
    """
    NODE 1: Router.

    Looks at the user's question and decides which agent should handle it.
    It does NOT answer the question itself - it only picks a category.
    """
    state["agent"] = classify_question(state["question"])
    return state


def resume_node(state: GraphState) -> GraphState:
    """NODE 2: Resume Agent."""
    result = run_resume_agent(state["question"])
    state["answer"] = result["answer"]
    state["sources"] = result["sources"]
    return state


def career_node(state: GraphState) -> GraphState:
    """NODE 3: Career Agent."""
    result = run_career_agent(state["question"])
    state["answer"] = result["answer"]
    state["sources"] = result["sources"]
    return state


def interview_node(state: GraphState) -> GraphState:
    """NODE 4: Interview Agent."""
    result = run_interview_agent(state["question"])
    state["answer"] = result["answer"]
    state["sources"] = result["sources"]
    return state


def decide_next_node(state: GraphState) -> Literal["resume", "career", "interview"]:
    """
    This function tells LangGraph which node to go to after the router.
    It just reads the category the router already decided and stored in state.
    """
    return state["agent"]


def build_graph():
    """
    Builds and compiles the LangGraph workflow.
    Called once when the app starts (see main.py).
    """
    graph = StateGraph(GraphState)

    # Register all 4 nodes
    graph.add_node("router", router_node)
    graph.add_node("resume", resume_node)
    graph.add_node("career", career_node)
    graph.add_node("interview", interview_node)

    # The graph always starts at the router
    graph.set_entry_point("router")

    # After the router runs, branch to one of the 3 agents based on
    # decide_next_node()'s return value
    graph.add_conditional_edges(
        "router",
        decide_next_node,
        {
            "resume": "resume",
            "career": "career",
            "interview": "interview",
        },
    )

    # Whichever agent runs, the graph ends after it (this gives us the
    # "Final Answer" step from the spec)
    graph.add_edge("resume", END)
    graph.add_edge("career", END)
    graph.add_edge("interview", END)

    return graph.compile()


# Built once at import time and reused for every chat request
compiled_graph = build_graph()
