import os
import pytest
from app.services import search_kaggle, add_dataset_to_collection

def test_search_kaggle():
    results = search_kaggle("iris")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "ref" in results[0]
    assert "title" in results[0]
    assert "url" in results[0]

def test_add_dataset_to_collection(tmp_path):
    dataset_ref = "uciml/iris"
    result = add_dataset_to_collection(dataset_ref, "iris_collection")

    assert result["inserted"] > 0
    assert result["collection"] == "iris_collection"
