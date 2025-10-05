import pandas as pd
import google.generativeai as genai
from ..core.config import settings
from ..database import pinecone_vector_database  
from .text_handle_service import embed_text

genai.configure(api_key=settings.GEMINI_API_KEY)

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
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


def process_dataset(user_id: str, csv_path: str, dataset_name: str, source: str = "kaggle"):
    print("Processing Dataset")
    df = pd.read_csv(csv_path)
    summary = summarize_dataset(df, dataset_name)
    embedding = embed_text(summary)

    pinecone_vector_database.add_to_pinecone(embedding, {
        "user_id": user_id,
        "dataset_name": dataset_name,
        "summary": summary,
        "source": source
    })

    return {
        "user_id": user_id,
        "dataset_name": dataset_name,
        "summary": summary,
        "source": source
    }
