from sentence_transformers import SentenceTransformer
import numpy as np

def embed_text(text: str) -> np.ndarray:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text, convert_to_numpy=True)