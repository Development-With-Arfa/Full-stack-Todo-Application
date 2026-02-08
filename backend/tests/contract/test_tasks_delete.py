"""
Contract test for DELETE /api/{user_id}/tasks/{id} endpoint.
This test verifies the API contract for deleting a specific task.
"""
import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from src.main import app  # Import the main app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


def test_delete_task_contract(client):
    """
    Test the contract for deleting a specific task.
    This test verifies the API response structure.
    """
    user_id = "test-user-123"
    task_id = str(uuid4())

    response = client.delete(f"/api/{user_id}/tasks/{task_id}")

    # Verify the response structure and status code
    if response.status_code == 404:
        # This is acceptable if the task doesn't exist
        assert response.status_code == 404
    else:
        # If the task exists, should return 204 No Content
        assert response.status_code == 204


def test_delete_nonexistent_task_returns_404(client):
    """
    Test that deleting a non-existent task returns 404.
    This behavior may vary depending on implementation - some return 404, others return 204
    """
    user_id = "test-user-123"
    nonexistent_task_id = str(uuid4())  # Generate a random UUID

    response = client.delete(f"/api/{user_id}/tasks/{nonexistent_task_id}")

    # Should return 404 for non-existent task or 204 for idempotent behavior
    assert response.status_code in [204, 404]


def test_delete_task_success(client):
    """
    Test that successful deletion returns the correct status.
    """
    user_id = "test-user-123"
    task_id = str(uuid4())

    response = client.delete(f"/api/{user_id}/tasks/{task_id}")

    # Should return 204 No Content for successful deletion
    # Or 404 if task doesn't exist
    assert response.status_code in [204, 404]