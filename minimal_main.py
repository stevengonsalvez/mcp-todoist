"""
Minimal MCP-Todoist Integration for testing

This is a minimalist version of the MCP server that integrates with Todoist.
It only includes core functionality to test if the MCP Inspector works properly.
"""

import asyncio
from typing import Any, Dict, List, Optional, Tuple

from mcp.server.fastmcp import Context, FastMCP

from config import load_config
from todoist_tools import TodoistTools
from todoist_resources import TodoistResources


def create_server() -> FastMCP:
    """
    Create and configure the MCP server.
    
    Returns:
        FastMCP: Configured MCP server
    """
    # Load configuration
    config = load_config()
    
    # Create MCP server
    server = FastMCP(
        config.server_name,
        # List dependencies for installation without version constraints
        dependencies=[
            "todoist-api-python",
            "pydantic",
            "python-dotenv",
        ],
    )
    
    # Initialize Todoist clients
    todoist_tools = TodoistTools(config.todoist.api_token)
    todoist_resources = TodoistResources(config.todoist.api_token)
    
    # Register only a few core Todoist tools for testing
    
    @server.tool()
    async def create_task(
        content: str,
        description: Optional[str] = None,
        due_string: Optional[str] = None,
        priority: Optional[int] = None,
        project_id: Optional[str] = None,
        section_id: Optional[str] = None,
        ctx: Context = None,
    ) -> Dict[str, Any]:
        """
        Create a new task in Todoist.
        
        Args:
            content: The content/title of the task
            description: Detailed description of the task (optional)
            due_string: Natural language due date like 'tomorrow', 'next Monday' (optional)
            priority: Task priority from 1 (normal) to 4 (urgent) (optional)
            project_id: ID of the project to add the task to (optional)
            section_id: ID of the section to add the task to (optional)
            ctx: MCP context (injected automatically)
            
        Returns:
            Dictionary containing task data
        """
        return await todoist_tools.create_task(
            content=content,
            description=description,
            due_string=due_string,
            priority=priority,
            project_id=project_id,
            section_id=section_id,
            ctx=ctx,
        )
    
    @server.tool()
    async def get_tasks(
        project_id: Optional[str] = None,
        section_id: Optional[str] = None,
        label: Optional[str] = None,
        filter_query: Optional[str] = None,
        ctx: Context = None,
    ) -> List[Dict[str, Any]]:
        """
        Get tasks from Todoist based on filters.
        
        Args:
            project_id: Filter tasks by project ID (optional)
            section_id: Filter tasks by section ID (optional)
            label: Filter tasks by label name (optional)
            filter_query: Filter tasks using Todoist's filter language (optional)
            ctx: MCP context (injected automatically)
            
        Returns:
            List of task dictionaries
        """
        return await todoist_tools.get_tasks(
            project_id=project_id,
            section_id=section_id,
            label=label,
            filter_query=filter_query,
            ctx=ctx,
        )
    
    # Register only one resource for testing
    
    @server.resource("todoist://tasks")
    async def tasks_resource() -> Tuple[str, str]:
        """
        Get all tasks as a resource.
        
        Returns:
            Tuple of (data, mime_type)
        """
        return await todoist_resources.get_tasks_resource()
    
    return server


def main():
    """Main entry point for the MCP-Todoist server."""
    try:
        # Run the server
        server.run()
    except Exception as e:
        print(f"Error starting MCP server: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    return 0


# Create the server instance at module level
server = create_server()

if __name__ == "__main__":
    exit(main()) 