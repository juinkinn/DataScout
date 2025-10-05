from pinecone import Pinecone, ServerlessSpec
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
