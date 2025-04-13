# MCP-Todoist Integration

This project provides a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that integrates with Todoist, allowing language models to interact with Todoist tasks and projects.

## Features

- Create, read, update, and complete Todoist tasks
- Access Todoist projects, sections, and labels
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
mcp dev main.py
```

This will start the MCP Inspector, allowing you to test the server interactively.

### Installing in Claude Desktop

To install the server in Claude Desktop:

```bash
mcp install main.py
```

### Available Tools

The following Todoist tools are available:

- `create_task` - Create a new task
- `get_tasks` - Get tasks based on filters
- `get_task` - Get a specific task by ID
- `update_task` - Update an existing task
- `complete_task` - Mark a task as complete
- `delete_task` - Delete a task
- `get_projects` - Get all projects

### Available Resources

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

## Development

To contribute to the project or modify it for your needs:

1. Fork the repository
2. Make your changes
3. Test with `mcp dev main.py`
4. Submit a pull request

## License

MIT
