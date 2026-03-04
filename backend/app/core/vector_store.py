import faiss
import numpy as np

index = None
stored_chunks = []


def build_index(embeddings, chunks):

    global index, stored_chunks

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    stored_chunks = chunks


def search(query_embedding, top_k=5):

    global index, stored_chunks

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        results.append(stored_chunks[idx])

    return results