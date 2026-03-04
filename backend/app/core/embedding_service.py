import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle
import os
from dotenv import load_dotenv

load_dotenv()


# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_DIR = "storage/processed"
INDEX_FILE = os.path.join(VECTOR_DIR, "faiss_index.bin")
META_FILE = os.path.join(VECTOR_DIR, "metadata.pkl")


def embed_chunks(chunks):
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts)

    return np.array(embeddings).astype("float32")


def store_in_faiss(chunks, embeddings):

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    os.makedirs(VECTOR_DIR, exist_ok=True)

    faiss.write_index(index, INDEX_FILE)

    with open(META_FILE, "wb") as f:
        pickle.dump(chunks, f)