"""
Embedding + Vector Store and Retrieval stages of the pipeline
(see planning.md ## Retrieval Approach and ## Architecture).

Embeds each chunk from chunk.py with all-MiniLM-L6-v2 and stores it in a
persistent ChromaDB collection along with its source metadata (source name,
description, URL, doc id) so retrieved results can be attributed. Also
exposes retrieve(query, k=4) for the Generation stage to call.
"""

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from chunk import Chunk, chunk_all_documents, parse_document, DOCUMENTS_DIR

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_DB_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "crochet_stitches"
TOP_K = 4

_model = None


def get_model() -> SentenceTransformer:
    """Lazily load the embedding model once per process."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def get_collection(db_dir: Path = CHROMA_DB_DIR):
    client = chromadb.PersistentClient(path=str(db_dir))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def _chunk_metadata(chunk: Chunk, doc_metadata: dict) -> dict:
    return {
        "doc_id": chunk.doc_id,
        "chunk_index": chunk.chunk_index,
        "source": chunk.source,
        "description": doc_metadata.get("description", ""),
        "url": chunk.url,
    }


def embed_and_store(
    chunks: list[Chunk] | None = None,
    documents_dir: Path = DOCUMENTS_DIR,
    db_dir: Path = CHROMA_DB_DIR,
) -> int:
    """
    Embed every chunk with all-MiniLM-L6-v2 and upsert it into ChromaDB,
    attaching source/description/url metadata so results are attributable
    back to a specific tutorial. Returns the number of chunks stored.
    """
    if chunks is None:
        chunks = chunk_all_documents(documents_dir)
    if not chunks:
        return 0

    # doc_id -> parsed header metadata (source/description/url), so each
    # chunk's stored metadata includes the description from planning.md's
    # Documents table, not just what chunk.py already carries.
    doc_metadata_by_id = {}
    for path in documents_dir.glob("*.txt"):
        metadata, _ = parse_document(path)
        doc_metadata_by_id[metadata.get("id", path.stem)] = metadata

    model = get_model()
    collection = get_collection(db_dir)

    texts = [chunk.text for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=False).tolist()
    ids = [f"{chunk.doc_id}__{chunk.chunk_index}" for chunk in chunks]
    metadatas = [
        _chunk_metadata(chunk, doc_metadata_by_id.get(chunk.doc_id, {}))
        for chunk in chunks
    ]

    collection.upsert(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    return len(chunks)


def retrieve(query: str, k: int = TOP_K, db_dir: Path = CHROMA_DB_DIR) -> list[dict]:
    """
    Retrieve the top-k chunks most semantically similar to query.

    Returns a list of dicts: {text, source, description, url, doc_id,
    chunk_index, distance}, ordered from most to least similar.
    """
    model = get_model()
    collection = get_collection(db_dir)

    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)

    retrieved = []
    for text, metadata, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        retrieved.append(
            {
                "text": text,
                "source": metadata.get("source", "unknown"),
                "description": metadata.get("description", ""),
                "url": metadata.get("url", ""),
                "doc_id": metadata.get("doc_id", ""),
                "chunk_index": metadata.get("chunk_index", -1),
                "distance": distance,
            }
        )
    return retrieved


if __name__ == "__main__":
    count = embed_and_store()
    print(f"Embedded and stored {count} chunks in ChromaDB at {CHROMA_DB_DIR}\n")

    sample_queries = [
        "How do I make the basket weave stitch?",
        "What stitches create a raised bumpy texture?",
    ]
    for query in sample_queries:
        print(f"Query: {query!r}")
        for i, result in enumerate(retrieve(query), 1):
            preview = result["text"][:150].replace("\n", " ")
            print(f"  {i}. [{result['source']}] (distance={result['distance']:.3f}) {preview}...")
        print()
