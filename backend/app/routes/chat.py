import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.graph.workflow import compiled_graph, classify_question
from app.agents.resume_agent import stream_resume_agent
from app.agents.career_agent import stream_career_agent
from app.agents.interview_agent import stream_interview_agent
from app.rag.vector_store import has_resume_data
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter()

STREAMING_AGENTS = {
    "resume": stream_resume_agent,
    "career": stream_career_agent,
    "interview": stream_interview_agent,
}


@router.post("/chat", response_model=ChatResponse)
async def chat_with_resume(request: ChatRequest):
    if not has_resume_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume before starting the chat.",
        )

    result = compiled_graph.invoke({"question": request.question})

    return ChatResponse(
        agent=result["agent"],
        answer=result["answer"],
        sources=result["sources"],
    )


@router.post("/chat/stream")
async def chat_with_resume_streaming(request: ChatRequest):
    if not has_resume_data():
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume before starting the chat.",
        )

    def event_stream():
        agent_name = classify_question(request.question)
        yield json.dumps({"type": "agent", "agent": agent_name}) + "\n"

        stream_function = STREAMING_AGENTS[agent_name]

        for event in stream_function(request.question):
            yield json.dumps(event) + "\n"

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")