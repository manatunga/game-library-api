from __future__ import annotations

import pytest
import mongomock
from unittest.mock import patch
from fastapi.testclient import TestClient

@pytest.fixture
def mock_collection():
    mock_client = mongomock.MongoClient()
    mock_collection = mock_client["test_db"]["games"]

    with patch("routes.games.games_collection", mock_collection):
        yield mock_collection

    mock_collection.delete_many({})


@pytest.fixture
def client(mock_collection: mongomock.Collection):
    from main import app

    with TestClient(app) as test_client:
        yield test_client

