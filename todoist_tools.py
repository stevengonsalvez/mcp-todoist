"""
Implementation of Todoist tools for the MCP server.

This module defines the MCP tools that allow language models to interact
with Todoist data and functionality.
"""

from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import Context
from todoist_api_python.api import TodoistAPI


class TodoistTools:
    """Implements Todoist operations as MCP tools."""
    
    def __init__(self, api_token: str):
        """
        Initialize TodoistTools with Todoist API client.
        
        Args:
            api_token: Todoist API token for authentication
        """
        self.api = TodoistAPI(api_token)
    
    async def create_task(
        self, 
        content: str, 
        description: Optional[str] = None,
        due_string: Optional[str] = None,
        priority: Optional[int] = None,
        project_id: Optional[str] = None,
        section_id: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
        parent_id: Optional[str] = None,
        ctx: Optional[Context] = None,
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
            label_ids: List of label IDs to apply to the task (optional)
            parent_id: ID of the parent task for subtasks (optional)
            ctx: MCP context (optional)
            
        Returns:
            Dict containing task data
        """
        # Log action if context is provided
        if ctx:
            ctx.info(f"Creating Todoist task: {content}")
        
        # Prepare task data with only non-None values
        task_data = {"content": content}
        if description is not None:
            task_data["description"] = description
        if due_string is not None:
            task_data["due_string"] = due_string
        if priority is not None:
            task_data["priority"] = priority
        if project_id is not None:
            task_data["project_id"] = project_id
        if section_id is not None:
            task_data["section_id"] = section_id
        if label_ids is not None:
            task_data["label_ids"] = label_ids
        if parent_id is not None:
            task_data["parent_id"] = parent_id
        
        try:
            # Create the task in Todoist
            task = self.api.add_task(**task_data)
            
            # Return task data as dictionary
            return {
                "id": task.id,
                "content": task.content,
                "description": task.description,
                "url": task.url,
                "created_at": task.created_at,
                "priority": task.priority,
                "due": task.due.dict() if task.due else None,
                "project_id": task.project_id,
                "section_id": task.section_id,
                "parent_id": task.parent_id,
                "label_ids": task.label_ids,
            }
        except Exception as e:
            # Log error if context is provided
            if ctx:
                ctx.error(f"Failed to create Todoist task: {str(e)}")
            raise ValueError(f"Failed to create Todoist task: {str(e)}")
    
    async def get_tasks(
        self,
        project_id: Optional[str] = None,
        section_id: Optional[str] = None,
        label: Optional[str] = None,
        filter_query: Optional[str] = None,
        ctx: Optional[Context] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get tasks from Todoist based on filters.
        
        Args:
            project_id: Filter tasks by project ID (optional)
            section_id: Filter tasks by section ID (optional)
            label: Filter tasks by label name (optional)
            filter_query: Filter tasks using Todoist's filter language (optional)
            ctx: MCP context (optional)
            
        Returns:
            List of task dictionaries
        """
        # Log action if context is provided
        if ctx:
            ctx.info("Fetching Todoist tasks")
        
        try:
            if filter_query:
                # Use filter query if provided
                tasks_iterator = self.api.filter_tasks(query=filter_query)
                tasks_list = list(next(tasks_iterator))
            else:
                # Otherwise use the get_tasks method with provided filters
                kwargs = {}
                if project_id:
                    kwargs["project_id"] = project_id
                if section_id:
                    kwargs["section_id"] = section_id
                if label:
                    kwargs["label"] = label
                
                tasks_iterator = self.api.get_tasks(**kwargs)
                tasks_list = list(next(tasks_iterator))
            
            # Convert tasks to dictionaries
            return [
                {
                    "id": task.id,
                    "content": task.content,
                    "description": task.description,
                    "url": task.url,
                    "created_at": task.created_at,
                    "priority": task.priority,
                    "due": task.due.dict() if task.due else None,
                    "project_id": task.project_id,
                    "section_id": task.section_id,
                    "parent_id": task.parent_id,
                    "label_ids": task.label_ids,
                }
                for task in tasks_list
            ]
        except Exception as e:
            # Log error if context is provided
            if ctx:
                ctx.error(f"Failed to get Todoist tasks: {str(e)}")
            raise ValueError(f"Failed to get Todoist tasks: {str(e)}")
    
    async def get_task(
        self,
        task_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Get a specific task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            ctx: MCP context (optional)
            
        Returns:
            Task dictionary
        """
        # Log action if context is provided
        if ctx:
            ctx.info(f"Fetching Todoist task: {task_id}")
        
        try:
            # Get the task by ID
            task = self.api.get_task(task_id)
            
            # Return task data as dictionary
            return {
                "id": task.id,
                "content": task.content,
                "description": task.description,
                "url": task.url,
                "created_at": task.created_at,
                "priority": task.priority,
                "due": task.due.dict() if task.due else None,
                "project_id": task.project_id,
                "section_id": task.section_id,
                "parent_id": task.parent_id,
                "label_ids": task.label_ids,
            }
        except Exception as e:
            # Log error if context is provided
            if ctx:
                ctx.error(f"Failed to get Todoist task: {str(e)}")
            raise ValueError(f"Failed to get Todoist task: {str(e)}")
    
    async def update_task(
        self,
        task_id: str,
        content: Optional[str] = None,
        description: Optional[str] = None,
        due_string: Optional[str] = None,
        priority: Optional[int] = None,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing task.
        
        Args:
            task_id: ID of the task to update
            content: New task content/title (optional)
            description: New task description (optional)
            due_string: New due date in natural language (optional)
            priority: New priority level (optional)
            ctx: MCP context (optional)
            
        Returns:
            Updated task dictionary
        """
        # Log action if context is provided
        if ctx:
            ctx.info(f"Updating Todoist task: {task_id}")
        
        # Prepare update data with only non-None values
        update_data = {"id": task_id}
        if content is not None:
            update_data["content"] = content
        if description is not None:
            update_data["description"] = description
        if due_string is not None:
            update_data["due_string"] = due_string
        if priority is not None:
            update_data["priority"] = priority
        
        # If only ID is provided, nothing to update
        if len(update_data) == 1:
            raise ValueError("No update data provided")
        
        try:
            # Update the task
            success = self.api.update_task(**update_data)
            
            if not success:
                raise ValueError("Failed to update task")
            
            # Get the updated task
            return await self.get_task(task_id, ctx)
        except Exception as e:
            # Log error if context is provided
            if ctx:
                ctx.error(f"Failed to update Todoist task: {str(e)}")
            raise ValueError(f"Failed to update Todoist task: {str(e)}")
    
    async def complete_task(
        self,
        task_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Complete a task.
        
        Args:
            task_id: ID of the task to complete
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        # Log action if context is provided
        if ctx:
            ctx.info(f"Completing Todoist task: {task_id}")
        
        try:
            # Complete the task
            success = self.api.close_task(task_id)
            
            if not success:
                raise ValueError(f"Failed to complete task {task_id}")
            
            return {
                "status": "success",
                "message": f"Task {task_id} completed successfully",
            }
        except Exception as e:
            # Log error if context is provided
            if ctx:
                ctx.error(f"Failed to complete Todoist task: {str(e)}")
            raise ValueError(f"Failed to complete Todoist task: {str(e)}")
    
    async def delete_task(
        self,
        task_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        # Log action if context is provided
        if ctx:
            ctx.info(f"Deleting Todoist task: {task_id}")
        
        try:
            # Delete the task
            success = self.api.delete_task(task_id)
            
            if not success:
                raise ValueError(f"Failed to delete task {task_id}")
            
            return {
                "status": "success",
                "message": f"Task {task_id} deleted successfully",
            }
        except Exception as e:
            # Log error if context is provided
            if ctx:
                ctx.error(f"Failed to delete Todoist task: {str(e)}")
            raise ValueError(f"Failed to delete Todoist task: {str(e)}")
    
    async def get_projects(
        self,
        ctx: Optional[Context] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all projects.
        
        Args:
            ctx: MCP context (optional)
            
        Returns:
            List of project dictionaries
        """
        # Log action if context is provided
        if ctx:
            ctx.info("Fetching Todoist projects")
        
        try:
            # Get all projects
            projects = self.api.get_projects()
            
            # Convert projects to dictionaries
            return [
                {
                    "id": project.id,
                    "name": project.name,
                    "color": project.color,
                    "comment_count": project.comment_count,
                    "is_favorite": project.is_favorite,
                    "is_inbox_project": project.is_inbox_project,
                    "is_team_inbox": project.is_team_inbox,
                    "order": project.order,
                    "parent_id": project.parent_id,
                    "url": project.url,
                    "view_style": project.view_style,
                }
                for project in projects
            ]
        except Exception as e:
            # Log error if context is provided
            if ctx:
                ctx.error(f"Failed to get Todoist projects: {str(e)}")
            raise ValueError(f"Failed to get Todoist projects: {str(e)}")
