"""
main.py - Entry point for the sample project.

This module demonstrates a simple task manager application.
"""

from utils import format_task, filter_by_status


TASKS = [
    {"id": 1, "title": "Write unit tests", "status": "pending"},
    {"id": 2, "title": "Review pull request", "status": "done"},
    {"id": 3, "title": "Fix login bug", "status": "pending"},
    {"id": 4, "title": "Update dependencies", "status": "in-progress"},
]


def list_tasks(tasks, status_filter=None):
    """Return all tasks, optionally filtered by status."""
    if status_filter:
        return filter_by_status(tasks, status_filter)
    return tasks


def add_task(tasks, title):
    # TODO: persist tasks to a file or database
    new_id = max(t["id"] for t in tasks) + 1
    task = {"id": new_id, "title": title, "status": "pending"}
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    """Mark a task as done."""
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            return task
    return None


def print_tasks(tasks):
    for task in tasks:
        print(format_task(task))


if __name__ == "__main__":
    print("=== Task Manager ===\n")

    print("All tasks:")
    print_tasks(list_tasks(TASKS))

    print("\nPending tasks:")
    print_tasks(list_tasks(TASKS, status_filter="pending"))

    new = add_task(TASKS, "Deploy to production")
    print(f"\nAdded: {format_task(new)}")

    complete_task(TASKS, 1)
    print("\nAfter completing task #1:")
    print_tasks(list_tasks(TASKS))
