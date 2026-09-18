import os

from google import genai
from dotenv import load_dotenv

from retrieve import retrieve


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, top_k=12):

    # --------------------------------------------------------
    # Retrieve relevant PDF content
    # --------------------------------------------------------

    chunks = retrieve(
        question,
        top_k=top_k
    )

    # --------------------------------------------------------
    # No PDF content available
    # --------------------------------------------------------

    if not chunks:

        return {
            "answer": (
                "I don't have enough information in the "
                "provided notes."
            ),
            "sources": [],
            "chunks_used": []
        }

    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context_parts = []

    for chunk in chunks:

        source = chunk.get(
            "source",
            "Unknown"
        )

        text = chunk.get(
            "text",
            ""
        )

        context_parts.append(
            f"Document: {source}\n{text}"
        )

    context = "\n\n".join(
        context_parts
    )

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an intelligent college-level RAG Study Assistant.

Your task is to answer the student's question using the
provided study notes.

IMPORTANT:

The answer must be based ONLY on the information contained
in the provided study notes.

Do not invent facts.

Do not use outside knowledge.

If the exact answer is available in the notes, explain it
clearly and completely.

If the answer is not available in the notes, say:

"I don't have enough information in the provided notes."

ANSWER STYLE:

Write a detailed, descriptive and exam-ready answer.

The student is a beginner, so explain concepts in simple
academic language.

Do not give extremely short answers.

For a theoretical question, normally include:

Definition
Explanation
Important points
Example
Conclusion

For a "What is" question:

1. Definition
2. Explanation
3. Example
4. Conclusion

For a "Why" question:

1. Meaning
2. Reasons
3. Explanation of each reason
4. Example
5. Conclusion

For a "How" question:

1. Introduction
2. Step-by-step process
3. Example
4. Conclusion

For "Types" questions:

Explain each type separately.

For "Advantages and disadvantages":

Explain each point in complete sentences.

For comparison questions:

Clearly explain the differences between the concepts.

For algorithms:

Explain the algorithm step-by-step in the correct order.

EXAM REQUIREMENT:

Make the answer suitable for a 5-10 mark college
examination.

Use enough theory to make the answer descriptive.

Do not unnecessarily repeat the same information.

FORMATTING:

Use plain text only.

Do NOT use Markdown.

Do NOT use:
#
##
###
*
**
---
[Source: ...]

Use simple headings such as:

Definition

Explanation

Types

Example

Advantages

Disadvantages

Conclusion

Use numbered points such as:

1. First point
2. Second point
3. Third point

Do not mention document filenames inside the answer.

Do not add citations after individual sentences.

The application will display the source documents separately.

STUDY NOTES:

{context}

STUDENT QUESTION:

{question}

Now provide the best detailed exam-ready answer possible
using ONLY the study notes.
"""

    # --------------------------------------------------------
    # Generate response
    # --------------------------------------------------------

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    answer = response.text.strip()

    # --------------------------------------------------------
    # Sources
    # --------------------------------------------------------

    sources = []

    for chunk in chunks:

        source = chunk.get("source")

        if source and source not in sources:
            sources.append(source)

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": chunks
    }