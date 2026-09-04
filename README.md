# The Unofficial Guide — Project 1

## Demo Video

[Crochet Stitch Guide with Source Grounding (Loom, with captions)](https://www.loom.com/share/f38e2dff7b8c45d68cb5ce863429e183)

---

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

**Crochet stitches.** For any given stitch (shell, bobble, basket weave, coral mesh, etc.), dozens of independent hobbyist bloggers publish their own tutorial, each with slightly different wording, abbreviations (US vs. UK terms), stitch counts, and troubleshooting tips. There's no single official reference that consolidates this: pattern-writing bodies define standard abbreviations but don't cover technique nuance, variations, or common mistakes. A beginner searching "how do I do a bobble stitch" has to open 5–10 tabs, compare instructions, and reconcile conflicting terminology on their own — the knowledge that would answer their question exists, but it's scattered across low-SEO independent blogs with no cross-referencing. This system pulls together the specific fact or step a crocheter needs from across those sources without requiring them to manually read and compare multiple full tutorials.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
| - | ------ | ---- | ---------------- |
| 1 | The Spruce Crafts — How to Crochet Shell Stitch | Blog tutorial (web) | [https://www.thesprucecrafts.com/how-to-crochet-a-shell-stitch-979096](https://www.thesprucecrafts.com/how-to-crochet-a-shell-stitch-979096) |
| 2 | Heart. Hook. Home. — Argyle Shell Crochet Stitch Tutorial | Blog tutorial (web) | [https://hearthookhome.com/argyle-shell-crochet-stitch-tutorial/](https://hearthookhome.com/argyle-shell-crochet-stitch-tutorial/) |
| 3 | Amanda Crochets: Handmade with Love — How to Make the Basket Weave Stitch | Blog tutorial (web) | [https://www.amandacrochets.com/how-to-make-the-basket-weave-stitch/](https://www.amandacrochets.com/how-to-make-the-basket-weave-stitch/) |
| 4 | Hookfully: Happy Crochet Family — Bobble Stitch Tutorial | Blog tutorial (web) | [https://hookfully.com/bobble-stitch-tutorial/](https://hookfully.com/bobble-stitch-tutorial/) |
| 5 | Handmade by Stacy J — Blackberry Salad Crochet Stitch | Blog tutorial (web) | [https://handmadebystacyj.com/2020/03/14/blackberry-salad-crochet-tutorial/](https://handmadebystacyj.com/2020/03/14/blackberry-salad-crochet-tutorial/) |
| 6 | Creations by Courtney — Crochet Heart: Stitch Tutorial | Blog tutorial (web) | [https://creationsbycourtney.com/crochet-heart-stitch-tutorial/](https://creationsbycourtney.com/crochet-heart-stitch-tutorial/) |
| 7 | Selina Veronique: Crochet-DIY-Lifestyle — Crochet Lacy Shell Stitch Free Pattern | Blog tutorial (web) | [https://www.selinaveronique.com/crochet-lacy-shell-stitch-free-pattern](https://www.selinaveronique.com/crochet-lacy-shell-stitch-free-pattern) |
| 8 | Stardust Crochet — How to Crochet: Coral Mesh (Stitch Explorer Series) | Blog tutorial (web) | [https://stardustgoldcrochet.com/how-to-crochet-coral-mesh-crochet-video-tutorial-for-beginners-stitch-explorer-series/](https://stardustgoldcrochet.com/how-to-crochet-coral-mesh-crochet-video-tutorial-for-beginners-stitch-explorer-series/) |
| 9 | Stardust Crochet — How to Crochet: Bead Stitch (Stitch Explorer Series) | Blog tutorial (web) | [https://stardustgoldcrochet.com/how-to-crochet-bead-stitch-video-tutorial-for-beginners-stitch-explorer-series/](https://stardustgoldcrochet.com/how-to-crochet-bead-stitch-video-tutorial-for-beginners-stitch-explorer-series/) |
| 10 | Rich Textures Crochet — Mesh Cluster Stitch: How to Crochet | Blog tutorial (web) | [https://richtexturescrochet.com/mesh-cluster-stitch/](https://richtexturescrochet.com/mesh-cluster-stitch/) |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** ~500 characters (roughly 100–125 tokens), implemented in `chunk_text()` in `chunk.py`.

**Overlap:** 75 characters.

**Preprocessing before chunking:** Each source is fetched in `ingest.py`, parsed with BeautifulSoup, and narrowed to its actual article-body container (auto-detected as the largest of `<article>`, `elementor-widget-theme-post-content`, `entry-content`, or `post-content`, since some page-builder sites like Elementor put unrelated "related posts" teasers in `<article>` tags instead of the real content). `<script>`, `<style>`, `<nav>`, `<footer>`, and similar boilerplate tags are stripped, along with elements whose class/id matches comment/sidebar/related-post/advertisement/newsletter keywords, and a regex strips social-share button text (e.g. "11368 shares Tweet Reddit") that some themes render as plain text rather than a targetable CSS class. Each cleaned document is saved as a `.txt` file in `documents/` with a small header (source, description, URL) before chunking runs.

**Why these choices fit your documents:** My documents are blog-style tutorials, not short reviews — each page mixes an intro, a materials list, a numbered step-by-step instruction sequence, and troubleshooting tips, and a single tutorial can run 1,500–5,500+ characters. A chunk size much smaller than 500 characters would cut a single instructional step in half and make it unretrievable on its own; a chunk size much larger (e.g. a whole article as one chunk) would bury a specific fact inside a mass of unrelated prose and dilute the embedding, hurting retrieval precision. 500 characters keeps each chunk to roughly one instructional step or tip, matching how these tutorials are actually structured. The 75-character overlap protects against a step's setup (e.g. "insert hook into the next stitch, yarn over,") being separated from its conclusion ("...pull through and complete as normal") by a chunk boundary — with overlap, at least one of the two adjacent chunks is more likely to contain the full instruction, though as documented in Failure Case Analysis below, this doesn't eliminate the risk entirely.

**Final chunk count:** 82 chunks across the 10 documents (verified by running `chunk_all_documents()` in `chunk.py`), which falls in the healthy 50–2,000 range — not so few that chunks are overly broad, not so many that each carries too little semantic signal to distinguish from noise.

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

**Model used:** all-MiniLM-L6-v2 via sentence-transformers. It's small (~80MB), runs fully locally with no API key or rate limits, embeds in well under a second per chunk on CPU, and performs well on general English text like these tutorials — appropriate for a 10-source, 82-chunk corpus where latency and cost matter more than squeezing out marginal accuracy gains.

**Production tradeoff reflection:** If cost weren't a constraint, I'd consider a larger, higher-accuracy embedding model like OpenAI's text-embedding-3-large or Cohere's embed-v3 for better recall on nuanced domain-specific phrasing (e.g., distinguishing "front post double crochet" from "back post double crochet"). Tradeoffs I'd weigh: context length (less relevant here since my chunks are short, but would matter for longer documents), multilingual support (valuable if I wanted to include Spanish-language crochet tutorials, since terminology often differs meaningfully by region), accuracy on domain-specific text (a model with better recall on niche crafting vocabulary reduces the risk of confusing similar-sounding stitches), and latency (a larger, API-hosted model adds round-trip latency that matters more for a live chat interface than for one-time batch embedding). For a real product I'd benchmark a few candidates against my own eval questions rather than assume bigger is automatically better.

---

## Retrieval Test Results

<!-- Run these 3 queries through your retrieval system and record the top returned chunks.
     For at least 2 of the 3, explain why the returned chunks are relevant to the query.
     Results must be text — not screenshots. -->

**Query 1:** "According to Amanda Crochets, what foundation chain length is required for the basket weave stitch?"

Top returned chunks:

- [Amanda Crochets: Handmade with Love] (distance=0.392) "To begin, you will need a multiple of 6 stitches plus 4 more at the end for your foundation chain. For the purposes of this tutorial, I am making 16 chains. ROW 1: Double crochet..."
- [Heart. Hook. Home.] (distance=0.448) "Next you will single crochet in the second chain from the hook. Chain five, skip the next three chains, and single crochet in the next chain..."
- [Amanda Crochets: Handmade with Love] (distance=0.453) "...ain. Chain 2 and turn. ROW 5: Repeat row 4. That's how to make the basket weave stitch! Repeat rows 2-5 over and over again to practice..."

Relevance explanation: The top result directly answers the question with the exact expected fact ("multiple of 6 stitches plus 4 more") from the correct source, at a strong distance score (0.392). Results 2 and 3 are more loosely related (result 2 is a different tutorial's chain-counting instructions, pulled in because it shares similar foundation-chain language) but aren't off-topic noise — a top-k of 4 correctly surfaces the right answer first.

---

**Query 2:** "According to Stardust Crochet, what three techniques combine to make the coral mesh stitch?"

Top returned chunks:

- [Stardust Crochet: Inspire, Learn, Create] (distance=0.257) "a 5 mm hook. The Coral Mesh consists of a modified Solomon's knot, chains, and half double crochets. you may also like these stitch tutorials..."
- [Stardust Crochet: Inspire, Learn, Create] (distance=0.379) "...Complete video tutorial at bottom of post — for all the visual learners out there. Do you have a stitch or pattern you'd like a video created?..."
- [Heart. Hook. Home.] (distance=0.403) "...ttern. See the VIDEO tutorial for this stitch below! Note that one SHELL = double crochet, ch-1, double crochet, ch-1, double crochet all in the same stitch..."

Relevance explanation: The top chunk is a near-perfect match — it names all three techniques (modified Solomon's knot, chains, half double crochets) from exactly the source asked about, at the lowest distance score of any query tested (0.257). This confirms the embedding model correctly associates "coral mesh," "techniques," and the specific stitch names even though the query doesn't quote the tutorial verbatim.

---

**Query 3:** "According to Hookfully's tutorial, how many incomplete stitches are worked into the same stitch to make one bobble, and how many loops are pulled through at the end?"

Top returned chunks:

- [Hookfully: Happy Crochet Family] (distance=0.298) "...Bobble stitch crochet tutorial. Making a bobble Stitch. Yarn over, insert hook & pull up a loop, yarn over, pull through 2 loops on the hook. Repeat 4 m..."
- [Stardust Crochet: Inspire, Learn, Create] (distance=0.397) "...Stitch Guide: msol = modified Solomon's Knot. pull up a long loop (1/2" to 3/4"). yo, pull through. ch 1. hdc = half double crochet..."
- [Hookfully: Happy Crochet Family] (distance=0.427) "...2 row repeat and to complete the tutorial you will need to know the single crochet, instructions are included to learn the bobble stitch..."

Relevance explanation: The top chunk is from the correct source and contains the start of the exact instruction ("insert hook & pull up a loop, yarn over, pull through 2 loops... Repeat 4 m[ore times]"), which is the beginning of the answer but gets cut off at the 500-char chunk boundary before stating the final "pull through all 6 loops" step. This is a useful, realistic example of the chunk-boundary risk I flagged in planning.md's Anticipated Challenges — the answer is present but split across adjacent chunks, so the LLM would need at least 2 of the top-4 chunks to fully answer this question.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** From `generate.py`'s `SYSTEM_PROMPT`: "Answer the question using only the information in the provided documents below — never your own general knowledge of crochet... If the documents don't contain enough information to answer, say exactly: 'I don't have enough information on that.' Do not guess or fall back on outside knowledge... Do not add your own citations, footnote markers, or a source list... Source attribution is handled separately by the system after your answer is generated." The context passed to the model is strictly limited to the top-k retrieved chunks — the model is never given tool access, web access, or any other way to pull in outside information, so grounding is enforced both by instruction and by the structural fact that retrieved text is the only information available to it.

**How source attribution is surfaced in the response:** Attribution is built programmatically, not left to the model. `_format_sources()` in `generate.py` reads the `source`, `description`, and `url` metadata directly off the chunks that ChromaDB actually returned for that query and de-duplicates them into a source list, which the Gradio interface (`app.py`) renders in a separate "Sources" panel below the answer — the model's answer text never determines what gets cited. As an extra safety net, `_strip_citation_markers()` regex-strips any inline citation-style text (e.g. `[Excerpt 1]`) the model adds despite being told not to, since a prompt instruction alone is not a guarantee — this was needed in practice: an earlier test run had the model insert a `【Excerpt 1 — Amanda Crochets】` marker into its answer on its own.

---

## Example Responses

<!-- Provide at least 2 grounded responses (query + response + source attribution)
     and 1 out-of-scope query showing your system's refusal.
     All entries must be text — not screenshots. -->

**Grounded response 1**

Query: "What three techniques combine to make the coral mesh stitch, according to Stardust Crochet?"

Response: "The coral mesh stitch is made by combining a modified Solomon's knot, chains, and half-double crochets."

Source attribution: [Stardust Crochet: Inspire, Learn, Create — How to Crochet: Coral Mesh; Stitch Explorer Series](https://stardustgoldcrochet.com/how-to-crochet-coral-mesh-crochet-video-tutorial-for-beginners-stitch-explorer-series/)

Grounding check: The top retrieved chunk (distance=0.257) reads verbatim "The Coral Mesh consists of a modified Solomon's knot, chains, and half double crochets" — the response is a direct, traceable restatement of retrieved text, not a paraphrase invented from general crochet knowledge. Passes the "could this have come from anywhere else?" test — no, this specific three-part technique list only exists in this one tutorial.

---

**Grounded response 2**

Query: "According to Amanda Crochets, what foundation chain length is required for the basket weave stitch?"

Response: "Amanda Crochets says the basket-weave stitch starts with a foundation chain that must be a multiple of 6 stitches plus 4 extra stitches. In the tutorial she uses 16 chains as an example."

Source attribution: [Amanda Crochets: Handmade with Love — How to Make the Basket Weave Stitch](https://www.amandacrochets.com/how-to-make-the-basket-weave-stitch/); [Heart. Hook. Home. — Argyle Shell Crochet Stitch Tutorial](https://hearthookhome.com/argyle-shell-crochet-stitch-tutorial/)

Grounding check: The specific numbers ("multiple of 6 plus 4," "16 chains") match the retrieved Amanda Crochets chunk word-for-word ("a multiple of 6 stitches plus 4 more... I am making 16 chains"). This is a very specific, non-generic fact — a model relying on training data alone would have no way to know this particular blogger's specific example chain count, which confirms the answer is grounded rather than guessed. Note: a second, unrelated source (Heart. Hook. Home.) was also retrieved and listed in attribution even though the answer text doesn't draw from it — see Failure Case Analysis below for why over-inclusive attribution is a related but distinct risk from grounding failure.

---

**Out-of-scope query**

Query: "What crochet hook size should I use for amigurumi?"

System response (refusal): "I don't have enough information on that."

Grounding check: No source appears in the corpus that discusses amigurumi or general hook-sizing guidance, and the system's own attribution list came back empty for this query (retrieval still returned its top-4 nearest chunks, since ChromaDB always returns *something*, but the model correctly judged none of them relevant and refused rather than filling the gap with plausible-sounding general knowledge — e.g. it did NOT say something like "a 3.5mm hook is commonly recommended for amigurumi with worsted weight yarn," which would be true-sounding, common advice but entirely unsupported by this system's documents).

---

## Query Interface

<!-- Describe your query interface: what are the input fields, what does the output look like?
     Then provide a complete sample interaction transcript showing a real exchange. -->

**Input fields:** A single text box ("Ask about a crochet stitch") where the user types a natural-language question.

**Output format:** Two output panels below the input: an "Answer" text box with the grounded response, and a "Sources" markdown panel listing each source document actually used (name, description, and URL), rendered as a bulleted list — or a note that no sources were used if the system refused to answer.

---

**Sample Interaction Transcript**

<!-- Show a complete query → response exchange as it actually appears in your interface.
     Must be text — not a screenshot. -->

> **User:** What three techniques combine to make the coral mesh stitch, according to Stardust Crochet?

> **System:**
> Answer: The coral mesh stitch is made by combining a modified Solomon's knot, chains, and half-double crochets.
>
> Sources:
> - **Stardust Crochet: Inspire, Learn, Create** - How to Crochet: Coral Mesh; Stitch Explorer Series (https://stardustgoldcrochet.com/how-to-crochet-coral-mesh-crochet-video-tutorial-for-beginners-stitch-explorer-series/)
> - **Heart. Hook. Home.** — Argyle Shell Crochet Stitch Tutorial (https://hearthookhome.com/argyle-shell-crochet-stitch-tutorial/)

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | According to Amanda Crochets, what foundation chain length is required for the basket weave stitch? | A multiple of 6 stitches plus 4 more (chain length = 6n + 4, e.g. 10, 16, 22, 28...) | "Amanda Crochets says the basket-weave stitch starts with a foundation chain that must be a multiple of 6 stitches plus 4 extra stitches—she uses 16 chains as her example." | Relevant | Accurate |
| 2 | According to Hookfully's tutorial, how many incomplete stitches are worked into the same stitch to make one bobble, and how many loops are pulled through at the end? | 5 incomplete stitches, then pull through all 6 loops on the hook | "The tutorial works five incomplete stitches into the same stitch, then finishes by pulling all six loops on the hook through at the end." | Relevant | Accurate |
| 3 | According to Creations by Courtney, what two stitch types form the foundation row of the crochet heart pattern, and what stitches make up the heart motif itself? | Foundation row: treble and chain stitches. Heart motif: treble, double crochet, and single crochet stitches plus a picot detail | "The foundation row is worked with treble stitches and chain stitches. The heart motif itself is made from single-crochet stitches and slip stitches." | Partially relevant | Partially accurate |
| 4 | According to Stardust Crochet, what three techniques combine to make the coral mesh stitch? | A modified Solomon's knot, half double crochet, and chain stitches | "The coral mesh stitch is made by combining a modified Solomon's knot, chains, and half-double crochets." | Relevant | Accurate |
| 5 | What is the "modified Solomon's knot" loop length recommended in Stardust Crochet's coral mesh tutorial? | A loop of 1/2" to 3/4" is pulled up before working the yarn over and chain 1 | "The tutorial advises pulling up a long loop that is about ½ inch to ¾ inch long." | Relevant | Accurate |

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

**Question that failed:** "According to Creations by Courtney, what two stitch types form the foundation row of the crochet heart pattern?"

**What the system returned:** "According to Creations by Courtney, the foundation row is made of treble stitches and chain stitches." This sounds confident and specific, and both stitch types genuinely appear on that source's page — but when I inspected the actual retrieved chunks, none of the 4 top-k chunks contains a sentence that states "the foundation row is made of treble stitches and chain stitches." The closest chunk says "I chose to work the stitches into a treble stitch rather than chains, as chain stitches work great for creating a vertical row of hearts rather than a horizontal row" — which is discussing a design choice between two options, not describing the foundation row's composition. A second retrieved chunk lists "Ch(s): chain(s)... Tr: treble crochet" in a general abbreviation key, unconnected to "foundation row" specifically.

**Root cause (tied to a specific pipeline stage):** This is a retrieval + chunking issue, not a pure generation issue. Two of the top-4 retrieved chunks (Heart. Hook. Home. results) were about a completely unrelated stitch (Argyle Shell), diluting the context with off-topic material. Of the two Creations by Courtney chunks that were relevant, neither one contains the specific "foundation row" fact in one place — the actual answer likely lives in a chunk that wasn't retrieved, or is split by our 500-char chunking so the "foundation row" description and the treble/chain stitch names never appear together in a single chunk. The model then plausibly stitched together "treble" and "chain" from two nearby but disconnected chunk fragments into an answer that reads as one coherent fact, which is a subtle grounding failure: technically every word it used appears somewhere in the retrieved context, but the specific claim as stated isn't a direct restatement of any one passage — it's an inference across fragments, which is exactly the kind of response that "sounds authoritative but didn't strictly come from the retrieved text."

**What I would change to fix it:** (1) Increase chunk overlap or chunk size for pages with structural/procedural detail like this one, so a fact like "foundation row = X + Y" is less likely to be split across chunk boundaries. (2) Tighten the system prompt to explicitly forbid synthesizing a claim by combining facts from multiple non-adjacent chunks unless the combination is stated directly in at least one chunk — e.g., "only state a fact if it is explicitly present in a single excerpt; do not infer relationships between separate excerpts." (3) Consider a stricter distance-score cutoff so the two off-topic Heart. Hook. Home. chunks (which shouldn't have been within top-4 for a heart-pattern-specific query) don't get passed to the model as context at all.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Having the exact chunk size (500 characters) and overlap (75 characters) numbers pinned down in planning.md before writing any code meant `chunk_text()` in `chunk.py` had a concrete, testable target instead of a vague "chunk it reasonably" goal — when I ran `chunk.py` and inspected the sample chunks, I could directly check whether real chunks matched the reasoning I'd already written down (one instructional step per chunk), rather than discovering after the fact that my chunking logic didn't match my own justification. It also made prompting the AI tool for the chunking implementation much more precise, since I could hand it exact numbers instead of asking it to guess reasonable defaults.

**One way your implementation diverged from the spec, and why:** planning.md's Retrieval Approach section specified `all-MiniLM-L6-v2` and top-k=4, which I implemented as written and did not change. Where I did diverge from the original plan was the generation model: planning.md and the assignment instructions both pointed to specific Groq models (initially I tried `llama-3.3-70b-versatile`, then the assignment's recommended `meta-llama/llama-4-scout-17b-16e-instruct`), but neither was available on my Groq account when I checked with `client.models.list()`. I substituted `openai/gpt-oss-120b`, which is available on my key and, like the recommended models, is served through Groq's OpenAI-compatible chat completions endpoint, so no other part of the pipeline needed to change. I documented this substitution directly in a code comment in `generate.py` rather than silently swapping it, since a grader or future me re-running this project might hit the same unavailable-model error.

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

- *What I gave the AI:* My planning.md Documents table (10 source URLs) and Chunking Strategy section (500-char chunks, 75-char overlap, and my reasoning about instructional steps), and asked it to implement `ingest.py` (scrape + clean each URL into plain text) and `chunk.py` (`chunk_text()` matching my exact spec).
- *What it produced:* A working scraper using `requests` + BeautifulSoup with a generic "strip noise by CSS class/id keyword" cleaning step, and a chunker that split text into 500-char windows with 75-char overlap on word boundaries.
- *What I changed or overrode:* The first version of `clean_html()` was too aggressive — a generic "sidebar" keyword matched an unrelated Neve-theme layout class (`nv-sidebar-right`) and deleted entire article bodies, and the generic "widget" keyword matched Elementor's own content-wrapper class (`elementor-widget-container`) on another site, reducing several documents to a few dozen characters of just the page title. I diagnosed this by inspecting raw HTML and intermediate soup output per-site, then rewrote the cleaning logic to scope noise-removal to inside the already-identified content root (instead of the whole page) and dropped the overly generic "widget"/"share" keywords in favor of more specific ones. I verified the fix by re-running ingestion and confirming all 10 documents came back with substantial (1,600–5,500 char) content instead of near-empty stubs.

**Instance 2**

- *What I gave the AI:* My planning.md Retrieval Approach section (all-MiniLM-L6-v2, top-k=4, ChromaDB) and the assignment's suggested prompt template and Gradio skeleton, and asked it to implement `embed.py` (embedding + ChromaDB storage + `retrieve()`), `generate.py` (grounded generation with programmatic source attribution), `query.py` (an `ask()` entry point), and `app.py` (the Gradio UI).
- *What it produced:* A working embed/retrieve pipeline, a `generate_answer()` function with a grounding system prompt initially targeting `llama-3.3-70b-versatile`, and a Gradio `Interface`.
- *What I changed or overrode:* (1) The initial generation model didn't exist on my Groq key (404 error), so I had the AI list available models via `client.models.list()` and substitute `openai/gpt-oss-120b`. (2) During grounding tests, the model inserted an inline citation marker (`【Excerpt 1 — Amanda Crochets】`) into its answer text despite the system prompt telling it not to — I had the AI add a regex-based `_strip_citation_markers()` safety net rather than trusting the prompt instruction alone, since "instructed not to" and "structurally cannot" are different guarantees. (3) I rebuilt the Gradio interface from the initial `gr.Interface` version to a `gr.Blocks` version with a submit button and Enter-to-submit, matching the assignment's suggested code pattern more closely, and split source attribution into its own output field rather than combining it into the answer text.
