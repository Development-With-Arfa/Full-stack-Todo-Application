"""
Contract test for POST /api/{user_id}/tasks endpoint.
This test verifies the API contract without implementation.
"""
import pytest
from fastapi.testclient import TestClient
from main import app  # Import the main app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


def test_create_task_contract(client):
    """
    Test the contract for creating a task.
    This test should initially FAIL before implementation.
    """
    user_id = "test-user-123"
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=task_data)

    # Verify the response structure and status code
    assert response.status_code == 201  # Should return 201 Created

    # Verify response body structure
    response_data = response.json()
    assert "id" in response_data
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["completed"] == task_data["completed"]
    assert response_data["user_id"] == user_id
    assert "created_at" in response_data
    assert "updated_at" in response_data


def test_create_task_validation_error(client):
    """
    Test that validation errors are properly handled.
    """
    user_id = "test-user-123"
    invalid_task_data = {
        "title": "",  # Empty title should fail validation
        "description": "Test Description"
    }

    response = client.post(f"/api/{user_id}/tasks", json=invalid_task_data)

    # Should return 422 for validation error
    assert response.status_code in [400, 422]


def test_create_task_missing_title(client):
    """
    Test that missing title results in validation error.
    """
    user_id = "test-user-123"
    invalid_task_data = {
        "description": "Test Description"
        # Missing required title field
    }

    response = client.post(f"/api/{user_id}/tasks", json=invalid_task_data)

    # Should return 422 for validation error
    assert response.status_code in [400, 422]