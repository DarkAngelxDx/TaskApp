import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from todo.stats import get_stats
from todo.users import list_users, switch_user, create_user
 
import argcomplete

from todo.dp import init_db, add_task, fetch_tasks, mark_done, delete_task

console = Console()

PRIORITY_COLORS = {
    "low": "green",
    "medium": "yellow",
    "high": "red"
}


def render_tasks(tasks, title):
    table = Table(title=title, header_style="bold cyan")
    table.add_column("ID", justify="right")
    table.add_column("Task")
    table.add_column("Priority")
    table.add_column("Deadline")
    table.add_column("Status")

    today = datetime.now().strftime("%Y-%m-%d")

    for task in tasks:
        priority = Text(task.priority.upper(), style=PRIORITY_COLORS.get(task.priority))
        status = "[green]DONE[/green]" if task.done else "[yellow]TODO[/yellow]"

        deadline_style = "red" if task.deadline and task.deadline < today else "white"

        table.add_row(
            str(task.id),
            task.title,
            priority,
            Text(task.deadline or "-", style=deadline_style),
            status
        )

    console.print(table)


def cmd_add(args):
    add_task(args.title, args.priority, args.deadline)
    console.print("[bold green]✓ Task added[/bold green]")


def cmd_list(_):
    tasks = fetch_tasks(where="1 ORDER BY done, priority, deadline")
    render_tasks(tasks, "📋 All Tasks")


def cmd_today(_):
    today = datetime.now().strftime("%Y-%m-%d")
    tasks = fetch_tasks(
        where="done=0 AND (deadline <= ?)",
        params=(today,)
    )
    render_tasks(tasks, "⏳ Today")


def cmd_done(args):
    mark_done(args.id)
    console.print(f"[bold green]✓ Task {args.id} completed[/bold green]")


def cmd_delete(args):
    delete_task(args.id)
    console.print(f"[bold red]✗ Task {args.id} deleted[/bold red]")


def cmd_export(_):
    import csv

    tasks = fetch_tasks()
    with open("tasks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "title", "priority", "deadline", "done"])
        for t in tasks:
            writer.writerow([t.id, t.title, t.priority, t.deadline, t.done])

    console.print("[bold cyan]📤 Exported to tasks.csv[/bold cyan]")


def main():
    init_db()

    parser = argparse.ArgumentParser(description="Advanced CLI Todo Manager")
    subparsers = parser.add_subparsers()

    add = subparsers.add_parser("add")
    add.add_argument("title")
    add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    add.add_argument("--deadline")
    add.set_defaults(func=cmd_add)

    subparsers.add_parser("list").set_defaults(func=cmd_list)
    subparsers.add_parser("today").set_defaults(func=cmd_today)

    done = subparsers.add_parser("done")
    done.add_argument("id", type=int)
    done.set_defaults(func=cmd_done)

    delete = subparsers.add_parser("delete")
    delete.add_argument("id", type=int)
    delete.set_defaults(func=cmd_delete)

    subparsers.add_parser("export").set_defaults(func=cmd_export)

    stats = subparsers.add_parser("stats")
    stats.set_defaults(func=lambda _: console.print(
        Panel.fit(
            "\n".join(
                f"{k}: {v}" for k, v in get_stats().items()
            ),
            title="📊 Stats"
        )
    ))

    user = subparsers.add_parser("user")
    user_sub = user.add_subparsers(dest="action")

    user_sub.add_parser("list").set_defaults(
        func=lambda _: console.print(list_users())
    )

    switch = user_sub.add_parser("switch")
    switch.add_argument("name")
    switch.set_defaults(func=lambda a: switch_user(a.name))

    create = user_sub.add_parser("create")
    create.add_argument("name")
    create.set_defaults(func=lambda a: create_user(a.name))



    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
