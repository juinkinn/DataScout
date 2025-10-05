from app.database import datasets_db

def test_insert_sample():
    col = datasets_db["sample_collection"]

    result = col.insert_one({"name": "Test", "value": 123})
    print("Inserted ID:", result.inserted_id)

    print("Collections after insert:", datasets_db.list_collection_names())

    assert "sample_collection" in datasets_db.list_collection_names()


def test_mongo_connection():
    collections = datasets_db.list_collection_names()
    print("Collections:", collections)
    assert datasets_db.name == "kaggle_datasets"
