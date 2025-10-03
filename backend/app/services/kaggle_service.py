import subprocess
import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from app.database import db
from .summarize_dataset import process_dataset_for_faiss

def search_kaggle(query):
    api = KaggleApi()
    api.authenticate()
    datasets = api.dataset_list(search=query)
    return [
        {
            "ref": d.ref,
            "title": d.title,
            "subtitle": d.subtitle,
            "url": d.url
        }
        for d in datasets
    ]

def download_kaggle(dataset_ref: str, collection_name: str, user_id: str):
    download_path = f"/tmp/{dataset_ref.replace('/', '_')}"
    os.makedirs(download_path, exist_ok=True)

    subprocess.check_call([
        "kaggle", "datasets", "download", "-d", dataset_ref,
        "--path", download_path, "--unzip"
    ])

    inserted = 0
    for file in os.listdir(download_path):
        if file.endswith(".csv"):
            csv_path = os.path.join(download_path, file)
            df = pd.read_csv(csv_path)

            records = df.to_dict(orient="records")
            if records:
                for r in records:
                    r.setdefault("_source", "kaggle")
                    r.setdefault("_dataset_ref", dataset_ref)
                db[collection_name].insert_many(records)
                inserted += len(records)

            dataset_name = file
            process_dataset_for_faiss(user_id=user_id, csv_path=csv_path, dataset_name=dataset_name, source="kaggle")

    return {"collection": collection_name, "inserted": inserted}
