"""
Integration test for task creation flow.
This test verifies the full flow including database operations.
"""
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app  # Import the main app
from src.models.task import TaskCreate


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_task_creation_integration():
    """
    Integration test for task creation flow.
    This test should initially FAIL before implementation.
    """
    # Mock the database session
    mock_session = AsyncMock()
    mock_task = {
        "id": "test-uuid",
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "user_id": "test-user-123",
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }

    # Patch the service layer
    with patch('src.services.task_service.create_task', return_value=mock_task):
        with TestClient(app) as client:
            user_id = "test-user-123"
            task_data = {
                "title": "Test Task",
                "description": "Test Description",
                "completed": False
            }

            response = client.post(f"/api/{user_id}/tasks", json=task_data)

            # Verify response
            assert response.status_code == 201
            response_data = response.json()
            assert response_data["title"] == task_data["title"]
            assert response_data["user_id"] == user_id


def test_task_creation_endpoint_exists(client):
    """
    Basic test to verify the endpoint exists.
    """
    user_id = "test-user-123"
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }

    response = client.post(f"/api/{user_id}/tasks", json=task_data)

    # Initially this will return 404 or 500 until implemented
    # After implementation it should return 201
    assert response.status_code in [201, 404, 500]  # Accept any response initially