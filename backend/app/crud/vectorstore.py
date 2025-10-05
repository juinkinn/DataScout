import numpy as np
from ..database.pinecone_vector_database import index
from ..services.text_handle_service import embed_text

def create_vector(embedding: np.ndarray, meta: dict):
    vector_id = f"{meta['user_id']}_{meta['dataset_name']}"
    index.upsert(vectors=[{
        "id": vector_id,
        "values": embedding.tolist(),
        "metadata": meta
    }])
    return {"status": "inserted", "id": vector_id}


def read_vectors(query: str, top_k: int = 5):
    query_embedding = embed_text(query)
    res = index.query(
        vector=query_embedding.tolist(),
        top_k=top_k,
        include_metadata=True
    )
    return [match["metadata"] for match in res["matches"]]


def delete_vector(vector_id: str):
    index.delete(ids=[vector_id])
    return {"status": "deleted", "id": vector_id}
