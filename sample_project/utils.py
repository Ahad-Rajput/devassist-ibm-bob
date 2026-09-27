"""
utils.py - Utility functions for the sample project.
"""

STATUS_ICONS = {
    "pending": "⏳",
    "in-progress": "🔄",
    "done": "✅",
}


def format_task(task):
    """Return a human-readable string for a task dict."""
    icon = STATUS_ICONS.get(task["status"], "❓")
    return f"  [{task['id']:>2}] {icon}  {task['title']}  ({task['status']})"


def filter_by_status(tasks, status):
    # FIXME: status comparison should be case-insensitive
    return [t for t in tasks if t["status"] == status]


def summarise(tasks):
    counts = {}
    for task in tasks:
        try:
            counts[task["status"]] += 1
        except:
            counts[task["status"]] = 1
    return counts
