import json
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def score_groundedness(answer, context_chunks):
    context = "\n\n".join([c["text"] for c in context_chunks])
    prompt = f"""You are a strict fact-checker. Given the CONTEXT and an ANSWER,
determine if every claim in the ANSWER is supported by the CONTEXT.

CONTEXT:
{context}

ANSWER:
{answer}

Respond with ONLY a JSON object, no other text, no markdown formatting:
{{"grounded": true or false, "unsupported_claims": [], "score": a number 0-100}}"""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except:
        return {"grounded": None, "unsupported_claims": [], "score": None}