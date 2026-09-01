"""
Chunking stage of the pipeline (see planning.md ## Chunking Strategy).

Splits each cleaned document in documents/ into ~500-character chunks with
75-character overlap, sized so each chunk holds roughly one instructional
step or tip without splitting a stitch instruction across a hard boundary.
"""

from dataclasses import dataclass
from pathlib import Path

DOCUMENTS_DIR = Path(__file__).parent / "documents"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 75


@dataclass
class Chunk:
    doc_id: str
    source: str
    url: str
    chunk_index: int
    text: str


def parse_document(path: Path) -> tuple[dict, str]:
    """Split a documents/*.txt file into its header metadata and body text."""
    raw = path.read_text(encoding="utf-8")
    header, _, body = raw.partition("---\n")

    metadata = {"id": path.stem}
    for line in header.strip().splitlines():
        key, _, value = line.partition(":")
        metadata[key.strip().lower()] = value.strip()

    return metadata, body.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping fixed-size chunks.

    Cuts are made on the nearest preceding whitespace within the window so a
    chunk doesn't end mid-word; overlap re-includes the tail of the previous
    chunk so an instruction split across the boundary still appears whole in
    at least one chunk.
    """
    text = text.strip()
    if len(text) <= chunk_size:
        return [text] if text else []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        if end < text_length:
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap

    return chunks


def chunk_all_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[Chunk]:
    all_chunks = []
    for path in sorted(documents_dir.glob("*.txt")):
        metadata, body = parse_document(path)
        for index, text in enumerate(chunk_text(body)):
            all_chunks.append(
                Chunk(
                    doc_id=metadata.get("id", path.stem),
                    source=metadata.get("source", "unknown"),
                    url=metadata.get("url", ""),
                    chunk_index=index,
                    text=text,
                )
            )
    return all_chunks


if __name__ == "__main__":
    chunks = chunk_all_documents()
    print(f"Produced {len(chunks)} chunks from {len(list(DOCUMENTS_DIR.glob('*.txt')))} documents.\n")
    for chunk in chunks[:5]:
        print(f"--- {chunk.doc_id} [{chunk.chunk_index}] ({len(chunk.text)} chars) ---")
        print(chunk.text[:200].replace("\n", " ") + "...")
        print()
