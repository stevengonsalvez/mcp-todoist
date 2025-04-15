# MCP-Todoist Integration

This project provides a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that integrates with Todoist, allowing language models to interact with Todoist tasks and projects.

## Features

- Complete Todoist API integration
- Create, read, update, and delete tasks, projects, sections, labels, and comments
- Access project collaborators
- Filter tasks by various criteria
- Well-documented tools and resources for use with language models

## Requirements

- Python 3.10 or higher
- Todoist account with API token
- MCP-compatible client (like Claude Desktop)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/mcp-todoist.git
   cd mcp-todoist
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Todoist API token:
   ```bash
   cp .env.example .env
   # Edit .env file to add your Todoist API token
   ```

## Getting a Todoist API Token

1. Log in to your Todoist account
2. Go to Settings > Integrations
3. Copy your API token from the "API token" section

## Usage

### Running with MCP Dev Tools

For testing and development, use the MCP dev tools:

```bash
mcp run main.py
```

This will start the MCP server, allowing you to test it interactively.

To run with the MCP Inspector for visual interaction:

```bash
mcp dev main.py
```



### Using with Claude Desktop

To use this MCP server with Claude Desktop:

1. Install the server:
   - If published to PyPI: `pip install mcp-todoist`
   - If cloned: Follow the installation instructions above

2. Add the server to Claude Desktop's MCP configuration:
   - Open Claude Desktop
   - Go to Settings > Advanced
   - Under "MCP Servers Configuration", add to the JSON configuration:
     ```json
     "mcpServers": {
       "todoist": {
         "command": "mcp-todoist"
       }
     }
     ```
   - Or if using the cloned repository:
     ```json
     "mcpServers": {
       "todoist": {
         "command": "mcp",
         "args": ["run", "/path/to/mcp-todoist/main.py"]
       }
     }
     ```
   - If you're using uvx or uv for package management:
     ```json
     "mcpServers": {
       "todoist": {
         "command": "uvx",
         "args": ["mcp-todoist"]
       }
     }
     ```

3. Save the configuration and restart Claude Desktop
4. You can now access the Todoist MCP server in your Claude conversations by asking Claude to use Todoist

## Available Tools

The following Todoist tools are available:

### Task Management
- `create_task` - Create a new task with title, due date, project, etc.
- `get_tasks` - Get tasks based on filters
- `get_task` - Get a specific task by ID
- `update_task` - Update an existing task
- `complete_task` - Mark a task as complete
- `uncomplete_task` - Mark a completed task as incomplete
- `delete_task` - Delete a task

### Project Management
- `get_projects` - Get all projects
- `get_project` - Get a specific project by ID
- `add_project` - Create a new project
- `update_project` - Update an existing project
- `delete_project` - Delete a project
- `archive_project` - Archive a project
- `unarchive_project` - Unarchive a project

### Section Management
- `get_sections` - Get all sections in a project
- `get_section` - Get a specific section by ID
- `add_section` - Create a new section
- `update_section` - Update an existing section
- `delete_section` - Delete a section

### Label Management
- `get_labels` - Get all labels
- `get_label` - Get a specific label by ID
- `add_label` - Create a new label
- `update_label` - Update an existing label
- `delete_label` - Delete a label

### Comment Management
- `get_comments` - Get comments for a task or project
- `get_comment` - Get a specific comment by ID
- `add_comment` - Add a comment to a task or project
- `update_comment` - Update an existing comment
- `delete_comment` - Delete a comment

### Collaboration
- `get_collaborators` - Get collaborators for a project

## Available Resources

The following Todoist resources are available:

- `todoist://tasks` - All tasks
- `todoist://tasks/project/{project_id}` - Tasks in a specific project
- `todoist://tasks/section/{section_id}` - Tasks in a specific section
- `todoist://tasks/label/{label}` - Tasks with a specific label
- `todoist://projects` - All projects
- `todoist://sections/{project_id}` - Sections in a specific project
- `todoist://labels` - All labels

## Examples

### Creating a Task

```
Please create a new task in Todoist called "Buy groceries" due tomorrow.
```

### Getting Tasks from a Project

```
Show me all tasks in my "Work" project.
```

### Completing a Task

```
Mark the "Buy groceries" task as complete.
```

### Adding a Comment to a Task

```
Add a comment to the task with ID "12345678" saying "Don't forget milk and eggs".
```

### Creating a New Project with Sections

```
Create a new project called "Home Renovation" and add sections for "Kitchen", "Bathroom", and "Living Room".
```

## Development

To contribute to the project or modify it for your needs:

1. Fork the repository
2. Make your changes
3. Test with `mcp run main.py` or `mcp dev main.py`
4. Submit a pull request

## License

MIT
