"""
Script para processar o PDF do Tortora em chunks + embeddings.

Uso:
    python scripts/index_tortora.py /caminho/para/tortora.pdf

Output:
    data/tortora_chunks.json  — chunks de texto com metadata
    data/embeddings.npz       — embeddings pre-computados
"""

import json
import sys
from pathlib import Path

import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_DIR = Path(__file__).parent.parent / "data"
CHUNK_SIZE = 500  # tokens approx (chars / 4)
CHUNK_OVERLAP = 50


def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """Extract text from PDF, organized by page."""
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():
            pages.append({
                "page": i + 1,
                "text": text.strip(),
            })
    doc.close()
    print(f"Extracted {len(pages)} pages with text")
    return pages


def chunk_text(pages: list[dict], chunk_chars: int = 2000, overlap_chars: int = 200) -> list[dict]:
    """Split pages into overlapping chunks."""
    chunks = []
    for page_data in pages:
        text = page_data["text"]
        page_num = page_data["page"]

        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) > chunk_chars and current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "section": f"Page {page_num}",
                    "page": page_num,
                })
                # Keep overlap
                current_chunk = current_chunk[-overlap_chars:] + "\n\n" + para
            else:
                current_chunk += "\n\n" + para if current_chunk else para

        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "section": f"Page {page_num}",
                "page": page_num,
            })

    print(f"Created {len(chunks)} chunks")
    return chunks


def compute_embeddings(chunks: list[dict], model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    """Compute embeddings for all chunks."""
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)

    texts = [c["text"] for c in chunks]
    print(f"Computing embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

    return np.array(embeddings)


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/index_tortora.py <caminho_para_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not Path(pdf_path).exists():
        print(f"Ficheiro não encontrado: {pdf_path}")
        sys.exit(1)

    DATA_DIR.mkdir(exist_ok=True)

    # Extract
    pages = extract_text_from_pdf(pdf_path)

    # Chunk
    chunks = chunk_text(pages)

    # Save chunks
    chunks_path = DATA_DIR / "tortora_chunks.json"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"Saved chunks to {chunks_path}")

    # Embeddings
    embeddings = compute_embeddings(chunks)

    # Save embeddings
    embeddings_path = DATA_DIR / "embeddings.npz"
    np.savez_compressed(embeddings_path, embeddings=embeddings)
    print(f"Saved embeddings to {embeddings_path}")

    print("\nDone! Knowledge base ready.")
    print(f"  Chunks: {len(chunks)}")
    print(f"  Embeddings shape: {embeddings.shape}")


if __name__ == "__main__":
    main()
