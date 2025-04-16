"""Basic tests for mcp-todoist."""

import os
from unittest import mock

import pytest
from todoist_api_python.models import Task


def test_import():
    """Test that we can import the main module."""
    import main

    assert main is not None


@pytest.fixture
def mock_env_token():
    """Mock environment variables for testing."""
    with mock.patch.dict(os.environ, {"TODOIST_API_TOKEN": "fake_test_token"}):
        yield


@pytest.fixture
def mock_todoist_api():
    """Mock the Todoist API."""
    with mock.patch("todoist_api_python.api.TodoistAPI") as mock_api:
        # Create a mock task instance
        mock_task = mock.MagicMock(spec=Task)
        mock_task.id = "123456789"
        mock_task.content = "Test task"
        mock_task.description = "Test description"
        mock_task.completed = False
        mock_task.labels = ["test-label"]
        mock_task.priority = 1
        mock_task.project_id = "project123"
        
        # Configure the mock API instance
        api_instance = mock_api.return_value
        api_instance.get_tasks.return_value = [mock_task]
        
        yield api_instance


@pytest.mark.asyncio
async def test_get_tasks(mock_env_token, mock_todoist_api):
    """Test getting tasks from Todoist."""
    from todoist_tools import TodoistTools
    
    # Initialize TodoistTools with our mocked API
    todoist_tools = TodoistTools("fake_test_token")
    
    # The mocked API is already configured to return our mock task
    tasks = await todoist_tools.get_tasks()
    
    # Verify the API was called correctly
    mock_todoist_api.get_tasks.assert_called_once()
    
    # Check that we got our task
    assert len(tasks) == 1
    assert tasks[0]["id"] == "123456789"
    assert tasks[0]["content"] == "Test task"
    assert not tasks[0]["is_completed"]
    assert "test-label" in tasks[0]["labels"]
