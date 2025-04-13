"""
MCP-Todoist Integration

This is the main entry point for the MCP server that integrates with Todoist.
It sets up the server and registers the tools and resources.
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
    
    # Register Todoist tools
    
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
    
    @server.tool()
    async def get_task(
        task_id: str,
        ctx: Context = None,
    ) -> Dict[str, Any]:
        """
        Get a specific task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            ctx: MCP context (injected automatically)
            
        Returns:
            Task dictionary
        """
        return await todoist_tools.get_task(
            task_id=task_id,
            ctx=ctx,
        )
    
    @server.tool()
    async def update_task(
        task_id: str,
        content: Optional[str] = None,
        description: Optional[str] = None,
        due_string: Optional[str] = None,
        priority: Optional[int] = None,
        ctx: Context = None,
    ) -> Dict[str, Any]:
        """
        Update an existing task.
        
        Args:
            task_id: ID of the task to update
            content: New task content/title (optional)
            description: New task description (optional)
            due_string: New due date in natural language (optional)
            priority: New priority level (optional)
            ctx: MCP context (injected automatically)
            
        Returns:
            Updated task dictionary
        """
        return await todoist_tools.update_task(
            task_id=task_id,
            content=content,
            description=description,
            due_string=due_string,
            priority=priority,
            ctx=ctx,
        )
    
    @server.tool()
    async def complete_task(
        task_id: str,
        ctx: Context = None,
    ) -> Dict[str, str]:
        """
        Complete a task.
        
        Args:
            task_id: ID of the task to complete
            ctx: MCP context (injected automatically)
            
        Returns:
            Dictionary with status information
        """
        return await todoist_tools.complete_task(
            task_id=task_id,
            ctx=ctx,
        )
    
    @server.tool()
    async def delete_task(
        task_id: str,
        ctx: Context = None,
    ) -> Dict[str, str]:
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            ctx: MCP context (injected automatically)
            
        Returns:
            Dictionary with status information
        """
        return await todoist_tools.delete_task(
            task_id=task_id,
            ctx=ctx,
        )
    
    @server.tool()
    async def get_projects(
        ctx: Context = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all projects.
        
        Args:
            ctx: MCP context (injected automatically)
            
        Returns:
            List of project dictionaries
        """
        return await todoist_tools.get_projects(
            ctx=ctx,
        )
    
    # Register Todoist resources
    
    @server.resource("todoist://tasks")
    async def tasks_resource() -> Tuple[str, str]:
        """
        Get all tasks as a resource.
        
        Returns:
            Tuple of (data, mime_type)
        """
        return await todoist_resources.get_tasks_resource()
    
    @server.resource("todoist://tasks/project/{project_id}")
    async def project_tasks_resource(project_id: str) -> Tuple[str, str]:
        """
        Get tasks for a specific project as a resource.
        
        Args:
            project_id: ID of the project to get tasks for
            
        Returns:
            Tuple of (data, mime_type)
        """
        return await todoist_resources.get_tasks_resource(
            project_id=project_id,
        )
    
    @server.resource("todoist://tasks/section/{section_id}")
    async def section_tasks_resource(section_id: str) -> Tuple[str, str]:
        """
        Get tasks for a specific section as a resource.
        
        Args:
            section_id: ID of the section to get tasks for
            
        Returns:
            Tuple of (data, mime_type)
        """
        return await todoist_resources.get_tasks_resource(
            section_id=section_id,
        )
    
    @server.resource("todoist://tasks/label/{label}")
    async def label_tasks_resource(label: str) -> Tuple[str, str]:
        """
        Get tasks with a specific label as a resource.
        
        Args:
            label: Label name to get tasks for
            
        Returns:
            Tuple of (data, mime_type)
        """
        return await todoist_resources.get_tasks_resource(
            label=label,
        )
    
    @server.resource("todoist://projects")
    async def projects_resource() -> Tuple[str, str]:
        """
        Get all projects as a resource.
        
        Returns:
            Tuple of (data, mime_type)
        """
        return await todoist_resources.get_projects_resource()
    
    @server.resource("todoist://sections/{project_id}")
    async def sections_resource(project_id: str) -> Tuple[str, str]:
        """
        Get sections for a project as a resource.
        
        Args:
            project_id: ID of the project to get sections for
            
        Returns:
            Tuple of (data, mime_type)
        """
        return await todoist_resources.get_sections_resource(
            project_id=project_id,
        )
    
    @server.resource("todoist://labels")
    async def labels_resource() -> Tuple[str, str]:
        """
        Get all labels as a resource.
        
        Returns:
            Tuple of (data, mime_type)
        """
        return await todoist_resources.get_labels_resource()
    
    # Add some helpful prompts
    
    @server.prompt()
    def create_task_prompt(content: str, due_date: Optional[str] = None) -> str:
        """
        Prompt to create a new task.
        
        Args:
            content: Task content/title
            due_date: Optional due date in natural language
        """
        prompt = f"Please create a new task titled '{content}'"
        if due_date:
            prompt += f" due {due_date}"
        prompt += "."
        return prompt
    
    @server.prompt()
    def show_tasks_prompt() -> str:
        """Prompt to show all tasks."""
        return "Please show me my current tasks in Todoist."
    
    @server.prompt()
    def complete_task_prompt(task_name: str) -> str:
        """
        Prompt to complete a task by name.
        
        Args:
            task_name: Name of the task to complete
        """
        return f"Please mark the task '{task_name}' as complete."
    
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
