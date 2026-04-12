from typing import Any, Optional
import httpx
import json

BASE_URL = "http://localhost:8000/api"

async def call_api(method: str, endpoint: str, data: Optional[dict] = None) -> dict:
    """Helper to call the backend API"""
    url = f"{BASE_URL}{endpoint}"
    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url)
        elif method == "POST":
            response = await client.post(url, json=data)
        elif method == "PUT":
            response = await client.put(url, json=data)
        elif method == "DELETE":
            response = await client.delete(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()


#task tools
async def create_task(description: str, date: str, start_time: str, end_time: str, priority: Optional[str] = None) -> dict:
    """Create a new task
    
    Args:
        description: Task description
        date: Task date (YYYY-MM-DD format)
        start_time: Start time (HH:MM format)
        end_time: End time (HH:MM format)
        priority: Task priority (optional)
    
    Returns:
        Created task data
    """
    data = {
        "description": description,
        "date": date,
        "startTime": start_time,
        "endTime": end_time,
    }
    if priority:
        data["priority"] = priority
    
    return await call_api("POST", "/tasks", data)


async def get_tasks() -> list:
    """Retrieve all tasks"""
    result = await call_api("GET", "/tasks")
    return result.get("tasks", [])


async def get_task(task_id: str) -> dict:
    """Retrieve a specific task by ID"""
    return await call_api("GET", f"/tasks/{task_id}")


async def update_task(task_id: str, **kwargs) -> dict:
    """Update a task"""
    return await call_api("PUT", f"/tasks/{task_id}", kwargs)


async def delete_task(task_id: str) -> dict:
    """Delete a task"""
    return await call_api("DELETE", f"/tasks/{task_id}")


async def get_tasks_by_date(date: str) -> list:
    """Get all tasks for a specific date"""
    result = await call_api("GET", f"/tasks/date/{date}")
    return result.get("tasks", [])


#note tools
async def create_note(content: str) -> dict:
    """Create a new note
    
    Args:
        content: Note content
    
    Returns:
        Created note data with ID and creation time
    """
    return await call_api("POST", "/notes", {"content": content})


async def get_notes() -> list:
    """Retrieve all notes"""
    result = await call_api("GET", "/notes")
    return result.get("notes", [])


async def get_note(note_id: str) -> dict:
    """Retrieve a specific note by ID"""
    return await call_api("GET", f"/notes/{note_id}")


async def update_note(note_id: str, content: str) -> dict:
    """Update note content"""
    return await call_api("PUT", f"/notes/{note_id}", {"content": content})


async def delete_note(note_id: str) -> dict:
    """Delete a note"""
    return await call_api("DELETE", f"/notes/{note_id}")


async def search_notes(keyword: str) -> list:
    """Search notes by keyword"""
    result = await call_api("GET", f"/notes/search?keyword={keyword}")
    return result.get("notes", [])


#schedule tools
async def get_schedule(date: Optional[str] = None) -> dict:
    """Get schedule for a date
    
    Args:
        date: Date in YYYY-MM-DD format (optional, defaults to today)
    
    Returns:
        Schedule with tasks for the day
    """
    endpoint = "/schedule" if not date else f"/schedule?date={date}"
    return await call_api("GET", endpoint)


async def get_week_schedule(start_date: str) -> dict:
    """Get schedule for a week"""
    return await call_api("GET", f"/schedule/week?start={start_date}")


async def get_month_schedule(month: str, year: str) -> dict:
    """Get schedule for a month"""
    return await call_api("GET", f"/schedule/month?month={month}&year={year}")


#timer tools
async def start_timer(duration_seconds: int, label: Optional[str] = None) -> dict:
    """Start a timer
    
    Args:
        duration_seconds: Timer duration in seconds
        label: Optional timer label
    
    Returns:
        Timer data with ID
    """
    data = {"duration": duration_seconds}
    if label:
        data["label"] = label
    return await call_api("POST", "/timers", data)


async def pause_timer(timer_id: str) -> dict:
    """Pause an active timer"""
    return await call_api("POST", f"/timers/{timer_id}/pause", {})


async def resume_timer(timer_id: str) -> dict:
    """Resume a paused timer"""
    return await call_api("POST", f"/timers/{timer_id}/resume", {})


async def stop_timer(timer_id: str) -> dict:
    """Stop a timer"""
    return await call_api("DELETE", f"/timers/{timer_id}")


async def get_timers() -> list:
    """Get all active timers"""
    result = await call_api("GET", "/timers")
    return result.get("timers", [])


#ai misc tools
async def ask_ai(question: str, context: Optional[dict] = None) -> dict:
    """Ask the AI agent a question
    
    Args:
        question: The question to ask
        context: Optional context data
    
    Returns:
        AI response
    """
    data = {"question": question}
    if context:
        data["context"] = context
    return await call_api("POST", "/ai/ask", data)


async def get_ai_suggestions() -> dict:
    """Get AI suggestions for productivity"""
    return await call_api("GET", "/ai/suggestions")


#stat tools
async def get_stats(period: Optional[str] = None) -> dict:
    """Get productivity statistics
    
    Args:
        period: Time period (day, week, month)
    
    Returns:
        Statistics data
    """
    endpoint = "/stats" if not period else f"/stats?period={period}"
    return await call_api("GET", endpoint)


async def get_task_stats() -> dict:
    """Get task-related statistics"""
    return await call_api("GET", "/stats/tasks")


async def get_note_stats() -> dict:
    """Get note-related statistics"""
    return await call_api("GET", "/stats/notes")


AVAILABLE_TOOLS = {
    "create_task": {
        "description": "Create a new task",
        "func": create_task,
        "params": {
            "description": "Task description",
            "date": "Task date (YYYY-MM-DD)",
            "start_time": "Start time (HH:MM)",
            "end_time": "End time (HH:MM)",
            "priority": "Priority level (optional)"
        }
    },
    "get_tasks": {
        "description": "Retrieve all tasks",
        "func": get_tasks,
        "params": {}
    },
    "get_task": {
        "description": "Retrieve a specific task",
        "func": get_task,
        "params": {"task_id": "Task ID"}
    },
    "update_task": {
        "description": "Update a task",
        "func": update_task,
        "params": {"task_id": "Task ID", "fields": "Fields to update"}
    },
    "delete_task": {
        "description": "Delete a task",
        "func": delete_task,
        "params": {"task_id": "Task ID"}
    },
    "get_tasks_by_date": {
        "description": "Get tasks for a specific date",
        "func": get_tasks_by_date,
        "params": {"date": "Date (YYYY-MM-DD)"}
    },
    
    "create_note": {
        "description": "Create a new note",
        "func": create_note,
        "params": {"content": "Note content"}
    },
    "get_notes": {
        "description": "Retrieve all notes",
        "func": get_notes,
        "params": {}
    },
    "get_note": {
        "description": "Retrieve a specific note",
        "func": get_note,
        "params": {"note_id": "Note ID"}
    },
    "update_note": {
        "description": "Update a note",
        "func": update_note,
        "params": {"note_id": "Note ID", "content": "New content"}
    },
    "delete_note": {
        "description": "Delete a note",
        "func": delete_note,
        "params": {"note_id": "Note ID"}
    },
    "search_notes": {
        "description": "Search notes by keyword",
        "func": search_notes,
        "params": {"keyword": "Search keyword"}
    },
    
    "get_schedule": {
        "description": "Get schedule for a date",
        "func": get_schedule,
        "params": {"date": "Date (YYYY-MM-DD, optional)"}
    },
    "get_week_schedule": {
        "description": "Get weekly schedule",
        "func": get_week_schedule,
        "params": {"start_date": "Week start date"}
    },
    "get_month_schedule": {
        "description": "Get monthly schedule",
        "func": get_month_schedule,
        "params": {"month": "Month (1-12)", "year": "Year"}
    },
    
    "start_timer": {
        "description": "Start a timer",
        "func": start_timer,
        "params": {"duration_seconds": "Duration in seconds", "label": "Timer label (optional)"}
    },
    "get_timers": {
        "description": "Get all active timers",
        "func": get_timers,
        "params": {}
    },
    "pause_timer": {
        "description": "Pause a timer",
        "func": pause_timer,
        "params": {"timer_id": "Timer ID"}
    },
    "resume_timer": {
        "description": "Resume a timer",
        "func": resume_timer,
        "params": {"timer_id": "Timer ID"}
    },
    "stop_timer": {
        "description": "Stop a timer",
        "func": stop_timer,
        "params": {"timer_id": "Timer ID"}
    },
    
    "ask_ai": {
        "description": "Ask the AI agent a question",
        "func": ask_ai,
        "params": {"question": "Question", "context": "Context (optional)"}
    },
    "get_ai_suggestions": {
        "description": "Get AI productivity suggestions",
        "func": get_ai_suggestions,
        "params": {}
    },
    
    "get_stats": {
        "description": "Get productivity statistics",
        "func": get_stats,
        "params": {"period": "Time period (day/week/month, optional)"}
    },
    "get_task_stats": {
        "description": "Get task statistics",
        "func": get_task_stats,
        "params": {}
    },
    "get_note_stats": {
        "description": "Get note statistics",
        "func": get_note_stats,
        "params": {}
    },
}
