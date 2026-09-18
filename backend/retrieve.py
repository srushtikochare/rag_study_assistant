import os
import chromadb
from sentence_transformers import SentenceTransformer


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CHROMA_PATH = os.path.join(
    BASE_DIR,
    "chroma_db"
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
# RETRIEVE RELEVANT INFORMATION
# ============================================================

def retrieve(question, top_k=12):

    # No documents available
    total_documents = collection.count()

    if total_documents == 0:
        return []

    # --------------------------------------------------------
    # Convert question into embedding
    # --------------------------------------------------------

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    # --------------------------------------------------------
    # Search database
    # --------------------------------------------------------

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, total_documents),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    chunks = []

    # --------------------------------------------------------
    # Prepare results
    # --------------------------------------------------------

    for i, document in enumerate(documents):

        if not document:
            continue

        metadata = (
            metadatas[i]
            if i < len(metadatas)
            else {}
        )

        distance = (
            distances[i]
            if i < len(distances)
            else None
        )

        source = metadata.get(
            "source",
            "Unknown document"
        )

        chunks.append({
            "text": document,
            "source": source,
            "distance": distance
        })

    return chunks