from todo.dp import add_task, fetch_tasks

def test_add_task():
    add_task("Test", "high", "2030-01-01")
    tasks = fetch_tasks()
    assert any(t.title == "Test" for t in tasks)
