# CareerPilot AI

An AI-powered Resume & Career Coach. Upload your resume (PDF) and chat with
an AI that answers based only on your actual resume content.

## How it works (high level)

```
1. Upload PDF  →  extract text (PyMuPDF)  →  chunk + embed  →  store in ChromaDB
2. Ask a question  →  LangGraph Router Node classifies it
                    →  routes to Resume / Career / Interview Agent
                    →  agent retrieves relevant resume chunks (RAG)
                    →  Groq LLM generates a grounded answer
                    →  answer returned to the chat UI
```

## Tech Stack
- **Frontend:** React (Vite) + Tailwind CSS + Axios + React Router
- **Backend:** FastAPI + Pydantic
- **AI:** LangChain + LangGraph + Groq API
- **Embeddings:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (runs locally, free)
- **Vector DB:** ChromaDB (local, file-based)
- **PDF parsing:** PyMuPDF

## Running the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then open .env and paste your free Groq API key from https://console.groq.com

uvicorn app.main:app --reload
# backend runs at http://localhost:8000
# interactive API docs at http://localhost:8000/docs
```

## Running the frontend

```bash
cd frontend
npm install
npm run dev
# frontend runs at http://localhost:5173
```

## Project Structure

```
backend/
  app/
    agents/        # 3 LangGraph agent nodes (resume, career, interview) + shared LLM client
    graph/          # LangGraph workflow: router -> agent -> answer
    rag/            # ChromaDB storage, chunking, retrieval
    parser/         # PDF -> plain text extraction
    routes/         # FastAPI endpoints (/upload, /chat, /resume)
    models/         # Pydantic request/response schemas
    main.py         # FastAPI app entrypoint
  data/
    uploads/        # saved resume PDFs
    chroma_db/      # ChromaDB persistent storage
frontend/
  src/
    api/            # Axios client - all backend calls in one place
    components/     # Navbar, ChatBubble
    pages/          # Home, Upload, Chat, History
    App.jsx         # routes
```

## API Endpoints

| Method | Path      | Purpose                                   |
|--------|-----------|--------------------------------------------|
| POST   | `/upload` | Upload a resume PDF, extract + index it   |
| POST   | `/chat`   | Ask a question, get an AI-routed answer   |
| GET    | `/resume` | Check if a resume is already uploaded     |

## The LangGraph Workflow (4 nodes)

```
User Question
     ↓
Router Node        (classifies: resume / career / interview)
     ↓
┌────────────┬────────────┬──────────────┐
Resume Agent   Career Agent   Interview Agent
└────────────┴────────────┴──────────────┘
     ↓
Final Answer
```

Each agent retrieves relevant resume chunks from ChromaDB before answering,
so responses stay grounded in the user's actual resume instead of the LLM
making things up.
