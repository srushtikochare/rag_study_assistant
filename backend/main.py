import os
import shutil

from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

from ingest import (
    ingest_pdf,
    list_documents
)

from generate import (
    generate_answer
)

from evaluate import (
    score_groundedness
)

from history import (
    load_history,
    save_message,
    clear_history
)


app = FastAPI(
    title="RAG Study Assistant API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    os.makedirs(
        "data",
        exist_ok=True
    )

    filename = os.path.basename(
        file.filename
    )

    path = os.path.join(
        "data",
        filename
    )

    with open(
        path,
        "wb"
    ) as f:

        shutil.copyfileobj(
            file.file,
            f
        )

    result = ingest_pdf(
        path,
        filename
    )

    return result


@app.post("/ask")
def ask_question(
    payload: Question
):

    result = generate_answer(
        payload.question
    )

    save_message(
        payload.question,
        result["answer"]
    )

    return result


@app.post("/evaluate")
def evaluate_answer(
    payload: Question
):

    result = generate_answer(
        payload.question
    )

    score = score_groundedness(
        result["answer"],
        result["chunks_used"]
    )

    save_message(
        payload.question,
        result["answer"]
    )

    return {
        **result,
        "evaluation": score
    }


@app.get("/documents")
def get_documents():

    return {
        "documents": list_documents()
    }


@app.get("/history")
def get_history():

    return {
        "history": load_history()
    }


@app.delete("/history")
def delete_history():

    clear_history()

    return {
        "message": "History cleared"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }