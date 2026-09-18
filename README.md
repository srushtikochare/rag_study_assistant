# 📚 RAG Study Assistant

A full-stack Retrieval-Augmented Generation (RAG) application that lets you upload your own subject notes as PDFs and ask questions about them in plain English. Answers are grounded strictly in the uploaded material — cited by source, with a groundedness evaluation layer that flags any unsupported claims instead of letting the model hallucinate.

## What it does

- Upload subject notes/textbook PDFs
- Ask questions in plain English and get exam-ready, detailed answers
- Every answer is grounded only in the uploaded notes — if the answer isn't in your notes, it says so instead of guessing
- A separate evaluation layer scores each answer's groundedness (0–100) and flags any unsupported claims
- Correctly refuses to answer questions outside the scope of the uploaded notes

## Why this isn't just a chatbot wrapper

Most student RAG demos skip the hardest part: proving the system doesn't hallucinate. This project adds a dedicated evaluation layer — a second LLM call that fact-checks the generated answer against the retrieved source chunks and produces a groundedness score. That score, not just the answer itself, is the actual deliverable.

## Architecture

React Frontend (Vite)
↓ HTTP (axios)
FastAPI Backend
↓
PDF Ingestion → Chunking → Embeddings (sentence-transformers) → ChromaDB
↓
Retrieval → Gemini (grounded answer generation)
↓
Evaluation layer → Gemini (groundedness scoring)


## Tech stack

**Backend:** Python, FastAPI, ChromaDB, sentence-transformers, pypdf, langchain-text-splitters, Google Gemini API

**Frontend:** React (Vite), axios

## Features

- PDF ingestion with automatic chunking and embedding
- Semantic retrieval using vector similarity search
- Grounded answer generation with source citations
- Groundedness evaluation layer (LLM-as-judge pattern) with a 0–100 score
- Correctly refuses out-of-scope questions instead of hallucinating
- Clean REST API (`/upload`, `/ask`, `/evaluate`, `/documents`, `/health`)
- React frontend with live upload and Q&A interface

## Running it locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

GOOGLE_API_KEY=your_gemini_api_key_here


Run the backend:
```bash
uvicorn main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/upload` | POST | Upload and ingest a PDF |
| `/ask` | POST | Ask a question, get a grounded answer with sources |
| `/evaluate` | POST | Ask a question, get the answer plus a groundedness score |
| `/documents` | GET | List all ingested documents |
| `/health` | GET | Health check |

## A real challenge I hit

Google deprecated the Gemini model I originally built against mid-development, and later I hit strict free-tier daily quota limits on the newer model. Rather than treat this as a blocker, I queried the Gemini API's `/models` endpoint directly to see exactly which models my key could access and their relative quota tiers, then switched to a lighter model (`gemini-flash-lite-latest`) with a much higher free-tier ceiling — a reminder that working against live, evolving APIs means designing for change, not just for the first successful call.

## Possible next steps

- Batch evaluation dashboard showing groundedness scores across a full test set, charted
- Multi-document support with per-document filtering
- Deploy backend and frontend for a live hosted demo

## Author

Srushti Kochare — B.Tech Artificial Intelligence and Data Science, YCCE Nagpur
