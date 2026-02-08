"""
Contract test for GET /api/{user_id}/tasks endpoint.
This test verifies the API contract for listing tasks.
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app  # Import the main app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


def test_list_tasks_contract(client):
    """
    Test the contract for listing user tasks.
    This test verifies the API response structure.
    """
    user_id = "test-user-123"

    response = client.get(f"/api/{user_id}/tasks")

    # Verify the response structure and status code
    assert response.status_code == 200  # Should return 200 OK

    # Verify response is a list
    response_data = response.json()
    assert isinstance(response_data, list)

    # If tasks exist, they should follow the TaskRead schema
    for task in response_data:
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "user_id" in task
        assert "created_at" in task
        assert "updated_at" in task


def test_list_tasks_empty_response(client):
    """
    Test that an empty list is returned when no tasks exist.
    """
    user_id = "empty-user-123"

    response = client.get(f"/api/{user_id}/tasks")

    # Should return 200 OK with an empty list
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == []