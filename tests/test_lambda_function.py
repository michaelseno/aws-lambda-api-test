import unittest
import pytest
from src.api_request import fetch_data


@pytest.mark.parametrize("url, expected_status", [
    ("https://jsonplaceholder.typicode.com/posts/1", 200),
    ("https://jsonplaceholder.typicode.com/posts/2", 200),
    ("https://jsonplaceholder.typicode.com/posts/404", 404),
])
def test_fetch_data(url, expected_status):
    response = fetch_data(url)
    assert response["status_code"] == expected_status
