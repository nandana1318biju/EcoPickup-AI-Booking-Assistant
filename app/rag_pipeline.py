# app/rag_pipeline.py

import os
import tempfile
import pdfplumber
import streamlit as st
from typing import List, Dict

import chromadb
from chromadb.utils import embedding_functions

# ------------------------------
# Embedding model
# ------------------------------
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE = 700
CHUNK_OVERLAP = 100

@st.cache_resource
def load_embed_fn():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL_NAME
    )

embed_fn = load_embed_fn()

# ------------------------------
# Initialize ChromaDB client & collection
# ------------------------------
@st.cache_resource
def get_chroma_collection():
    client = chromadb.Client()

    return client.get_or_create_collection(
        name="ecopickup_docs",
        metadata={"hnsw:space": "cosine"},
        embedding_function=embed_fn
    )

collection = get_chroma_collection()


# ------------------------------
# PDF Extraction
# ------------------------------
def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF using pdfplumber."""
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        path = tmp.name

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    finally:
        try:
            os.remove(path)
        except:
            pass

    return text


def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> List[str]:
    """Chunk text into overlapping segments."""
    text = text.replace("\r", " ")
    chunks = []
    start = 0
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


# ------------------------------
# Add uploaded PDFs to vector store
# ------------------------------
def add_documents_from_uploaded_files(uploaded_files):
    ids = []
    documents = []
    metadatas = []

    for f in uploaded_files:
        raw = f.read()
        text = extract_text_from_pdf_bytes(raw)
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            ids.append(f"{f.name}_{i}")
            documents.append(chunk)
            metadatas.append({
                "source": f.name,
                "text": chunk
            })

    if not documents:
        return {"success": False, "message": "No text extracted from uploaded PDFs."}

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )

    return {"success": True, "added_chunks": len(documents)}


# ------------------------------
# Retrieval
# ------------------------------
def retrieve(query: str, top_k: int = 4) -> List[Dict]:
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    if not results or not results.get("metadatas"):
        return []

    metadatas = results["metadatas"][0]
    return metadatas


# ------------------------------
# Build RAG Prompt
# ------------------------------
def rag_answer(query: str, top_k=4):
    snippets = retrieve(query, top_k)

    if not snippets:
        return {
            "success": False,
            "answer": "No documents found. Please upload PDFs first.",
            "sources": []
        }

    # Prepare context block
    context = "\n\n".join(
        [f"Source: {s['source']}\n{s['text']}" for s in snippets]
    )

    prompt = (
        "You are EcoPickup assistant. Use ONLY the following document snippets to answer. "
        "If the answer is not found in the text, say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"User question: {query}\n\n"
        "Answer concisely and cite sources:"
    )

    return {
        "success": True,
        "prompt": prompt,
        "sources": snippets
    }
