# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Sample Chunks

<!-- Paste 5 representative chunks from your document collection after running your ingestion pipeline.
     For each chunk, note which source document it came from.
     These must be actual text — not screenshots. -->

| # | Source document | Chunk text |
| - | --------------- | ---------- |
| 1 | argyle_shell_heart_hook_home | Reddit 8 Threads The Argyle Shell Stitch is gorgeous and lightweight. It is airy and perfect for summer tops and beach cover ups! Learn this beautiful crochet stitch set with this Argyle Shell tutorial! ChatGPT Google AI Claude Add as a Google source Argyle Shell Crochet Stitch Tutorial The Argyle Shell is perfect for lightweight yarns to make tops, tunics, or wraps, such as my NEW and FREE Shell Yeah! Tunic pattern. You will want to block your finished piece to really see the |
| 2 | basket_weave_amanda_crochets | Share Pin 3K 3K Shares Hey everyone! In today's Crochet 101 lesson, I'm going to teach you how to make the basket weave stitch. This stitch is made working groups of front post double crochets and back post double crochets along the row. As you work more rows, you will begin to notice that some groups appear to be worked vertically while others horizontally. This effect happens by working different combinations of front and back post double crochets over four different rows. For today's |
| 3 | bead_stitch_stardust_crochet | Facebook This weeks Stitch Explorers cover the Bead Stitch. The bead stitch creates beautiful puffs and is very similar to the pineapple and pineapple puff stitch. It combines two basic stitches, the single crochet and the double crochet, which makes it perfect for a beginner to learn! You can come back to this link and explore the rest of the stitches, there is so much to learn! This is the fourth of five stitches we are going to learn leading up to creating the coolest 5 stitch project |
| 4 | blackberry_salad_handmade_by_stacy_j | The Blackberry Salad Crochet Stitch is a fun and simple crochet stitch that offers lots of texture! It works in increments of 4+1 and over a 4 row repeat. If you can chain and double crochet, YOU CAN DO THIS! There are written directions below for the Blackberry Salad Crochet Stitch, as well as a pin to save to your boards. The video tutorial is directly below. DIRECTIONS for the Blackberry Salad Crochet Stitch: Increments of 4+1 (+2 for the base chain) 1: Skip 3 chains (counts as dc), dc |
| 5 | bobble_stitch_hookfully | Bobble Stitch Tutorial The bobble stitch tutorial will help you to crochet a 3D texture, just like little bubbles! Even though it's single sided, the reverse has a very interesting design too. The bobble stitch can be used for almost any crochet project and is defo one of my favourite special stitches! How to crochet the bobble stitch The bobble stitch crochet tutorial is easy to intermediate skill level. Its a 2 row repeat and to complete the tutorial you will need to know the single |

**Inspection notes:** Chunks 4 and 5 are clean, complete instructional units that would make sense retrieved on their own. Chunks 1, 2, and 3 each open with leftover social-share widget text ("Reddit 8 Threads", "Share Pin 3K Shares", "Facebook") that survived HTML cleaning — different blog themes render share-button counts as plain text in slightly different formats, and our `clean_html()` regex in `ingest.py` only catches some of those variants. This is a known, un-fixed artifact at the time of this snapshot (documented honestly rather than hidden); the real instructional content directly after the noise is otherwise intact and retrievable. We plan to tighten the share-widget regex as a follow-up polish pass.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:**

Top returned chunks:
-
-
-

Relevance explanation:

---

**Query 2:**

Top returned chunks:
-
-
-

Relevance explanation:

---

**Query 3:**

Top returned chunks:
-
-
-

Relevance explanation:

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query:

Response:

Source attribution:

---

**Grounded response 2**

Query:

Response:

Source attribution:

---

**Out-of-scope query**

Query:

System response (refusal):

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:**

**Output format:**

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** 

> **System:** 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
