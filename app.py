"""
Query Interface for the Unofficial Crochet Stitch Guide (see planning.md
## Architecture — this is the front end of the Generation stage).

A single text box for the question, an "Answer" output, and a "Retrieved
from" output listing the sources actually used — attribution comes from
query.ask()'s programmatically-built source list, not from anything the
model wrote into its answer text.
"""

import gradio as gr

from query import ask


def handle_query(question: str):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"]) or "(no sources — see answer)"
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide: Crochet Stitches") as demo:
    gr.Markdown(
        "# The Unofficial Guide: Crochet Stitches\n"
        "Ask a question about any of the crochet stitch tutorials in this system's corpus. "
        "Answers are grounded strictly in the retrieved tutorial excerpts — if the corpus "
        "doesn't cover it, the system will say so instead of guessing."
    )
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. How many chains do I need to start the basket weave stitch?",
    )
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
