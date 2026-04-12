# AI Agent MCP Server

Model Context Protocol (MCP) server for the AI Productivity Planner agent, providing tools for task management, note-taking, scheduling, and timer operations.

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Server

```bash
python server.py
```

## Available Tools

### Task Management
- `create_task` - Create a new task with date and time
- `get_tasks` - Retrieve all tasks
- `get_task` - Get a specific task by ID
- `update_task` - Update task details
- `delete_task` - Delete a task
- `get_tasks_by_date` - Get all tasks for a specific date

### Note Management
- `create_note` - Create a new note
- `get_notes` - Retrieve all notes
- `get_note` - Get a specific note by ID
- `update_note` - Update note content
- `delete_note` - Delete a note
- `search_notes` - Search notes by keyword

### Scheduling
- `get_schedule` - Get schedule for a date
- `get_week_schedule` - Get weekly schedule
- `get_month_schedule` - Get monthly schedule

### Timers
- `start_timer` - Start a new timer
- `get_timers` - Get all active timers
- `pause_timer` - Pause a timer
- `resume_timer` - Resume a paused timer
- `stop_timer` - Stop a timer

### AI & Statistics
- `ask_ai` - Ask the AI agent a question
- `get_ai_suggestions` - Get productivity suggestions
- `get_stats` - Get productivity statistics
- `get_task_stats` - Get task-related statistics
- `get_note_stats` - Get note-related statistics

## Configuration

### Backend URL
By default, the server connects to `http://localhost:8000/api`. Modify the `BASE_URL` in `tools.py` to change this.

### API Compatibility
The tools expect the backend to expose RESTful API endpoints. Ensure your Java backend provides:
- Task endpoints: `/api/tasks`, `/api/tasks/{id}`
- Note endpoints: `/api/notes`, `/api/notes/{id}`
- Schedule endpoints: `/api/schedule`
- Timer endpoints: `/api/timers`
- Stats endpoints: `/api/stats`

## Integration with Claude/AI Clients

Configure your AI client (Claude, etc.) to use this MCP server:

```json
{
  "mcpServers": {
    "ai-agent": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {}
    }
  }
}
```

The AI will have direct access to all available tools without needing them defined in the system prompt.

## Development

To add new tools:

1. Create a new async function in `tools.py`
2. Add it to the `AVAILABLE_TOOLS` dictionary with its description and parameters
3. Restart the server

Example:
```python
async def my_new_tool(param1: str, param2: int) -> dict:
    """Tool description"""
    return await call_api("GET", "/endpoint", {"param1": param1, "param2": param2})
```

Credit: Readme made by Grok (X) AI
