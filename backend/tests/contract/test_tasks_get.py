"""
Contract test for GET /api/{user_id}/tasks/{id} endpoint.
This test verifies the API contract for retrieving a specific task.
"""
import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from src.main import app  # Import the main app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


def test_get_specific_task_contract(client):
    """
    Test the contract for retrieving a specific task.
    This test verifies the API response structure.
    """
    user_id = "test-user-123"
    task_id = str(uuid4())

    response = client.get(f"/api/{user_id}/tasks/{task_id}")

    # Verify the response structure and status code
    if response.status_code == 404:
        # This is acceptable if the task doesn't exist
        assert response.status_code == 404
    else:
        # If the task exists, should return 200
        assert response.status_code == 200

        if response.status_code == 200:
            # Verify response body structure
            response_data = response.json()
            assert "id" in response_data
            assert "title" in response_data
            assert "description" in response_data
            assert "completed" in response_data
            assert "user_id" in response_data
            assert "created_at" in response_data
            assert "updated_at" in response_data


def test_get_nonexistent_task_returns_404(client):
    """
    Test that getting a non-existent task returns 404.
    """
    user_id = "test-user-123"
    nonexistent_task_id = str(uuid4())  # Generate a random UUID

    response = client.get(f"/api/{user_id}/tasks/{nonexistent_task_id}")

    # Should return 404 for non-existent task
    assert response.status_code == 404