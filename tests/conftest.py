import os

print(os.getcwd())
import pytest

from app import app
import main

@pytest.fixture
def test_client():
    return app.test_client()
