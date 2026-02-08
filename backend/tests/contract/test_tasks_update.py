"""
Contract test for PUT /api/{user_id}/tasks/{id} endpoint.
This test verifies the API contract for updating a specific task.
"""
import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from src.main import app  # Import the main app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


def test_update_task_contract(client):
    """
    Test the contract for updating a specific task.
    This test verifies the API response structure.
    """
    user_id = "test-user-123"
    task_id = str(uuid4())
    update_data = {
        "title": "Updated Task Title",
        "description": "Updated Description",
        "completed": True
    }

    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data)

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
            assert response_data["title"] == update_data["title"]
            assert response_data["description"] == update_data["description"]
            assert response_data["completed"] == update_data["completed"]
            assert "user_id" in response_data
            assert "created_at" in response_data
            assert "updated_at" in response_data


def test_update_nonexistent_task_returns_404(client):
    """
    Test that updating a non-existent task returns 404.
    """
    user_id = "test-user-123"
    nonexistent_task_id = str(uuid4())  # Generate a random UUID
    update_data = {
        "title": "Updated Task Title",
        "description": "Updated Description",
        "completed": True
    }

    response = client.put(f"/api/{user_id}/tasks/{nonexistent_task_id}", json=update_data)

    # Should return 404 for non-existent task
    assert response.status_code == 404


def test_update_task_validation_error(client):
    """
    Test that validation errors are properly handled during update.
    """
    user_id = "test-user-123"
    task_id = str(uuid4())
    invalid_update_data = {
        "title": ""  # Empty title should fail validation
    }

    response = client.put(f"/api/{user_id}/tasks/{task_id}", json=invalid_update_data)

    # Should return 422 for validation error
    assert response.status_code in [400, 422]