import os
import pytest
from app.services.kaggle_service import search_kaggle, download_kaggle

def test_search_kaggle():
    results = search_kaggle("iris")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "ref" in results[0]
    assert "title" in results[0]
    assert "url" in results[0]

def test_download_kaggle(tmp_path):
    dataset_ref = "uciml/iris"
    result = download_kaggle(dataset_ref, "iris_collection")

    assert result["inserted"] > 0
    assert result["collection"] == "iris_collection"
