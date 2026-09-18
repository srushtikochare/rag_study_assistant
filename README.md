# 📚 RAG Study Assistant — Grounded Question Answering with LLM Evaluation

A full-stack **Retrieval-Augmented Generation (RAG)** application that allows users to upload subject notes or textbook PDFs and ask questions in natural language.

The system retrieves relevant information from the uploaded documents before generating an answer with **Google Gemini**. Each response includes source information, while a separate evaluation layer checks whether the generated answer is supported by the retrieved material.

🔗 **GitHub Repository:** https://github.com/srushtikochare/rag_study_assistant

---

## 🚀 Overview

Large language models can generate fluent answers but may produce information that is not supported by the user's study material.

This project addresses that problem using a **retrieval-first architecture**.

Instead of asking Gemini to answer directly:

```text
Question → LLM → Answer
```

the application follows:

```text
Question
   ↓
Query Embedding
   ↓
Vector Search
   ↓
Relevant Document Chunks
   ↓
Gemini
   ↓
Grounded Answer + Sources
   ↓
Evaluation Layer
   ↓
Groundedness Assessment
```

The application is designed to answer questions **using the uploaded study material as the primary knowledge source** and to reject questions that fall outside the available content.

---

## 🎯 Key Objectives

* Build a complete end-to-end RAG pipeline.
* Allow users to upload PDF-based study material.
* Convert documents into searchable vector representations.
* Retrieve semantically relevant content for a user query.
* Generate answers grounded in retrieved source material.
* Provide source references with generated responses.
* Add an independent evaluation layer for checking answer groundedness.
* Provide a REST API for document ingestion and question answering.
* Build a usable React frontend for interacting with the system.

---

## 🏗️ System Architecture

```text
                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                                ▼
                     ┌────────────────────┐
                     │   React Frontend   │
                     └─────────┬──────────┘
                               │
                         HTTP / Axios
                               │
                               ▼
                     ┌────────────────────┐
                     │   FastAPI Backend  │
                     └─────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
          PDF Upload                        User Query
              │                                 │
              ▼                                 ▼
        ┌───────────┐                    Query Embedding
        │   pypdf   │                           │
        └─────┬─────┘                           ▼
              │                           ┌───────────┐
              ▼                           │ ChromaDB  │
        Text Extraction                   └─────┬─────┘
              │                                 │
              ▼                                 ▼
          Chunking                        Top-K Chunks
              │                                 │
              ▼                                 │
     Sentence Transformers                     │
              │                                 │
              └──────────────┐                  │
                             ▼                  │
                       ┌────────────┐           │
                       │ ChromaDB   │◄──────────┘
                       └─────┬──────┘
                             │
                             ▼
                     Retrieved Context
                             │
                             ▼
                       ┌──────────┐
                       │ Gemini   │
                       └────┬─────┘
                            │
                            ▼
                    Grounded Answer
                            │
                            ▼
                    Evaluation Layer
                            │
                            ▼
               Groundedness Assessment
                            │
                            ▼
                       React UI
```

---

## ✨ Features

### 1. PDF Document Ingestion

Users can upload subject notes and textbook PDFs.

The ingestion pipeline:

```text
PDF
 ↓
Text Extraction
 ↓
Text Chunking
 ↓
Embedding Generation
 ↓
Vector Storage
```

The resulting embeddings are stored in ChromaDB for semantic retrieval.

---

### 2. Semantic Search

When a user asks a question, the query is converted into an embedding.

The system searches the vector database for semantically similar document chunks.

This allows the system to retrieve relevant information even when the question does not use exactly the same words as the source material.

---

### 3. Grounded Answer Generation

The retrieved document chunks are provided as context to Gemini.

The model generates the answer using this retrieved context rather than relying solely on its pretrained knowledge.

Example:

```text
User:
"Explain the working principle of photovoltaic cells."

        ↓

Retriever:
Finds relevant chunks from uploaded solar-energy notes.

        ↓

Gemini:
Generates an explanation using the retrieved material.

        ↓

Application:
Returns the answer with source information.
```

---

### 4. Source Citations

Generated responses include information about the retrieved source material.

This allows the user to understand **where the answer came from** instead of receiving an unsupported response.

---

### 5. Groundedness Evaluation

The project includes a separate evaluation stage that checks the generated answer against the retrieved source chunks.

Conceptually:

```text
Retrieved Context
       +
Generated Answer
       ↓
Evaluation Model
       ↓
Groundedness Score
       +
Unsupported Claim Detection
```

The evaluator produces a **0–100 groundedness score** and identifies potentially unsupported claims.

This follows an **LLM-as-a-judge evaluation pattern**.

> The score is treated as an evaluation signal rather than a guaranteed objective measure of factual correctness.

---

### 6. Out-of-Scope Question Handling

