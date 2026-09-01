"""
Document Ingestion stage of the pipeline (see planning.md ## Architecture).

Fetches each crochet tutorial URL, strips it down to the main article text
(dropping nav bars, ads, scripts, and comment sections), and writes one
plain-text file per source into documents/.
"""

import re
from dataclasses import dataclass
from pathlib import Path

import requests
from bs4 import BeautifulSoup

DOCUMENTS_DIR = Path(__file__).parent / "documents"

# Matches the "Documents" table in planning.md.
SOURCES = [
    {
        "id": "shell_stitch_the_spruce_crafts",
        "source": "The Spruce Crafts",
        "description": "How to Crochet Shell Stitch",
        "url": "https://www.thesprucecrafts.com/how-to-crochet-a-shell-stitch-979096",
    },
    {
        "id": "argyle_shell_heart_hook_home",
        "source": "Heart. Hook. Home.",
        "description": "Argyle Shell Crochet Stitch Tutorial",
        "url": "https://hearthookhome.com/argyle-shell-crochet-stitch-tutorial/",
    },
    {
        "id": "basket_weave_amanda_crochets",
        "source": "Amanda Crochets: Handmade with Love",
        "description": "How to Make the Basket Weave Stitch",
        "url": "https://www.amandacrochets.com/how-to-make-the-basket-weave-stitch/",
    },
    {
        "id": "bobble_stitch_hookfully",
        "source": "Hookfully: Happy Crochet Family",
        "description": "Bobble Stitch Tutorial",
        "url": "https://hookfully.com/bobble-stitch-tutorial/",
    },
    {
        "id": "blackberry_salad_handmade_by_stacy_j",
        "source": "Handmade by Stacy J",
        "description": "Blackberry Salad Crochet Stitch",
        "url": "https://handmadebystacyj.com/2020/03/14/blackberry-salad-crochet-tutorial/",
    },
    {
        "id": "crochet_heart_creations_by_courtney",
        "source": "Creations by Courtney",
        "description": "Crochet Heart: Stitch Tutorial",
        "url": "https://creationsbycourtney.com/crochet-heart-stitch-tutorial/",
    },
    {
        "id": "lacy_shell_selina_veronique",
        "source": "Selina Veronique: Crochet-DIY-Lifestyle",
        "description": "Crochet Lacy Shell Stitch Free Pattern",
        "url": "https://www.selinaveronique.com/crochet-lacy-shell-stitch-free-pattern",
    },
    {
        "id": "coral_mesh_stardust_crochet",
        "source": "Stardust Crochet: Inspire, Learn, Create",
        "description": "How to Crochet: Coral Mesh; Stitch Explorer Series",
        "url": "https://stardustgoldcrochet.com/how-to-crochet-coral-mesh-crochet-video-tutorial-for-beginners-stitch-explorer-series/",
    },
    {
        "id": "bead_stitch_stardust_crochet",
        "source": "Stardust Crochet: Inspire, Learn, Create",
        "description": "How to Crochet: Bead Stitch; Stitch Explorer Series",
        "url": "https://stardustgoldcrochet.com/how-to-crochet-bead-stitch-video-tutorial-for-beginners-stitch-explorer-series/",
    },
    {
        "id": "mesh_cluster_rich_textures_crochet",
        "source": "Rich Textures Crochet",
        "description": "Mesh Cluster Stitch; How to Crochet",
        "url": "https://richtexturescrochet.com/mesh-cluster-stitch/",
    },
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

# Tags that never contain the tutorial's own instructional text.
STRIP_TAGS = [
    "script", "style", "nav", "footer", "header", "aside", "form",
    "iframe", "noscript", "svg", "button",
]


@dataclass
class Document:
    id: str
    source: str
    description: str
    url: str
    text: str


def clean_html(html: str) -> str:
    """Strip boilerplate and collapse whitespace, keeping the article prose."""
    soup = BeautifulSoup(html, "html.parser")

    for tag_name in STRIP_TAGS:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Narrow to the article/main content root FIRST, so noise-keyword stripping
    # below can't nuke everything via an unrelated layout-class ancestor
    # (e.g. a theme wrapper div named "nv-sidebar-right" that just controls
    # page layout, not an actual sidebar widget).
    #
    # Prefer the largest of several common "this is the actual post body"
    # containers, since some page builders (e.g. Elementor) put unrelated
    # "related posts" teasers in <article> tags and the real content in a
    # widget div instead.
    candidates = soup.find_all("article") + soup.find_all(
        class_=["elementor-widget-theme-post-content", "entry-content", "post-content"]
    )
    article = max(candidates, key=lambda tag: len(tag.get_text()), default=None) or (
        soup.find("main") or soup.body or soup
    )

    # Drop obvious non-content blocks (comments, related-post widgets, ads)
    # by class/id keyword, since blog themes vary too much to rely on one tag.
    # "widget" and "share" are deliberately excluded: page builders like
    # Elementor name their generic content wrappers "elementor-widget-*",
    # and "share" alone matches unrelated classes too often — both caused
    # the entire article body to be decomposed on some sources.
    NOISE_KEYWORDS = ("comment", "sidebar", "related-post", "advert", "newsletter", "social-share")
    for tag in article.find_all(True):
        if tag.attrs is None:
            continue  # already decomposed as a child of an earlier noise match
        attr_text = " ".join(tag.get("class", []) + [tag.get("id", "")]).lower()
        if any(keyword in attr_text for keyword in NOISE_KEYWORDS):
            tag.decompose()

    text = article.get_text(separator="\n")

    # Collapse repeated blank lines / spaces left behind by decomposed tags.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Strip social-share button text (e.g. "11368 shares Share 2088 Tweet
    # Reddit 8 Threads") that some themes render as plain text rather than
    # a class we can target with NOISE_KEYWORDS.
    text = re.sub(
        r"\b[\d,]+\s*shares?\b.*?\b(Tweet|Reddit|Threads|Pinterest|Flipboard)\b",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    return text.strip()


def fetch_document(source: dict) -> Document:
    response = requests.get(source["url"], headers=HEADERS, timeout=15)
    response.raise_for_status()
    text = clean_html(response.text)
    return Document(
        id=source["id"],
        source=source["source"],
        description=source["description"],
        url=source["url"],
        text=text,
    )


def save_document(document: Document, out_dir: Path = DOCUMENTS_DIR) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{document.id}.txt"
    header = (
        f"SOURCE: {document.source}\n"
        f"DESCRIPTION: {document.description}\n"
        f"URL: {document.url}\n"
        f"---\n"
    )
    path.write_text(header + document.text, encoding="utf-8")
    return path


def ingest_all(sources: list[dict] = SOURCES) -> list[Document]:
    """Fetch + clean every source, saving each to documents/, skipping failures."""
    documents = []
    for source in sources:
        try:
            document = fetch_document(source)
            save_document(document)
            documents.append(document)
            print(f"[ok]   {source['id']} ({len(document.text)} chars)")
        except requests.RequestException as exc:
            print(f"[fail] {source['id']} -> {exc}")
    return documents


if __name__ == "__main__":
    ingest_all()
