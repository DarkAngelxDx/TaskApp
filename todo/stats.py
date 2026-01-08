from datetime import datetime
from todo.dp import fetch_tasks


def get_stats():
    tasks = fetch_tasks()
    today = datetime.now().strftime("%Y-%m-%d")

    total = len(tasks)
    done = sum(t.done for t in tasks)
    overdue = sum(
        1 for t in tasks
        if not t.done and t.deadline and t.deadline < today
    )

    return {
        "total": total,
        "done": done,
        "pending": total - done,
        "overdue": overdue,
        "percent": int((done / total) * 100) if total else 0
    }
