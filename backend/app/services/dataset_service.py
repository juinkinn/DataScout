import subprocess
import os
import pandas as pd
import google.generativeai as genai
from ..core.config import settings
from ..crud.vectorstore import create_vector
from .text_handle_service import embed_text
from ..crud.user_dataset import insert_user_dataset


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

    create_vector(embedding, {
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

def download_kaggle_dataset(dataset_ref: str) -> str:
    download_path = f"/tmp/{dataset_ref.replace('/', '_')}"
    os.makedirs(download_path, exist_ok=True)

    subprocess.check_call([
        "kaggle", "datasets", "download", "-d", dataset_ref,
        "--path", download_path, "--unzip"
    ])
    return download_path

def add_dataset_to_collection(dataset_ref: str, user_id: str):
    download_path = download_kaggle_dataset(dataset_ref)
    total_inserted = 0

    for file in os.listdir(download_path):
        if file.endswith(".csv"):
            csv_path = os.path.join(download_path, file)
            inserted = insert_user_dataset(user_id, dataset_ref, csv_path)
            total_inserted += inserted

            process_dataset(
                user_id=user_id,
                csv_path=csv_path,
                dataset_name=file,
                source="kaggle"
            )

    return {
        "user_id": user_id,
        "dataset_ref": dataset_ref,
        "inserted": total_inserted
    }