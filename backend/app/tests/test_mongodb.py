from app.database import db

def test_insert_sample():
    col = db["sample_collection"]

    result = col.insert_one({"name": "Test", "value": 123})
    print("Inserted ID:", result.inserted_id)

    print("Collections after insert:", db.list_collection_names())

    assert "sample_collection" in db.list_collection_names()


def test_mongo_connection():
    collections = db.list_collection_names()
    print("Collections:", collections)
    assert db.name == "kaggle_datasets"