The system is designed to avoid answering questions that cannot be supported by the uploaded material.

For example, if the uploaded document contains only solar-energy notes and the user asks:

```text
"What is the capital of Japan?"
```

the system can indicate that the information is outside the available study material instead of generating an unrelated answer.

---

### 7. REST API

The backend exposes a clean API for:

| Endpoint     | Method | Purpose                                       |
| ------------ | ------ | --------------------------------------------- |
| `/upload`    | POST   | Upload and ingest a PDF                       |
| `/ask`       | POST   | Ask a question and retrieve a grounded answer |
| `/evaluate`  | POST   | Generate an answer and evaluate groundedness  |
| `/documents` | GET    | List ingested documents                       |
| `/health`    | GET    | Check backend status                          |

Interactive API documentation is available through FastAPI's Swagger interface.

---

## 🧩 RAG Pipeline

### Step 1 — Document Loading

PDF files are processed using `pypdf`.

### Step 2 — Text Chunking

Extracted text is divided into smaller chunks using a text-splitting strategy.

Chunking allows the retriever to search smaller sections of the document instead of passing the entire document to the LLM.

### Step 3 — Embedding Generation

The chunks are converted into numerical vector representations using **Sentence Transformers**.

### Step 4 — Vector Storage

Embeddings and associated document information are stored in **ChromaDB**.

### Step 5 — Query Retrieval

A user's question is embedded and compared against stored vectors to retrieve relevant chunks.

### Step 6 — Answer Generation

Retrieved context is provided to Gemini to generate the final response.

### Step 7 — Evaluation

The generated answer and supporting context are passed to a separate evaluation step to assess groundedness.

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* ChromaDB
* Sentence Transformers
* pypdf
* LangChain Text Splitters
* Google Gemini API

### Frontend

* React
* Vite
* Axios

### AI / NLP

* Retrieval-Augmented Generation
* Text embeddings
* Semantic similarity search
* LLM-based answer generation
* LLM-as-a-judge evaluation

---

## ▶️ Running Locally

### Backend

Clone the repository:

```bash
git clone https://github.com/srushtikochare/rag_study_assistant
cd rag_study_assistant
```

Create and activate a virtual environment:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on:

```text
http://localhost:5173
```

---

## 🧪 Evaluation Approach

The project separates **answer generation** from **answer evaluation**.

The evaluation stage considers:

* Whether claims in the answer are supported by retrieved context.
* Whether unsupported information appears in the response.
* How strongly the generated answer is grounded in the retrieved material.

The resulting score is intended to provide an additional quality signal for the RAG pipeline.

### Important limitation

LLM-based evaluation is itself probabilistic and can make mistakes. Therefore, a groundedness score should not be interpreted as absolute proof that an answer is correct.

A future improvement is to build a manually labelled evaluation dataset and compare automated evaluation against human judgements.

---

## 🧠 Technical Challenge

During development, the Gemini model used by the original implementation was deprecated, requiring changes to the API integration.

Later, the application encountered strict free-tier API quota limitations.

Instead of hardcoding a model name and assuming the API would remain unchanged, I queried the Gemini API's available model information and adapted the application to use a model compatible with the available API access and quota constraints.

This highlighted an important practical challenge in GenAI development:

**AI APIs and model availability change rapidly, so applications need to account for evolving models, quotas, and API interfaces.**

---

## 🔐 Current Limitations

The current implementation has several areas that can be improved:

* Evaluation currently relies on an LLM-as-a-judge approach.
* Retrieval quality depends on chunking and embedding choices.
* Large document collections require more sophisticated retrieval strategies.
* Authentication and user-specific document isolation are not currently implemented.
* The current deployment architecture is intended primarily as a demonstration application.

---

## 🔮 Future Improvements

* Quantitative RAG evaluation using a labelled benchmark dataset
* Recall@K and retrieval-quality measurements
* Human-vs-LLM evaluator comparison
* Hybrid keyword + semantic retrieval
* Reranking of retrieved chunks
* Multi-document support with document-level filtering
* Conversation history with source-aware context
* Authentication and user-specific document collections
* Batch evaluation dashboard
* Production deployment of frontend and backend

---

## 💡 What This Project Demonstrates

This project demonstrates practical experience with:

* Retrieval-Augmented Generation
* Vector databases
* Text embeddings
* Semantic search
* LLM integration
* Prompt and context management
* Hallucination mitigation
* LLM-based evaluation
* REST API development
* FastAPI
* React
* PDF processing
* Debugging evolving AI APIs
* Full-stack AI application development

---

## 👩‍💻 Author

**Srushti Kochare**
B.Tech — Artificial Intelligence & Data Science
Yeshwantrao Chavan College of Engineering (YCCE), Nagpur

GitHub: https://github.com/srushtikochare
