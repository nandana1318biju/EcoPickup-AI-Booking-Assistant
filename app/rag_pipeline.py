# app/rag_pipeline.py
import os
import tempfile
import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict
import streamlit as st

# Model for embeddings
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
# default chunk sizes (chars)
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

# Load embedder once
@st.cache_resource
def load_embedder():
    return SentenceTransformer(EMBED_MODEL_NAME)

embedder = load_embedder()


# -------------------------
# Text extraction + chunking
# -------------------------
def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from a PDF bytes blob using pdfplumber."""
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    finally:
        try:
            os.remove(tmp_path)
        except:
            pass

    return text


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Chunk text into overlapping chunks of approx chunk_size characters."""
    if not text:
        return []
    text = text.replace("\r", " ")
    start = 0
    chunks = []
    L = len(text)
    while start < L:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


# -------------------------
# Vector store helpers
# -------------------------
def _normalize(vecs: np.ndarray) -> np.ndarray:
    """L2-normalize vectors row-wise."""
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1e-10
    return vecs / norms


def create_faiss_index(dim: int):
    """Create a FAISS index for inner-product (works with normalized vectors for cosine)."""
    index = faiss.IndexFlatIP(dim)
    return index


def embed_texts(texts: List[str]) -> np.ndarray:
    """Return normalized embeddings for a list of texts."""
    if len(texts) == 0:
        return np.zeros((0, embedder.get_sentence_embedding_dimension()), dtype="float32")
    vecs = embedder.encode(texts, convert_to_numpy=True)
    vecs = vecs.astype("float32")
    vecs = _normalize(vecs)
    return vecs


# -------------------------
# Build / add documents to vector store (stored in st.session_state)
# -------------------------
def init_vector_store():
    """Initialize vector store in session_state if not present."""
    if "vector_store" not in st.session_state:
        st.session_state["vector_store"] = {
            "index": None,          # faiss index
            "metadatas": [],        # list of dicts: {"text": chunk_text, "source": filename}
            "emb_dim": None
        }


def add_documents_from_uploaded_files(uploaded_files):
    """
    uploaded_files: list of UploadedFile objects from st.file_uploader
    This function will extract text, chunk, embed, and add to FAISS index.
    """
    init_vector_store()
    vs = st.session_state["vector_store"]

    all_chunks = []
    all_metas = []
    for f in uploaded_files:
        raw = f.read()
        text = extract_text_from_pdf_bytes(raw)
        chunks = chunk_text(text)
        for c in chunks:
            all_chunks.append(c)
            all_metas.append({"text": c, "source": getattr(f, "name", "uploaded_pdf")})

    if len(all_chunks) == 0:
        return {"success": False, "message": "No text extracted from uploaded PDFs."}

    vecs = embed_texts(all_chunks)
    dim = vecs.shape[1]

    # initialize index if needed
    if vs["index"] is None:
        vs["index"] = create_faiss_index(dim)
        vs["emb_dim"] = dim

    # if dimension mismatch, re-create index (simple approach)
    if vs["emb_dim"] != dim:
        vs["index"] = create_faiss_index(dim)
        vs["metadatas"] = []
        vs["emb_dim"] = dim

    # add vectors and metadata
    vs["index"].add(vecs)
    vs["metadatas"].extend(all_metas)

    return {"success": True, "added_chunks": len(all_chunks)}


# -------------------------
# Retrieval
# -------------------------
def retrieve(query: str, top_k: int = 4) -> List[Dict]:
    """Return top_k metadata dicts (with 'text' and 'source') for the query."""
    init_vector_store()
    vs = st.session_state["vector_store"]
    if vs["index"] is None or len(vs["metadatas"]) == 0:
        return []

    qvec = embed_texts([query])
    D, I = vs["index"].search(qvec, top_k)
    I = I[0]
    results = []
    for idx in I:
        if idx < 0 or idx >= len(vs["metadatas"]):
            continue
        results.append(vs["metadatas"][idx])
    return results


# -------------------------
# RAG answer builder (returns text)
# -------------------------
def rag_answer(query: str, top_k: int = 4) -> Dict:
    """
    Returns:
    {
      "success": True/False,
      "answer": "text",
      "sources": [ {"source": filename, "text": snippet}, ... ]
    }
    """
    snippets = retrieve(query, top_k=top_k)
    if not snippets:
        return {"success": True, "answer": "I don't have any uploaded documents to search. Please upload PDFs first.", "sources": []}

    # Build context string
    context = "\n\n".join([f"Source: {s.get('source', '')}\n{s.get('text','')}" for s in snippets])

    # Short prompt to LLM (the actual LLM call will be in tools/llm)
    prompt = (
        "You are EcoPickup assistant. Use the following document snippets to answer the user's question. "
        "If the answer cannot be found in the snippets, say you don't know and offer to help otherwise.\n\n"
        f"Context:\n{context}\n\nUser question: {query}\n\nAnswer concisely and cite sources (filename) if applicable:"
    )

    # Return prompt + snippets so the caller can pass to an LLM
    return {"success": True, "prompt": prompt, "sources": snippets}
