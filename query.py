"""
End-to-end query entry point for the interface layer (see planning.md
## Architecture — this is what app.py calls).

Wraps generate.generate_answer() and flattens its "sources" list of dicts
into plain display strings, since the UI layer just needs to print them.
"""

from generate import generate_answer


def ask(question: str) -> dict:
    """
    Run the full retrieval + grounded generation pipeline for question.

    Returns {"answer": str, "sources": list[str]} where each source string
    is "Source Name — Description (url)", built from retrieval metadata
    programmatically (see generate._format_sources) — never from text the
    model wrote itself.
    """
    result = generate_answer(question)
    sources = [
        f"{s['source']} — {s['description']} ({s['url']})" for s in result["sources"]
    ]
    return {"answer": result["answer"], "sources": sources}
