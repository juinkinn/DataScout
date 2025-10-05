import os
from pinecone import Pinecone, ServerlessSpec
import numpy as np
from ..services import embed_text
from ..core.config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

INDEX_NAME = "dataset-index"
DIM = 384

if INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIM,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(INDEX_NAME)

def add_to_pinecone(embedding: np.ndarray, meta: dict):
    vector_id = f"{meta['user_id']}_{meta['dataset_name']}"
    index.upsert(vectors=[{
        "id": vector_id,
        "values": embedding.tolist(),
        "metadata": meta
    }])
    return {"status": "inserted", "id": vector_id}


def search_pinecone(query: str, top_k: int = 5):
    query_embedding = embed_text(query)
    res = index.query(vector=query_embedding.tolist(), top_k=top_k, include_metadata=True)
    return [match["metadata"] for match in res["matches"]]
