import os
import shutil

from pypdf import PdfReader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

import chromadb

from sentence_transformers import (
    SentenceTransformer
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "chroma_db"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ============================================================
# EMBEDDING MODEL
# ============================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="study_notes"
)


# ============================================================
# EXTRACT PDF TEXT
# ============================================================

def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        page_text = page.extract_text() or ""

        if page_text.strip():

            pages.append(
                f"Page {page_number}\n"
                f"{page_text.strip()}"
            )

    return "\n\n".join(pages)


# ============================================================
# CREATE CHUNKS
# ============================================================

def chunk_text(
    text,
    filename,
    chunk_size=1000,
    chunk_overlap=150
):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            "; ",
            ", ",
            " ",
            ""
        ]
    )

    splits = splitter.split_text(
        text
    )

    chunks = []

    for index, chunk in enumerate(splits):

        if not chunk.strip():
            continue

        chunks.append({
            "text": chunk.strip(),
            "source": filename,
            "chunk_id": (
                f"{filename}_{index}"
            )
        })

    return chunks


# ============================================================
# INGEST PDF
# ============================================================

def ingest_pdf(
    pdf_path,
    filename
):

    filename = os.path.basename(
        filename
    )

    # --------------------------------------------------------
    # Save permanent PDF
    # --------------------------------------------------------

    permanent_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if os.path.abspath(pdf_path) != os.path.abspath(
        permanent_path
    ):

        shutil.copy2(
            pdf_path,
            permanent_path
        )

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    text = extract_text(
        permanent_path
    )

    if not text.strip():

        return {
            "filename": filename,
            "chunks_added": 0,
            "message": "No readable text found in PDF."
        }

    # --------------------------------------------------------
    # Create chunks
    # --------------------------------------------------------

    chunks = chunk_text(
        text,
        filename
    )

    if not chunks:

        return {
            "filename": filename,
            "chunks_added": 0
        }

    # --------------------------------------------------------
    # Remove old chunks of same PDF
    # --------------------------------------------------------

    existing = collection.get(
        where={
            "source": filename
        },
        include=["metadatas"]
    )

    old_ids = existing.get(
        "ids",
        []
    )

    if old_ids:

        collection.delete(
            ids=old_ids
        )

    # --------------------------------------------------------
    # Create embeddings
    # --------------------------------------------------------

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    ).tolist()

    # --------------------------------------------------------
    # Store in ChromaDB
    # --------------------------------------------------------

    collection.add(
        ids=[
            chunk["chunk_id"]
            for chunk in chunks
        ],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {
                "source": filename
            }
            for chunk in chunks
        ]
    )

    return {
        "filename": filename,
        "chunks_added": len(chunks),
        "message": "PDF uploaded and indexed successfully."
    }


# ============================================================
# LIST DOCUMENTS
# ============================================================

def list_documents():

    documents = []

    if os.path.exists(
        UPLOAD_FOLDER
    ):

        for filename in os.listdir(
            UPLOAD_FOLDER
        ):

            if filename.lower().endswith(
                ".pdf"
            ):

                documents.append(
                    filename
                )

    return sorted(
        documents
    )