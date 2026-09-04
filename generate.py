"""
Generation stage of the pipeline (see planning.md ## Architecture and
## Anticipated Challenges).

Takes a user query, retrieves the top-k chunks via embed.retrieve(), and
asks the Claude/Groq-hosted LLM to answer using ONLY those chunks. Grounding
is enforced two ways:
  1. The system prompt instructs the model to answer strictly from the
     provided context and to say so explicitly if the context is insufficient.
  2. Source attribution is NOT left to the model — it is built
     programmatically from the retrieved chunks' metadata and appended
     after generation, so it can't be dropped, altered, or fabricated.
"""

import os
import re

from dotenv import load_dotenv
from groq import Groq

from embed import retrieve, TOP_K

load_dotenv()

# The assignment's recommended default, meta-llama/llama-4-scout-17b-16e-instruct,
# is not available on this Groq account/key (checked via client.models.list()).
# openai/gpt-oss-120b is used instead: it's free-tier on this key and, like the
# recommended model, is served through Groq's OpenAI-compatible chat completions
# endpoint, so the rest of this integration is unaffected.
GENERATION_MODEL = "openai/gpt-oss-120b"

REFUSAL_MESSAGE = "I don't have enough information on that."

SYSTEM_PROMPT = f"""Answer the question using only the information in the provided documents \
below — never your own general knowledge of crochet.

Rules:
- If the documents contain the answer, answer clearly and specifically, quoting exact \
numbers/stitch counts/instructions from the documents where relevant.
- If the documents don't contain enough information to answer, say exactly: \
"{REFUSAL_MESSAGE}" Do not guess or fall back on outside knowledge.
- Do not fabricate source names, stitch names, or instructions that are not present in the \
context.
- Do not add your own citations, footnote markers, or a source list (e.g. no "[Excerpt 1]", \
no "(Source: ...)", no bracketed document names) anywhere in your answer — plain prose only. \
Source attribution is handled separately by the system after your answer is generated."""


# Matches stray citation markers the model sometimes inserts despite the
# system prompt (e.g. "[Excerpt 1]", "【Excerpt 2 — Source Name】"), as a
# belt-and-suspenders cleanup on top of the prompt instruction — a prompt
# alone is a suggestion, not a guarantee, so attribution formatting must not
# depend on the model actually obeying it.
_CITATION_MARKER_RE = re.compile(r"[\[【]\s*Excerpt\s*\d+[^\]】]*[\]】]", re.IGNORECASE)


def _strip_citation_markers(answer: str) -> str:
    return re.sub(r"\s+", " ", _CITATION_MARKER_RE.sub("", answer)).strip()


def _build_context(chunks: list[dict]) -> str:
    blocks = []
    for i, chunk in enumerate(chunks, 1):
        blocks.append(f"[Excerpt {i} — {chunk['source']}]\n{chunk['text']}")
    return "\n\n".join(blocks)


def _format_sources(chunks: list[dict]) -> list[dict]:
    """Deduplicate retrieved chunks down to one attribution entry per source document."""
    seen = {}
    for chunk in chunks:
        key = chunk["doc_id"]
        if key not in seen:
            seen[key] = {
                "source": chunk["source"],
                "description": chunk["description"],
                "url": chunk["url"],
            }
    return list(seen.values())


def generate_answer(query: str, k: int = TOP_K) -> dict:
    """
    Retrieve top-k chunks for query and generate a grounded answer.

    Returns {"answer": str, "sources": list[dict], "chunks": list[dict]}.
    "sources" is built directly from retrieval metadata, independent of
    whatever the model does or doesn't say — this is the programmatic
    attribution guarantee.
    """
    chunks = retrieve(query, k=k)

    if not chunks:
        return {
            "answer": REFUSAL_MESSAGE,
            "sources": [],
            "chunks": [],
        }

    context = _build_context(chunks)
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    response = client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}",
            },
        ],
        temperature=0.0,
    )

    answer = _strip_citation_markers(response.choices[0].message.content.strip())
    is_refusal = answer.startswith(REFUSAL_MESSAGE)

    return {
        "answer": answer,
        # Suppress attribution on a refusal — the retrieved chunks were judged
        # irrelevant by the model, so listing them as "sources" would falsely
        # imply they support an answer that was never actually given.
        "sources": [] if is_refusal else _format_sources(chunks),
        "chunks": chunks,
    }


if __name__ == "__main__":
    sample_queries = [
        "According to Amanda Crochets, what foundation chain length is required for the basket weave stitch?",
        "What is the best crochet hook brand?",  # out-of-scope: should trigger the refusal
    ]
    for query in sample_queries:
        result = generate_answer(query)
        print(f"Q: {query}")
        print(f"A: {result['answer']}")
        print("Sources:")
        for source in result["sources"]:
            print(f"  - {source['source']}: {source['description']} ({source['url']})")
        print()
