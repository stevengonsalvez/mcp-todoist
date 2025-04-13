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
                    "is_favorite": project.is_favorite,
                    "is_inbox_project": project.is_inbox_project,
                    "order": project.order,
                    "parent_id": project.parent_id,
                    "url": project.url,
                }
                for project in projects
            ]
        except Exception as e:
            # Log error if context is provided
            if ctx:
                ctx.error(f"Failed to get Todoist projects: {str(e)}")
            raise ValueError(f"Failed to get Todoist projects: {str(e)}")
    
    # New methods below
    
    async def add_task_quick(
        self,
        text: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Add a task using natural language quick add syntax.
        
        Args:
            text: Text with task details in natural language
            ctx: MCP context (optional)
            
        Returns:
            Task dictionary
        """
        if ctx:
            ctx.info(f"Quick adding Todoist task: {text}")
        
        try:
            task = self.api.add_task_quick(text)
            return self._task_to_dict(task)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to quick add Todoist task: {str(e)}")
            raise ValueError(f"Failed to quick add Todoist task: {str(e)}")
    
    async def uncomplete_task(
        self,
        task_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Uncomplete a task.
        
        Args:
            task_id: ID of the task to uncomplete
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        if ctx:
            ctx.info(f"Uncompleting Todoist task: {task_id}")
        
        try:
            self.api.uncomplete_task(task_id)
            return {"status": "success", "message": f"Task {task_id} uncompleted"}
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to uncomplete Todoist task: {str(e)}")
            raise ValueError(f"Failed to uncomplete Todoist task: {str(e)}")
    
    async def get_completed_tasks(
        self,
        since: Optional[str] = None,
        until: Optional[str] = None,
        project_id: Optional[str] = None,
        section_id: Optional[str] = None,
        ctx: Optional[Context] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get completed tasks.
        
        Args:
            since: Only return tasks completed on or after this date (YYYY-MM-DD)
            until: Only return tasks completed before this date (YYYY-MM-DD)
            project_id: Filter by project ID
            section_id: Filter by section ID
            ctx: MCP context (optional)
            
        Returns:
            List of completed task dictionaries
        """
        if ctx:
            ctx.info("Fetching completed Todoist tasks")
        
        try:
            kwargs = {}
            if since:
                kwargs["since"] = since
            if until:
                kwargs["until"] = until
            if project_id:
                kwargs["project_id"] = project_id
            if section_id:
                kwargs["section_id"] = section_id
            
            tasks = self.api.get_completed_tasks(**kwargs)
            return [self._task_to_dict(task) for task in tasks]
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get completed Todoist tasks: {str(e)}")
            raise ValueError(f"Failed to get completed Todoist tasks: {str(e)}")
    
    async def add_project(
        self,
        name: str,
        parent_id: Optional[str] = None,
        color: Optional[str] = None,
        is_favorite: Optional[bool] = None,
        view_style: Optional[str] = None,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            name: Name of the project
            parent_id: ID of the parent project for nested projects
            color: Color for the project
            is_favorite: Whether the project is a favorite
            view_style: Style of the project view
            ctx: MCP context (optional)
            
        Returns:
            Project dictionary
        """
        if ctx:
            ctx.info(f"Creating Todoist project: {name}")
        
        try:
            project_data = {"name": name}
            if parent_id:
                project_data["parent_id"] = parent_id
            if color:
                project_data["color"] = color
            if is_favorite is not None:
                project_data["is_favorite"] = is_favorite
            if view_style:
                project_data["view_style"] = view_style
            
            project = self.api.add_project(**project_data)
            return self._project_to_dict(project)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to create Todoist project: {str(e)}")
            raise ValueError(f"Failed to create Todoist project: {str(e)}")
    
    async def get_project(
        self,
        project_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Get a specific project by ID.
        
        Args:
            project_id: ID of the project to retrieve
            ctx: MCP context (optional)
            
        Returns:
            Project dictionary
        """
        if ctx:
            ctx.info(f"Fetching Todoist project: {project_id}")
        
        try:
            project = self.api.get_project(project_id)
            return self._project_to_dict(project)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get Todoist project: {str(e)}")
            raise ValueError(f"Failed to get Todoist project: {str(e)}")
    
    async def update_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        is_favorite: Optional[bool] = None,
        view_style: Optional[str] = None,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing project.
        
        Args:
            project_id: ID of the project to update
            name: New name for the project
            color: New color for the project
            is_favorite: Whether the project is a favorite
            view_style: New style for the project view
            ctx: MCP context (optional)
            
        Returns:
            Updated project dictionary
        """
        if ctx:
            ctx.info(f"Updating Todoist project: {project_id}")
        
        try:
            update_data = {"id": project_id}
            if name:
                update_data["name"] = name
            if color:
                update_data["color"] = color
            if is_favorite is not None:
                update_data["is_favorite"] = is_favorite
            if view_style:
                update_data["view_style"] = view_style
            
            if len(update_data) == 1:
                raise ValueError("No update data provided")
            
            project = self.api.update_project(**update_data)
            return self._project_to_dict(project)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to update Todoist project: {str(e)}")
            raise ValueError(f"Failed to update Todoist project: {str(e)}")
    
    async def delete_project(
        self,
        project_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Delete a project.
        
        Args:
            project_id: ID of the project to delete
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        if ctx:
            ctx.info(f"Deleting Todoist project: {project_id}")
        
        try:
            self.api.delete_project(project_id)
            return {"status": "success", "message": f"Project {project_id} deleted"}
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to delete Todoist project: {str(e)}")
            raise ValueError(f"Failed to delete Todoist project: {str(e)}")
    
    async def archive_project(
        self,
        project_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Archive a project.
        
        Args:
            project_id: ID of the project to archive
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        if ctx:
            ctx.info(f"Archiving Todoist project: {project_id}")
        
        try:
            self.api.archive_project(project_id)
            return {"status": "success", "message": f"Project {project_id} archived"}
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to archive Todoist project: {str(e)}")
            raise ValueError(f"Failed to archive Todoist project: {str(e)}")
    
    async def unarchive_project(
        self,
        project_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Unarchive a project.
        
        Args:
            project_id: ID of the project to unarchive
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        if ctx:
            ctx.info(f"Unarchiving Todoist project: {project_id}")
        
        try:
            self.api.unarchive_project(project_id)
            return {"status": "success", "message": f"Project {project_id} unarchived"}
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to unarchive Todoist project: {str(e)}")
            raise ValueError(f"Failed to unarchive Todoist project: {str(e)}")
    
    async def get_sections(
        self,
        project_id: Optional[str] = None,
        ctx: Optional[Context] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get sections.
        
        Args:
            project_id: Filter by project ID
            ctx: MCP context (optional)
            
        Returns:
            List of section dictionaries
        """
        if ctx:
            ctx.info("Fetching Todoist sections")
        
        try:
            kwargs = {}
            if project_id:
                kwargs["project_id"] = project_id
            
            sections = self.api.get_sections(**kwargs)
            return [self._section_to_dict(section) for section in sections]
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get Todoist sections: {str(e)}")
            raise ValueError(f"Failed to get Todoist sections: {str(e)}")
    
    async def get_section(
        self,
        section_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Get a specific section by ID.
        
        Args:
            section_id: ID of the section to retrieve
            ctx: MCP context (optional)
            
        Returns:
            Section dictionary
        """
        if ctx:
            ctx.info(f"Fetching Todoist section: {section_id}")
        
        try:
            section = self.api.get_section(section_id)
            return self._section_to_dict(section)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get Todoist section: {str(e)}")
            raise ValueError(f"Failed to get Todoist section: {str(e)}")
    
    async def add_section(
        self,
        name: str,
        project_id: str,
        order: Optional[int] = None,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Create a new section.
        
        Args:
            name: Name of the section
            project_id: ID of the project to add the section to
            order: Order of the section within the project
            ctx: MCP context (optional)
            
        Returns:
            Section dictionary
        """
        if ctx:
            ctx.info(f"Creating Todoist section: {name}")
        
        try:
            section_data = {"name": name, "project_id": project_id}
            if order is not None:
                section_data["order"] = order
            
            section = self.api.add_section(**section_data)
            return self._section_to_dict(section)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to create Todoist section: {str(e)}")
            raise ValueError(f"Failed to create Todoist section: {str(e)}")
    
    async def update_section(
        self,
        section_id: str,
        name: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing section.
        
        Args:
            section_id: ID of the section to update
            name: New name for the section
            ctx: MCP context (optional)
            
        Returns:
            Updated section dictionary
        """
        if ctx:
            ctx.info(f"Updating Todoist section: {section_id}")
        
        try:
            section = self.api.update_section(section_id, name)
            return self._section_to_dict(section)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to update Todoist section: {str(e)}")
            raise ValueError(f"Failed to update Todoist section: {str(e)}")
    
    async def delete_section(
        self,
        section_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Delete a section.
        
        Args:
            section_id: ID of the section to delete
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        if ctx:
            ctx.info(f"Deleting Todoist section: {section_id}")
        
        try:
            self.api.delete_section(section_id)
            return {"status": "success", "message": f"Section {section_id} deleted"}
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to delete Todoist section: {str(e)}")
            raise ValueError(f"Failed to delete Todoist section: {str(e)}")
    
    async def get_labels(
        self,
        ctx: Optional[Context] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all labels.
        
        Args:
            ctx: MCP context (optional)
            
        Returns:
            List of label dictionaries
        """
        if ctx:
            ctx.info("Fetching Todoist labels")
        
        try:
            labels = self.api.get_labels()
            return [self._label_to_dict(label) for label in labels]
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get Todoist labels: {str(e)}")
            raise ValueError(f"Failed to get Todoist labels: {str(e)}")
    
    async def get_label(
        self,
        label_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Get a specific label by ID.
        
        Args:
            label_id: ID of the label to retrieve
            ctx: MCP context (optional)
            
        Returns:
            Label dictionary
        """
        if ctx:
            ctx.info(f"Fetching Todoist label: {label_id}")
        
        try:
            label = self.api.get_label(label_id)
            return self._label_to_dict(label)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get Todoist label: {str(e)}")
            raise ValueError(f"Failed to get Todoist label: {str(e)}")
    
    async def add_label(
        self,
        name: str,
        color: Optional[str] = None,
        favorite: Optional[bool] = None,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Create a new label.
        
        Args:
            name: Name of the label
            color: Color for the label
            favorite: Whether the label is a favorite
            ctx: MCP context (optional)
            
        Returns:
            Label dictionary
        """
        if ctx:
            ctx.info(f"Creating Todoist label: {name}")
        
        try:
            label_data = {"name": name}
            if color:
                label_data["color"] = color
            if favorite is not None:
                label_data["favorite"] = favorite
            
            label = self.api.add_label(**label_data)
            return self._label_to_dict(label)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to create Todoist label: {str(e)}")
            raise ValueError(f"Failed to create Todoist label: {str(e)}")
    
    async def update_label(
        self,
        label_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
        favorite: Optional[bool] = None,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing label.
        
        Args:
            label_id: ID of the label to update
            name: New name for the label
            color: New color for the label
            favorite: Whether the label is a favorite
            ctx: MCP context (optional)
            
        Returns:
            Updated label dictionary
        """
        if ctx:
            ctx.info(f"Updating Todoist label: {label_id}")
        
        try:
            update_data = {"id": label_id}
            if name:
                update_data["name"] = name
            if color:
                update_data["color"] = color
            if favorite is not None:
                update_data["favorite"] = favorite
            
            if len(update_data) == 1:
                raise ValueError("No update data provided")
            
            label = self.api.update_label(**update_data)
            return self._label_to_dict(label)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to update Todoist label: {str(e)}")
            raise ValueError(f"Failed to update Todoist label: {str(e)}")
    
    async def delete_label(
        self,
        label_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Delete a label.
        
        Args:
            label_id: ID of the label to delete
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        if ctx:
            ctx.info(f"Deleting Todoist label: {label_id}")
        
        try:
            self.api.delete_label(label_id)
            return {"status": "success", "message": f"Label {label_id} deleted"}
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to delete Todoist label: {str(e)}")
            raise ValueError(f"Failed to delete Todoist label: {str(e)}")
    
    async def get_comments(
        self,
        task_id: Optional[str] = None,
        project_id: Optional[str] = None,
        ctx: Optional[Context] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get comments for a task or project.
        
        Args:
            task_id: ID of the task to get comments for
            project_id: ID of the project to get comments for
            ctx: MCP context (optional)
            
        Returns:
            List of comment dictionaries
        """
        if ctx:
            ctx.info("Fetching Todoist comments")
        
        try:
            if not task_id and not project_id:
                raise ValueError("Either task_id or project_id must be provided")
            
            kwargs = {}
            if task_id:
                kwargs["task_id"] = task_id
            if project_id:
                kwargs["project_id"] = project_id
            
            comments = self.api.get_comments(**kwargs)
            return [self._comment_to_dict(comment) for comment in comments]
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get Todoist comments: {str(e)}")
            raise ValueError(f"Failed to get Todoist comments: {str(e)}")
    
    async def get_comment(
        self,
        comment_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Get a specific comment by ID.
        
        Args:
            comment_id: ID of the comment to retrieve
            ctx: MCP context (optional)
            
        Returns:
            Comment dictionary
        """
        if ctx:
            ctx.info(f"Fetching Todoist comment: {comment_id}")
        
        try:
            comment = self.api.get_comment(comment_id)
            return self._comment_to_dict(comment)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get Todoist comment: {str(e)}")
            raise ValueError(f"Failed to get Todoist comment: {str(e)}")
    
    async def add_comment(
        self,
        content: str,
        task_id: Optional[str] = None,
        project_id: Optional[str] = None,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Add a comment to a task or project.
        
        Args:
            content: Content of the comment
            task_id: ID of the task to add comment to
            project_id: ID of the project to add comment to
            ctx: MCP context (optional)
            
        Returns:
            Comment dictionary
        """
        if ctx:
            ctx.info("Adding Todoist comment")
        
        try:
            if not task_id and not project_id:
                raise ValueError("Either task_id or project_id must be provided")
            
            comment_data = {"content": content}
            if task_id:
                comment_data["task_id"] = task_id
            if project_id:
                comment_data["project_id"] = project_id
            
            comment = self.api.add_comment(**comment_data)
            return self._comment_to_dict(comment)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to add Todoist comment: {str(e)}")
            raise ValueError(f"Failed to add Todoist comment: {str(e)}")
    
    async def update_comment(
        self,
        comment_id: str,
        content: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing comment.
        
        Args:
            comment_id: ID of the comment to update
            content: New content for the comment
            ctx: MCP context (optional)
            
        Returns:
            Updated comment dictionary
        """
        if ctx:
            ctx.info(f"Updating Todoist comment: {comment_id}")
        
        try:
            comment = self.api.update_comment(comment_id, content)
            return self._comment_to_dict(comment)
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to update Todoist comment: {str(e)}")
            raise ValueError(f"Failed to update Todoist comment: {str(e)}")
    
    async def delete_comment(
        self,
        comment_id: str,
        ctx: Optional[Context] = None,
    ) -> Dict[str, str]:
        """
        Delete a comment.
        
        Args:
            comment_id: ID of the comment to delete
            ctx: MCP context (optional)
            
        Returns:
            Dictionary with status information
        """
        if ctx:
            ctx.info(f"Deleting Todoist comment: {comment_id}")
        
        try:
            self.api.delete_comment(comment_id)
            return {"status": "success", "message": f"Comment {comment_id} deleted"}
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to delete Todoist comment: {str(e)}")
            raise ValueError(f"Failed to delete Todoist comment: {str(e)}")
    
    async def get_collaborators(
        self,
        project_id: str,
        ctx: Optional[Context] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get collaborators for a project.
        
        Args:
            project_id: ID of the project to get collaborators for
            ctx: MCP context (optional)
            
        Returns:
            List of collaborator dictionaries
        """
        if ctx:
            ctx.info(f"Fetching collaborators for project: {project_id}")
        
        try:
            collaborators = self.api.get_collaborators(project_id)
            return [
                {
                    "id": collab.id,
                    "name": collab.name,
                    "email": collab.email,
                }
                for collab in collaborators
            ]
        except Exception as e:
            if ctx:
                ctx.error(f"Failed to get project collaborators: {str(e)}")
            raise ValueError(f"Failed to get project collaborators: {str(e)}")
    
    # Helper methods for converting Todoist objects to dictionaries
    
    def _task_to_dict(self, task):
        """Convert a Todoist Task object to a dictionary."""
        task_dict = {}
        for attr in ["id", "content", "description", "url", "created_at", 
                    "priority", "project_id", "section_id", "parent_id"]:
            if hasattr(task, attr):
                task_dict[attr] = getattr(task, attr)
        
        # Handle due date
        if hasattr(task, "due") and task.due:
            due_dict = {}
            for due_attr in ["date", "string", "is_recurring", "datetime", "timezone"]:
                if hasattr(task.due, due_attr):
                    due_dict[due_attr] = getattr(task.due, due_attr)
            task_dict["due"] = due_dict
        else:
            task_dict["due"] = None
        
        # Handle labels
        if hasattr(task, "labels"):
            task_dict["labels"] = task.labels
        elif hasattr(task, "label_ids"):
            task_dict["label_ids"] = task.label_ids
        
        return task_dict
    
    def _project_to_dict(self, project):
        """Convert a Todoist Project object to a dictionary."""
        return {
            "id": project.id,
            "name": project.name,
            "color": project.color,
            "is_favorite": project.is_favorite,
            "is_inbox_project": project.is_inbox_project,
            "order": project.order,
            "parent_id": project.parent_id,
            "url": project.url,
        }
    
    def _section_to_dict(self, section):
        """Convert a Todoist Section object to a dictionary."""
        return {
            "id": section.id,
            "name": section.name,
            "order": section.order,
            "project_id": section.project_id,
        }
    
    def _label_to_dict(self, label):
        """Convert a Todoist Label object to a dictionary."""
        return {
            "id": label.id,
            "name": label.name,
            "color": label.color,
            "order": label.order,
            "favorite": label.favorite if hasattr(label, "favorite") else False,
        }
    
    def _comment_to_dict(self, comment):
        """Convert a Todoist Comment object to a dictionary."""
        comment_dict = {
            "id": comment.id,
            "content": comment.content,
            "posted_at": comment.posted_at,
        }
        
        if hasattr(comment, "task_id") and comment.task_id:
            comment_dict["task_id"] = comment.task_id
            
        if hasattr(comment, "project_id") and comment.project_id:
            comment_dict["project_id"] = comment.project_id
            
        return comment_dict
