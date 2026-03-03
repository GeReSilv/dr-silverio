import json
import logging
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"

_chunks: list[dict] = []
_embeddings: np.ndarray | None = None
_model = None


def _get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Sentence transformer model loaded")
        except Exception as e:
            logger.warning(f"Could not load sentence transformer: {e}")
    return _model


def load_knowledge_base():
    """Load pre-processed chunks and embeddings from disk."""
    global _chunks, _embeddings

    chunks_path = DATA_DIR / "tortora_chunks.json"
    embeddings_path = DATA_DIR / "embeddings.npz"

    if chunks_path.exists():
        with open(chunks_path, "r", encoding="utf-8") as f:
            _chunks = json.load(f)
        logger.info(f"Loaded {len(_chunks)} chunks from knowledge base")
    else:
        logger.warning("No tortora_chunks.json found — RAG disabled")
        return

    if embeddings_path.exists():
        data = np.load(embeddings_path)
        _embeddings = data["embeddings"]
        logger.info(f"Loaded embeddings: shape {_embeddings.shape}")
    else:
        logger.warning("No embeddings.npz found — RAG disabled")


def search(query: str, top_k: int = 3) -> str:
    """Search knowledge base for relevant context."""
    if not _chunks or _embeddings is None:
        return ""

    model = _get_model()
    if model is None:
        return ""

    try:
        query_embedding = model.encode([query])[0]
        similarities = np.dot(_embeddings, query_embedding) / (
            np.linalg.norm(_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        context_parts = []
        for idx in top_indices:
            if similarities[idx] > 0.3:
                chunk = _chunks[idx]
                section = chunk.get("section", "")
                text = chunk.get("text", "")
                context_parts.append(f"[{section}]\n{text}")

        return "\n\n---\n\n".join(context_parts)
    except Exception as e:
        logger.error(f"RAG search error: {e}")
        return ""
