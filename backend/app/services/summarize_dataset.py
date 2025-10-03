import os
import pandas as pd
import faiss
import numpy as np
from google import genai
from sentence_transformers import SentenceTransformer
from ..core.config import settings

gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)

DIM = 3072  
index = faiss.IndexFlatL2(DIM)
metadata = []

FAISS_INDEX_FILE = "faiss_index.bin"
METADATA_FILE = "metadata.pkl"

def save_faiss_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    pd.DataFrame(metadata).to_pickle(METADATA_FILE)

def load_faiss_index():
    global index, metadata
    if os.path.exists(FAISS_INDEX_FILE):
        index = faiss.read_index(FAISS_INDEX_FILE)
        metadata = pd.read_pickle(METADATA_FILE).to_dict('records')

load_faiss_index()

def summarize_dataset(df: pd.DataFrame, dataset_name: str) -> str:
    sample_data = df.head(5).to_dict()
    prompt = f"""
Dataset: {dataset_name}
Please provide a short summary including:
- Content of the dataset
- Main columns
- Data types (numerical, categorical)
- Potential applications
Sample rows: {sample_data}
"""
    response = gemini_client.responses.create(
        model="gemini-1.5",
        prompt=prompt,
        max_output_tokens=300
    )
    summary = response.output_text
    return summary


def embed_text(text: str) -> np.ndarray:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(text, convert_to_numpy=True)

def save_to_faiss(user_id: str, dataset_name: str, summary: str, embedding: np.ndarray, source: str = "kaggle"):
    index.add(np.expand_dims(embedding, axis=0))
    metadata.append({
        "user_id": user_id,
        "dataset_name": dataset_name,
        "summary": summary,
        "source": source
    })
    save_faiss_index()

def process_dataset_for_faiss(user_id: str, csv_path: str, dataset_name: str, source: str = "kaggle"):
    df = pd.read_csv(csv_path)
    summary = summarize_dataset(df, dataset_name)
    embedding = embed_text(summary)
    save_to_faiss(user_id, dataset_name, summary, embedding, source)
    return {
        "user_id": user_id,
        "dataset_name": dataset_name,
        "summary": summary,
        "source": source
    }

def search_faiss(query: str, top_k: int = 5):
    q_emb = embed_text(query)
    D, I = index.search(np.expand_dims(q_emb, axis=0), top_k)
    results = [metadata[i] for i in I[0]]
    return results
